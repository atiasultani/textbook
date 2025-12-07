from typing import List, Optional
from src.models.chat import ChatSession, ChatMessage, ChatResponse, Source
from src.models.embeddings import SearchResult
from src.config.settings import settings
import asyncio
import uuid
from datetime import datetime
import openai
from src.services.qdrant_service import store_embeddings, search_embeddings, create_collection

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

# In-memory storage for chat sessions
chat_sessions = {}

async def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings for a text using OpenAI API"""
    try:
        response = await openai_client.embeddings.create(
            input=text,
            model=settings.openai_model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return a mock embedding in case of error
        return [0.0] * 1536  # Size for ada-002 embeddings

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

    # First, try to find relevant content using vector search if available
    try:
        # Generate embedding for the query
        query_embedding = await generate_embeddings(query_text)

        # Search in Qdrant for similar content
        search_results = await search_embeddings(query_embedding, top_k=3)

        if search_results:
            # Use vector search results
            best_result = search_results[0]

            # Get the full chapter content to include in response
            chapter_data = textbook_storage.get(best_result["chapter_id"])
            if chapter_data:
                source = Source(
                    chapter_id=best_result["chapter_id"],
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:500] + "...",  # Truncate for display
                    similarity_score=best_result["similarity_score"]
                )

                # Generate a response based on the content
                response_text = f"Based on the textbook chapter '{chapter_data['title']}', here's what I found: {chapter_data['content'][:200]}..."
            else:
                # Fallback if chapter not found in storage
                source = Source(
                    chapter_id=best_result["chapter_id"],
                    chapter_title="Unknown Chapter",
                    content="Relevant content found in textbook.",
                    similarity_score=best_result["similarity_score"]
                )
                response_text = "I found relevant information in the textbook. Please refer to the specific chapter for details."
        else:
            # If no results from vector search, fallback to keyword matching
            best_match = None
            best_score = 0

            query_lower = query_text.lower()
            for chapter_id, chapter_data in textbook_storage.items():
                content_lower = chapter_data["content"].lower()
                title_lower = chapter_data["title"].lower()

                # Calculate a simple relevance score
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
                    content=best_match["content"][:500] + "...",  # Truncate for display
                    similarity_score=best_score / 3.0  # Normalize score
                )

                # Generate a response based on the content
                response_text = f"Based on the textbook chapter '{best_match['title']}', here's what I found: {best_match['content'][:200]}..."
            else:
                # If no good match found, provide a default response
                source = Source(
                    chapter_id="",
                    chapter_title="No relevant content found",
                    content="The textbook does not contain information about this topic.",
                    similarity_score=0.0
                )
                response_text = "I couldn't find specific information about this topic in the textbook. Please try rephrasing your question or check other chapters."
    except Exception as e:
        # Fallback to keyword matching if vector search fails
        print(f"Vector search failed, falling back to keyword matching: {e}")
        best_match = None
        best_score = 0

        query_lower = query_text.lower()
        for chapter_id, chapter_data in textbook_storage.items():
            content_lower = chapter_data["content"].lower()
            title_lower = chapter_data["title"].lower()

            # Calculate a simple relevance score
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
                content=best_match["content"][:500] + "...",  # Truncate for display
                similarity_score=best_score / 3.0  # Normalize score
            )

            # Generate a response based on the content
            response_text = f"Based on the textbook chapter '{best_match['title']}', here's what I found: {best_match['content'][:200]}..."
        else:
            # If no good match found, provide a default response
            source = Source(
                chapter_id="",
                chapter_title="No relevant content found",
                content="The textbook does not contain information about this topic.",
                similarity_score=0.0
            )
            response_text = "I couldn't find specific information about this topic in the textbook. Please try rephrasing your question or check other chapters."

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
    from src.services.qdrant_service import search_embeddings
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Generate embedding for the query
        query_embedding = await generate_embeddings(query)

        # Search in Qdrant for similar content
        vector_results = await search_embeddings(query_embedding, top_k)

        # Convert vector search results to SearchResults
        results = []
        for result in vector_results:
            chapter_data = textbook_storage.get(result["chapter_id"])
            if chapter_data:
                search_result = SearchResult(
                    chapter_id=result["chapter_id"],
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:300] + "...",  # Truncate for display
                    similarity_score=result["similarity_score"]
                )
                results.append(search_result)

        return results
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        # Fallback to keyword matching if vector search fails
        query_lower = query.lower()
        results = []

        for chapter_id, chapter_data in textbook_storage.items():
            content_lower = chapter_data["content"].lower()
            title_lower = chapter_data["title"].lower()

            # Calculate a simple relevance score
            score = 0
            if query_lower in content_lower:
                score += 2
            if query_lower in title_lower:
                score += 1

            if score > 0:
                result = SearchResult(
                    chapter_id=chapter_id,
                    chapter_title=chapter_data["title"],
                    content=chapter_data["content"][:300] + "...",  # Truncate for display
                    similarity_score=score / 3.0  # Normalize score
                )
                results.append(result)

        # Sort by similarity score (descending) and return top_k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]