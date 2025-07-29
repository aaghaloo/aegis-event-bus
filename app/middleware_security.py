# app/middleware_security.py
"""
Security middleware with rate limiting and structured logging.
"""

import time
from collections import defaultdict
from typing import Dict, List

import structlog
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings

log = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with IP-based tracking."""

    def __init__(self, app, requests_per_minute: int = 60, burst_limit: int = 10):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for test environment
        if settings.is_development and "test" in client_ip.lower():
            response = await call_next(request)
            return response

        # Clean old requests (older than 1 minute)
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] if now - req_time < 60
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            log.warning(
                "rate_limit_exceeded",
                client_ip=client_ip,
                requests_count=len(self.requests[client_ip]),
            )
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Please try again later."
            )

        # Check burst limit
        recent_requests = [
            req_time for req_time in self.requests[client_ip] if now - req_time < 1
        ]
        if len(recent_requests) >= self.burst_limit:
            log.warning(
                "burst_limit_exceeded",
                client_ip=client_ip,
                recent_requests=len(recent_requests),
            )
            raise HTTPException(
                status_code=429, detail="Too many requests. Please slow down."
            )

        # Add current request
        self.requests[client_ip].append(now)

        # Process request
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Log request
        log.info(
            "request_processed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=duration,
            client_ip=client_ip,
            user_agent=request.headers.get("user-agent", "unknown"),
        )

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Remove server information
        if "server" in response.headers:
            del response.headers["server"]

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Structured request logging middleware."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request start
        log.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", "unknown"),
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Log successful request
            log.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration,
            )

            return response

        except Exception as e:
            duration = time.time() - start_time

            # Log error
            log.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
                duration=duration,
            )
            raise
