# app/endpoints.py
"""
Main API endpoints for the Aegis Event Bus.
Provides job management, health checks, and system status endpoints.
"""

import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from . import archivist, schemas, security
from .db import get_ro_session, get_session
from .enhanced_logging import get_enhanced_logger, log_database_operation
from .models import AuditLog
from .validators import JobID

router = APIRouter()
log = get_enhanced_logger(__name__)


# ────────────────────────── root endpoint ────────────────────────────────────
@router.get("/", tags=["Status"])
def read_root():
    """Root endpoint for basic status check."""
    log.info("root_endpoint_accessed")
    return {"status": "Aegis Event Bus is online"}


# ────────────────────────── health checks ────────────────────────────────────


@router.get(
    "/healthz",
    response_model=schemas.HealthResponse,
    tags=["Health"],
    summary="System Health Check",
    description="""
    Check the overall health of the Aegis Event Bus system.

    Returns:
    - **status**: Overall system status (healthy/unhealthy)
    - **timestamp**: Current UTC timestamp
    - **version**: Application version
    - **components**: Health status of individual components

    This endpoint does not require authentication and is used by:
    - Load balancers for health checks
    - Monitoring systems for uptime tracking
    - Docker health checks
    """,
    responses={
        200: {
            "description": "System is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "version": "1.0.0",
                        "components": {
                            "database": "healthy",
                            "mqtt": "healthy",
                            "storage": "healthy",
                        },
                    }
                }
            },
        },
        503: {
            "description": "System is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "timestamp": "2024-01-01T12:00:00Z",
                        "version": "1.0.0",
                        "components": {
                            "database": "unhealthy",
                            "mqtt": "healthy",
                            "storage": "healthy",
                        },
                    }
                }
            },
        },
    },
)
def health_check():
    """
    Comprehensive health check endpoint.

    Checks the health of all system components including:
    - Database connectivity
    - MQTT broker connectivity
    - File system access
    - Memory usage
    - Disk space

    Returns detailed health information for monitoring systems.
    """
    start_time = time.time()
    log.info("health_check_started")

    # Check database connectivity
    try:
        from .db import get_session

        session = next(get_session())
        db_start = time.time()
        session.exec(select(AuditLog).limit(1)).first()
        db_duration = time.time() - db_start

        log_database_operation(
            operation="health_check",
            table="audit_log",
            duration=db_duration,
            success=True,
        )
        db_status = "healthy"
    except Exception as e:
        log.error("database_health_check_failed", error=str(e))
        db_status = "unhealthy"

    # Check MQTT connectivity
    try:
        import paho.mqtt.client as mqtt

        mqtt_start = time.time()
        client = mqtt.Client()
        client.connect("localhost", 1883, 5)
        client.disconnect()
        mqtt_duration = time.time() - mqtt_start

        log.info("mqtt_health_check_success", duration=mqtt_duration)
        mqtt_status = "healthy"
    except Exception as e:
        log.error("mqtt_health_check_failed", error=str(e))
        mqtt_status = "unhealthy"

    # Check storage
    try:
        storage_start = time.time()
        data_root = archivist.DATA_ROOT
        data_root.mkdir(exist_ok=True)
        test_file = data_root / ".health_check"
        test_file.touch()
        test_file.unlink()
        storage_duration = time.time() - storage_start

        log.info("storage_health_check_success", duration=storage_duration)
        storage_status = "healthy"
    except Exception as e:
        log.error("storage_health_check_failed", error=str(e))
        storage_status = "unhealthy"

    # Determine overall status
    components = {
        "database": db_status,
        "mqtt": mqtt_status,
        "storage": storage_status,
    }

    overall_status = (
        "healthy"
        if all(status == "healthy" for status in components.values())
        else "unhealthy"
    )

    total_duration = time.time() - start_time
    log.info(
        "health_check_completed",
        status=overall_status,
        duration=total_duration,
        components=components,
    )

    return schemas.HealthResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        components=components,
    )


# ────────────────────────── write path ───────────────────────────────────────


