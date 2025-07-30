# app/main.py
# FastAPI entrypoint: sets logging, middleware, metrics, routers.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from prometheus_fastapi_instrumentator import Instrumentator

from . import endpoints, logging_config, security
from .agent_router import router as agent_router
from .config import settings
from .middleware_security import (
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from .task_router import router as task_router

# ---- logging & metrics setup ----
logging_config.setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema is created/updated by Alembic migrations; nothing to do here.
    yield


def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Aegis Event Bus API",
        version="1.0.0",
        description="""
        # Aegis Event Bus API

        A secure, scalable event bus system for multi-agent coordination.

        ## Features

        * **Multi-Agent Support**: Register and manage multiple agents
        * **Task Management**: Create, assign, and track tasks across agents
        * **Secure Authentication**: JWT-based authentication with role-based access
        * **Real-time Communication**: MQTT-based event messaging
        * **Audit Logging**: Comprehensive audit trails for all operations
        * **Health Monitoring**: Built-in health checks and metrics

        ## Authentication

        All endpoints require authentication except `/healthz` and `/metrics`.
        Use the `/token` endpoint to obtain a JWT token.

        ## Rate Limiting

        * Default: 100 requests/minute
        * Authentication: 5 requests/minute
        * API endpoints: 1000 requests/minute

        ## Security

        * HTTPS/TLS encryption
        * SQL injection protection
        * XSS protection
        * CSRF protection
        * Input validation and sanitization
        """,
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /token endpoint",
        }
    }

    # Add security requirements
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Add server information
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.aegis-event-bus.com", "description": "Production server"},
    ]

    # Add tags metadata
    openapi_schema["tags"] = [
        {"name": "Authentication", "description": "JWT-based authentication endpoints"},
        {"name": "Jobs", "description": "Job creation and management"},
        {"name": "Agents", "description": "Agent registration and status management"},
        {"name": "Tasks", "description": "Task assignment and status tracking"},
        {"name": "Health", "description": "System health and monitoring endpoints"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title="Aegis Event Bus",
    description="Secure multi-agent event bus system",
    version="1.0.0",
    contact={"name": "Aegis Event Bus Support", "email": "support@aegis-event-bus.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    lifespan=lifespan,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

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
app.include_router(agent_router)
app.include_router(task_router)
