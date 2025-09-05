"""Gemini AI client."""

from typing import Optional

import google.generativeai as genai
from loguru import logger

from app.ai.models import ChatResponse
from app.core.config import config


class GeminiClient:
    """Gemini AI API client."""

    def __init__(self):
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        logger.info(f"Gemini initialized: {config.gemini_model}")

    async def chat(self, message: str, context: str = "",
                   temperature: Optional[float] = None) -> ChatResponse:
        """Send chat request to Gemini."""
        try:
            if context:
                if config.rag_only_mode:
                    prompt = f"{config.system_prompt}\n\nContext:\n{context}\n\nQuestion: {message}"
                else:
                    prompt = f"Context:\n{context}\n\nQuestion: {message}"
            else:
                if config.rag_only_mode:
                    prompt = f"{config.system_prompt}\n\nQuestion: {message}\nContext: No context found."
                else:
                    prompt = message

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature or config.gemini_temperature
                )
            )

            return ChatResponse(
                content=response.text,
                model=config.gemini_model,
                rag_enabled=bool(context)
            )

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return ChatResponse(
                content="Error occurred",
                model=config.gemini_model,
                success=False,
                error=str(e)
            )
