"""Embedding generation via Ollama."""

from typing import List

import ollama

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
        return list(response['embedding'])
