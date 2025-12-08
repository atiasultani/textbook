from typing import List, Optional
from src.models.chat import ChatSession, ChatMessage, ChatResponse, Source
from src.models.embeddings import SearchResult
from src.config.settings import settings
import asyncio
import uuid
from datetime import datetime
from src.services.qdrant_service import store_embeddings, search_embeddings, create_collection
from cohere import AsyncClient  # <-- Use Cohere async client

# Initialize Cohere client
cohere_client = AsyncClient(api_key=settings.cohere_api_key)

# In-memory storage for chat sessions
chat_sessions = {}

async def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings using Cohere API"""
    try:
        response = await cohere_client.embed(
            model=settings.embedding_model,  # "embed-english-v3.0"
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

async def query_rag(session_id: str, query_text: str, context: Optional[List[ChatMessage]] = None) -> ChatResponse:
    """Process a query using RAG and return a response"""
    from src.services.neon_service import textbook_storage

    # Generate embedding for the query
    query_embedding = await generate_embeddings(query_text)

    # Search in Qdrant for similar content
    search_results = await search_embeddings(query_embedding, top_k=3)

    # Fallback to keyword matching if needed
    if not search_results:
        best_match = None
        best_score = 0
        query_lower = query_text.lower()
        for chapter_id, chapter_data in textbook_storage.items():
            content_lower = chapter_data["content"].lower()
            title_lower = chapter_data["title"].lower()
            score = 0
            if query_lower in content_lower:
                score += 2
            if query_lower in title_lower:
                score += 1
            if score > best_score:
                best_score = score
                best_match = chapter_data

        if best_match:
            source = Source(
                chapter_id=best_match["id"],
                chapter_title=best_match["title"],
                content=best_match["content"][:500] + "...",
                similarity_score=best_score / 3.0
            )
            response_text = f"Based on the textbook chapter '{best_match['title']}', here's what I found: {best_match['content'][:200]}..."
        else:
            source = Source(
                chapter_id="",
                chapter_title="No relevant content found",
                content="The textbook does not contain information about this topic.",
                similarity_score=0.0
            )
            response_text = "I couldn't find specific information about this topic in the textbook."
    else:
        best_result = search_results[0]
        chapter_data = textbook_storage.get(best_result["chapter_id"])
        if chapter_data:
            source = Source(
                chapter_id=best_result["chapter_id"],
                chapter_title=chapter_data["title"],
                content=chapter_data["content"][:500] + "...",
                similarity_score=best_result["similarity_score"]
            )
            response_text = f"Based on the textbook chapter '{chapter_data['title']}', here's what I found: {chapter_data['content'][:200]}..."
        else:
            source = Source(
                chapter_id=best_result["chapter_id"],
                chapter_title="Unknown Chapter",
                content="Relevant content found in textbook.",
                similarity_score=best_result["similarity_score"]
            )
            response_text = "I found relevant information in the textbook. Please refer to the specific chapter for details."

    # Create the chat response
    response = ChatResponse(
        response=response_text,
        sources=[source],
        session_id=session_id,
        timestamp=datetime.now()
    )

    # Update the session with the new interaction
    if session_id in chat_sessions:
        chat_sessions[session_id].updated_at = datetime.now()
        if context:
            chat_sessions[session_id].context_window.extend(context)

    return response

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
