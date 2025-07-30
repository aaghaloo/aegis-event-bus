# app/middleware_security.py
"""
Security middleware for FastAPI.
Implements rate limiting, security headers, and request logging.
"""

import time
from typing import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .monitoring import performance_monitor
from .security_config import RATE_LIMIT_CONFIG, SECURITY_HEADERS

log = structlog.get_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add security headers
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value

        # Add Content Security Policy
        csp_parts = []
        for directive, sources in SECURITY_HEADERS.get("CSP", {}).items():
            csp_parts.append(f"{directive} {' '.join(sources)}")

        if csp_parts:
            response.headers["Content-Security-Policy"] = "; ".join(csp_parts)

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Implement rate limiting for API endpoints."""

    def __init__(self, app):
        super().__init__(app)
        self.request_counts = {}
        self.lockout_until = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host

        # Skip rate limiting for test environments
        if client_ip in ["127.0.0.1", "localhost", "test"]:
            return await call_next(request)

        # Check if client is locked out
        if client_ip in self.lockout_until:
            if time.time() < self.lockout_until[client_ip]:
                return Response(
                    content="Rate limit exceeded. Please try again later.",
                    status_code=429,
                    headers={"Retry-After": "300"},
                )
            else:
                del self.lockout_until[client_ip]

        # Determine rate limit based on endpoint
        path = request.url.path
        if path.startswith("/auth"):
            limit_key = "auth"
        elif path.startswith("/health"):
            limit_key = "health"
        elif path.startswith("/api"):
            limit_key = "api"
        else:
            limit_key = "default"

        limit_config = RATE_LIMIT_CONFIG.get(limit_key, "100/minute")
        max_requests, window = self._parse_rate_limit(limit_config)

        # Check rate limit
        current_time = time.time()
        window_start = current_time - window

        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []

        # Remove old requests outside the window
        self.request_counts[client_ip] = [
            req_time
            for req_time in self.request_counts[client_ip]
            if req_time > window_start
        ]

        # Check if limit exceeded
        if len(self.request_counts[client_ip]) >= max_requests:
            # Lock out client for 5 minutes
            self.lockout_until[client_ip] = current_time + 300
            log.warning("rate_limit_exceeded", client_ip=client_ip, path=path)
            return Response(
                content="Rate limit exceeded. Please try again later.",
                status_code=429,
                headers={"Retry-After": "300"},
            )

        # Record request
        self.request_counts[client_ip].append(current_time)

        return await call_next(request)

    def _parse_rate_limit(self, limit_str: str) -> tuple[int, int]:
        """Parse rate limit string like '100/minute'."""
        try:
            count, period = limit_str.split("/")
            count = int(count)

            if period == "second":
                window = 1
            elif period == "minute":
                window = 60
            elif period == "hour":
                window = 3600
            else:
                window = 60  # Default to minute

            return count, window
        except (ValueError, AttributeError):
            return 100, 60  # Default fallback


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with performance metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Log request start
        log.info(
            "request_started",
            method=request.method,
            path=str(request.url.path),
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Record performance metrics
            performance_monitor.record_request(
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration=duration,
            )

            # Log request completion
            log.info(
                "request_completed",
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration=duration,
                client_ip=request.client.host,
            )

            return response

        except Exception as e:
            duration = time.time() - start_time

            # Record error metrics
            performance_monitor.record_request(
                method=request.method,
                path=str(request.url.path),
                status_code=500,
                duration=duration,
            )

            # Log error
            log.error(
                "request_error",
                method=request.method,
                path=str(request.url.path),
                error=str(e),
                duration=duration,
                client_ip=request.client.host,
            )

            raise
