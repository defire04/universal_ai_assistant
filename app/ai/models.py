"""AI request/response models."""

from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Chat request to AI."""
    message: str
    use_rag: bool = False
    temperature: Optional[float] = None


class ChatResponse(BaseModel):
    """AI response with metadata."""
    content: str
    model: str
    success: bool = True
    error: Optional[str] = None
    rag_enabled: bool = False