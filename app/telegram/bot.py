"""Telegram bot initialization."""

from aiogram import Bot, Dispatcher
from loguru import logger

from app.core.config import config
from app.telegram.handlers import messages
from app.telegram.middlewares.access import AccessControlMiddleware


async def create_bot(rag_service, gemini_client) -> tuple[Bot, Dispatcher]:
    """Creates and configures Bot and Dispatcher instances."""

    bot = Bot(token=config.telegram_bot_token)
    dp = Dispatcher()

    # Pass services to handlers through data
    dp["rag_service"] = rag_service
    dp["gemini_client"] = gemini_client

    # Register middlewares
    dp.message.middleware(AccessControlMiddleware())

    # Register handlers
    dp.include_router(messages.router)

    logger.info("Telegram bot configured successfully")
    return bot, dp