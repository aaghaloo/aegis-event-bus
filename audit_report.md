# Aegis Event Bus – Full Code Audit

Generated (UTC): 2025-07-20T05:33:17

Git commit: `8104f9935535f044d46c848c457482bde8c8da8d`

Python: 3.13.5

---

## Repository Tree (selected)

- `.env.example`
- `.pre-commit-config.yaml`
- `Dockerfile`
- `alembic.ini`
- `app\__init__.py`
- `app\archivist.py`
- `app\cli.py`
- `app\db.py`
- `app\endpoints.py`
- `app\logging_config.py`
- `app\main.py`
- `app\models.py`
- `app\schemas.py`
- `app\security.py`
- `docker-compose.yml`
- `migrations\env.py`
- `migrations\versions\bd536313df34_create_audit_log.py`
- `pyproject.toml`
- `pytest.ini`
- `requirements.txt`
- `scripts\make_code_bundle.py`
- `scripts\make_full_audit.py`
- `scripts\no_bom_check.py`
- `scripts\remove_bom.py`
- `tests\conftest.py`
- `tests\test_api.py`
- `tests\test_archivist.py`
- `tests\test_pagination.py`

## File Summary

| File | Lines | Bytes | SHA256 | EOL | Encoding |
|------|-------|-------|--------|-----|----------|
| `.env.example` | 12 | 363 | `3a475fdc12` | CRLF | UTF-8/Unknown (no BOM) |
| `.pre-commit-config.yaml` | 20 | 472 | `39a6676a98` | CRLF | UTF-8/Unknown (no BOM) |
| `Dockerfile` | 14 | 344 | `73bf3c4404` | CRLF | UTF-8/Unknown (no BOM) |
| `alembic.ini` | 148 | 4985 | `e0e0116da2` | CRLF | UTF-8/Unknown (no BOM) |
| `app\__init__.py` | 0 | 0 | `e3b0c44298` | LF | UTF-8/Unknown (no BOM) |
| `app\archivist.py` | 24 | 681 | `ce43d6b0b9` | CRLF | UTF-8/Unknown (no BOM) |
| `app\cli.py` | 26 | 692 | `82766a449a` | CRLF | UTF-8/Unknown (no BOM) |
| `app\db.py` | 27 | 616 | `3f19dc66a3` | CRLF | UTF-8/Unknown (no BOM) |
| `app\endpoints.py` | 77 | 2377 | `5cff78b774` | CRLF | UTF-8/Unknown (no BOM) |
| `app\logging_config.py` | 30 | 959 | `824e2f476a` | CRLF | UTF-8/Unknown (no BOM) |
| `app\main.py` | 26 | 702 | `3c539085e8` | CRLF | UTF-8/Unknown (no BOM) |
| `app\models.py` | 18 | 515 | `820db431eb` | CRLF | UTF-8/Unknown (no BOM) |
| `app\schemas.py` | 20 | 334 | `69514ff5ba` | CRLF | UTF-8/Unknown (no BOM) |
| `app\security.py` | 93 | 3120 | `481f01fb71` | CRLF | UTF-8/Unknown (no BOM) |
| `docker-compose.yml` | 39 | 1024 | `51aa0eb2fe` | CRLF | UTF-8/Unknown (no BOM) |
| `migrations\env.py` | 60 | 2042 | `9365101da4` | CRLF | UTF-8/Unknown (no BOM) |
| `migrations\versions\bd536313df34_create_audit_log.py` | 47 | 1514 | `8061f85c31` | CRLF | UTF-8/Unknown (no BOM) |
| `pyproject.toml` | 21 | 554 | `fd8b31bd66` | CRLF | UTF-8/Unknown (no BOM) |
| `pytest.ini` | 2 | 24 | `b281451f0a` | CRLF | UTF-8/Unknown (no BOM) |
| `requirements.txt` | 36 | 824 | `beda21544e` | CRLF | UTF-8/Unknown (no BOM) |
| `scripts\make_code_bundle.py` | 222 | 6064 | `0cd106e1dc` | CRLF | UTF-8/Unknown (no BOM) |
| `scripts\make_full_audit.py` | 212 | 5093 | `220c58c66d` | LF | UTF-8/Unknown (no BOM) |
| `scripts\no_bom_check.py` | 11 | 303 | `8f4920fdac` | CRLF | UTF-8/Unknown (no BOM) |
| `scripts\remove_bom.py` | 15 | 346 | `33733ab83f` | CRLF | UTF-8/Unknown (no BOM) |
| `tests\conftest.py` | 49 | 1426 | `f9af561237` | CRLF | UTF-8/Unknown (no BOM) |
| `tests\test_api.py` | 66 | 2473 | `3b0eb5d20a` | CRLF | UTF-8/Unknown (no BOM) |
| `tests\test_archivist.py` | 27 | 792 | `323cab0573` | CRLF | UTF-8/Unknown (no BOM) |
| `tests\test_pagination.py` | 45 | 1700 | `51989b7aff` | CRLF | UTF-8/Unknown (no BOM) |

