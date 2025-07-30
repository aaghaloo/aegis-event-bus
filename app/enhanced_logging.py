# app/enhanced_logging.py
"""
Enhanced logging configuration for the Aegis Event Bus.
Provides structured logging with context, performance tracking, and security monitoring.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from structlog.processors import (
    JSONRenderer,
    StackInfoRenderer,
    TimeStamper,
    add_log_level,
    dict_tracebacks,
    format_exc_info,
)
from structlog.stdlib import LoggerFactory

from .config import settings


class ContextualLogger:
    """Enhanced logger with context management and performance tracking."""

    def __init__(self, name: str):
        self.logger = structlog.get_logger(name)
        self.context: Dict[str, Any] = {}
        self.name = name  # Store the name for access

    def bind(self, **kwargs) -> "ContextualLogger":
        """Bind context variables to the logger."""
        new_logger = ContextualLogger(self.name)
        new_logger.logger = self.logger.bind(**kwargs)
        new_logger.context = {**self.context, **kwargs}
        return new_logger

    def log_request(
        self, method: str, path: str, status_code: int, duration: float, **kwargs
    ):
        """Log HTTP request with performance metrics."""
        self.logger.info(
            "http_request",
            method=method,
            path=path,
            status_code=status_code,
            duration=duration,
            **kwargs,
        )

    def log_security_event(self, event_type: str, details: Dict[str, Any], **kwargs):
        """Log security-related events."""
        self.logger.warning(
            "security_event", event_type=event_type, details=details, **kwargs
        )

    def log_database_operation(
        self, operation: str, table: str, duration: float, **kwargs
    ):
        """Log database operations with performance metrics."""
        self.logger.info(
            "database_operation",
            operation=operation,
            table=table,
            duration=duration,
            **kwargs,
        )

    def log_mqtt_event(self, event_type: str, topic: str, payload_size: int, **kwargs):
        """Log MQTT events."""
        self.logger.info(
            "mqtt_event",
            event_type=event_type,
            topic=topic,
            payload_size=payload_size,
            **kwargs,
        )

    def log_task_event(self, task_id: str, agent_id: str, event_type: str, **kwargs):
        """Log task-related events."""
        self.logger.info(
            "task_event",
            task_id=task_id,
            agent_id=agent_id,
            event_type=event_type,
            **kwargs,
        )

    def log_agent_event(self, agent_id: str, event_type: str, **kwargs):
        """Log agent-related events."""
        self.logger.info(
            "agent_event", agent_id=agent_id, event_type=event_type, **kwargs
        )

    def __getattr__(self, name):
        """Delegate unknown attributes to the underlying logger."""
        return getattr(self.logger, name)


def setup_enhanced_logging() -> None:
    """Configure comprehensive structured logging for the service."""

    # Create logs directory if it doesn't exist
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)

    # Configure log level based on settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper())

    # Timestamp processor with ISO format
    timestamper = TimeStamper(fmt="iso", utc=True)

    # Configure structlog with enhanced processors
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
        processors=[
            # Add context variables (request-id, user-id, etc.)
            structlog.contextvars.merge_contextvars,
            # Add log level
            add_log_level,
            # Add timestamp
            timestamper,
            # Add stack info for errors
            StackInfoRenderer(),
            # Format exceptions nicely
            format_exc_info,
            # Add traceback information
            dict_tracebacks,
            # Add environment and service information
            _add_service_info,
            # Add performance context
            _add_performance_context,
            # Final JSON renderer
            JSONRenderer(),
        ],
        logger_factory=LoggerFactory(),
        context_class=dict,
    )

    # Configure standard library logging
    # Clear existing handlers to avoid conflicts
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    # Add console handler
    root_logger.addHandler(console_handler)
    root_logger.setLevel(log_level)

    # Add file handlers in production
    if settings.is_production:
        app_handler = logging.FileHandler(log_dir / "app.log")
        app_handler.setLevel(log_level)
        app_handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(app_handler)

        error_handler = logging.FileHandler(log_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(error_handler)

    # Configure specific loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)

    # Log startup information
    logger = structlog.get_logger(__name__)
    logger.info(
        "enhanced_logging_configured",
        log_level=settings.LOG_LEVEL,
        environment=settings.ENV,
        debug_mode=settings.DEBUG,
        log_dir=str(log_dir),
    )


def _add_service_info(logger, method_name, event_dict):
    """Add service information to all log entries."""
    event_dict.update(
        {
            "service": "aegis-event-bus",
            "version": "1.0.0",
            "environment": settings.ENV,
        }
    )
    return event_dict


def _add_performance_context(logger, method_name, event_dict):
    """Add performance context to log entries."""
    if "duration" in event_dict:
        duration = event_dict["duration"]
        if duration > 1.0:
            event_dict["slow_request"] = True
        if duration > 5.0:
            event_dict["very_slow_request"] = True

    return event_dict


def get_enhanced_logger(name: str) -> ContextualLogger:
    """Get a contextual logger instance."""
    return ContextualLogger(name)


# Global logger instances for common use cases
security_logger = get_enhanced_logger("security")
performance_logger = get_enhanced_logger("performance")
database_logger = get_enhanced_logger("database")
mqtt_logger = get_enhanced_logger("mqtt")
task_logger = get_enhanced_logger("task")
agent_logger = get_enhanced_logger("agent")


def log_request_context(request_id: str, user_id: Optional[str] = None, **kwargs):
    """Set request context for structured logging."""
    context_vars = {"request_id": request_id}
    if user_id:
        context_vars["user_id"] = user_id
    context_vars.update(kwargs)

    structlog.contextvars.clear_contextvars()
    for key, value in context_vars.items():
        structlog.contextvars.bind_contextvars(**{key: value})


def log_security_alert(
    event_type: str, severity: str, details: Dict[str, Any], **kwargs
):
    """Log security alerts with appropriate severity."""
    logger = security_logger.bind(
        event_type=event_type,
        severity=severity,
        timestamp=datetime.utcnow().isoformat(),
    )

    if severity.upper() == "CRITICAL":
        logger.error("security_alert", details=details, **kwargs)
    elif severity.upper() == "HIGH":
        logger.warning("security_alert", details=details, **kwargs)
    else:
        logger.info("security_alert", details=details, **kwargs)


def log_performance_metric(
    metric_name: str, value: float, unit: str = "seconds", **kwargs
):
    """Log performance metrics."""
    performance_logger.info(
        "performance_metric", metric_name=metric_name, value=value, unit=unit, **kwargs
    )


def log_database_operation(
    operation: str, table: str, duration: float, success: bool, **kwargs
):
    """Log database operations with performance tracking."""
    logger = database_logger.bind(
        operation=operation,
        table=table,
        duration=duration,
        success=success,
    )

    if success:
        logger.info("database_operation", **kwargs)
    else:
        logger.error("database_operation_failed", **kwargs)


def log_mqtt_operation(
    operation: str, topic: str, payload_size: int, success: bool, **kwargs
):
    """Log MQTT operations."""
    logger = mqtt_logger.bind(
        operation=operation,
        topic=topic,
        payload_size=payload_size,
        success=success,
    )

    if success:
        logger.info("mqtt_operation", **kwargs)
    else:
        logger.error("mqtt_operation_failed", **kwargs)
