from fastapi import APIRouter, HTTPException
from src.models.chat import ChatSession, ChatQuery, ChatResponse
from src.services.rag_service import create_session, query_rag
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat/start", response_model=ChatSession)
async def start_chat_session():
    """Start a new chat session"""
    try:
        session = await create_session()
        logger.info(f"New chat session created with ID: {session.id}")
        return session
    except Exception as e:
        logger.error(f"Error starting chat session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting chat session: {str(e)}")


@router.post("/chat/{session_id}/query", response_model=ChatResponse)
async def chat_query(session_id: str, query: ChatQuery):
    """Send a query to the RAG chatbot"""
    # Validate input
    if not query.message or len(query.message.strip()) < 1:
        raise HTTPException(status_code=400, detail="Query message cannot be empty")

    if len(query.message) > 1000:  # Limit query length
        raise HTTPException(status_code=400, detail="Query message is too long (max 1000 characters)")

    try:
        response = await query_rag(session_id, query.message, query.context)
        logger.info(f"Processed query for session {session_id}")
        return response
    except Exception as e:
        logger.error(f"Error processing query for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")