**Total lines:** 1387

---

## Full File Contents

### `.env.example`

**Lines:** 12  |  **SHA256:** `3a475fdc1272e824ffe12e79b606b57c3d7fdcff89229f2e5ecd4911743a70cc`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# .env.example
# This file is a template for the required environment variables.
# Copy this to a file named .env and fill in the values.

APP_NAME="Aegis Event Bus"
DATA_ROOT="./projects_data"
DB_PATH="eventbus.db"

# For JWT Authentication
SECRET_KEY="a_very_secret_key_that_should_be_long_and_random"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

### `.pre-commit-config.yaml`

**Lines:** 20  |  **SHA256:** `39a6676a981e17bbf8b267352238d7a8d6b435db83a85aea00436a5e72b7ea6f`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
repos:
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.10
    hooks:
      - id: ruff
        args: [--fix]

  - repo: local
    hooks:
      - id: no-bom
        name: Ensure requirements.txt has no UTF-8 BOM
        language: system
        entry: python scripts/no_bom_check.py
        pass_filenames: false
        files: ^requirements\.txt$

```

### `Dockerfile`

**Lines:** 14  |  **SHA256:** `73bf3c44047e0e8e15e2c9b1e878d5c15cccc60c748208bfd2d9e5c950848d2c`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
FROM python:3.11-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# include Alembic bits so the container knows where migrations live
COPY alembic.ini .
COPY migrations ./migrations

COPY ./app ./app

CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000

```

### `alembic.ini`

**Lines:** 148  |  **SHA256:** `e0e0116da23a2b14b3a78fb5a9a83e59806e44d575db18b43dc20f232454786c`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# A generic, single database configuration.

[alembic]
# path to migration scripts.
# this is typically a path given in POSIX (e.g. forward slashes)
# format, relative to the token %(here)s which refers to the location of this
# ini file
script_location = migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.  for multiple paths, the path separator
# is defined by "path_separator" below.
prepend_sys_path = .


# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library and tzdata library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to <script_location>/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "path_separator"
# below.
# version_locations = %(here)s/bar:%(here)s/bat:%(here)s/alembic/versions

# path_separator; This indicates what character is used to split lists of file
# paths, including version_locations and prepend_sys_path within configparser
# files such as alembic.ini.
# The default rendered in new alembic.ini files is "os", which uses os.pathsep
# to provide os-dependent path splitting.
#
# Note that in order to support legacy alembic.ini files, this default does NOT
# take place if path_separator is not present in alembic.ini.  If this
# option is omitted entirely, fallback logic is as follows:
#
# 1. Parsing of the version_locations option falls back to using the legacy
#    "version_path_separator" key, which if absent then falls back to the legacy
#    behavior of splitting on spaces and/or commas.
# 2. Parsing of the prepend_sys_path option falls back to the legacy
#    behavior of splitting on spaces, commas, or colons.
#
# Valid values for path_separator are:
#
# path_separator = :
# path_separator = ;
# path_separator = space
# path_separator = newline
#
# Use os.pathsep. Default configuration used for new projects.
path_separator = os

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = ${DATABASE_URL}



