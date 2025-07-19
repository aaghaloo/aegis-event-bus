# tests/conftest.py
"""
Pytest fixtures for the Event Bus service.

We intentionally set DATABASE_URL *before* importing `app.db` so the
application uses an in‑memory SQLite engine during tests.

Ruff rule E402 (imports not at top) is suppressed because of this one
required assignment.
"""

# ruff: noqa: E402

import os

# Must be set before importing app.db so its engine points to SQLite memory.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.db as db
from app.main import app

# ---------- shared in-memory engine ----------
engine = create_engine(
    "sqlite://",  # single in-memory DB
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # one global connection so tables persist across sessions
)
db.engine = engine  # make the app use this engine
# ---------------------------------------------


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Override dependency to always return our shared session
    db.get_session = lambda: session
    yield TestClient(app)
