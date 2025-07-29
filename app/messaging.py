"""
MQTT messaging constants for multi-agent system.
Defines topic patterns for agent communication.
"""

# Base topic patterns
TOPIC_BASE = "aegis"

# Job-related topics (existing)
TOPIC_JOB_CREATED = f"{TOPIC_BASE}/job/created"

# Agent-related topics (new)
TOPIC_AGENT_BASE = f"{TOPIC_BASE}/agent"
TOPIC_AGENT_TASK_ASSIGNED = f"{TOPIC_AGENT_BASE}/{{agent_id}}/task/assigned"
TOPIC_AGENT_TASK_STARTED = f"{TOPIC_AGENT_BASE}/{{agent_id}}/task/started"
TOPIC_AGENT_TASK_COMPLETED = f"{TOPIC_AGENT_BASE}/{{agent_id}}/task/completed"
TOPIC_AGENT_TASK_FAILED = f"{TOPIC_AGENT_BASE}/{{agent_id}}/task/failed"
TOPIC_AGENT_HEARTBEAT = f"{TOPIC_AGENT_BASE}/{{agent_id}}/heartbeat"
TOPIC_AGENT_STATUS = f"{TOPIC_AGENT_BASE}/{{agent_id}}/status"

# Task-related topics (new)
TOPIC_TASK_BASE = f"{TOPIC_BASE}/task"
TOPIC_TASK_CREATED = f"{TOPIC_TASK_BASE}/created"
TOPIC_TASK_ASSIGNED = f"{TOPIC_TASK_BASE}/assigned"
TOPIC_TASK_COMPLETED = f"{TOPIC_TASK_BASE}/completed"
TOPIC_TASK_FAILED = f"{TOPIC_TASK_BASE}/failed"

# System-wide topics
TOPIC_SYSTEM_HEALTH = f"{TOPIC_BASE}/system/health"
TOPIC_SYSTEM_STATUS = f"{TOPIC_BASE}/system/status"


def format_agent_topic(topic_pattern: str, agent_id: str) -> str:
    """Format agent-specific topic with agent_id."""
    return topic_pattern.format(agent_id=agent_id)


def get_agent_task_topics(agent_id: str) -> dict:
    """Get all task-related topics for a specific agent."""
    return {
        "task_assigned": format_agent_topic(TOPIC_AGENT_TASK_ASSIGNED, agent_id),
        "task_started": format_agent_topic(TOPIC_AGENT_TASK_STARTED, agent_id),
        "task_completed": format_agent_topic(TOPIC_AGENT_TASK_COMPLETED, agent_id),
        "task_failed": format_agent_topic(TOPIC_AGENT_TASK_FAILED, agent_id),
        "heartbeat": format_agent_topic(TOPIC_AGENT_HEARTBEAT, agent_id),
        "status": format_agent_topic(TOPIC_AGENT_STATUS, agent_id),
    }
