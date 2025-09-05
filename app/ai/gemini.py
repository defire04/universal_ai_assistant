"""Provides typed client for Gemini AI API interactions."""

import google.generativeai as genai
from loguru import logger

from app.ai.models import ChatRequest, ChatResponse
from app.core.config import config


class GeminiClient:
    """Handles communication with Gemini AI API."""

    def __init__(self) -> None:
        """Initializes Gemini client with API configuration."""
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        logger.info(f"Gemini client initialized with model: {config.gemini_model}")

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Sends chat request to Gemini and returns response.

        Args:
            request: Chat request with user message

        Returns:
            ChatResponse with AI-generated content
        """
        try:
            # NEW: Build prompt with RAG context if enabled
            if request.use_rag:
                from app.vector_db.vector_store import vector_store

                # Search for relevant context
                search_results = await vector_store.search(request.message)

                if search_results:
                    context = "\n".join([result["content"] for result in search_results])
                    prompt = f"Context:\n{context}\n\nQuestion: {request.message}"
                    logger.info(f"Using RAG context with {len(search_results)} chunks")
                else:
                    prompt = f"No relevant context found.\nQuestion: {request.message}"
                    logger.info("No RAG context found")
            else:
                prompt = request.message

            logger.info(f"Sending request to Gemini: {prompt[:50]}...")

            # Use request temperature or config default
            temperature = request.temperature or config.gemini_temperature

            # Send request to Gemini
            response = self.model.generate_content(
                prompt,  # NEW: Using prompt instead of request.message
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )

            content = response.text
            logger.info(f"Received response from Gemini: {len(content)} characters")

            return ChatResponse(
                content=content,
                model=config.gemini_model,
                rag_enabled=request.use_rag  # NEW: Track if RAG was used
            )

        except Exception as e:
            error_msg = f"Error communicating with Gemini: {str(e)}"
            logger.error(error_msg)

            return ChatResponse(
                content="Sorry, an error occurred while processing your request.",
                model=config.gemini_model,
                success=False,
                error=error_msg
            )


# Global client instance
gemini_client = GeminiClient()