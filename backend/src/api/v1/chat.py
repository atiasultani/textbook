from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.models.chat import (
    ChatSession,
    ChatMessage,
    ChatResponse,
    Source,
    RAGChatRequest,
    RAGChatResponse,
    ChatStatusEnum
)
from src.services.rag_service import create_session, query_rag, AuthenticatedRAGService
from src.services.auth_service import AuthService
from src.auth.auth_handler import get_current_user
import uuid
import logging


class ChatQueryWithSelection(BaseModel):
    message: str
    context: Optional[List[ChatMessage]] = None
    selected_text: Optional[str] = None

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
rag_service = AuthenticatedRAGService()

# Existing chat functionality
@router.post("/chat/start", response_model=ChatSession)
async def start_chat_session(current_user=Depends(get_current_user)):
    """Start a new chat session (requires authentication)"""
    try:
        session = await create_session()
        logger.info(f"New chat session created with ID: {session.id} for user: {current_user.username}")
        return session
    except Exception as e:
        logger.error(f"Error starting chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting chat session: {str(e)}")


@router.post("/chat/{session_id}/query", response_model=ChatResponse)
async def chat_query(session_id: str, query: ChatQueryWithSelection, current_user=Depends(get_current_user)):
    """Send a query to the RAG chatbot (requires authentication)"""
    # Validate input
    if not query.message or len(query.message.strip()) < 1:
        raise HTTPException(status_code=400, detail="Query message cannot be empty")

    if len(query.message) > 1000:  # Limit query length
        raise HTTPException(status_code=400, detail="Query message is too long (max 1000 characters)")

    try:
        response = await query_rag(session_id, query.message, query.context, query.selected_text)
        logger.info(f"Processed query for session {session_id} by user: {current_user.username}")
        return response
    except Exception as e:
        logger.error(f"Error processing query for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# New authenticated, context-locked RAG functionality
@router.post("/chat/rag", response_model=RAGChatResponse)
async def process_rag_chat(request: RAGChatRequest, req: Request):
    """
    Process user question with RAG assistant.
    Process authenticated user questions and return answers based only on provided context.
    """
    # Check authentication status from request state (set by middleware)
    auth_status = getattr(req.state, 'auth_status', None)

    if not auth_status or auth_status.status != "authenticated":
        # Return the exact message required by the specification
        return RAGChatResponse(
            answer="Please sign in or create an account to use the chatbot.",
            status=ChatStatusEnum.unauthorized,
            context_used=None,
            timestamp=datetime.utcnow()
        )

    # Process the request using the RAG service
    response = rag_service.process_request(request)

    return response


# Additional endpoint for testing the RAG functionality with authentication check
@router.post("/chat/rag/test")
async def test_rag_chat_with_auth_check(request: RAGChatRequest, req: Request):
    """
    Test endpoint that shows authentication status before processing.
    """
    # Check authentication status from request state (set by middleware)
    auth_status = getattr(req.state, 'auth_status', None)

    if not auth_status or auth_status.status != "authenticated":
        return {
            "authenticated": False,
            "message": "Please sign in or create an account to use the chatbot.",
            "timestamp": datetime.utcnow()
        }

    # If authenticated, process the request
    response = rag_service.process_request(request)

    return {
        "authenticated": True,
        "user_id": auth_status.user_id,
        "response": response,
        "timestamp": datetime.utcnow()
    }