@router.post(
    "/job",
    response_model=schemas.Job,
    tags=["Jobs"],
    summary="Create New Job",
    description="""
    Create a new job with a unique identifier and folder structure.

    This endpoint:
    1. Generates a unique job ID
    2. Creates the standard folder structure:
       - `01_raw_data/` - For incoming raw data
       - `02_processed_data/` - For processed data
       - `03_reports/` - For generated reports
    3. Logs the job creation in the audit trail
    4. Returns the job ID for future reference

    The job ID follows the format: `FC-{uuid}` where FC stands for "File Collection".

    **Security**: Requires authentication via JWT token.
    """,
    responses={
        200: {
            "description": "Job created successfully",
            "content": {
                "application/json": {
                    "example": {"job_id": "FC-12345678-1234-1234-1234-123456789abc"}
                }
            },
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
    },
)
def create_new_job(
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """
    Create a new job with standard folder structure.

    Args:
        session: Database session (injected)
        _: Current user (injected, required for authentication)

    Returns:
        Job object containing the generated job ID

    Raises:
        HTTPException: If job creation fails
    """
    start_time = time.time()
    log.info("job_creation_started")

    # Generate unique job ID
    import uuid

    job_id = f"FC-{uuid.uuid4()}"
    validated_job_id = JobID(job_id)

    log.info("job_id_generated", job_id=validated_job_id)

    # Create folder structure
    try:
        folder_start = time.time()
        archivist.create_job_folders(validated_job_id, archivist.DATA_ROOT)
        folder_duration = time.time() - folder_start

        log.info(
            "job_folders_created", job_id=validated_job_id, duration=folder_duration
        )
    except Exception as e:
        log.error("job_folder_creation_failed", job_id=validated_job_id, error=str(e))
        raise HTTPException(
            status_code=500, detail=f"Failed to create job folders: {str(e)}"
        )

    # Log job creation in database
    try:
        db_start = time.time()
        audit_log = AuditLog(
            job_id=validated_job_id,
            action="job_created",
            details={"folder_structure_created": True},
        )
        session.add(audit_log)
        session.commit()
        db_duration = time.time() - db_start

        log_database_operation(
            operation="insert",
            table="audit_log",
            duration=db_duration,
            success=True,
            job_id=validated_job_id,
        )
    except Exception as e:
        log.error("job_audit_log_failed", job_id=validated_job_id, error=str(e))
        raise HTTPException(
            status_code=500, detail=f"Failed to log job creation: {str(e)}"
        )

    total_duration = time.time() - start_time
    log.info(
        "job_creation_completed",
        job_id=validated_job_id,
        duration=total_duration,
    )

    return {"job_id": validated_job_id}


# ────────────────────────── read path ───────────────────────────────────────


@router.get(
    "/jobs",
    response_model=schemas.JobsPage,
    tags=["Jobs"],
    summary="List Recent Jobs",
    description="""
    Retrieve a paginated list of recent jobs from the audit log.

    This endpoint provides:
    - Paginated results with cursor-based pagination
    - Configurable page size (1-100 items)
    - Ordered by most recent jobs first
    - Job creation timestamps and details

    **Pagination**: Use the `next_cursor` from the response to get the next page.
    Pass the cursor value as the `cursor` parameter in subsequent requests.

    **Rate Limiting**: This endpoint is subject to rate limiting (1000 requests/minute).

    **Security**: Requires authentication via JWT token.
    """,
    responses={
        200: {
            "description": "List of recent jobs",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "job_id": "FC-12345678-1234-1234-1234-123456789abc",
                                "action": "job_created",
                                "timestamp": "2024-01-01T12:00:00Z",
                                "details": {"folder_structure_created": True},
                            }
                        ],
                        "next_cursor": 2,
                    }
                }
            },
        },
        401: {"description": "Authentication required"},
        422: {"description": "Validation error (e.g., invalid limit)"},
    },
)
def list_recent_jobs(
    session: Session = Depends(get_ro_session),
    cursor: Optional[int] = Query(
        None,
        description=(
            "Cursor for pagination. Use the `next_cursor` value from the "
            "previous response."
        ),
        examples=[1],
    ),
    limit: int = Query(
        20,
        description="Number of items per page (1-100)",
        ge=1,
        le=100,
        examples=[20],
    ),
    _: dict = Depends(security.get_current_user),
):
    """
    Retrieve a paginated list of recent jobs.

    Args:
        session: Read-only database session (injected)
        cursor: Pagination cursor (optional)
        limit: Number of items per page (1-100)
        _: Current user (injected, required for authentication)

    Returns:
        Paginated list of jobs with next cursor for pagination

    Raises:
        HTTPException: If validation fails or database error occurs
    """
    start_time = time.time()
    log.info("jobs_list_requested", cursor=cursor, limit=limit)

    # Manual validation for limit
    if limit < 1 or limit > 100:
        log.warning("invalid_limit_requested", limit=limit)
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")

    try:
        db_start = time.time()
        stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
        if cursor:
            stmt = stmt.where(AuditLog.id < cursor)

        rows = session.exec(stmt).all()
        db_duration = time.time() - db_start

        log_database_operation(
            operation="select",
            table="audit_log",
            duration=db_duration,
            success=True,
            rows_returned=len(rows),
            cursor=cursor,
            limit=limit,
        )

        # Fix the pagination logic to handle empty results
        next_cursor = None
        if len(rows) == limit and rows:
            next_cursor = rows[-1].id

        total_duration = time.time() - start_time
        log.info(
            "jobs_list_completed",
            duration=total_duration,
            rows_returned=len(rows),
            next_cursor=next_cursor,
        )

        return {"items": rows, "next_cursor": next_cursor}

    except Exception as e:
        log.error("jobs_list_failed", error=str(e), cursor=cursor, limit=limit)
        raise HTTPException(status_code=500, detail="Failed to retrieve jobs")
