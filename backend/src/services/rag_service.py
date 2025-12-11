from typing import List, Optional
from src.models.chat import ChatSession, ChatMessage, ChatResponse, Source
from src.models.embeddings import SearchResult
from src.config.settings import settings
import asyncio
import uuid
from datetime import datetime
from src.services.qdrant_service import store_embeddings, search_embeddings, create_collection
from src.services.cohere_service import CohereService
import cohere

# Initialize Cohere service
cohere_service = CohereService()

# In-memory storage for chat sessions
chat_sessions = {}

async def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings using Cohere API"""
    try:
        # Create a temporary client to generate embeddings
        api_key = settings.cohere_api_key
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        temp_client = cohere.AsyncClient(api_key=api_key)
        response = await temp_client.embed(
            model=settings.embedding_model or "embed-english-v3.0",  # "embed-english-v3.0"
            texts=[text]
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"Error generating Cohere embeddings: {e}")
        # Return zero vector of size 1024 for embedding-english-v3.0
        return [0.0] * 1024

async def chunk_text(text: str, chunk_size: int = 1000) -> List[dict]:
    """Split text into chunks with embeddings"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i + chunk_size]
        embedding = await generate_embeddings(chunk_text)
        chunks.append({
            "content": chunk_text,
            "embedding": embedding
        })
    return chunks

async def index_chapter_content(chapter_id: str, content: str):
    """Generate and store embeddings for a chapter"""
    # Create the Qdrant collection if it doesn't exist
    await create_collection()

    # Split content into chunks and generate embeddings
    chunks = await chunk_text(content)

    # Store embeddings in Qdrant
    await store_embeddings(chapter_id, chunks)

# Mock implementation of RAG functionality
async def create_session() -> ChatSession:
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    session = ChatSession(
        id=session_id,
        user_id=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        context_window=[]
    )
    chat_sessions[session_id] = session
    return session

async def query_rag(session_id: str, query_text: str, context: Optional[List[ChatMessage]] = None, selected_text: Optional[str] = None) -> ChatResponse:
    """Process a query using RAG and return a response using Cohere service"""
    from src.services.neon_service import textbook_storage

    # Validate inputs
    if not session_id:
        raise ValueError("Session ID is required")

    if not query_text or len(query_text.strip()) == 0:
        raise ValueError("Query text cannot be empty")

    if len(query_text) > 2000:  # Limit query length
        raise ValueError("Query text is too long (max 2000 characters)")

    if selected_text and len(selected_text) > 2000:  # Limit selected text length
        raise ValueError("Selected text is too long (max 2000 characters)")

    try:
        # Generate embedding for the query
        query_embedding = await generate_embeddings(query_text)

        # Search in Qdrant for similar content
        search_results = await search_embeddings(query_embedding, top_k=3)

        # Convert search results to Source objects
        sources = []
        for result in search_results:
            chapter_data = textbook_storage.get(result["chapter_id"])
            if chapter_data:
                source = Source(
                    chapter_id=result["chapter_id"],
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:500] + "...",
                    similarity_score=result["similarity_score"]
                )
                sources.append(source)

        # Use Cohere service to generate response based on sources and selected text
        response_data = cohere_service.generate_response(
            query=query_text,
            context_sources=sources,
            selected_text=selected_text
        )

        # Create the chat response using the Cohere service response
        response = ChatResponse(
            response=response_data["response"],
            sources=response_data["sources"],
            confidence_score=response_data["confidence_score"],
            is_hallucinated=response_data["is_hallucinated"],
            session_id=session_id,
            timestamp=datetime.now()
        )

        # Update the session with the new interaction
        if session_id in chat_sessions:
            chat_sessions[session_id].updated_at = datetime.now()
            if context:
                chat_sessions[session_id].context_window.extend(context)

        return response
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in query_rag: {str(e)}")

        # Return a safe error response
        return ChatResponse(
            response="Sorry, I encountered an error processing your request. Please try again.",
            sources=[],
            confidence_score=0.0,
            is_hallucinated=False,
            session_id=session_id,
            timestamp=datetime.now()
        )

async def search_content(query: str, top_k: int = 5) -> List[SearchResult]:
    """Search textbook content and return top results"""
    from src.services.neon_service import textbook_storage
    import logging

    logger = logging.getLogger(__name__)

    try:
        query_embedding = await generate_embeddings(query)
        vector_results = await search_embeddings(query_embedding, top_k)
        results = []
        for result in vector_results:
            chapter_data = textbook_storage.get(result["chapter_id"])
            if chapter_data:
                search_result = SearchResult(
                    chapter_id=result["chapter_id"],
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:300] + "...",
                    similarity_score=result["similarity_score"]
                )
                results.append(search_result)
        return results
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        # Fallback to keyword matching
        query_lower = query.lower()
        results = []
        for chapter_id, chapter_data in textbook_storage.items():
            content_lower = chapter_data["content"].lower()
            title_lower = chapter_data["title"].lower()
            score = 0
            if query_lower in content_lower:
                score += 2
            if query_lower in title_lower:
                score += 1
            if score > 0:
                results.append(SearchResult(
                    chapter_id=chapter_id,
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:300] + "...",
                    similarity_score=score / 3.0
                ))
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
