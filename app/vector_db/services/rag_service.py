"""RAG coordination service."""

from pathlib import Path
from typing import List, Dict

from loguru import logger

from app.core.config import config
from app.vector_db.repositories.vector_repository import VectorRepository
from app.vector_db.services.embedding_service import EmbeddingService


class RAGService:
    """Coordinates RAG operations."""

    def __init__(self, vector_repo: VectorRepository, embedding_service: EmbeddingService):
        self.vector_repo = vector_repo
        self.embedding_service = embedding_service

    async def initialize_documents(self) -> None:
        """Load and process all documents from configured folder."""
        from app.vector_db.reader import DocumentReader

        docs_path = Path(config.documents_folder)
        if not docs_path.exists():
            logger.warning(f"Documents folder not found: {config.documents_folder}")
            return

        document_reader = DocumentReader()
        supported_files = [f for f in docs_path.iterdir()
                           if f.is_file() and f.suffix.lower() in ['.pdf', '.txt']]

        for file_path in supported_files:
            content = document_reader.read_file(str(file_path))
            chunks = document_reader.split_text(content)
            await self.add_chunks(chunks, str(file_path))

    async def add_chunks(self, chunks: List[str], source: str) -> int:
        """Add text chunks to vector store."""
        for i, chunk in enumerate(chunks):
            embedding = await self.embedding_service.embed_text(chunk)
            chunk_id = f"{Path(source).stem}_{i}"
            metadata = {"source": source, "chunk_index": i}
            await self.vector_repo.save_chunk(chunk_id, chunk, embedding, metadata)

        logger.info(f"Added {len(chunks)} chunks from {source}")
        return len(chunks)

    async def search_context(self, query: str, top_k: int = None) -> List[Dict]:
        """Search for relevant context."""
        if top_k is None:
            top_k = config.rag_top_k
        query_embedding = await self.embedding_service.embed_text(query)
        results = await self.vector_repo.search_similar(query_embedding, top_k)

        if results:
            sources = {r["metadata"]["source"] for r in results}
            scores = [f"{r['similarity']:.3f}" for r in results]
            logger.info(f"RAG: {len(results)} chunks from {sources}, scores: {scores}")

            if config.debug_rag:
                full_context = "\n".join([f"Chunk {i}: {result['content']}" for i, result in enumerate(results)])
                logger.debug(f"RAG Full Context:\n{full_context}")
        else:
            logger.warning("RAG: no relevant context found")

        return results
