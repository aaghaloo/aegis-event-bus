# app/schemas.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator

from .models import AgentStatus, AuditLog, TaskStatus
from .validators import _validate_agent_id, _validate_job_id, _validate_task_id


class Job(BaseModel):
    job_id: str

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        return _validate_job_id(v)


class Token(BaseModel):
    access_token: str
    token_type: str


class JobsPage(BaseModel):
    items: List[AuditLog]
    next_cursor: Optional[int] = None


class AgentRegistration(BaseModel):
    """Schema for agent registration."""

    agent_id: str
    capabilities: List[str]

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        return _validate_agent_id(v)


class AgentStatus(BaseModel):
    """Schema for agent status response."""

    agent_id: str
    status: AgentStatus
    capabilities: List[str]
    last_heartbeat: str
    is_stale: bool
    created_at: str
    updated_at: str


class TaskCreate(BaseModel):
    """Schema for task creation."""

    job_id: str
    agent_id: str
    payload: Dict[str, Any]
    required_capabilities: Optional[List[str]] = None

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        return _validate_job_id(v)

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        return _validate_agent_id(v)


class TaskAssignment(BaseModel):
    """Schema for task assignment."""

    task_id: str
    agent_id: str

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        return _validate_task_id(v)

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        return _validate_agent_id(v)


class TaskUpdate(BaseModel):
    """Schema for task status update."""

    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
