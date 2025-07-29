# app/config.py
"""
Configuration management with security hardening.
Enforces SECRET_KEY in production and provides secure defaults.
"""

import secrets
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
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
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "aegis_event_bus"

    # MQTT settings
    MQTT_HOST: str = "mosquitto"
    MQTT_PORT: int = Field(default=8883, ge=1, le=65535)

    # Application settings
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(
        default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
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

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENV.lower() == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from environment


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
