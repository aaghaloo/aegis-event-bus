"""
Task service layer for multi-agent system.
Handles task assignment, status tracking, and result collection.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from sqlmodel import Session, select

from .models import Task, TaskStatus

log = structlog.get_logger(__name__)


class TaskService:
    """Thin CRUD / workflow wrapper around the Task table."""

    def __init__(self, session: Session):
        self.session = session

    # ---------- create / assign -------------------------------------------------
    def create_task(self, job_id: str, agent_id: str, payload: Dict[str, Any]) -> Task:
        """Create a new task."""
        # Record metrics
        from .monitoring import performance_monitor

        performance_monitor.prometheus_metrics.record_task_creation(agent_id, "pending")

        task = Task(
            job_id=job_id,
            agent_id=agent_id,
            status=TaskStatus.PENDING,
            payload=payload,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    # ---------- state transitions ----------------------------------------------
    def update_status(
        self, task_id: str, status: TaskStatus, result: Optional[Dict[str, Any]] = None
    ) -> Task:
        """Update task status and result."""
        task = self.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Record metrics
        from .monitoring import performance_monitor

        # Handle both string and enum status values
        status_value = status.value if hasattr(status, "value") else status
        performance_monitor.prometheus_metrics.record_task_completion(
            task.agent_id, status_value
        )

        task.status = status
        task.result = result

        if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            task.completed_at = datetime.now(timezone.utc)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    # ---------- queries ---------------------------------------------------------
    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def list_by_job(self, job_id: str) -> List[Task]:
        return self.session.exec(select(Task).where(Task.job_id == job_id)).all()
