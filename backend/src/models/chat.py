from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ChatSessionBase(BaseModel):
    user_id: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    context_window: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True


class UserQueryBase(BaseModel):
    query_text: str
    session_id: str
    selected_text: Optional[str] = None  # Text selected by user for targeted questioning
    language: str = "en"


class UserQueryCreate(UserQueryBase):
    user_id: Optional[str] = None


class UserQuery(UserQueryBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatQuery(BaseModel):
    message: str
    context: Optional[List[ChatMessage]] = None


class Source(BaseModel):
    chapter_id: str
    chapter_title: str
    content: str
    similarity_score: float


class ChatResponse(BaseModel):
    response: str
    sources: List[Source]
    confidence_score: float  # Confidence level of the response (0-1)
    is_hallucinated: bool  # Flag if response was not based on textbook content
    session_id: str
    timestamp: datetime