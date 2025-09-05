"""Access control middleware for Telegram bot."""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from app.core.config import config


class AccessControlMiddleware(BaseMiddleware):
    """Middleware to control bot access by user ID."""

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """Check if user is allowed to use the bot."""

        user_id = event.from_user.id
        username = event.from_user.username or "unknown"

        # Check if user is in allowed list
        allowed_users = config.allowed_users_list

        if allowed_users and user_id not in allowed_users:
            logger.warning(f"Access denied for user {username} ({user_id})")
            await event.answer(
                "❌ Access to the bot is restricted.\n"
                "Please contact the administrator for access."
            )
            return None

        logger.info(f"User {username} ({user_id}) accessed bot")
        return await handler(event, data)