# tests/conftest.py
"""
Pytest fixtures for an isolated in-memory SQLite database.

 * Forces the app to think it is talking to SQLite.
 * Builds a fresh engine for **each test**, so primary-key counters
   reset to 1 and tests remain deterministic.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.db as db
from app.main import app

# Ensure every library that relies on DATABASE_URL sees SQLite and
# integration tests that require Postgres will auto-skip.
os.environ["DATABASE_URL"] = "sqlite://"


@pytest.fixture()
def engine():
    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keeps the in-memory DB alive per test
    )
    yield eng
    eng.dispose()


@pytest.fixture()
def session(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sess:
        yield sess
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(session, engine):
    """
    • Point the application’s engines at our test engine.
    • Override FastAPI's `get_session` dependency so every request
      uses a brand-new Session bound to that engine.
    """
    db.engine_rw = engine
    db.engine_ro = engine

    def _session_override():
        with Session(engine) as s:
            yield s

    app.dependency_overrides[db.get_session] = _session_override

    cl = TestClient(app)
    yield cl

    app.dependency_overrides.clear()
