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
ÿþ#   r e q u i r e m e n t s . t x t  
  
 #   - - -   C o r e   A p p l i c a t i o n   F r a m e w o r k   - - -  
 f a s t a p i  
 u v i c o r n [ s t a n d a r d ]  
 p y t h o n - d o t e n v  
 s t r u c t l o g  
 t y p e r > = 0 . 1 6                     #   n o    [ a l l ]    s u f f i x   r e q u i r e d  
  
  
 #   - - -   D a t a b a s e   &   O R M   - - -  
 s q l m o d e l  
 a l e m b i c  
 a s y n c p g  
 p s y c o p g 2 - b i n a r y  
  
 #   - - -   S e c u r i t y   &   A u t h e n t i c a t i o n   - - -  
 b c r y p t > = 4 . 1 . 2 , < 5  
 p a s s l i b [ b c r y p t ] > = 1 . 7 . 4  
 p y t h o n - j o s e [ c r y p t o g r a p h y ]  
 p y t h o n - m u l t i p a r t  
  
 #   - - -   E v e n t   M e s s a g i n g   - - -  
 p a h o - m q t t  
  
 #   - - -   O b s e r v a b i l i t y   - - -  
 p r o m e t h e u s - f a s t a p i - i n s t r u m e n t a t o r    
  
 #   - - -   T e s t i n g   - - - -  
 p y t e s t  
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
