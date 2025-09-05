"""PostgreSQL vector operations."""

import asyncpg
import json
from typing import List, Dict


class VectorRepository:
    """Handles vector storage in PostgreSQL."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def initialize(self) -> None:
        """Initialize database and tables."""
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


    async def save_chunk(self, chunk_id: str, content: str,
                        embedding: List[float], metadata: Dict) -> None:
        """Save chunk with embedding to database."""
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"

        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO vector_store (id, content, metadata, embedding)
                VALUES ($1, $2, $3, $4::vector)
                ON CONFLICT (id) DO UPDATE SET 
                content = $2, metadata = $3, embedding = $4::vector
            """, chunk_id, content, json.dumps(metadata), embedding_str)

    async def search_similar(self, query_embedding: List[float],
                           top_k: int = 5) -> List[Dict]:
        """Search for similar vectors."""
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT content, metadata, 1 - (embedding <=> $1::vector) as similarity
                FROM vector_store
                WHERE 1 - (embedding <=> $1::vector) > 0.3
                ORDER BY embedding <=> $1::vector
                LIMIT $2
            """, embedding_str, top_k)

        return [{"content": row["content"],
                "similarity": row["similarity"],
                "metadata": json.loads(row["metadata"])} for row in rows]