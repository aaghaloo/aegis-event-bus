#!/usr/bin/env python3
"""
Setup script for aegis-event-bus
"""

from setuptools import find_packages, setup

setup(
    name="aegis-event-bus",
    version="0.1.0",
    description="Aegis Event Bus Application",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "pydantic",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "python-dotenv",
        "structlog",
        "paho-mqtt",
        "alembic",
        "psycopg2-binary",
    ],
    extras_require={"dev": ["pytest", "pytest-asyncio", "httpx", "black", "ruff"]},
)