[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the module runner, against the "ruff" module
# hooks = ruff
# ruff.type = module
# ruff.module = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Alternatively, use the exec runner to execute a binary found on your PATH
# hooks = ruff
# ruff.type = exec
# ruff.executable = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Logging configuration.  This is also consumed by the user-maintained
# env.py script only.
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```

### `app\__init__.py`

**Lines:** 0  |  **SHA256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`  |  **EOL:** LF  |  **Encoding:** UTF-8/Unknown (no BOM)

```


```

### `app\archivist.py`

**Lines:** 24  |  **SHA256:** `ce43d6b0b9d2944c3377792963f86a308da4bf6d60315fe02d0a70f02b5000e3`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/archivist.py
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# We still define DATA_ROOT here to be used by the main application
DATA_ROOT = Path(os.getenv("DATA_ROOT", "projects_data"))


def create_job_folders(job_id: str, base_path: Path):
    """
    Creates the standard folder structure for a new job inside a given base_path.
    """
    job_root = base_path / job_id
    subfolders = ["01_raw_data", "02_processed_data", "03_reports"]

    # Ensure the main data root directory exists
    base_path.mkdir(exist_ok=True)

    for sub in subfolders:
        (job_root / sub).mkdir(parents=True, exist_ok=True)

```

### `app\cli.py`

**Lines:** 26  |  **SHA256:** `82766a449ad159d70169e106dd26862934221915eac40504b7847295cf2c0f6e`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/cli.py
import datetime as dt
import os

import typer
from dotenv import load_dotenv
from jose import jwt

load_dotenv()
app = typer.Typer()

SECRET = os.getenv("SECRET_KEY")
ALG = os.getenv("ALGORITHM", "HS256")


@app.command(help="Generate a short-lived admin JWT")
def create_token(username: str, minutes: int = 60):
    """Generates a JWT for the given username, valid for a number of minutes."""
    exp = dt.datetime.utcnow() + dt.timedelta(minutes=minutes)
    token = jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALG)
    typer.echo(f"Generated token for user '{username}':")
    typer.echo(token)


if __name__ == "__main__":
    app()

```

### `app\db.py`

**Lines:** 27  |  **SHA256:** `3f19dc66a3522711358e266c3fd41e444733847f62195e3689dea0eee8f6e44c`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/db.py
import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///eventbus.db")
IS_SQLITE = DB_URL.startswith("sqlite")

engine = create_engine(
    DB_URL,
    echo=False,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
)


def init_db() -> None:
    """Create tables only for SQLite.  In Postgres we rely on Alembic."""
    if IS_SQLITE:
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

```

### `app\endpoints.py`

**Lines:** 77  |  **SHA256:** `5cff78b77486d0f361aaed4f8d2760ed98e3afebcef13b18e44beba634578498`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/endpoints.py
import json
import os
from uuid import uuid4

import paho.mqtt.publish as mqtt_publish
import structlog
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, text

from . import archivist, schemas, security
from .db import get_session
from .models import AuditLog

router = APIRouter()
log = structlog.get_logger(__name__)

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))


@router.get("/healthz", include_in_schema=False)
def health_check(session: Session = Depends(get_session)):
    """A simple health check endpoint that pings the database."""
    session.exec(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/", tags=["Status"])
def read_root():
    return {"status": "Aegis Event Bus is online"}


@router.post("/job", response_model=schemas.Job, tags=["Jobs"])
def create_new_job(
    session: Session = Depends(get_session),
    _: dict = Depends(security.get_current_user),
):
    job_id = f"FC-{uuid4()}"
    archivist.create_job_folders(job_id, archivist.DATA_ROOT)

    with session:
        entry = AuditLog(job_id=job_id, action="job.created")
        session.add(entry)
        session.commit()
        session.refresh(entry)

    payload = {"job_id": job_id, "timestamp": entry.timestamp.isoformat()}
    try:
        mqtt_publish.single(
            topic="aegis/job/created",
            payload=json.dumps(payload),
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            tls={"ca_certs": "./mosquitto/certs/ca.crt"},
        )
    except Exception as exc:
        log.warning("mqtt.publish_failed", job_id=job_id, err=str(exc))

    return {"job_id": job_id}


@router.get("/jobs", response_model=schemas.JobsPage, tags=["Jobs"])
def list_recent_jobs(
    session: Session = Depends(get_session),
    cursor: int | None = Query(None, description="last row id from prev page"),
    limit: int = Query(20, le=100),
    _: dict = Depends(security.get_current_user),
):
    stmt = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if cursor:
        stmt = stmt.where(AuditLog.id < cursor)

    rows = session.exec(stmt).all()

    next_cursor = rows[-1].id if len(rows) == limit else None
    return {"items": rows, "next_cursor": next_cursor}

```

### `app\logging_config.py`

**Lines:** 30  |  **SHA256:** `824e2f476aa240bdf206097a5a6f5dbcfcebbfe9145f55a9a62f61df387c3213`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/logging_config.py
import logging
import sys

import structlog
from structlog.processors import JSONRenderer, TimeStamper


def setup_logging() -> None:
    """One‑shot Structlog configuration for the whole service."""
    timestamper = TimeStamper(fmt="iso", utc=True)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
        processors=[
            structlog.contextvars.merge_contextvars,  # request‑id etc.
            structlog.processors.add_log_level,
            timestamper,
            structlog.processors.dict_tracebacks,  # pretty tracebacks
            JSONRenderer(),  # final JSON out
        ],
    )

    # The std‑lib side; structlog will feed into this.
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # structlog already produced JSON
        stream=sys.stdout,
    )

