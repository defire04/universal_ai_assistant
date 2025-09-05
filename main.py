"""Provides CLI entry point for the AI assistant application."""

import asyncio
import os
from pathlib import Path
from loguru import logger

from app.core.logger import setup_logger
from app.ai.gemini import gemini_client
from app.ai.models import ChatRequest
from app.vector_db.reader import document_reader
from app.vector_db.vector_store import vector_store


async def main() -> None:
    """Runs CLI interface for AI chat application."""

    setup_logger()
    await vector_store.initialize()

    # НАСТРОЙКИ - меняй здесь
    DOCUMENTS_FOLDER = "./documents"  # Папка с документами
    QUESTION = "Когда день рождение у Олаби Дмитрия?"  # Твой вопрос

    try:
        # Загружаем все документы из папки
        docs_path = Path(DOCUMENTS_FOLDER)

        if not docs_path.exists():
            logger.error(f"Папка не найдена: {DOCUMENTS_FOLDER}")
            logger.info("Создай папку './documents' и положи туда PDF или TXT файлы")
            return

        # Находим все поддерживаемые файлы
        supported_files = []
        for file_path in docs_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt']:
                supported_files.append(file_path)

        if not supported_files:
            logger.error(f"В папке {DOCUMENTS_FOLDER} нет PDF или TXT файлов")
            return

        logger.info(f"Найдено {len(supported_files)} файлов для обработки")

        # Загружаем каждый документ
        total_chunks = 0
        for file_path in supported_files:
            logger.info(f"Обрабатываю: {file_path.name}")

            # Читаем файл
            content = document_reader.read_file(str(file_path))

            # Разбиваем на чанки
            chunks = document_reader.split_text(content)

            # Добавляем в векторную БД
            count = await vector_store.add_chunks(chunks, str(file_path))
            total_chunks += count

            logger.info(f"Добавлено {count} чанков из {file_path.name}")

        logger.info(f"Всего обработано {total_chunks} чанков из {len(supported_files)} документов")

        # Задаем вопрос с RAG
        logger.info(f"Задаю вопрос: {QUESTION}")

        request = ChatRequest(message=QUESTION, use_rag=True)
        response = await gemini_client.chat(request)

        if response.success:
            print(f"\n🤖 AI (с использованием документов): {response.content}")
        else:
            logger.error(f"Ошибка: {response.error}")

    finally:
        await vector_store.close()


if __name__ == "__main__":
    asyncio.run(main())