# app/error_handling.py
"""
Advanced error handling and recovery system for the Aegis Event Bus.
Provides comprehensive error handling, recovery mechanisms, and resilience features.
"""

import functools
import time
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from .enhanced_logging import get_enhanced_logger, log_security_alert

log = get_enhanced_logger(__name__)

# Type variables for generic functions
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


class ErrorSeverity(Enum):
    """Error severity levels for classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""

    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATABASE = "database"
    NETWORK = "network"
    MQTT = "mqtt"
    STORAGE = "storage"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class ErrorRecoveryStrategy(Enum):
    """Error recovery strategies."""

    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    DEGRADED_MODE = "degraded_mode"
    FAIL_FAST = "fail_fast"


class CircuitBreaker:
    """Circuit breaker pattern implementation."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful execution."""
        self.failure_count = 0
        self.state = "CLOSED"
        log.info("circuit_breaker_success", state=self.state)

    def _on_failure(self):
        """Handle failed execution."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            log.warning(
                "circuit_breaker_opened",
                failure_count=self.failure_count,
                threshold=self.failure_threshold,
            )

    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset."""
        if self.last_failure_time is None:
            return True

        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout


class RetryHandler:
    """Retry mechanism with exponential backoff."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: tuple = (Exception,),
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.exceptions = exceptions

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e

                if attempt == self.max_retries:
                    log.error(
                        "retry_exhausted",
                        function=func.__name__,
                        max_retries=self.max_retries,
                        final_error=str(e),
                    )
                    raise e

                delay = min(
                    self.base_delay * (self.exponential_base**attempt), self.max_delay
                )

                log.warning(
                    "retry_attempt",
                    function=func.__name__,
                    attempt=attempt + 1,
                    max_retries=self.max_retries,
                    delay=delay,
                    error=str(e),
                )

                time.sleep(delay)

        raise last_exception


class ErrorHandler:
    """Centralized error handling and classification."""

    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_handlers: Dict[str, RetryHandler] = {}

    def classify_error(self, error: Exception) -> tuple[ErrorCategory, ErrorSeverity]:
        """Classify error by category and severity."""
        error_str = str(error).lower()

        # Database errors
        if isinstance(error, SQLAlchemyError):
            return ErrorCategory.DATABASE, ErrorSeverity.HIGH

        # Authentication errors
        if "authentication" in error_str or "unauthorized" in error_str:
            return ErrorCategory.AUTHENTICATION, ErrorSeverity.MEDIUM

        # Authorization errors
        if "authorization" in error_str or "forbidden" in error_str:
            return ErrorCategory.AUTHORIZATION, ErrorSeverity.MEDIUM

        # Validation errors
        if "validation" in error_str or "invalid" in error_str:
            return ErrorCategory.VALIDATION, ErrorSeverity.LOW

        # Network errors
        if "connection" in error_str or "timeout" in error_str:
            return ErrorCategory.NETWORK, ErrorSeverity.HIGH

        # MQTT errors
        if "mqtt" in error_str or "broker" in error_str:
            return ErrorCategory.MQTT, ErrorSeverity.HIGH

        # Storage errors
        if "storage" in error_str or "disk" in error_str:
            return ErrorCategory.STORAGE, ErrorSeverity.HIGH

        # System errors
        if "system" in error_str or "internal" in error_str:
            return ErrorCategory.SYSTEM, ErrorSeverity.CRITICAL

        return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM

    def handle_error(
        self,
        error: Exception,
        context: Dict[str, Any],
        recovery_strategy: ErrorRecoveryStrategy = ErrorRecoveryStrategy.FAIL_FAST,
    ) -> None:
        """Handle and log error with appropriate recovery strategy."""
        category, severity = self.classify_error(error)

        # Update error counts
        error_key = f"{category.value}_{severity.value}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1

        # Log error with context
        log.error(
            "error_occurred",
            error_type=type(error).__name__,
            error_message=str(error),
            category=category.value,
            severity=severity.value,
            recovery_strategy=recovery_strategy.value,
            context=context,
            error_count=self.error_counts[error_key],
        )

        # Security alert for critical errors
        if severity == ErrorSeverity.CRITICAL:
            log_security_alert(
                event_type="critical_error",
                severity="CRITICAL",
                details={
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "category": category.value,
                    "context": context,
                },
            )

    def get_circuit_breaker(self, key: str) -> CircuitBreaker:
        """Get or create circuit breaker for a specific key."""
        if key not in self.circuit_breakers:
            self.circuit_breakers[key] = CircuitBreaker()
        return self.circuit_breakers[key]

    def get_retry_handler(self, key: str) -> RetryHandler:
        """Get or create retry handler for a specific key."""
        if key not in self.retry_handlers:
            self.retry_handlers[key] = RetryHandler()
        return self.retry_handlers[key]


# Global error handler instance
error_handler = ErrorHandler()


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""

    pass


class DegradedModeError(Exception):
    """Raised when system is in degraded mode."""

    pass


def with_error_handling(
    recovery_strategy: ErrorRecoveryStrategy = ErrorRecoveryStrategy.FAIL_FAST,
    context: Optional[Dict[str, Any]] = None,
):
    """Decorator for error handling with recovery strategies."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ctx = context or {}
                ctx.update(
                    {
                        "function": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs),
                    }
                )

                error_handler.handle_error(e, ctx, recovery_strategy)

                if recovery_strategy == ErrorRecoveryStrategy.FAIL_FAST:
                    raise e
                elif recovery_strategy == ErrorRecoveryStrategy.RETRY:
                    retry_handler = error_handler.get_retry_handler(func.__name__)
                    return retry_handler.call(func, *args, **kwargs)
                elif recovery_strategy == ErrorRecoveryStrategy.CIRCUIT_BREAKER:
                    circuit_breaker = error_handler.get_circuit_breaker(func.__name__)
                    return circuit_breaker.call(func, *args, **kwargs)
                else:
                    raise e

        return wrapper

    return decorator