```

### `app\main.py`

**Lines:** 26  |  **SHA256:** `3c539085e86051e37045834b35dd716f7eb4552c8fae0da1c1921cd3344b2a17`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import db, endpoints, logging_config, security

# ---------- logging & metrics set‑up ----------
logging_config.setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # creates tables when running under pytest (SQLite)
    yield


# ---------------------------------------------

app = FastAPI(title="Aegis Event Bus", lifespan=lifespan)

Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.include_router(endpoints.router)
app.include_router(security.router)

```

### `app\models.py`

**Lines:** 18  |  **SHA256:** `820db431eb9e980aee1ee0ece9287f90f2144c05278f830a3dc6068c0a83d6a5`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/models.py
import datetime as dt
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True)
    action: str
    timestamp: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

```

### `app\schemas.py`

**Lines:** 20  |  **SHA256:** `69514ff5baf77b8cfcc685323e479cfad2886cc0552fe1bf8cd7e4dfbfd778e9`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/schemas.py
from typing import List, Optional

from pydantic import BaseModel

from .models import AuditLog


class Job(BaseModel):
    job_id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class JobsPage(BaseModel):
    items: List[AuditLog]
    next_cursor: Optional[int] = None

```

### `app\security.py`

**Lines:** 93  |  **SHA256:** `481f01fb7121bd57b0fb570c8b34541733fbe3171ccf3a8b49c088f2598a3724`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# app/security.py
import os

# This is the key fix: importing timedelta directly from the datetime module
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import schemas

load_dotenv()
router = APIRouter()

# --- Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "a_default_secret_key_for_testing")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Fake User Database ---
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
    }
}


def get_user(username: str):
    return fake_users_db.get(username)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- The Main Security Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # This now works because timedelta was imported correctly
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

```

### `docker-compose.yml`

**Lines:** 39  |  **SHA256:** `51aa0eb2fec1483bd98fd182660b1c3d5f67bc4eb460de33450845c53e67cc61`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    env_file: .env
    ports: [ "${DB_PORT:-5432}:5432" ]
    volumes: [ pgdata:/var/lib/postgresql/data ]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # THIS IS THE MISSING SERVICE
  mosquitto:
    image: eclipse-mosquitto:2
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "8883:8883"
    volumes:
      - ./mosquitto/conf:/mosquitto/config
      - ./mosquitto/certs:/mosquitto/certs
      - mosquitto_data:/mosquitto/data

  eventbus:
    build: .
    restart: unless-stopped
    env_file: .env
    ports: [ "8000:8000" ]
    volumes: [ ./projects_data:/code/projects_data ]
    depends_on:
      postgres:  { condition: service_healthy }
      mosquitto: { condition: service_started }

volumes:
  pgdata:
  mosquitto_data: # Add this volume for mosquitto

```

### `migrations\env.py`

**Lines:** 60  |  **SHA256:** `9365101da41026d4b27e96c05872f083791588012ad6dc5cba707a7852ef6a4c`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
"""
Alembic migration environment.
Keeps DATABASE_URL in sync with .env and exposes SQLModel metadata.
"""

import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

load_dotenv()  # .env → env vars
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL not set")

# ——— Alembic config ————————————————————————————————————————————
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name:
    fileConfig(config.config_file_name)

# ——— Import models so Alembic can autogenerate ————————————
from sqlmodel import SQLModel  # noqa: E402

target_metadata = SQLModel.metadata
# ——————————————————————————————————————————————————————————————


def run_migrations_offline() -> None:
    """Run migrations without a DB connection (generates SQL)."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```

### `migrations\versions\bd536313df34_create_audit_log.py`

**Lines:** 47  |  **SHA256:** `8061f85c3104e9e949726c361e796d27c636699a0dbbe63808317de2c6478543`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
"""create audit_log

Revision ID: bd536313df34
Revises:
Create Date: 2025-07-13 22:18:24.110812

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "bd536313df34"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_auditlog_job_id"), table_name="auditlog")
    op.drop_table("auditlog")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auditlog",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("job_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("action", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "timestamp",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("auditlog_pkey")),
    )
    op.create_index(op.f("ix_auditlog_job_id"), "auditlog", ["job_id"], unique=False)
    # ### end Alembic commands ###

