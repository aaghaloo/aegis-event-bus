# app/error_router.py
"""
Error handling and recovery endpoints.
Provides endpoints for error management, circuit breaker status, and degraded mode
control.
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from . import security
from .enhanced_logging import get_enhanced_logger
from .error_handling import (
    DegradedModeError,
    degraded_mode_manager,
    error_handler,
)

router = APIRouter(prefix="/errors", tags=["Error Handling"])
log = get_enhanced_logger(__name__)


@router.get("/status", response_model=Dict[str, Any])
def get_error_status(_: dict = Depends(security.get_current_user)):
    """Get current error handling status."""
    try:
        # Get circuit breaker status
        circuit_breakers = {}
        for key, cb in error_handler.circuit_breakers.items():
            circuit_breakers[key] = {
                "state": cb.state,
                "failure_count": cb.failure_count,
                "last_failure_time": (
                    cb.last_failure_time.isoformat() if cb.last_failure_time else None
                ),
            }

        # Get retry handler status
        retry_handlers = {}
        for key, rh in error_handler.retry_handlers.items():
            retry_handlers[key] = {
                "max_retries": rh.max_retries,
                "base_delay": rh.base_delay,
                "max_delay": rh.max_delay,
            }

        # Get error counts
        error_counts = error_handler.error_counts.copy()

        # Get degraded mode status
        degraded_status = degraded_mode_manager.get_status()

        return {
            "circuit_breakers": circuit_breakers,
            "retry_handlers": retry_handlers,
            "error_counts": error_counts,
            "degraded_mode": degraded_status,
        }
    except Exception as e:
        log.error("error_status_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve error status")


@router.post("/degraded-mode/enable")
def enable_degraded_mode(
    reason: str,
    _: dict = Depends(security.get_current_user),
):
    """Enable degraded mode."""
    try:
        degraded_mode_manager.enable_degraded_mode(reason)
        return {
            "message": "Degraded mode enabled",
            "reason": reason,
            "timestamp": degraded_mode_manager.degraded_since.isoformat(),
        }
    except Exception as e:
        log.error("enable_degraded_mode_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to enable degraded mode")


@router.post("/degraded-mode/disable")
def disable_degraded_mode(_: dict = Depends(security.get_current_user)):
    """Disable degraded mode."""
    try:
        degraded_mode_manager.disable_degraded_mode()
        return {
            "message": "Degraded mode disabled",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        log.error("disable_degraded_mode_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to disable degraded mode")


@router.get("/degraded-mode/status")
def get_degraded_mode_status(_: dict = Depends(security.get_current_user)):
    """Get degraded mode status."""
    try:
        return degraded_mode_manager.get_status()
    except Exception as e:
        log.error("get_degraded_mode_status_failed", error=str(e))
        raise HTTPException(
            status_code=500, detail="Failed to get degraded mode status"
        )


@router.post("/circuit-breaker/{key}/reset")
def reset_circuit_breaker(
    key: str,
    _: dict = Depends(security.get_current_user),
):
    """Reset a specific circuit breaker."""
    try:
        if key not in error_handler.circuit_breakers:
            raise HTTPException(
                status_code=404, detail=f"Circuit breaker '{key}' not found"
            )

        circuit_breaker = error_handler.circuit_breakers[key]
        circuit_breaker.state = "CLOSED"
        circuit_breaker.failure_count = 0
        circuit_breaker.last_failure_time = None

        log.info("circuit_breaker_reset", key=key)
        return {
            "message": f"Circuit breaker '{key}' reset",
            "key": key,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error("reset_circuit_breaker_failed", key=key, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to reset circuit breaker")


@router.post("/circuit-breaker/{key}/open")
def open_circuit_breaker(
    key: str,
    _: dict = Depends(security.get_current_user),
):
    """Manually open a circuit breaker."""
    try:
        if key not in error_handler.circuit_breakers:
            raise HTTPException(
                status_code=404, detail=f"Circuit breaker '{key}' not found"
            )

        circuit_breaker = error_handler.circuit_breakers[key]
        circuit_breaker.state = "OPEN"
        circuit_breaker.last_failure_time = datetime.now()

        log.info("circuit_breaker_manually_opened", key=key)
        return {
            "message": f"Circuit breaker '{key}' opened",
            "key": key,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error("open_circuit_breaker_failed", key=key, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to open circuit breaker")


@router.get("/error-counts")
def get_error_counts(_: dict = Depends(security.get_current_user)):
    """Get error counts by category and severity."""
    try:
        return {
            "error_counts": error_handler.error_counts,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        log.error("get_error_counts_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get error counts")


@router.post("/error-counts/reset")
def reset_error_counts(_: dict = Depends(security.get_current_user)):
    """Reset all error counts."""
    try:
        error_handler.error_counts.clear()
        log.info("error_counts_reset")
        return {
            "message": "Error counts reset",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        log.error("reset_error_counts_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to reset error counts")


@router.get("/test/circuit-breaker")
def test_circuit_breaker(_: dict = Depends(security.get_current_user)):
    """Test circuit breaker functionality."""
    try:
        # This will trigger the circuit breaker
        circuit_breaker = error_handler.get_circuit_breaker("test")

        def failing_function():
            raise Exception("Test error for circuit breaker")

        circuit_breaker.call(failing_function)
        return {"message": "Circuit breaker test completed"}
    except Exception as e:
        return {"message": f"Circuit breaker test failed: {str(e)}"}


@router.get("/test/degraded-mode")
def test_degraded_mode(_: dict = Depends(security.get_current_user)):
    """Test degraded mode functionality."""
    try:
        if degraded_mode_manager.is_degraded():
            raise DegradedModeError("System is in degraded mode")
        return {"message": "System is operating normally"}
    except DegradedModeError as e:
        return {"message": f"Degraded mode test: {str(e)}"}
