# app/middleware_security.py
"""
Security middleware for FastAPI.
Implements rate limiting, security headers, and request logging.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .enhanced_logging import get_enhanced_logger, log_request_context
from .monitoring import performance_monitor
from .security_config import SECURITY_HEADERS

log = get_enhanced_logger(__name__)


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

    def __init__(self, app, requests_per_minute: int = 60, burst_limit: int = 10):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.request_counts = {}
        self.logger = get_enhanced_logger("rate_limit")

    def _get_client_key(self, request: Request) -> str:
        """Get client identifier for rate limiting."""
        # Use X-Forwarded-For if available, otherwise client IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _is_rate_limited(self, client_key: str) -> bool:
        """Check if client is rate limited."""
        now = time.time()
        window_start = now - 60  # 1 minute window

        # Clean old entries
        if client_key in self.request_counts:
            self.request_counts[client_key] = [
                req_time
                for req_time in self.request_counts[client_key]
                if req_time > window_start
            ]

        # Check burst limit
        if client_key in self.request_counts:
            recent_requests = len(self.request_counts[client_key])
            if recent_requests >= self.burst_limit:
                return True

        # Check rate limit
        if client_key in self.request_counts:
            total_requests = len(self.request_counts[client_key])
            if total_requests >= self.requests_per_minute:
                return True

        return False

    def _record_request(self, client_key: str):
        """Record a request for rate limiting."""
        now = time.time()
        if client_key not in self.request_counts:
            self.request_counts[client_key] = []
        self.request_counts[client_key].append(now)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_key = self._get_client_key(request)

        # Check rate limiting
        if self._is_rate_limited(client_key):
            self.logger.warning(
                "rate_limit_exceeded",
                client_key=client_key,
                path=str(request.url.path),
                method=request.method,
            )
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": "60"},
            )

        # Record the request
        self._record_request(client_key)

        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with performance metrics and context."""

    def __init__(self, app):
        super().__init__(app)
        self.logger = get_enhanced_logger("request")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        request_id = str(uuid.uuid4())

        # Set request context for structured logging
        log_request_context(
            request_id=request_id,
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", ""),
        )

        # Log request start
        self.logger.info(
            "request_started",
            method=request.method,
            path=str(request.url.path),
            query_params=str(request.query_params),
            headers=dict(request.headers),
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

            # Log request completion with performance data
            self.logger.log_request(
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration=duration,
                request_id=request_id,
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

            # Log error with context
            self.logger.error(
                "request_error",
                method=request.method,
                path=str(request.url.path),
                error=str(e),
                error_type=type(e).__name__,
                duration=duration,
                request_id=request_id,
            )

            raise