```

### `pyproject.toml`

**Lines:** 21  |  **SHA256:** `fd8b31bd663299433e7999be7af4cb1ca6e6c0450db6e7e5b81c211571ea0f16`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# pyproject.toml

[tool.black]
line-length = 88
target-version = ["py311"]
# Optional (locks version so CI & local stay identical):
# required-version = "25.1.0"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

# (Optional) add ignores or per-file-ignores here later.

[tool.ruff.format]
# Only put *formatting* options here if you customize them.
# For now we leave it empty so Ruff uses defaults
# (indent-style, quote-style, etc. not needed unless you want custom behavior).

```

### `pytest.ini`

**Lines:** 2  |  **SHA256:** `b281451f0af7c3d8bd4f6fa8aa4abdf5e55f0070fdf07244be910b4b9278e6d4`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
[pytest]
pythonpath = .

```

### `requirements.txt`

**Lines:** 36  |  **SHA256:** `beda21544e02495c5ac111fe6b58c77956c2bd5e9089ce765abc8787e3425429`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# =========================
# Aegis Event Bus – Requirements
# =========================
# Strategy:
# - Pin to compatible minor ranges using ~= so you get bug fixes but not breaking major jumps.
# - Testing & dev tools live here for simplicity (can later split into prod/dev files).

# --- Core Framework ---
fastapi~=0.111.0
uvicorn[standard]~=0.30.0
python-dotenv~=1.0.0
structlog~=24.1.0
typer~=0.12.0

# --- Database & ORM ---
sqlmodel~=0.0.22
alembic~=1.13.0
asyncpg~=0.29.0
psycopg2-binary~=2.9.0

# --- Security & Auth ---
bcrypt>=4.1.2,<5
passlib[bcrypt]~=1.7.4
python-jose[cryptography]~=3.3.0
python-multipart~=0.0.9

# --- Event Messaging ---
paho-mqtt~=2.1.0

# --- Observability ---
prometheus-fastapi-instrumentator~=7.0.0

# --- Testing ---
pytest~=8.4.0
httpx~=0.27.0


```

### `scripts\make_code_bundle.py`

**Lines:** 222  |  **SHA256:** `0cd106e1dc82525f9e2436350660dbb228c534687b70fa415bbb4365dc02df50`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
#!/usr/bin/env python
"""
Generate a single markdown bundle (code_bundle.md) containing:
- Metadata (timestamp UTC, git commit if available)
- File manifest (name, size, lines, sha256)
- Global integrity hash (sha256 of all per-file hashes concatenated in
  sorted order)
- Full contents of each file in fenced code blocks (language guessed
  by extension)

Intended for: offline audit sharing, reproducibility, integrity
verification.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import pathlib
import subprocess
import sys
from typing import Iterable, List, Tuple

# ---- Configuration ---------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALLOW_EXT = {
    ".py",
    ".yml",
    ".yaml",
    ".md",
    ".toml",
    ".ini",
    ".txt",
    ".conf",
    ".sh",
    ".sql",
    ".env",  # only template / sanitized; actual .env skipped below
}

ALLOW_NAMED = {
    "Dockerfile",
    ".gitignore",
    ".env.example",
    "Makefile",
}

EXCLUDE_DIRS = {
    ".git",
    ".ruff_cache",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "projects_data",
    "mosquitto/certs",  # exclude certs / binary secrets
    "pgdata",
}

EXCLUDE_FILES = {
    "eventbus.db",
    "test.db",
    "tls.crt",
    "tls.key",
    "audit_report.md",
    "code_bundle.md",
}

OUTPUT_FILE = ROOT / "code_bundle.md"


# ---- Helpers ---------------------------------------------------------------


def is_allowed(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDE_FILES:
        return False
    for d in EXCLUDE_DIRS:
        if rel == d or rel.startswith(d + "/"):
            return False
    if path.name in ALLOW_NAMED:
        return True
    if path.suffix.lower() in ALLOW_EXT:
        # Skip *real* .env to avoid leaking secrets (allow only example)
        if path.name == ".env":
            return False
        return True
    return False


def iter_files() -> Iterable[pathlib.Path]:
    for p in ROOT.rglob("*"):
        if p.is_file() and is_allowed(p):
            yield p


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def detect_language(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    return {
        ".py": "python",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
        ".md": "markdown",
        ".txt": "text",
        ".conf": "conf",
        ".sh": "bash",
        ".sql": "sql",
        ".env": "bash",
        "": "",
    }.get(ext, "")


def get_git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except Exception:
        return "N/A"


def read_text_preserve(path: pathlib.Path) -> str:
    """
    Read file as UTF-8; fall back to latin-1 if necessary (rare).
    Avoid altering raw content (no newline normalization here).
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


