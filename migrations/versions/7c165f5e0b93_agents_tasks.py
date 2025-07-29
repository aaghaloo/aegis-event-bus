"""agents & tasks

Revision ID: 7c165f5e0b93
Revises: bd536313df34_tz_default
Create Date: 2024-01-01 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7c165f5e0b93"
down_revision = "bd536313df34_tz_default"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create agents table
    op.create_table(
        "agents",
        sa.Column("agent_id", sa.String(), nullable=False),
        sa.Column(
            "capabilities", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("agent_id"),
    )

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column("task_id", sa.String(), nullable=False),
        sa.Column("agent_id", sa.String(), nullable=True),
        sa.Column("job_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("payload", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("result", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("task_id"),
    )

    # Create indexes
    op.create_index(op.f("ix_tasks_agent_id"), "tasks", ["agent_id"], unique=False)
    op.create_index(op.f("ix_tasks_job_id"), "tasks", ["job_id"], unique=False)

    # Create foreign key constraint
    op.create_foreign_key(None, "tasks", "agents", ["agent_id"], ["agent_id"])


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint(None, "tasks", type_="foreignkey")

    # Drop indexes
    op.drop_index(op.f("ix_tasks_job_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_agent_id"), table_name="tasks")

    # Drop tables
    op.drop_table("tasks")
    op.drop_table("agents")
