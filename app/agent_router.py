"""
Agent router for multi-agent system.
Provides endpoints for agent registration, status, and heartbeat.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from . import schemas, security, validators
from .agent_service import agent_service
from .db import get_session

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/register", response_model=Dict[str, Any])
def register_agent(
    agent_data: schemas.AgentRegistration,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """Register a new agent or update existing agent."""
    try:
        agent = agent_service.register_agent(
            session=session,
            agent_id=agent_data.agent_id,
            capabilities=agent_data.capabilities,
        )

        return {
            "message": "Agent registered successfully",
            "agent_id": agent.agent_id,
            "status": agent.status,
            "capabilities": agent.capabilities,
            "created_at": agent.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register agent: {str(e)}",
        )


@router.post("/{agent_id}/ping")
def agent_heartbeat(
    agent_id: validators.AgentID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """Update agent heartbeat."""
    agent = agent_service.update_heartbeat(session=session, agent_id=agent_id)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )

    return {
        "message": "Heartbeat updated",
        "agent_id": agent.agent_id,
        "status": agent.status,
        "last_heartbeat": agent.last_heartbeat.isoformat(),
    }


@router.get("/{agent_id}/status")
def get_agent_status(
    agent_id: validators.AgentID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """Get agent status and health information."""
    status_info = agent_service.get_agent_status(session=session, agent_id=agent_id)

    if not status_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )

    return status_info


@router.get("/", response_model=List[Dict[str, Any]])
def list_agents(
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """List all agents with their status."""
    return agent_service.list_agents(session=session)


@router.get("/available", response_model=List[Dict[str, Any]])
def get_available_agents(
    capabilities: List[str] = None,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """Get list of available agents that match required capabilities."""
    return agent_service.get_available_agents(
        session=session, capabilities=capabilities
    )


@router.delete("/{agent_id}")
def deregister_agent(
    agent_id: validators.AgentID,
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    """Deregister an agent."""
    success = agent_service.deregister_agent(session=session, agent_id=agent_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )

    return {"message": "Agent deregistered successfully"}
