"""Loads application configuration from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
from loguru import logger
import sys


class Config(BaseSettings):
    """Application configuration loaded from .env file."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_temperature: float = 0.7

    # Application Configuration
    app_name: str = "Universal AI Assistant"

    # Vector Database Configuration
    database_url: str = ""
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text:v1.5"

    # Document Processing
    chunk_size: int = 1200
    min_chunk_size: int = 250
    max_chunks: int = 10000

    def __post_init__(self):
        """Validate required fields after initialization."""
        if not self.gemini_api_key:
            logger.error("GEMINI_API_KEY is required in .env file")
            sys.exit(1)
        if not self.database_url:
            logger.error("DATABASE_URL is required in .env file")
            sys.exit(1)


# Create config with validation
try:
    config = Config()
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)