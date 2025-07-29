"""
Task service layer for multi-agent system.
Handles task assignment, status tracking, and result collection.
"""

import datetime as dt
from typing import Any, Dict, List, Optional
from uuid import uuid4

import structlog
from sqlmodel import Session, select

from .models import Agent, AgentStatus, Task, TaskStatus

log = structlog.get_logger(__name__)


class TaskService:
    """Service for task management operations."""

    def __init__(self):
        self.task_timeout = dt.timedelta(hours=1)  # 1 hour timeout

    def create_task(
        self,
        session: Session,
        job_id: str,
        payload: dict,
        required_capabilities: Optional[List[str]] = None,
    ) -> Task:
        """Create a new task."""
        task_id = f"TASK-{uuid4()}"
        now = dt.datetime.now(dt.UTC)

        task = Task(
            task_id=task_id,
            job_id=job_id,
            status=TaskStatus.PENDING,
            payload=payload,
            created_at=now,
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        log.info(
            "task_created",
            task_id=task_id,
            job_id=job_id,
            required_capabilities=required_capabilities,
        )
        return task

    def assign_task(
        self, session: Session, task_id: str, agent_id: str
    ) -> Optional[Task]:
        """Assign a task to an agent."""
        now = dt.datetime.now(dt.UTC)

        # Get the task
        task = session.exec(select(Task).where(Task.task_id == task_id)).first()

        if not task:
            log.warning("task_not_found", task_id=task_id)
            return None

        # Check if task is already assigned
        if task.status != TaskStatus.PENDING:
            log.warning(
                "task_already_assigned", task_id=task_id, current_status=task.status
            )
            return None

        # Get the agent
        agent = session.exec(select(Agent).where(Agent.agent_id == agent_id)).first()

        if not agent:
            log.warning("agent_not_found", agent_id=agent_id)
            return None

        # Check if agent is available
        if agent.status != AgentStatus.ONLINE:
            log.warning("agent_not_available", agent_id=agent_id, status=agent.status)
            return None

        # Check if agent is stale
        if (now - agent.last_heartbeat) > dt.timedelta(minutes=5):
            log.warning("agent_stale", agent_id=agent_id)
            return None

        # Assign the task
        task.agent_id = agent_id
        task.status = TaskStatus.ASSIGNED
        task.assigned_at = now

        session.add(task)
        session.commit()
        session.refresh(task)

        log.info(
            "task_assigned", task_id=task_id, agent_id=agent_id, job_id=task.job_id
        )
        return task

    def update_task_status(
        self,
        session: Session,
        task_id: str,
        status: TaskStatus,
        result: Optional[dict] = None,
        error_message: Optional[str] = None,
    ) -> Optional[Task]:
        """Update task status and optionally add result."""
        now = dt.datetime.now(dt.UTC)

        task = session.exec(select(Task).where(Task.task_id == task_id)).first()

        if not task:
            log.warning("task_not_found", task_id=task_id)
            return None

        # Update task
        task.status = status
        task.updated_at = now

        if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            task.completed_at = now

        if result is not None:
            task.result = result

        if error_message is not None:
            task.error_message = error_message

        session.add(task)
        session.commit()
        session.refresh(task)

        log.info(
            "task_status_updated",
            task_id=task_id,
            status=status,
            has_result=result is not None,
            has_error=error_message is not None,
        )
        return task

    def get_task_status(
        self, session: Session, task_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get task status and details."""
        task = session.exec(select(Task).where(Task.task_id == task_id)).first()

        if not task:
            return None

        return {
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "job_id": task.job_id,
            "status": task.status,
            "payload": task.payload,
            "result": task.result,
            "error_message": task.error_message,
            "created_at": task.created_at.isoformat(),
            "assigned_at": task.assigned_at.isoformat() if task.assigned_at else None,
            "completed_at": (
                task.completed_at.isoformat() if task.completed_at else None
            ),
        }

    def get_tasks_by_job(self, session: Session, job_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific job."""
        tasks = session.exec(select(Task).where(Task.job_id == job_id)).all()

        return [
            {
                "task_id": task.task_id,
                "agent_id": task.agent_id,
                "status": task.status,
                "payload": task.payload,
                "result": task.result,
                "error_message": task.error_message,
                "created_at": task.created_at.isoformat(),
                "assigned_at": (
                    task.assigned_at.isoformat() if task.assigned_at else None
                ),
                "completed_at": (
                    task.completed_at.isoformat() if task.completed_at else None
                ),
            }
            for task in tasks
        ]

    def get_pending_tasks(self, session: Session) -> List[Dict[str, Any]]:
        """Get all pending tasks."""
        tasks = session.exec(
            select(Task).where(Task.status == TaskStatus.PENDING)
        ).all()

        return [
            {
                "task_id": task.task_id,
                "job_id": task.job_id,
                "payload": task.payload,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

    def get_tasks_by_agent(
        self, session: Session, agent_id: str
    ) -> List[Dict[str, Any]]:
        """Get all tasks assigned to a specific agent."""
        tasks = session.exec(select(Task).where(Task.agent_id == agent_id)).all()

        return [
            {
                "task_id": task.task_id,
                "job_id": task.job_id,
                "status": task.status,
                "payload": task.payload,
                "result": task.result,
                "error_message": task.error_message,
                "created_at": task.created_at.isoformat(),
                "assigned_at": (
                    task.assigned_at.isoformat() if task.assigned_at else None
                ),
                "completed_at": (
                    task.completed_at.isoformat() if task.completed_at else None
                ),
            }
            for task in tasks
        ]

    def cleanup_stale_tasks(self, session: Session) -> int:
        """Clean up tasks that have been pending for too long."""
        now = dt.datetime.now(dt.UTC)
        cutoff_time = now - self.task_timeout

        stale_tasks = session.exec(
            select(Task).where(
                (Task.status == TaskStatus.PENDING) & (Task.created_at < cutoff_time)
            )
        ).all()

        cleaned_count = 0
        for task in stale_tasks:
            task.status = TaskStatus.CANCELLED
            task.error_message = "Task timed out"
            session.add(task)
            cleaned_count += 1

        if cleaned_count > 0:
            session.commit()
            log.info("stale_tasks_cleaned", count=cleaned_count)

        return cleaned_count


# Global task service instance
task_service = TaskService()
