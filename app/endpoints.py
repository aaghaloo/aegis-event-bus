# app/endpoints.py
import json
from uuid import uuid4

import paho.mqtt.publish as mqtt_publish
import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from starlette.responses import Response

from . import archivist, schemas, security
from .cert_manager import cert_manager
from .config import settings
from .db import get_ro_session, get_session
from .models import AuditLog
from .monitoring import health_checker, performance_monitor
from .validators import Cursor, _validate_job_id

router = APIRouter()
log = structlog.get_logger(__name__)


# ────────────────────────── root endpoint ────────────────────────────────────
@router.get("/", tags=["Status"])
def read_root():
    return {"status": "Aegis Event Bus is online"}


# ────────────────────────── health checks ────────────────────────────────────
@router.get("/healthz", tags=["Health"])
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}


@router.get("/healthz/detailed", tags=["Health"])
def detailed_health_check():
    """Detailed health check including certificate validation."""
    health_status = {
        "status": "ok",
        "timestamp": "2024-01-01T00:00:00Z",  # Would use real timestamp
        "version": "1.0.0",
        "components": {"database": "ok", "mqtt": "ok", "certificates": "ok"},
    }

    # Check certificate expiry
    cert_status = cert_manager.validate_certificate_expiry()
    if any(info and info.get("is_expired", False) for info in cert_status.values()):
        health_status["components"]["certificates"] = "warning"
        health_status["certificate_warnings"] = cert_status

    return health_status


@router.get("/healthz/comprehensive", tags=["Health"])
def comprehensive_health_check():
    """Comprehensive health check of all system components."""
    return health_checker.comprehensive_health_check()


# ────────────────────────── monitoring endpoints ──────────────────────────────
@router.get("/metrics/performance", tags=["Monitoring"])
def get_performance_metrics(_: dict = Depends(security.get_current_user)):
    """Get performance metrics (admin only)."""
    return performance_monitor.get_performance_stats()


@router.get("/metrics/system", tags=["Monitoring"])
def get_system_metrics(_: dict = Depends(security.get_current_user)):
    """Get system resource metrics (admin only)."""
    return performance_monitor.get_system_stats()


@router.get("/metrics/health", tags=["Monitoring"])
def get_health_metrics(_: dict = Depends(security.get_current_user)):
    """Get detailed health metrics (admin only)."""
    return {
        "database": health_checker.check_database_health(),
        "mqtt": health_checker.check_mqtt_health(),
        "certificates": health_checker.check_certificate_health(),
        "system": performance_monitor.get_system_stats(),
    }


@router.get("/metrics/prometheus", tags=["Monitoring"])
def get_prometheus_metrics():
    """Get metrics in Prometheus format for monitoring."""
    from .monitoring import performance_monitor

    return Response(
        content=performance_monitor.prometheus_metrics.get_prometheus_format(),
        media_type="text/plain",
    )


# ────────────────────────── write path ───────────────────────────────────────
@router.post("/job", response_model=schemas.Job, tags=["Jobs"])
def create_new_job(
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    job_id = f"FC-{uuid4()}"
    # Validate job_id using the validation function
    validated_job_id = _validate_job_id(job_id)
    archivist.create_job_folders(validated_job_id, archivist.DATA_ROOT)

    with session:
        entry = AuditLog(job_id=validated_job_id, action="job.created")
        session.add(entry)
        session.commit()
        session.refresh(entry)

    payload = {"job_id": validated_job_id, "timestamp": entry.timestamp.isoformat()}
    try:
        # Use certificate manager for TLS configuration
        tls_config = cert_manager.get_mqtt_tls_config()

        mqtt_publish.single(
            topic="aegis/job/created",
            payload=json.dumps(payload),
            hostname=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            tls=tls_config,
        )
    except Exception as exc:
        log.warning("mqtt.publish_failed", job_id=validated_job_id, err=str(exc))

    return {"job_id": validated_job_id}


# ──────────────────────────  read path  ─────────────────────────────────
@router.get("/jobs", response_model=schemas.JobsPage, tags=["Jobs"])
def list_recent_jobs(
    session: Session = Depends(get_ro_session),
    cursor: Cursor = Query(None, description="last row id from prev page"),
    limit: int = Query(20, description="items per page"),
    _: dict = Depends(security.get_current_user),
):
    # Manual validation for limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")

    stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if cursor:
        stmt = stmt.where(AuditLog.id < cursor)

    rows = session.exec(stmt).all()
    next_cursor = rows[-1].id if len(rows) == limit else None
    return {"items": rows, "next_cursor": next_cursor}
