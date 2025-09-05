"""Embedding generation via Ollama."""

import ollama
from typing import List
from loguru import logger
from app.core.config import config


class EmbeddingService:
    """Generates embeddings using Ollama."""

    def __init__(self):
        self.client = ollama.Client(host=config.ollama_base_url)

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings(
            model=config.embedding_model,
            prompt=text
        )
        return response['embedding']