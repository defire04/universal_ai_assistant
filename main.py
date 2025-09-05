"""Application entry point."""

import asyncio

import asyncpg

from app.ai.gemini import GeminiClient
from app.core.config import config
from app.core.logger import setup_logger
from app.telegram.bot import create_bot
from app.vector_db.repositories.vector_repository import VectorRepository
from app.vector_db.services.embedding_service import EmbeddingService
from app.vector_db.services.rag_service import RAGService


async def main() -> None:
    """Main application."""
    setup_logger(config.log_level)

    pool = await asyncpg.create_pool(config.database_url)
    vector_repo = VectorRepository(pool)
    await vector_repo.initialize()

    embedding_service = EmbeddingService()
    rag_service = RAGService(vector_repo, embedding_service)
    await rag_service.initialize_documents()

    gemini_client = GeminiClient()

    bot, dp = await create_bot(rag_service, gemini_client)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
