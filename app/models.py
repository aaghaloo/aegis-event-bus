# app/models.py

import datetime as dt
from enum import Enum
from typing import List, Optional

from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(str, Enum):
    """Agent status enumeration."""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


class AuditLog(SQLModel, table=True):
    """
    Core immutable event log for A0.

    sha256 is a tamper‑evident hash (computed in DB trigger) of job_id.
    """

    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True)
    action: str
    # Keep timezone‑aware timestamps (your existing style)
    timestamp: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    # NEW integrity column (filled ONLY by DB trigger)
    sha256: Optional[str] = Field(
        default=None, description="Integrity hash of job_id (sha256)"
    )


class Agent(SQLModel, table=True):
    """
    Agent registry for multi-agent system.
    Tracks agent capabilities, status, and heartbeat.
    """

    __tablename__ = "agents"

    agent_id: str = Field(primary_key=True, description="Unique agent identifier")
    capabilities: List[str] = Field(
        sa_column=Column(JSON), description="List of agent capabilities"
    )
    status: AgentStatus = Field(default=AgentStatus.OFFLINE)
    last_heartbeat: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Last heartbeat timestamp",
    )
    created_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class Task(SQLModel, table=True):
    """
    Task management for multi-agent system.
    Tracks task assignment, status, and results.
    """

    __tablename__ = "tasks"

    task_id: str = Field(primary_key=True, description="Unique task identifier")
    agent_id: str = Field(foreign_key="agents.agent_id", index=True)
    job_id: str = Field(index=True, description="Associated job ID")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    payload: dict = Field(sa_column=Column(JSON), description="Task payload/parameters")
    result: Optional[dict] = Field(
        default=None, sa_column=Column(JSON), description="Task result data"
    )
    error_message: Optional[str] = Field(
        default=None, description="Error message if failed"
    )
    created_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    assigned_at: Optional[dt.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="When task was assigned to agent",
    )
    completed_at: Optional[dt.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
        description="When task was completed",
    )
