"""Main message handlers for Telegram bot."""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command."""

    username = message.from_user.first_name or "User"

    welcome_text = (
        f"👋 Hello, {username}!\n\n"
        "🤖 I am the AI assistant of the company.\n"
        "📚 I have access to the corporate knowledge base.\n\n"
        "💬 Just write your question and I will answer based on company documents."
    )

    await message.answer(welcome_text)


@router.message()
async def handle_question(message: Message, rag_service, gemini_client) -> None:
    """Handle user questions with RAG."""

    user_question = message.text
    user_id = message.from_user.id

    logger.info(f"Question from {user_id}: {user_question[:50]}...")

    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        context_results = await rag_service.search_context(user_question)
        context = "\n".join([r["content"] for r in context_results])

        response = await gemini_client.chat(user_question, context)

        await message.answer(f"🤖 {response.content}")

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        await message.answer("❌ An error occurred. Please try again.")