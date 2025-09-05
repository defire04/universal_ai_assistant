"""Defines Pydantic models for AI request and response handling."""

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Represents a chat request to AI model."""

    message: str
    temperature: Optional[float] = None
    use_rag: bool = False


class ChatResponse(BaseModel):
    """Represents AI model response with metadata."""

    content: str
    model: str
    success: bool = True
    error: Optional[str] = None
    rag_enabled: bool = False