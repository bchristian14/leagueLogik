"""
Application settings and configuration.

This module handles environment variables and application configuration
using Pydantic settings for the Golf League Management System.
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Database Configuration
    database_url: str = Field(
        ...,
        description="PostgreSQL database URL connection string"
    )

    # API Configuration
    api_v1_str: str = Field(
        default="/api/v1",
        description="API version 1 path prefix"
    )
    project_name: str = Field(
        default="Golf League Management API",
        description="Project name for API documentation"
    )

    # Security Configuration
    secret_key: str = Field(
        ...,
        description="Secret key for JWT token signing"
    )
    algorithm: str = Field(
        default="HS256",
        description="Algorithm for JWT token signing"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="JWT access token expiration time in minutes"
    )

    # Environment Configuration
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    environment: str = Field(
        default="production",
        description="Environment name (development, production)"
    )

    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["http://localhost:5173"],
        description="Allowed CORS origins"
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Create global settings instance
settings = Settings()