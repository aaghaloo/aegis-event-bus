# Aegis Event Bus – Full Audit Bundle

Generated: 2025-07-19 21:00:32 UTC

## Included File Count

36 files

## File Tree (filtered)

```
.github/dependabot.yml
.github/workflows/ci.yml
.github/workflows/codeql.yml
.github/workflows/pyproject.toml
.gitignore
.pre-commit-config.yaml
alembic.ini
app/__init__.py
app/archivist.py
app/cli.py
app/db.py
app/endpoints.py
app/logging_config.py
app/main.py
app/models.py
app/schemas.py
app/security.py
audit_report.md
docker-compose.yml
Dockerfile
LICENSE
migrations/env.py
migrations/README
migrations/script.py.mako
migrations/versions/bd536313df34_create_audit_log.py
mosquitto/conf/mosquitto.conf
pyproject.toml
pytest.ini
README.md
scripts/gen-mqtt-cert.sh
scripts/make_audit_bundle.sh
scripts/make_full_audit.py
tests/conftest.py
tests/test_api.py
tests/test_archivist.py
tests/test_pagination.py
```

## File Contents

### .github/dependabot.yml

**SHA256:** `b2756be1660e8225dbe222f467ca22998821b45a7a864787bf5a0f931a21cbb3`  

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"          # location of requirements.txt
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels: ["dependencies"]

```

### .github/workflows/ci.yml

**SHA256:** `43e5c416ef41c81b2e9d4ac206ec965db3a0cddf9caa12da370cda656260a0f8`  

```yaml
# .github/workflows/ci.yml
name: Aegis CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

# This is the new security hardening section
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U test_user -d test_db"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Pytest
        env:
          DATABASE_URL: "postgresql+psycopg2://test_user:test_password@localhost:5432/test_db"
        run: pytest -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Ruff & Black Checks
        run: |
          ruff check .
          black --check .
```

### .github/workflows/codeql.yml

**SHA256:** `6df1f00b308263d27c6ba4843f25c29b2bcd0a753871f4c5c30275de79f1b694`  

```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: '30 20 * * 1' # Run every Monday at 20:30 UTC

# --- THIS IS THE FIX ---
# This block gives the workflow permission to write security events
permissions:
  contents: read
  actions: read
  security-events: write
# -----------------------

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        language: ['python']

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    # Initializes the CodeQL tools for scanning.
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

### .github/workflows/pyproject.toml

**SHA256:** `f32168f0048315685b6078fafc80751e61f83566dfe52fb853209140b17eda4d`  

```toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88

# Ruff ≥ 0.4 expects lint‑specific options in a nested table
[tool.ruff.lint]
select = ["E", "F", "W", "I"]

```

### .gitignore

**SHA256:** `5a3e5d64aa0aef90352807ca747d4e4b7e5690f2aed31e8cc7e8859430832d35`  

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor  
#  Cursor is an AI-powered code editor.`.cursorignore` specifies files/directories to 
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore
eventbus.db
.env
tls.key
tls.crt
```

### .pre-commit-config.yaml

**SHA256:** `abdc4dd045e762c63a637ad4c04065f89bb0e37f69456597f32a83cc0eb91192`  

```yaml
# .pre-commit-config.yaml
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
      - id: ruff-format
```

### alembic.ini

**SHA256:** `e0e0116da23a2b14b3a78fb5a9a83e59806e44d575db18b43dc20f232454786c`  

```ini
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

### app/__init__.py

**SHA256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`  

```python

```

### app/archivist.py

**SHA256:** `ce43d6b0b9d2944c3377792963f86a308da4bf6d60315fe02d0a70f02b5000e3`  

```python
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

### app/cli.py

**SHA256:** `82766a449ad159d70169e106dd26862934221915eac40504b7847295cf2c0f6e`  

```python
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

### app/db.py

**SHA256:** `3f19dc66a3522711358e266c3fd41e444733847f62195e3689dea0eee8f6e44c`  

```python
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

