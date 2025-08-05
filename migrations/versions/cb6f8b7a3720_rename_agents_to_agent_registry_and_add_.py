"""rename agents to agent_registry and add role field

Revision ID: cb6f8b7a3720
Revises: 7c165f5e0b93
Create Date: 2025-08-05 16:35:44.086800

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cb6f8b7a3720"
down_revision: Union[str, Sequence[str], None] = "7c165f5e0b93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add role column to agents table
    op.add_column("agents", sa.Column("role", sa.String(), nullable=True))

    # Rename last_heartbeat to last_seen
    op.alter_column("agents", "last_heartbeat", new_column_name="last_seen")

    # Rename table from agents to agent_registry
    op.rename_table("agents", "agent_registry")

    # Update foreign key constraint in tasks table
    op.drop_constraint("tasks_agent_id_fkey", "tasks", type_="foreignkey")
    op.create_foreign_key(
        "tasks_agent_id_fkey", "tasks", "agent_registry", ["agent_id"], ["agent_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraint
    op.drop_constraint("tasks_agent_id_fkey", "tasks", type_="foreignkey")

    # Rename table back from agent_registry to agents
    op.rename_table("agent_registry", "agents")

    # Rename last_seen back to last_heartbeat
    op.alter_column("agents", "last_seen", new_column_name="last_heartbeat")

    # Drop role column
    op.drop_column("agents", "role")

    # Recreate original foreign key constraint
    op.create_foreign_key(None, "tasks", "agents", ["agent_id"], ["agent_id"])
