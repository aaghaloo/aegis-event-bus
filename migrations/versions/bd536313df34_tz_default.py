# migrations/versions/xxxx_tz_default.py
"""Set UTC default for audit_log.timestamp"""

import sqlalchemy as sa
from alembic import op

revision = "xxxx_tz_default"
down_revision = "bd536313df34"  # change to your last rev
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "audit_log",
        "timestamp",
        server_default=sa.text("timezone('utc', now())"),
        existing_type=sa.TIMESTAMP(timezone=True),
    )


def downgrade():
    op.alter_column(
        "audit_log",
        "timestamp",
        server_default=None,
        existing_type=sa.TIMESTAMP(timezone=True),
    )
