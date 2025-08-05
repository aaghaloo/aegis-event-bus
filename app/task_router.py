# app/task_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, security, validators
from app.agent_service import agent_service
from app.db import get_session
from app.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def _check_agent_availability(session: Session, agent_id: str) -> bool:
    """Check if agent is available (online and not stale)."""
    status_info = agent_service.get_agent_status(session=session, agent_id=agent_id)
    if not status_info:
        return False

    # Check if agent is online and not stale
    return status_info["status"] == "online" and not status_info["is_stale"]


# ---------- create -------------------------------------------------------------
@router.post("/create", response_model=dict)
def create_task(
    task_in: schemas.TaskCreate,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """
    Create a task in *pending* state and immediately assign it to target agent.
    Checks agent registry to ensure agent is online before routing.
    """
    # Check if agent is available
    if not _check_agent_availability(session, task_in.agent_id):
        raise HTTPException(
            status_code=400,
            detail=f"Agent {task_in.agent_id} is not available (offline or stale)",
        )

    svc = TaskService(session)
    task = svc.create_task(
        job_id=task_in.job_id,
        agent_id=task_in.agent_id,
        payload=task_in.payload,
    )

    return {
        "task_id": task.task_id,
        "job_id": task.job_id,
        "agent_id": task.agent_id,
        "status": task.status,
        "payload": task.payload,
        "created_at": task.created_at.isoformat(),
    }


# ---------- fan-out: create multiple tasks for a job ---------------------------
@router.post("/job/{job_id}/create-bulk", response_model=List[dict])
def create_tasks_for_job(
    job_id: validators.JobID,
    tasks_data: List[schemas.TaskCreate],
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """
    Create multiple tasks for a job (fan-out pattern).
    Each task will be assigned to the specified agent.
    Checks agent registry to ensure agents are online before routing.
    """
    svc = TaskService(session)
    created_tasks = []
    skipped_tasks = []

    for task_data in tasks_data:
        # Ensure all tasks belong to the same job
        if task_data.job_id != job_id:
            raise HTTPException(
                status_code=400,
                detail=f"Task job_id {task_data.job_id} must match URL job_id {job_id}",
            )

        # Check if agent is available
        if not _check_agent_availability(session, task_data.agent_id):
            skipped_tasks.append(
                {"agent_id": task_data.agent_id, "reason": "Agent is offline or stale"}
            )
            continue

        task = svc.create_task(
            job_id=task_data.job_id,
            agent_id=task_data.agent_id,
            payload=task_data.payload,
        )

        created_tasks.append(
            {
                "task_id": task.task_id,
                "job_id": task.job_id,
                "agent_id": task.agent_id,
                "status": task.status,
                "payload": task.payload,
                "created_at": task.created_at.isoformat(),
            }
        )

    # Return both created and skipped tasks
    return {
        "created_tasks": created_tasks,
        "skipped_tasks": skipped_tasks,
        "total_requested": len(tasks_data),
        "total_created": len(created_tasks),
        "total_skipped": len(skipped_tasks),
    }


# ---------- fan-in: get job summary with task statuses ------------------------
@router.get("/job/{job_id}/summary", response_model=dict)
def get_job_summary(
    job_id: validators.JobID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """
    Get job summary with task status counts (fan-in pattern).
    """
    svc = TaskService(session)
    tasks = svc.list_by_job(job_id)

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for job")

    # Count tasks by status
    status_counts = {}
    total_tasks = len(tasks)
    completed_tasks = 0
    failed_tasks = 0

    for task in tasks:
        status = task.status.value
        status_counts[status] = status_counts.get(status, 0) + 1

        if status == "completed":
            completed_tasks += 1
        elif status == "failed":
            failed_tasks += 1

    # Calculate completion percentage
    completion_percentage = (
        (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    )

    return {
        "job_id": job_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "completion_percentage": round(completion_percentage, 2),
        "status_counts": status_counts,
        "is_complete": completed_tasks + failed_tasks == total_tasks,
    }


# ---------- status update ------------------------------------------------------
@router.post("/{task_id}/update", response_model=dict)
def update_task(
    task_id: validators.TaskID,
    upd: schemas.TaskUpdate,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    svc = TaskService(session)
    try:
        task = svc.update_status(task_id, upd.status, upd.result)
    except ValueError:
        raise HTTPException(status_code=404, detail="task not found")

    return {
        "task_id": task.task_id,
        "job_id": task.job_id,
        "agent_id": task.agent_id,
        "status": task.status,
        "payload": task.payload,
        "result": task.result,
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


# ---------- fetch --------------------------------------------------------------
@router.get("/{task_id}", response_model=dict)
def get_task(
    task_id: validators.TaskID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    svc = TaskService(session)
    task = svc.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    return {
        "task_id": task.task_id,
        "job_id": task.job_id,
        "agent_id": task.agent_id,
        "status": task.status,
        "payload": task.payload,
        "result": task.result,
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


@router.get("/job/{job_id}", response_model=list[dict])
def list_tasks_for_job(
    job_id: validators.JobID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    svc = TaskService(session)
    return [
        {
            "task_id": task.task_id,
            "job_id": task.job_id,
            "agent_id": task.agent_id,
            "status": task.status,
            "payload": task.payload,
            "result": task.result,
            "created_at": task.created_at.isoformat(),
            "completed_at": (
                task.completed_at.isoformat() if task.completed_at else None
            ),
        }
        for task in svc.list_by_job(job_id)
    ]
