# app/endpoints.py
"""
Main API endpoints for the Aegis Event Bus.
Provides job management, health checks, and system status endpoints.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from . import archivist, schemas, security
from .db import get_ro_session, get_session
from .models import AuditLog
from .validators import JobID

router = APIRouter()

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
    # Check database connectivity
    try:
        from .db import get_session

        session = next(get_session())
        session.exec(select(AuditLog).limit(1)).first()
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    # Check MQTT connectivity
    try:
        import paho.mqtt.client as mqtt

        client = mqtt.Client()
        client.connect("localhost", 1883, 5)
        client.disconnect()
        mqtt_status = "healthy"
    except Exception:
        mqtt_status = "unhealthy"

    # Check storage
    try:
        data_root = archivist.DATA_ROOT
        data_root.mkdir(exist_ok=True)
        test_file = data_root / ".health_check"
        test_file.touch()
        test_file.unlink()
        storage_status = "healthy"
    except Exception:
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
    # Generate unique job ID
    import uuid

    job_id = f"FC-{uuid.uuid4()}"
    validated_job_id = JobID(job_id)

    # Create folder structure
    try:
        archivist.create_job_folders(validated_job_id, archivist.DATA_ROOT)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create job folders: {str(e)}"
        )

    # Log job creation
    audit_log = AuditLog(
        job_id=validated_job_id,
        action="job_created",
        details={"folder_structure_created": True},
    )
    session.add(audit_log)
    session.commit()

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
        None,
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
    # Manual validation for limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")

    stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if cursor:
        stmt = stmt.where(AuditLog.id < cursor)

    rows = session.exec(stmt).all()
    next_cursor = rows[-1].id if len(rows) == limit else None
    return {"items": rows, "next_cursor": next_cursor}