### app/endpoints.py

**SHA256:** `5cff78b77486d0f361aaed4f8d2760ed98e3afebcef13b18e44beba634578498`  

```python
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

### app/logging_config.py

**SHA256:** `824e2f476aa240bdf206097a5a6f5dbcfcebbfe9145f55a9a62f61df387c3213`  

```python
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

### app/main.py

**SHA256:** `3c539085e86051e37045834b35dd716f7eb4552c8fae0da1c1921cd3344b2a17`  

```python
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

### app/models.py

**SHA256:** `820db431eb9e980aee1ee0ece9287f90f2144c05278f830a3dc6068c0a83d6a5`  

```python
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

### app/schemas.py

**SHA256:** `69514ff5baf77b8cfcc685323e479cfad2886cc0552fe1bf8cd7e4dfbfd778e9`  

```python
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

### app/security.py

**SHA256:** `481f01fb7121bd57b0fb570c8b34541733fbe3171ccf3a8b49c088f2598a3724`  

```python
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

### audit_report.md

**SHA256:** `93a4a9e78f362086f5303417155249ddefdde5c925b66d79e7ad59b8be3168d4`  

```markdown
# Aegis Event Bus Audit Bundle
Generated (UTC): Sat, Jul 19, 2025  8:36:23 PM

## Repo Tree (depth 4)

```
./.env
./.env.example
./.pre-commit-config.yaml
./.ruff_cache/0.12.3/12840763260191213445
./.ruff_cache/0.12.3/17677613968562772935
./.ruff_cache/0.12.3/2030677839569562225
./.ruff_cache/0.12.3/9900139933838107014
./.ruff_cache/0.4.10/17657817453628622975
./.ruff_cache/0.4.10/5333065534671793707
./.ruff_cache/0.4.10/5587334473803244617
./.ruff_cache/0.4.10/666783530088315385
./.ruff_cache/CACHEDIR.TAG
./alembic.ini
./app/archivist.py
./app/cli.py
./app/db.py
./app/endpoints.py
./app/logging_config.py
./app/main.py
./app/models.py
./app/schemas.py
./app/security.py
./app/__init__.py
./audit_report.md
./docker-compose.yml
./Dockerfile
./eventbus.db
./LICENSE
./migrations/env.py
./migrations/README
./migrations/script.py.mako
./migrations/versions/bd536313df34_create_audit_log.py
./mosquitto/certs/ca.crt
./mosquitto/certs/ca.key
./mosquitto/certs/ca.srl
./mosquitto/certs/server.crt
./mosquitto/certs/server.csr
./mosquitto/certs/server.key
./mosquitto/conf/mosquitto.conf
./pyproject.toml
./pytest.ini
./README.md
./requirements.txt
./scripts/gen-mqtt-cert.sh
./scripts/make_audit_bundle.sh
./test.db
./tests/conftest.py
./tests/test_api.py
./tests/test_archivist.py
./tests/test_pagination.py
./tls.crt
./tls.key
```

## LOC Summary

```
Install cloc for richer stats (pip install cloc)
```

## Source & Infra Files


### .env.example

```
# .env.example
# This file is a template for the required environment variables.
# Copy this to a file named .env and fill in the values.

APP_NAME="Aegis Event Bus"
DATA_ROOT="./projects_data"
DB_PATH="eventbus.db"

# For JWT Authentication
SECRET_KEY=***REDACTED***
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30```

### .pre-commit-config.yaml

```
# .pre-commit-config.yaml
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
      - id: ruff-format```

### Dockerfile

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

### alembic.ini

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

### docker-compose.yml

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
  mosquitto_data: # Add this volume for mosquitto```

### pyproject.toml

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

### requirements.txt

