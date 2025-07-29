# app/main.py
# FastAPI entrypoint: sets logging, middleware, metrics, routers.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import endpoints, logging_config, security
from .config import settings
from .middleware_security import (
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)

# ---- logging & metrics setup ----
logging_config.setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema is created/updated by Alembic migrations; nothing to do here.
    yield


app = FastAPI(title="Aegis Event Bus", lifespan=lifespan, debug=settings.DEBUG)

# Security middleware (order matters - add most specific first)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Only add rate limiting in production or when explicitly enabled
if settings.is_production or settings.ENV == "staging":
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60, burst_limit=10)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)

# Routers
app.include_router(endpoints.router)
app.include_router(security.router)
