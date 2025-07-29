"""
Task service layer for multi-agent system.
Handles task assignment, status tracking, and result collection.
"""

import datetime as dt
from typing import List, Optional

import structlog
from sqlmodel import Session, select

from .models import Task, TaskStatus

log = structlog.get_logger(__name__)


class TaskService:
    """Thin CRUD / workflow wrapper around the Task table."""

    def __init__(self, session: Session):
        self.session = session

    # ---------- create / assign -------------------------------------------------
    def create_task(
        self,
        job_id: str,
        agent_id: str,
        payload: dict,
    ) -> Task:
        task = Task(
            job_id=job_id,
            agent_id=agent_id,
            payload=payload,
            status=TaskStatus.PENDING,
            created_at=dt.datetime.now(dt.UTC),
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    # ---------- state transitions ----------------------------------------------
    def update_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[dict] = None,
    ) -> Task:
        task = self.session.get(Task, task_id)
        if not task:
            raise ValueError("task not found")

        task.status = status
        if result is not None:
            task.result = result
        if status in {TaskStatus.COMPLETED, TaskStatus.FAILED}:
            task.completed_at = dt.datetime.now(dt.UTC)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    # ---------- queries ---------------------------------------------------------
    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def list_by_job(self, job_id: str) -> List[Task]:
        return self.session.exec(select(Task).where(Task.job_id == job_id)).all()