```
ÿþ#   r e q u i r e m e n t s . t x t 
 
 
 
 #   - - -   C o r e   A p p l i c a t i o n   F r a m e w o r k   - - - 
 
 f a s t a p i 
 
 u v i c o r n [ s t a n d a r d ] 
 
 p y t h o n - d o t e n v 
 
 s t r u c t l o g 
 
 t y p e r > = 0 . 1 6                     #   n o    [ a l l ]    s u f f i x   r e q u i r e d 
 
 
 
 
 
 #   - - -   D a t a b a s e   &   O R M   - - - 
 
 s q l m o d e l 
 
 a l e m b i c 
 
 a s y n c p g 
 
 p s y c o p g 2 - b i n a r y 
 
 
 
 #   - - -   S e c u r i t y   &   A u t h e n t i c a t i o n   - - - 
 
 b c r y p t > = 4 . 1 . 2 , < 5 
 
 p a s s l i b [ b c r y p t ] > = 1 . 7 . 4 
 
 p y t h o n - j o s e [ c r y p t o g r a p h y ] 
 
 p y t h o n - m u l t i p a r t 
 
 
 
 #   - - -   E v e n t   M e s s a g i n g   - - - 
 
 p a h o - m q t t 
 
 
 
 #   - - -   O b s e r v a b i l i t y   - - - 
 
 p r o m e t h e u s - f a s t a p i - i n s t r u m e n t a t o r   
 
 
 
 #   - - -   T e s t i n g   - - - - 
 
 p y t e s t 
 
 h t t p x ```

## Migration Versions


### migrations/versions/bd536313df34_create_audit_log.py

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

```

### docker-compose.yml

**SHA256:** `51aa0eb2fec1483bd98fd182660b1c3d5f67bc4eb460de33450845c53e67cc61`  

```yaml
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

### Dockerfile

**SHA256:** `73bf3c44047e0e8e15e2c9b1e878d5c15cccc60c748208bfd2d9e5c950848d2c`  

```dockerfile
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

### LICENSE

**SHA256:** `14913bba016c200bfd062404af5fbe1072654024ed76f00b6f87939a405b0c3b`  

```
MIT License

Copyright (c) 2025 al sterling

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

### migrations/env.py

**SHA256:** `9365101da41026d4b27e96c05872f083791588012ad6dc5cba707a7852ef6a4c`  

```python
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

### migrations/README

**SHA256:** `31595cf53626af9ed16e15c44fa43183209cc163fbc3ebcb904b22ac436a8884`  

```
Generic single-database configuration.
```

### migrations/script.py.mako

**SHA256:** `a60ec52443699fdc2aec93254f06dfdcdfb7f9a5fc7432b7a7e12b9c253713db`  

```jinja
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}

```

### migrations/versions/bd536313df34_create_audit_log.py

**SHA256:** `8061f85c3104e9e949726c361e796d27c636699a0dbbe63808317de2c6478543`  

```python
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

### mosquitto/conf/mosquitto.conf

**SHA256:** `c2485eccd3f8290918656b04f4c922b1134bd49b597b5612f3fd2caf802d6c5c`  

```ini
# mosquitto/conf/mosquitto.conf
persistence true
persistence_location /mosquitto/data/
log_dest stdout

listener 1883

# TLS listener
listener 8883
cafile /mosquitto/certs/ca.crt
certfile /mosquitto/certs/server.crt
keyfile /mosquitto/certs/server.key
require_certificate false
```

### pyproject.toml

**SHA256:** `fd8b31bd663299433e7999be7af4cb1ca6e6c0450db6e7e5b81c211571ea0f16`  

```toml
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

### pytest.ini

**SHA256:** `b281451f0af7c3d8bd4f6fa8aa4abdf5e55f0070fdf07244be910b4b9278e6d4`  

```ini
[pytest]
pythonpath = .
```

### README.md

**SHA256:** `ce390138a9c601aea5ea3acc5bd9769a87573d87658f7beaf106af706c2fd168`  

```markdown
# Aegis Event-Bus (Agent A0) · v0.1

This is the secure, auditable, and scalable backbone for the Aegis Multi-Agent AI ecosystem. It is designed to handle job requests, manage data, and emit events for other agents to consume.

---
## Features

