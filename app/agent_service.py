"""
Agent service layer for multi-agent system.
Handles agent registration, heartbeat, and status management.
"""

import datetime as dt
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from sqlmodel import Session, select

from .models import AgentRegistry, AgentStatus

log = structlog.get_logger(__name__)


class AgentService:
    """Service for agent management operations."""

    def __init__(self):
        self.heartbeat_timeout = dt.timedelta(minutes=5)  # 5 minutes timeout

    def register_agent(
        self, session: Session, agent_id: str, role: str, capabilities: List[str]
    ) -> AgentRegistry:
        """Register a new agent or update existing agent."""
        # Record metrics
        from .monitoring import performance_monitor

        performance_monitor.prometheus_metrics.record_agent_registration(agent_id)

        # Check if agent already exists
        existing_agent = session.get(AgentRegistry, agent_id)

        if existing_agent:
            # Update existing agent
            existing_agent.role = role
            existing_agent.capabilities = capabilities
            existing_agent.status = AgentStatus.ONLINE
            existing_agent.last_seen = datetime.now(timezone.utc)
            existing_agent.updated_at = datetime.now(timezone.utc)
            session.add(existing_agent)
            session.commit()
            session.refresh(existing_agent)
            return existing_agent
        else:
            # Create new agent
            new_agent = AgentRegistry(
                agent_id=agent_id,
                role=role,
                capabilities=capabilities,
                status=AgentStatus.ONLINE,
                last_seen=datetime.now(timezone.utc),
            )
            session.add(new_agent)
            session.commit()
            session.refresh(new_agent)
            return new_agent

    def update_heartbeat(
        self, session: Session, agent_id: str
    ) -> Optional[AgentRegistry]:
        """Update agent heartbeat and return agent info."""
        # Record metrics
        from .monitoring import performance_monitor

        performance_monitor.prometheus_metrics.record_agent_heartbeat(agent_id)

        agent = session.get(AgentRegistry, agent_id)
        if agent:
            agent.last_seen = datetime.now(timezone.utc)
            agent.updated_at = datetime.now(timezone.utc)
            session.add(agent)
            session.commit()
            session.refresh(agent)
        return agent

    def get_agent_status(
        self, session: Session, agent_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get agent status and health information."""
        agent = session.exec(
            select(AgentRegistry).where(AgentRegistry.agent_id == agent_id)
        ).first()

        if not agent:
            return None

        # Check if agent is stale (no recent heartbeat)
        now = dt.datetime.now(dt.UTC)
        # Ensure both datetimes are timezone-aware
        last_seen = (
            agent.last_seen.replace(tzinfo=dt.UTC)
            if agent.last_seen.tzinfo is None
            else agent.last_seen
        )
        is_stale = (now - last_seen) > self.heartbeat_timeout

        if is_stale and agent.status != AgentStatus.OFFLINE:
            # Update status to offline if stale
            agent.status = AgentStatus.OFFLINE
            agent.updated_at = now
            session.add(agent)
            session.commit()

        return {
            "agent_id": agent.agent_id,
            "role": agent.role,
            "status": agent.status,
            "capabilities": agent.capabilities,
            "last_seen": agent.last_seen.isoformat(),
            "is_stale": is_stale,
            "created_at": agent.created_at.isoformat(),
            "updated_at": agent.updated_at.isoformat(),
        }

    def list_agents(self, session: Session) -> List[Dict[str, Any]]:
        """List all agents with their status."""
        agents = session.exec(select(AgentRegistry)).all()
        now = dt.datetime.now(dt.UTC)

        result = []
        for agent in agents:
            # Ensure both datetimes are timezone-aware
            last_seen = (
                agent.last_seen.replace(tzinfo=dt.UTC)
                if agent.last_seen.tzinfo is None
                else agent.last_seen
            )
            is_stale = (now - last_seen) > self.heartbeat_timeout

            if is_stale and agent.status != AgentStatus.OFFLINE:
                # Update status to offline if stale
                agent.status = AgentStatus.OFFLINE
                agent.updated_at = now
                session.add(agent)

            result.append(
                {
                    "agent_id": agent.agent_id,
                    "role": agent.role,
                    "status": agent.status,
                    "capabilities": agent.capabilities,
                    "last_seen": agent.last_seen.isoformat(),
                    "is_stale": is_stale,
                    "created_at": agent.created_at.isoformat(),
                }
            )

        # Commit any status updates
        session.commit()

        return result

    def get_available_agents(
        self, session: Session, required_capabilities: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get list of available agents that match required capabilities."""
        now = dt.datetime.now(dt.UTC)

        # Get online agents
        query = select(AgentRegistry).where(AgentRegistry.status == AgentStatus.ONLINE)
        agents = session.exec(query).all()

        available_agents = []
        for agent in agents:
            # Check if agent is not stale
            last_seen = (
                agent.last_seen.replace(tzinfo=dt.UTC)
                if agent.last_seen.tzinfo is None
                else agent.last_seen
            )
            if (now - last_seen) <= self.heartbeat_timeout:
                # Check if agent has required capabilities
                if required_capabilities is None or all(
                    cap in agent.capabilities for cap in required_capabilities
                ):
                    available_agents.append(
                        {
                            "agent_id": agent.agent_id,
                            "role": agent.role,
                            "capabilities": agent.capabilities,
                            "last_seen": agent.last_seen.isoformat(),
                        }
                    )

        return available_agents

    def deregister_agent(self, session: Session, agent_id: str) -> bool:
        """Deregister an agent (mark as offline)."""
        agent = session.exec(
            select(AgentRegistry).where(AgentRegistry.agent_id == agent_id)
        ).first()

        if not agent:
            return False

        agent.status = AgentStatus.OFFLINE
        agent.updated_at = dt.datetime.now(dt.UTC)

        session.add(agent)
        session.commit()

        log.info("agent_deregistered", agent_id=agent_id)
        return True


# Global agent service instance
agent_service = AgentService()