# ---- Main ------------------------------------------------------------------


def main() -> None:
    files: List[pathlib.Path] = sorted(
        iter_files(),
        key=lambda p: p.as_posix(),
    )
    if not files:
        print(
            "No files matched configuration. Adjust ALLOW lists.",
            file=sys.stderr,
        )
        sys.exit(1)

    manifest_rows: List[Tuple[str, int, int, str]] = []
    lines_out: List[str] = []

    utc_now = dt.datetime.utcnow().replace(microsecond=0)
    git_commit = get_git_commit()

    lines_out.append("# Consolidated Code Bundle\n")
    lines_out.append(f"Generated (UTC): {utc_now.isoformat()}  \n")
    lines_out.append(f"Git commit: `{git_commit}`\n")
    lines_out.append(f"Total files: {len(files)}\n\n")

    for f in files:
        data = f.read_bytes()
        text = read_text_preserve(f)
        line_count = text.count("\n") + (
            0 if text.endswith("\n") else (1 if text else 0)
        )
        file_hash = sha256_bytes(data)
        manifest_rows.append((f.as_posix(), len(data), line_count, file_hash))

    concat_hash_source = "".join(row[3] for row in manifest_rows).encode()
    global_hash = sha256_bytes(concat_hash_source)

    lines_out.append("## Integrity\n")
    lines_out.append(f"- Global concatenated file-hash SHA256: **{global_hash}**\n")
    lines_out.append(
        "  (Computed by concatenating each file's SHA256 (sorted by path) "
        "and hashing that string.)\n\n"
    )

    lines_out.append("## Manifest\n\n")
    lines_out.append("| File | Bytes | Lines | SHA256 |\n")
    lines_out.append("|------|-------|-------|--------|\n")
    for path_str, size_b, lc, h in manifest_rows:
        lines_out.append(f"| `{path_str}` | {size_b} | {lc} | `{h}` |\n")
    lines_out.append("\n---\n\n")

    for f, size_b, lc, h in manifest_rows:
        lang = detect_language(pathlib.Path(f))
        lines_out.append(f"### `{f}`\n\n")
        lines_out.append(f"- Size: {size_b} bytes  \n")
        lines_out.append(f"- Lines: {lc}  \n")
        lines_out.append(f"- SHA256: `{h}`\n\n")
        lines_out.append(f"```{lang}\n")
        file_text = read_text_preserve(ROOT / f)
        lines_out.append(file_text)
        if not file_text.endswith("\n"):
            lines_out.append("\n")
        lines_out.append("```\n\n")

    OUTPUT_FILE.write_text(
        "".join(lines_out),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Global integrity hash: {global_hash}")


if __name__ == "__main__":
    main()

```

### `scripts\make_full_audit.py`

**Lines:** 212  |  **SHA256:** `220c58c66d32d8ce707591360d23e4002f20c85970a6695257d6b976479327ec`  |  **EOL:** LF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
#!/usr/bin/env python
"""
make_full_audit.py

Generate audit_report.md containing:
  - Timestamp & current git commit (if repo)
  - Python version
  - Tree listing (filtered)
  - Per-file SHA256 + line counts
  - Full contents of source / infra / test files
  - Summary tables

Works on Windows & *nix (no external deps).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import subprocess
import sys
from pathlib import Path

EXPLICIT_FILES = {
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",
    "alembic.ini",
    "requirements.txt",
    "pyproject.toml",
    "pytest.ini",
    ".pre-commit-config.yaml",
    ".github/workflows/ci.yml",
    "audit_report.md",
}

INCLUDE_DIRS = {
    "app",
    "tests",
    "migrations",
    "scripts",
    "mosquitto/conf",
    "mosquitto/certs",
}

EXTENSIONS = {
    ".py",
    ".yml",
    ".yaml",
    ".ini",
    ".md",
    ".txt",
    ".conf",
    ".crt",
    ".key",
    ".csr",
    ".srl",
}

OUTPUT_FILE = Path("audit_report.md")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def want_file(p: Path) -> bool:
    if p.name == OUTPUT_FILE.name:
        return False
    if p.is_dir():
        return False
    rp = rel(p)
    if rp in EXPLICIT_FILES:
        return True
    if any(rp.startswith(d + os.sep) or rp == d for d in INCLUDE_DIRS):
        if p.suffix.lower() in EXTENSIONS or p.name in EXPLICIT_FILES:
            return True
    return False


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "N/A"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_read_bytes(p: Path) -> bytes:
    try:
        return p.read_bytes()
    except Exception as e:
        return f"<<ERROR READING FILE: {e}>>".encode()


def detect_eol(data: bytes) -> str:
    if b"\r\n" in data:
        return "CRLF"
    return "LF"


def classify_encoding(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        return "UTF-8-BOM"
    return "UTF-8/Unknown (no BOM)"


def main() -> None:
    now = dt.datetime.utcnow().replace(microsecond=0)
    commit = get_git_commit()
    root = Path.cwd()

    files = sorted(
        [p for p in root.rglob("*") if want_file(p)],
        key=lambda x: rel(x),
    )

    meta_rows = []
    total_lines = 0
    for f in files:
        raw = safe_read_bytes(f)
        try:
            text_preview = raw.decode("utf-8", errors="replace")
        except Exception:
            text_preview = ""
        line_count = text_preview.count("\n") + (
            1 if text_preview and not text_preview.endswith("\n") else 0
        )
        total_lines += line_count
        meta_rows.append(
            {
                "path": rel(f),
                "lines": line_count,
                "sha256": sha256_bytes(raw),
                "eol": detect_eol(raw),
                "enc": classify_encoding(raw),
                "size": len(raw),
            }
        )

    out = []
    out.append("# Aegis Event Bus – Full Code Audit\n")
    out.append(f"Generated (UTC): {now.isoformat()}\n")
    out.append(f"Git commit: `{commit}`\n")
    out.append(f"Python: {sys.version.split()[0]}\n")
    out.append("---\n")

    out.append("## Repository Tree (selected)\n")
    for f in files:
        out.append(f"- `{rel(f)}`")
    out.append("")

    out.append("## File Summary\n")
    header = "| File | Lines | Bytes | SHA256 | EOL | Encoding |"
    sep = "|------|-------|-------|--------|-----|----------|"
    out.append(header)
    out.append(sep)
    for r in meta_rows:
        short_hash = r["sha256"][:10]
        out.append(
            "| `{path}` | {lines} | {size} | `{hash}` | {eol} | {enc} |".format(
                path=r["path"],
                lines=r["lines"],
                size=r["size"],
                hash=short_hash,
                eol=r["eol"],
                enc=r["enc"],
            )
        )
    out.append(f"\n**Total lines:** {total_lines}\n")
    out.append("---\n")

    # Full contents
    out.append("## Full File Contents\n")
    for r in meta_rows:
        p = Path(r["path"])
        raw = safe_read_bytes(p)
        try:
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = "<<BINARY OR UNREADABLE>>"

        out.append(f"### `{r['path']}`\n")
        out.append(
            "**Lines:** {lines}  |  **SHA256:** `{sha}`  |  **EOL:** {eol}  |  "
            "**Encoding:** {enc}\n".format(
                lines=r["lines"],
                sha=r["sha256"],
                eol=r["eol"],
                enc=r["enc"],
            )
        )

        out.append("```")
        out.append(text)
        if not text.endswith("\n"):
            out.append("")
        out.append("```\n")

    OUTPUT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

```

### `scripts\no_bom_check.py`

**Lines:** 11  |  **SHA256:** `8f4920fdac4962dc114c890ffb3b3217d5b738ab20a79a14e3a0ef5523d8f732`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# scripts/no_bom_check.py
from pathlib import Path

p = Path("requirements.txt")
data = p.read_bytes()

if data.startswith(b"\xef\xbb\xbf"):
    print("BOM found in requirements.txt (remove it: Save As UTF-8 w/out BOM).")
    raise SystemExit(1)

print("No BOM present in requirements.txt.")

```

### `scripts\remove_bom.py`

**Lines:** 15  |  **SHA256:** `33733ab83f33d93df6a26ad08d561798ae79485df7876b669051f080fa583f79`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
from pathlib import Path


def strip_bom(path: str = "requirements.txt") -> None:
    p = Path(path)
    raw = p.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        p.write_bytes(raw[3:])
        print(f"{path}: BOM removed.")
    else:
        print(f"{path}: no BOM found.")


if __name__ == "__main__":
    strip_bom()

```

### `tests\conftest.py`

**Lines:** 49  |  **SHA256:** `f9af561237abf15e3b89403b06c29ede1eba379b9f39f63705d593e43d92912d`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
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

```

### `tests\test_api.py`

**Lines:** 66  |  **SHA256:** `3b0eb5d20a3420a84bbb98b6c5d507e5a450355f4f10103e1b92e5c4e1c90f3e`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# tests/test_api.py
"""
API integration tests (synchronous) for the Event Bus service.

Key policy:
-----------
All external side‑effects (MQTT publish) are mocked so the test
suite never opens network connections on CI (important for
GitHub Actions ToS compliance and speed).

We rely on fixtures from tests/conftest.py:
- client  : FastAPI TestClient
- session : SQLModel Session bound to the test DB
"""

import paho.mqtt.publish as mqtt_publish
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import AuditLog


# ────────────────────────── GLOBAL MQTT MOCK ──────────────────────────
@pytest.fixture(autouse=True)
def _mock_mqtt(monkeypatch):
    """
    Auto‑applied fixture that replaces paho.mqtt.publish.single with a no‑op.

    This guarantees **zero network traffic** for every test, even if a
    future test forgets to monkeypatch explicitly.
    """
    monkeypatch.setattr(mqtt_publish, "single", lambda *a, **k: None)


# ───────────────────────────── TESTS ──────────────────────────────────
def test_read_root_endpoint(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "Aegis Event Bus is online"}


def test_unauthenticated_routes(client: TestClient):
    # POST /job without token
    assert client.post("/job").status_code == 401
    # GET /jobs without token
    assert client.get("/jobs").status_code == 401


def test_auth_and_workflow(client: TestClient, session: Session):
    # 1. Obtain JWT
    token = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a job (MQTT publish is silently mocked)
    job_id = client.post("/job", headers=headers).json()["job_id"]

    # 3. Verify DB row
    db_row = session.exec(select(AuditLog).where(AuditLog.job_id == job_id)).one()
    assert db_row.action == "job.created"

    # 4. List jobs & confirm first returned matches
    jobs_page = client.get("/jobs", headers=headers).json()
    assert jobs_page["items"][0]["job_id"] == job_id

```

### `tests\test_archivist.py`

**Lines:** 27  |  **SHA256:** `323cab0573e829bbdf205363fd6b2138f84c27be85c36085300e10999b6b974d`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# tests/test_archivist.py

import shutil
from pathlib import Path

from app.archivist import create_job_folders

# Define a temporary folder name for our tests to use
TEST_DATA_ROOT = Path("test_projects_data_temp")


def test_folder_creation():
    """
    Tests if the create_job_folders function correctly creates the
    required directory structure.
    """
    job_id = "TEST-JOB-123"

    # --- Run the function we are testing, providing the base_path ---
    create_job_folders(job_id=job_id, base_path=TEST_DATA_ROOT)

    # --- Assert that the folders now exist ---
    assert (TEST_DATA_ROOT / job_id).is_dir()
    assert (TEST_DATA_ROOT / job_id / "01_raw_data").is_dir()

    # --- Clean up after the test is done ---
    shutil.rmtree(TEST_DATA_ROOT)

```

### `tests\test_pagination.py`

**Lines:** 45  |  **SHA256:** `51989b7aff92d167a2324aa784df6b8fefe77bace529a8612e733c42d3940ae5`  |  **EOL:** CRLF  |  **Encoding:** UTF-8/Unknown (no BOM)

```
# tests/test_pagination.py
import paho.mqtt.publish as mqtt_publish
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.models import AuditLog


def _login_and_get_headers(client: TestClient):
    """Helper function to log in and get auth headers."""
    data = {"username": "testuser", "password": "testpassword"}
    token = client.post("/token", data=data).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_jobs_pagination(client: TestClient, session: Session, monkeypatch):
    """Tests that the /jobs endpoint correctly paginates results."""
    headers = _login_and_get_headers(client)
    monkeypatch.setattr(mqtt_publish, "single", lambda *a, **k: None)

    # Clean the DB and create 3 new jobs
    session.exec(delete(AuditLog))
    session.commit()
    for _ in range(3):
        client.post("/job", headers=headers)

    # --- Test First Page ---
    page1_response = client.get("/jobs?limit=2", headers=headers)
    assert page1_response.status_code == 200
    page1 = page1_response.json()

    assert len(page1["items"]) == 2
    assert page1["next_cursor"] is not None
    assert page1["items"][0]["id"] == 3  # Should be the newest job
    assert page1["items"][1]["id"] == 2

    # --- Test Second Page ---
    cursor = page1["next_cursor"]
    page2_response = client.get(f"/jobs?limit=2&cursor={cursor}", headers=headers)
    assert page2_response.status_code == 200
    page2 = page2_response.json()

    assert len(page2["items"]) == 1  # Only one job left
    assert page2["next_cursor"] is None  # Should be the last page
    assert page2["items"][0]["id"] == 1

```
