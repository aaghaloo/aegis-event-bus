# app/main.py
# FastAPI entrypoint: sets logging, DB init on startup, middleware, metrics, routers.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import db, endpoints, logging_config, security
from .middleware import SecurityHeadersMiddleware

# ---- logging & metrics setup ----
logging_config.setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates tables when running under pytest (SQLite); harmless on Postgres.
    db.init_db()
    yield


app = FastAPI(title="Aegis Event Bus", lifespan=lifespan)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)

# Routers
app.include_router(endpoints.router)
app.include_router(security.router)
