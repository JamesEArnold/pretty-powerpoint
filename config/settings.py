"""Application configuration management."""
from typing import Literal
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    environment: Literal["local", "dev", "staging", "prod"] = "local"
    aws_region: str = "us-east-1"
    log_level: str = "INFO"

    # API Settings
    api_version: str = "v1"
    api_title: str = "Presentation Generator API"

    # External Services
    openai_api_key: str = ""
    openai_model: str = "gpt-4"

    class Config:
        """Pydantic configuration class."""

        env_file = ".env"
        env_file_encoding = "utf-8"
