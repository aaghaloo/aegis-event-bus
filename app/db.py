# app/db.py
"""Database helper.

• In Docker / production → Postgres (read-write / read-only URLs)
• In pytest              → SQLite (file or memory).  Tables are auto-created.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from sqlalchemy import exc as _sa_exc
from sqlalchemy import text as _sa_text
from sqlmodel import Session, SQLModel, create_engine

# ── 1  Environment ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

_RUNNING_TESTS: Final[bool] = "PYTEST_CURRENT_TEST" in os.environ or any(
    "pytest" in a for a in sys.argv
)


# ── 2  Resolve URLs ───────────────────────────────────────────────────────────
def _clean(url: str) -> str:
    """Strip accidental query-string fragments such as '?check_same_thread=…'."""
    return url.split("?", 1)[0]


if _RUNNING_TESTS:
    DB_URL_RW = DB_URL_RO = "sqlite://"
else:
    DB_URL_RW = _clean(os.getenv("DATABASE_URL", "sqlite:///eventbus.db"))
    DB_URL_RO = _clean(os.getenv("DATABASE_URL_RO") or DB_URL_RW)


# ── 3  Engine factory ─────────────────────────────────────────────────────────
def _mk_engine(url: str):
    if url.startswith("sqlite"):
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            isolation_level="AUTOCOMMIT",  # <- lets parallel sessions see changes
            echo=False,
        )
    return create_engine(url, echo=False)


engine_rw = _mk_engine(DB_URL_RW)  # main RW engine
engine_ro = _mk_engine(DB_URL_RO)  # optional RO engine


# ── 4  Create tables automatically for SQLite ────────────────────────────────
def _ensure_sqlite_schema() -> None:
    if engine_rw.url.drivername.startswith("sqlite"):
        from . import models  # noqa: F401  (register models)

        SQLModel.metadata.create_all(engine_rw)


if _RUNNING_TESTS:
    _ensure_sqlite_schema()


# ── 5  Helper to reset AUTOINCREMENT when running tests ──────────────────────
def _reset_sqlite_sequences(sess: Session) -> None:
    if not (_RUNNING_TESTS and engine_rw.url.drivername.startswith("sqlite")):
        return
    try:
        sess.execute(_sa_text("DELETE FROM sqlite_sequence"))
        sess.commit()
    except _sa_exc.OperationalError:
        sess.rollback()  # table doesn't exist yet — safe to ignore


# ── 6  FastAPI dependencies ──────────────────────────────────────────────────
def get_session():
    _ensure_sqlite_schema()
    with Session(engine_rw, expire_on_commit=False) as sess:
        _reset_sqlite_sequences(sess)
        yield sess


def get_ro_session():
    _ensure_sqlite_schema()
    with Session(engine_ro, expire_on_commit=False) as sess:
        yield sess