- **FastAPI Service:** Provides a modern, asynchronous API for job management.
- **JWT Authentication:** Endpoints are secured, requiring a valid token for access.
- **SQLite Backend:** Simple, file-based, and reliable data persistence.
- **Automated Folder Creation:** Creates a standardized directory structure for each new job.
- **MQTT Event Publishing:** Broadcasts a `job.created` event for other agents.
- **Containerized:** Runs entirely within Docker via a simple `docker-compose` command.
- **Automated Testing:** Includes a full suite of unit tests with `pytest` and automated CI via GitHub Actions.

---

## Prerequisites

| Tool           | Notes                          |
| -------------- | ------------------------------ |
| Python         | 3.11+                          |
| Docker         | Latest version                 |
| Docker Compose | Latest version (usually incl. with Docker) |

---

## 🚀 Quick Start (Using Docker Compose)

This is the recommended way to run the application.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/aegis-event-bus.git](https://github.com/your-username/aegis-event-bus.git)
    cd aegis-event-bus
    ```

2.  **Configure Environment:**
    Copy the example environment file. No changes are needed for default local startup.
    ```bash
    cp .env.example .env
    ```

3.  **Run the Application Stack:**
    This single command will build and start the FastAPI service and the MQTT broker.
    ```bash
    docker compose up --build
    ```

---

## Accessing the Services

- **API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **MQTT Broker:** `localhost:1883`

---

## 🧪 Running Tests

1.  Create and activate a Python virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  Install dependencies.
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the test suite.
    ```bash
    pytest -v
    ```
    ---
## Advanced Usage

### Pagination

The `GET /jobs` endpoint supports cursor-based pagination.

`GET /jobs?limit=20&cursor=<last_id>`

This will return a JSON object with `items` and a `next_cursor`. To fetch the next page, make the same request again, passing the received `next_cursor` value in the `cursor` query parameter.

### Generate an Admin JWT

You can generate a long-lived token for administrative or testing purposes using the built-in CLI.

```bash
python -m app.cli create-token admin --minutes 1440
```

### scripts/gen-mqtt-cert.sh

**SHA256:** `b0e6c78c6f706a5b683f5373558f3081d258cbefe43c6fe51f291246db22c48d`  

```bash
#!/usr/bin/env bash
set -e
mkdir -p mosquitto/certs
mkdir -p mosquitto/conf

# Root CA
# The //CN=... is the fix for Git Bash on Windows
openssl req -x509 -nodes -days 3650 \
  -newkey rsa:2048 \
  -keyout mosquitto/certs/ca.key \
  -out  mosquitto/certs/ca.crt \
  -subj "//CN=AegisDevCA"

# Server cert
# The //CN=... is the fix for Git Bash on Windows
openssl req -nodes -newkey rsa:2048 \
  -keyout mosquitto/certs/server.key \
  -out  mosquitto/certs/server.csr \
  -subj "//CN=mosquitto"

openssl x509 -req -days 3650 \
  -in  mosquitto/certs/server.csr \
  -CA  mosquitto/certs/ca.crt \
  -CAkey mosquitto/certs/ca.key -CAcreateserial \
  -out mosquitto/certs/server.crt

echo "TLS certs generated in mosquitto/certs/"
```

### scripts/make_audit_bundle.sh

**SHA256:** `1a75b4a9f41e718c2ec35330280a6d9659f44ee4a0b6e10217b67a11d40688b5`  

```bash
#!/usr/bin/env bash
set -e
OUT=audit_report.md

echo "# Aegis Event Bus Audit Bundle" > "$OUT"
echo "Generated (UTC): $(date -u)" >> "$OUT"

echo -e "\n## Repo Tree (depth 4)\n" >> "$OUT"
echo '```' >> "$OUT"
# If 'tree' exists use it; else fallback to find
if command -v tree >/dev/null 2>&1; then
  tree -L 4 -I '.git|.pytest_cache|__pycache__|projects_data|pgdata|.venv|*.pyc' >> "$OUT"
else
  find . -maxdepth 4 -type f | grep -v -E '\.git|__pycache__|\.pytest_cache|projects_data|pgdata|\.venv' >> "$OUT"
fi
echo '```' >> "$OUT"

echo -e "\n## LOC Summary\n" >> "$OUT"
echo '```' >> "$OUT"
if command -v cloc >/dev/null 2>&1; then
  cloc . --exclude-dir=.git,projects_data,pgdata,.pytest_cache,__pycache__,.venv >> "$OUT"
else
  echo "Install cloc for richer stats (pip install cloc)" >> "$OUT"
fi
echo '```' >> "$OUT"

echo -e "\n## Source & Infra Files\n" >> "$OUT"

FILES=$(git ls-files | grep -E '^(app/|tests/|migrations/|Dockerfile|docker-compose.yml|alembic.ini|requirements.txt|pyproject.toml|\.github/workflows/|\.pre-commit-config.yaml|\.env.example)$' || true)

for f in $FILES; do
  echo -e "\n### $f\n" >> "$OUT"
  echo '```' >> "$OUT"
  # Redact secrets if any
  sed -E 's/(SECRET_KEY=).*/\1***REDACTED***/' "$f" >> "$OUT"
  echo '```' >> "$OUT"
done

echo -e "\n## Migration Versions\n" >> "$OUT"
for f in migrations/versions/*.py; do
  [ -f "$f" ] || continue
  echo -e "\n### $f\n" >> "$OUT"
  echo '```' >> "$OUT"
  cat "$f" >> "$OUT"
  echo '```' >> "$OUT"
done

echo "✅ Wrote $OUT"

```

### scripts/make_full_audit.py

**SHA256:** `e159d664f9c3603637df6a235ab2805324068f59200794c96a0e4c95b5210f91`  

```python
#!/usr/bin/env python
"""
Generate a comprehensive audit bundle (Markdown) of all source & infra files.

Output: audit_full.md

Features:
- Lists repo tree (filtered) with depth
- Embeds each selected text file in fenced code blocks
- Skips binaries / large files / secrets (configurable)
- Adds SHA256 hash for integrity
- Pure stdlib (no extra dependencies)

Usage:
    python scripts/make_full_audit.py
"""

from __future__ import annotations
import os, sys, hashlib, datetime, pathlib, textwrap

# ------------ CONFIG  -------------------------------------------------

# Root (repo) = directory containing this script's parent (..)
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# File globs / suffixes to INCLUDE (case-insensitive match on suffix or exact name)
INCLUDE_SUFFIXES = {
    ".py", ".toml", ".yaml", ".yml", ".ini", ".conf", ".cfg", ".md",
    ".json", ".txt", ".sh", ".ps1", ".mako", ".env.example", ".sql",
    ".dockerfile",
}
INCLUDE_EXACT = {
    "Dockerfile", ".gitignore", "Makefile", "alembic.ini",
    "requirements.txt", "LICENSE", "README", "README.md",
}

# Paths (relative) / substrings to EXCLUDE
EXCLUDE_DIR_NAMES = {
    ".git", ".venv", "__pycache__", ".ruff_cache", ".pytest_cache",
    "dist", "build", ".mypy_cache", ".idea", ".vscode",
    "projects_data",
}

# Individual file name patterns to exclude
EXCLUDE_FILE_NAMES = {
    "eventbus.db", "test.db", "ca.key", "server.key", "ca.srl", "server.csr",
    "tls.key", "tls.crt",
}

# Skip any file larger than this (bytes)
MAX_FILE_BYTES = 200_000  # Adjust if you really want large assets.

# Detect binary by presence of null bytes
BINARY_SNIFF_BYTES = 2048

# Output file
OUTPUT_NAME = "audit_full.md"

# ------------ HELPERS -------------------------------------------------

def is_text_candidate(path: pathlib.Path) -> bool:
    name_lower = path.name.lower()
    suffix_lower = path.suffix.lower()

    if path.name in EXCLUDE_FILE_NAMES:
        return False

    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return False

    if path.is_dir():
        return False

    if path.stat().st_size > MAX_FILE_BYTES:
        return False

    if suffix_lower in INCLUDE_SUFFIXES or path.name in INCLUDE_EXACT:
        return True

    # Also treat certain extensionless files as text if small
    if "." not in path.name and path.stat().st_size < 50_000:
        # heuristically allow
        return True

    return False


def looks_binary(path: pathlib.Path) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(BINARY_SNIFF_BYTES)
        if b"\x00" in chunk:
            return True
    except Exception:
        return True
    return False


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def rel(p: pathlib.Path) -> str:
    return str(p.relative_to(REPO_ROOT)).replace("\\", "/")


def collect_files() -> list[pathlib.Path]:
    files = []
    for p in REPO_ROOT.rglob("*"):
        if p.is_file() and is_text_candidate(p):
            if not looks_binary(p):
                files.append(p)
    files.sort()
    return files


def build_tree(files: list[pathlib.Path]) -> str:
    """
    Produce a simple tree view limited to selected files (not *all* repo contents).
    """
    lines = []
    for f in files:
        lines.append(rel(f))
    return "\n".join(lines)


# ------------ MAIN ----------------------------------------------------

def main():
    files = collect_files()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    out_path = REPO_ROOT / OUTPUT_NAME

    with out_path.open("w", encoding="utf-8") as out:
        out.write(f"# Aegis Event Bus – Full Audit Bundle\n\n")
        out.write(f"Generated: {now}\n\n")
        out.write("## Included File Count\n\n")
        out.write(f"{len(files)} files\n\n")

        out.write("## File Tree (filtered)\n\n```\n")
        out.write(build_tree(files))
        out.write("\n```\n\n")

        out.write("## File Contents\n\n")
        for f in files:
            rel_path = rel(f)
            sha = sha256_of(f)
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # fallback as latin-1
                text = f.read_text(encoding="latin-1")

            # Trim trailing whitespace lines for neatness (optional)
            # Keep exactly as-is otherwise.
            out.write(f"### {rel_path}\n\n")
            out.write(f"**SHA256:** `{sha}`  \n\n")

            # Mark code fence language guess
            lang = ""
            suffix = f.suffix.lower()
            if suffix in (".py",):
                lang = "python"
            elif suffix in (".sh",):
                lang = "bash"
            elif suffix in (".yml", ".yaml"):
                lang = "yaml"
            elif suffix in (".toml",):
                lang = "toml"
            elif suffix in (".ini", ".conf"):
                lang = "ini"
            elif suffix in (".md",):
                lang = "markdown"
            elif suffix in (".mako",):
                lang = "jinja"
            elif suffix in (".json",):
                lang = "json"
            elif suffix in (".sql",):
                lang = "sql"
            elif f.name == "Dockerfile":
                lang = "dockerfile"

            out.write(f"```{lang}\n{text}\n```\n\n")

        out.write("---\n")
        out.write("**Note:** Private keys, databases, and large/binary files intentionally excluded.\n")

    print(f"[OK] Wrote {OUTPUT_NAME} with {len(files)} files.")


if __name__ == "__main__":
    main()

```

### tests/conftest.py

**SHA256:** `f9af561237abf15e3b89403b06c29ede1eba379b9f39f63705d593e43d92912d`  

```python
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

### tests/test_api.py

**SHA256:** `3b0eb5d20a3420a84bbb98b6c5d507e5a450355f4f10103e1b92e5c4e1c90f3e`  

```python
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

### tests/test_archivist.py

**SHA256:** `323cab0573e829bbdf205363fd6b2138f84c27be85c36085300e10999b6b974d`  

```python
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

### tests/test_pagination.py

**SHA256:** `51989b7aff92d167a2324aa784df6b8fefe77bace529a8612e733c42d3940ae5`  

```python
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

---
**Note:** Private keys, databases, and large/binary files intentionally excluded.