@contextmanager
def database_transaction(session: Session):
    """Context manager for database transactions with error handling."""
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        error_handler.handle_error(
            e,
            {"operation": "database_transaction"},
            ErrorRecoveryStrategy.FAIL_FAST,
        )
        raise
    except Exception as e:
        session.rollback()
        error_handler.handle_error(
            e,
            {"operation": "database_transaction"},
            ErrorRecoveryStrategy.FAIL_FAST,
        )
        raise


@asynccontextmanager
async def mqtt_operation_context():
    """Context manager for MQTT operations with error handling."""
    try:
        yield
    except Exception as e:
        error_handler.handle_error(
            e,
            {"operation": "mqtt_operation"},
            ErrorRecoveryStrategy.RETRY,
        )
        raise


def create_error_response(
    error: Exception,
    status_code: int = 500,
    include_details: bool = False,
) -> JSONResponse:
    """Create standardized error response."""
    error_id = f"ERR_{int(time.time())}"

    response_data = {
        "error_id": error_id,
        "message": "An error occurred while processing your request",
        "timestamp": datetime.now().isoformat(),
    }

    if include_details:
        category, severity = error_handler.classify_error(error)
        response_data.update(
            {
                "error_type": type(error).__name__,
                "category": category.value,
                "severity": severity.value,
                "details": str(error),
            }
        )

    log.error(
        "error_response_created",
        error_id=error_id,
        status_code=status_code,
        error_type=type(error).__name__,
        include_details=include_details,
    )

    return JSONResponse(
        status_code=status_code,
        content=response_data,
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for FastAPI."""
    # Classify the error
    category, severity = error_handler.classify_error(exc)

    # Handle specific error types
    if isinstance(exc, HTTPException):
        return create_error_response(exc, exc.status_code, include_details=True)

    # Handle database errors
    if isinstance(exc, SQLAlchemyError):
        return create_error_response(exc, 503, include_details=False)

    # Handle circuit breaker errors
    if isinstance(exc, CircuitBreakerOpenError):
        return create_error_response(exc, 503, include_details=False)

    # Handle degraded mode errors
    if isinstance(exc, DegradedModeError):
        return create_error_response(exc, 503, include_details=False)

    # Default error response
    return create_error_response(exc, 500, include_details=False)


def register_exception_handlers(app):
    """Register exception handlers with FastAPI app."""
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(SQLAlchemyError, global_exception_handler)
    app.add_exception_handler(CircuitBreakerOpenError, global_exception_handler)
    app.add_exception_handler(DegradedModeError, global_exception_handler)

    log.info("exception_handlers_registered")


class DegradedModeManager:
    """Manages system degraded mode for graceful degradation."""

    def __init__(self):
        self.degraded_mode = False
        self.degraded_since = None
        self.degraded_reason = None

    def enable_degraded_mode(self, reason: str):
        """Enable degraded mode."""
        self.degraded_mode = True
        self.degraded_since = datetime.now()
        self.degraded_reason = reason

        log.warning(
            "degraded_mode_enabled",
            reason=reason,
            timestamp=self.degraded_since.isoformat(),
        )

    def disable_degraded_mode(self):
        """Disable degraded mode."""
        if self.degraded_mode:
            duration = datetime.now() - self.degraded_since
            log.info(
                "degraded_mode_disabled",
                duration_seconds=duration.total_seconds(),
                reason=self.degraded_reason,
            )

        self.degraded_mode = False
        self.degraded_since = None
        self.degraded_reason = None

    def is_degraded(self) -> bool:
        """Check if system is in degraded mode."""
        return self.degraded_mode

    def get_status(self) -> Dict[str, Any]:
        """Get degraded mode status."""
        return {
            "degraded_mode": self.degraded_mode,
            "degraded_since": (
                self.degraded_since.isoformat() if self.degraded_since else None
            ),
            "degraded_reason": self.degraded_reason,
        }


# Global degraded mode manager
degraded_mode_manager = DegradedModeManager()
