"""Vector storage with PGVector."""

import asyncpg
import ollama
import json  # ДОБАВЬ ЭТОТ ИМПОРТ
from typing import List, Dict
from pathlib import Path
from loguru import logger

from app.core.config import config


class VectorStore:
    """Stores and searches vectors in PGVector."""

    def __init__(self):
        self.pool = None
        self.ollama = ollama.Client(host=config.ollama_base_url)

    async def initialize(self):
        """Setup database."""
        self.pool = await asyncpg.create_pool(config.database_url)

        async with self.pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS vector_store (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    embedding vector(768)
                );
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_embedding 
                ON vector_store USING hnsw (embedding vector_cosine_ops);
            """)

        logger.info("Vector store initialized")

    async def add_chunks(self, chunks: List[str], source: str) -> int:
        """Add text chunks to vector store."""
        added = 0

        async with self.pool.acquire() as conn:
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = await self._get_embedding(chunk)

                # Convert list to string format for pgvector
                embedding_str = "[" + ",".join(map(str, embedding)) + "]"

                # Save chunk
                chunk_id = f"{Path(source).stem}_{i}"
                metadata = {"source": source}

                await conn.execute("""
                    INSERT INTO vector_store (id, content, metadata, embedding)
                    VALUES ($1, $2, $3, $4::vector)
                    ON CONFLICT (id) DO UPDATE SET 
                    content = $2, metadata = $3, embedding = $4::vector
                """, chunk_id, chunk, json.dumps(metadata), embedding_str)
                added += 1

        logger.info(f"Added {added} chunks")
        return added

    async def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search similar chunks."""
        # Get query embedding
        query_embedding = await self._get_embedding(query)

        # Convert to string format for pgvector
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        # Search
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT content, metadata, 1 - (embedding <=> $1::vector) as similarity
                FROM vector_store
                WHERE 1 - (embedding <=> $1::vector) > 0.3
                ORDER BY embedding <=> $1::vector
                LIMIT $2
            """, embedding_str, top_k)

        results = []
        for row in rows:
            results.append({
                "content": row["content"],
                "similarity": row["similarity"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
            })

        return results

    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from Ollama."""
        response = self.ollama.embeddings(model=config.embedding_model, prompt=text)
        return response['embedding']

    async def close(self):
        """Close connections."""
        if self.pool:
            await self.pool.close()


# Global instance
vector_store = VectorStore()