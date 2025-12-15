from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from enum import Enum


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


# New models for the RAG assistant feature
class AuthenticationStatusEnum(str, Enum):
    authenticated = "authenticated"
    unauthenticated = "unauthenticated"


class ContextContentTypeEnum(str, Enum):
    user_selected = "user-selected"
    retrieved_excerpt = "retrieved-excerpt"


class ChatStatusEnum(str, Enum):
    success = "success"
    no_content = "no-content"
    unauthorized = "unauthorized"


class AuthenticationStatus(BaseModel):
    """Represents whether the user is authenticated (authenticated | unauthenticated)"""
    status: AuthenticationStatusEnum
    user_id: Optional[str] = None  # present when authenticated
    token: Optional[str] = None  # JWT token string
    expires_at: Optional[datetime] = None  # datetime when token expires


class ContextContent(BaseModel):
    """Authorized text that serves as the source of truth for responses (user-selected text OR retrieved book chunks)"""
    type: ContextContentTypeEnum
    content: str = Field(..., min_length=1, description="The actual text content")
    source_document_id: str = Field(..., min_length=1, description="Identifier for the source document")
    section_reference: Optional[str] = None  # page number, chapter, etc.
    retrieval_metadata: Optional[Dict[str, Any]] = None  # confidence scores, relevance, etc.

    class Config:
        # This ensures the enum values are validated
        use_enum_values = True


class UserQuestion(BaseModel):
    """The query submitted by the user that requires a response"""
    id: str
    question_text: str = Field(..., min_length=1, description="The actual question")
    user_id: str  # identifier for the authenticated user
    timestamp: datetime  # when the question was submitted
    context_id: str  # reference to the associated context content


class Response(BaseModel):
    """The system-generated answer that must be strictly based on the provided context"""
    id: str
    answer_text: str  # the generated answer
    question_id: str  # reference to the associated question
    context_used: str  # the context that was used to generate the response
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)  # how confident the system is in the response
    was_hallucinated: bool = False  # whether the response contained information not in the context
    timestamp: datetime  # when the response was generated


# API Request/Response Models for RAG assistant
class RAGChatRequest(BaseModel):
    question: str
    context: ContextContent
    auth_status: Optional[AuthenticationStatus] = None
    mode: str = Field(..., pattern=r"^(selection-restricted|rag-mode)$")



class RAGChatResponse(BaseModel):
    answer: str
    status: ChatStatusEnum  # "success" | "no-content" | "unauthorized"
    context_used: Optional[str] = None
    timestamp: datetime


class AuthCheckRequest(BaseModel):
    token: str


class AuthCheckResponse(BaseModel):
    authenticated: bool
    user_id: Optional[str] = None
    message: str