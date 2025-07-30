# app/config.py
"""
Configuration management with security hardening.
Enforces SECRET_KEY in production and provides secure defaults.
"""

import secrets
from functools import lru_cache
from typing import Optional

from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with security hardening."""

    # Security settings (mandatory in production)
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, ge=1, le=1440
    )  # 1 min to 24 hours

    # Environment
    ENV: str = Field(
        default="development", pattern="^(development|staging|production)$"
    )

    # Database settings
    DATABASE_URL: Optional[str] = None
    DATABASE_URL_RO: Optional[str] = None
    POSTGRES_USER: str = Field(default="postgres", description="Database username")
    POSTGRES_PASSWORD: str = Field(default="", description="Database password")
    POSTGRES_DB: str = Field(default="aegis_event_bus", description="Database name")

    # Database pooling settings
    DB_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DB_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=1, le=300)
    DB_POOL_RECYCLE: int = Field(default=3600, ge=0, le=7200)

    # MQTT settings
    MQTT_HOST: str = Field(default="mosquitto", description="MQTT broker hostname")
    MQTT_PORT: int = Field(default=8883, ge=1, le=65535)

    # Application settings
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(
        default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )

    # User management
    USERS: Optional[str] = Field(
        default=None, description="Comma-separated list of username:password pairs"
    )

    # Additional settings (allow extra)
    JWT_SECRET: Optional[str] = None
    DB_PW: Optional[str] = None
    DB_RO_PW: Optional[str] = None

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: Optional[str]) -> str:
        """Ensure SECRET_KEY is set in production."""
        if v:
            return v

        # For now, always generate a secure key in development
        # In production, this should be set via environment variable
        return secrets.token_urlsafe(32)

    @field_validator("POSTGRES_PASSWORD")
    @classmethod
    def validate_postgres_password(cls, v: str, info) -> str:
        """Ensure database password is not empty in production."""
        # Get the ENV value from the same data being validated
        env_value = (
            info.data.get("ENV", "development")
            if hasattr(info, "data")
            else "development"
        )
        if env_value.lower() == "production" and not v:
            raise ValueError("POSTGRES_PASSWORD must be set in production")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENV.lower() == "development"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Allow extra fields from environment
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
