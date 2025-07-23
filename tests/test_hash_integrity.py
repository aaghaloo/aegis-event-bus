# tests/test_hash_integrity.py
# Verify the Postgres trigger fills sha256 in audit_log (no skipping).

import hashlib
import os
import uuid
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlmodel import create_engine


def _get_pg_dsn() -> str:
    """Return a Postgres DSN from env or .env.local (fallback)."""
    dsn = os.getenv("DATABASE_URL", "")
    if not dsn or dsn.startswith("sqlite"):
        env_local = Path(".env.local")
        if env_local.exists():
            for line in env_local.read_text().splitlines():
                if line.startswith("DATABASE_URL="):
                    dsn = line.split("=", 1)[1].strip().strip('"')
                    break
    return dsn


@pytest.mark.integration
def test_audit_log_hash_trigger_direct():
    """Insert directly into audit_log and confirm sha256 is filled by trigger."""
    dsn = _get_pg_dsn()
    assert dsn.startswith(
        "postgresql"
    ), f"Postgres DSN not found. Got: {dsn or '<empty>'}"

    engine = create_engine(dsn)

    job_id = f"UT-{uuid.uuid4()}"
    action = "unit.test"

    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO audit_log (job_id, action) VALUES (:j, :a)"),
            {"j": job_id, "a": action},
        )
        row = conn.execute(
            text(
                "SELECT sha256 FROM audit_log "
                "WHERE job_id = :j ORDER BY id DESC LIMIT 1"
            ),
            {"j": job_id},
        ).one()

    expected = hashlib.sha256(job_id.encode()).hexdigest()
    assert row[0] == expected
    assert len(row[0]) == 64
