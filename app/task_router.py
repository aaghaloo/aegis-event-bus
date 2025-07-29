# app/task_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import schemas, security
from app.db import get_session
from app.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ---------- create -------------------------------------------------------------
@router.post("/create", response_model=dict)
def create_task(
    task_in: schemas.TaskCreate,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """
    Create a task in *pending* state and immediately assign it to target agent.
    """
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


# ---------- status update ------------------------------------------------------
@router.post("/{task_id}/update", response_model=dict)
def update_task(
    task_id: str,
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
    task_id: str,
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
    job_id: str,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
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
        for task in TaskService(session).list_by_job(job_id)
    ]
