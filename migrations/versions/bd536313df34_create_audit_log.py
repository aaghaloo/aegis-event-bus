"""create audit_log (corrected initial migration)

Revision ID: bd536313df34
Revises:
Create Date: 2025-07-13 22:18:24.110812
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic.
revision = "bd536313df34"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Ensure pgcrypto (digest()) is available
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    # 2. Create table (proper initial state)
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("job_id", sa.String, nullable=False, index=True),
        sa.Column("action", sa.String, nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("sha256", sa.Text, nullable=True),
    )

    # 3. Trigger function to populate sha256
    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_auditlog_sha()
        RETURNS trigger AS $$
        BEGIN
          NEW.sha256 := encode(digest(NEW.job_id,'sha256'),'hex');
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    # 4. Trigger itself
    op.execute(
        """
        CREATE TRIGGER audit_log_hash
        BEFORE INSERT ON audit_log
        FOR EACH ROW EXECUTE FUNCTION set_auditlog_sha();
        """
    )


def downgrade() -> None:
    # Drop trigger + function first
    op.execute("DROP TRIGGER IF EXISTS audit_log_hash ON audit_log;")
    op.execute("DROP FUNCTION IF EXISTS set_auditlog_sha();")
    # Drop table
    op.drop_table("audit_log")
