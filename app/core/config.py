"""Loads application configuration from environment variables."""

import sys
from typing import List
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    debug_rag: bool = False
    similarity_threshold: float = 0.5
    rag_top_k: int = 5

    documents_folder: str = "./documents"
    system_prompt: str = "Ти дружелюбний AI-помічник співробітників ТОВ \"ТРЕЙД СЕРВІС АЛЬЯНС\". Відповідай українською мовою, будь ввічливим та надавай стислі та конкретні відповіді на основі наданої інформації. Відповідай лише на те, що запитують - не додавай зайву інформацію як ID, телефони чи електронну пошту, якщо про це не питають конкретно. Якщо інформація не знайдена в документах, скажи про це ввічливо."

    # Logging Configuration
    log_level: str = "INFO"

    # Telegram Bot Configuration
    telegram_bot_token: str = ""
    allowed_user_ids: str = ""

    @property
    def allowed_users_list(self) -> List[int]:
        """Returns list of allowed user IDs."""
        if not self.allowed_user_ids:
            return []
        return [int(uid.strip()) for uid in self.allowed_user_ids.split(',') if uid.strip()]

    def __post_init__(self):
        """Validate required fields after initialization."""
        if not self.gemini_api_key:
            logger.error("GEMINI_API_KEY is required in .env file")
            sys.exit(1)
        if not self.database_url:
            logger.error("DATABASE_URL is required in .env file")
            sys.exit(1)
        if not self.telegram_bot_token:
            logger.error("TELEGRAM_BOT_TOKEN is required in .env file")
            sys.exit(1)


# Create config with validation
try:
    config = Config()
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)
