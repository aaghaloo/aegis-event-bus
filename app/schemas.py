# app/schemas.py
"""
Pydantic schemas for API request/response models.
Provides type-safe data validation and serialization.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Authentication token response model.

    Returned by the `/token` endpoint after successful authentication.
    Contains the JWT access token and token type.
    """

    access_token: str = Field(
        description="JWT access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    )
    token_type: str = Field(
        description="Token type (always 'bearer')", example="bearer", default="bearer"
    )


class TokenData(BaseModel):
    """
    Token data model for internal use.

    Used to decode and validate JWT token payload.
    """

    username: Optional[str] = Field(
        description="Username from token", example="testuser", default=None
    )


class HealthResponse(BaseModel):
    """
    Health check response model.

    Provides comprehensive system health information including:
    - Overall system status
    - Individual component health
    - System version and timestamp
    """

    status: str = Field(
        description="Overall system status",
        example="healthy",
        pattern="^(healthy|unhealthy)$",
    )
    timestamp: datetime = Field(
        description="Current UTC timestamp", example="2024-01-01T12:00:00Z"
    )
    version: str = Field(description="Application version", example="1.0.0")
    components: Dict[str, str] = Field(
        description="Health status of individual components",
        example={"database": "healthy", "mqtt": "healthy", "storage": "healthy"},
    )


class Job(BaseModel):
    """
    Job creation response model.

    Represents a newly created job with its unique identifier.
    The job ID follows the format: FC-{uuid} where FC stands for "File Collection".
    """

    job_id: str = Field(
        description="Unique job identifier",
        example="FC-12345678-1234-1234-1234-123456789abc",
        pattern="^FC-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    )


class AuditLogItem(BaseModel):
    """
    Audit log entry model.

    Represents a single audit log entry with:
    - Unique identifier
    - Job ID reference
    - Action performed
    - Timestamp
    - Additional details
    """

    id: int = Field(description="Unique audit log entry ID", example=1)
    job_id: str = Field(
        description="Associated job ID",
        example="FC-12345678-1234-1234-1234-123456789abc",
    )
    action: str = Field(description="Action performed", example="job_created")
    timestamp: datetime = Field(
        description="When the action occurred", example="2024-01-01T12:00:00Z"
    )
    details: Optional[Dict[str, Any]] = Field(
        description="Additional action details",
        example={"folder_structure_created": True},
        default=None,
    )


class JobsPage(BaseModel):
    """
    Paginated jobs response model.

    Provides a paginated list of audit log entries with:
    - List of job entries
    - Next cursor for pagination
    - Cursor-based pagination support
    """

    items: List[AuditLogItem] = Field(
        description="List of audit log entries",
        example=[
            {
                "id": 1,
                "job_id": "FC-12345678-1234-1234-1234-123456789abc",
                "action": "job_created",
                "timestamp": "2024-01-01T12:00:00Z",
                "details": {"folder_structure_created": True},
            }
        ],
    )
    next_cursor: Optional[int] = Field(
        description="Cursor for next page (null if no more pages)", example=2
    )


class AgentRegistration(BaseModel):
    """
    Agent registration request model.

    Used when registering a new agent with the system.
    Includes agent capabilities and metadata.
    """

    agent_id: str = Field(
        description="Unique agent identifier",
        example="agent-001",
        min_length=1,
        max_length=100,
    )
    capabilities: List[str] = Field(
        description="List of agent capabilities",
        example=["data_processing", "file_analysis", "report_generation"],
        min_items=1,
    )
    metadata: Optional[Dict[str, Any]] = Field(
        description="Additional agent metadata",
        example={"version": "1.0.0", "location": "us-east-1"},
        default=None,
    )


class AgentStatus(BaseModel):
    """
    Agent status response model.

    Provides current status information for a registered agent.
    """

    agent_id: str = Field(description="Agent identifier", example="agent-001")
    status: str = Field(
        description="Current agent status",
        example="online",
        pattern="^(online|offline|busy|idle)$",
    )
    last_seen: datetime = Field(
        description="Last heartbeat timestamp", example="2024-01-01T12:00:00Z"
    )
    capabilities: List[str] = Field(
        description="Agent capabilities", example=["data_processing", "file_analysis"]
    )


class TaskCreate(BaseModel):
    """
    Task creation request model.

    Used when creating a new task for an agent.
    """

    job_id: str = Field(
        description="Associated job ID",
        example="FC-12345678-1234-1234-1234-123456789abc",
    )
    agent_id: str = Field(description="Target agent ID", example="agent-001")
    payload: Dict[str, Any] = Field(
        description="Task payload/data",
        example={"file_path": "/data/input.txt", "operation": "process"},
    )


class TaskUpdate(BaseModel):
    """
    Task status update request model.

    Used when updating task status and results.
    """

    status: str = Field(
        description="New task status",
        example="completed",
        pattern="^(pending|assigned|in_progress|completed|failed|cancelled)$",
    )
    result: Optional[Dict[str, Any]] = Field(
        description="Task result data",
        example={"processed_files": 5, "output_path": "/data/output.txt"},
        default=None,
    )


class TaskResponse(BaseModel):
    """
    Task response model.

    Provides complete task information including status and metadata.
    """

    task_id: str = Field(
        description="Unique task identifier",
        example="task-12345678-1234-1234-1234-123456789abc",
    )
    job_id: str = Field(
        description="Associated job ID",
        example="FC-12345678-1234-1234-1234-123456789abc",
    )
    agent_id: str = Field(description="Assigned agent ID", example="agent-001")
    status: str = Field(description="Current task status", example="completed")
    payload: Dict[str, Any] = Field(
        description="Original task payload", example={"file_path": "/data/input.txt"}
    )
    result: Optional[Dict[str, Any]] = Field(
        description="Task result (if completed)",
        example={"processed_files": 5},
        default=None,
    )
    created_at: datetime = Field(
        description="Task creation timestamp", example="2024-01-01T12:00:00Z"
    )
    completed_at: Optional[datetime] = Field(
        description="Task completion timestamp",
        example="2024-01-01T12:05:00Z",
        default=None,
    )
