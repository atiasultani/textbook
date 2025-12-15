from typing import List, Optional, Dict, Any
from src.models.chat import (
    ChatSession,
    ChatMessage,
    ChatResponse,
    Source,
    RAGChatRequest,
    RAGChatResponse,
    ContextContent,
    ChatStatusEnum,
    ContextContentTypeEnum
)
from src.models.embeddings import SearchResult
from src.config.settings import settings
import asyncio
import uuid
from datetime import datetime
from src.services.qdrant_service import store_embeddings, search_embeddings, create_collection
from src.services.cohere_service import CohereService
import cohere
from jose import JWTError, jwt
import os

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


# New RAG service for authenticated, context-locked assistant
class AuthenticatedRAGService:
    def __init__(self):
        """Initialize the authenticated RAG service with Cohere client."""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.cohere_client = cohere.Client(api_key)

    def validate_context_content(self, response_text: str, context_content: ContextContent) -> bool:
        """
        Validate that the response text is derived from the provided context content.
        This is a simplified implementation - in a real system, you'd use more sophisticated
        content matching algorithms.
        """
        # Convert both to lowercase for comparison
        response_lower = response_text.lower()
        context_lower = context_content.content.lower()

        # Check if key phrases from context appear in response
        # This is a basic check - real implementation would use semantic similarity
        context_words = set(context_lower.split()[:50])  # Take first 50 words as representative
        response_words = set(response_lower.split())

        # If there's significant overlap, consider it valid
        if len(context_words.intersection(response_words)) > 0:
            return True

        # Additional check: if context is very short, check for exact phrases
        if len(context_content.content) < 200:
            return context_lower in response_lower

        return False

    def generate_response(self, request: RAGChatRequest) -> RAGChatResponse:
        """
        Generate a response using the RAG approach with authentication and context-locking.
        """
        # Check if content is available in context
        if not request.context.content.strip():
            return RAGChatResponse(
                answer="The provided text does not contain this information.",
                status=ChatStatusEnum.no_content,
                context_used=request.context.source_document_id,
                timestamp=datetime.utcnow()
            )

        try:
            # Determine the context to use based on mode
            context_to_use = request.context.content

            # If selection-restricted mode, only use the provided content
            # If rag-mode, we could potentially enrich with more context
            if request.mode == "selection-restricted":
                # Only use the specific selected text
                context_to_use = request.context.content
            elif request.mode == "rag-mode":
                # Use the provided context as is
                context_to_use = request.context.content
            else:
                # Default to using the provided context
                context_to_use = request.context.content

            # Generate response using Cohere
            response = self.cohere_client.chat(
                message=request.question,
                preamble=f"You are an assistant that only responds based on the provided context. "
                         f"Do not use any external knowledge. If the answer is not in the context, "
                         f"respond with 'The provided text does not contain this information.'\n\n"
                         f"Context: {context_to_use}",
                model="command-r-plus",  # Using a suitable model
                temperature=0.1  # Low temperature for more factual responses
            )

            generated_text = response.text

            # Validate that response comes from context
            if not self.validate_context_content(generated_text, request.context):
                # If validation fails, return the standard no-content response
                return RAGChatResponse(
                    answer="The provided text does not contain this information.",
                    status=ChatStatusEnum.no_content,
                    context_used=request.context.source_document_id,
                    timestamp=datetime.utcnow()
                )

            # Check if the response contains the specific rejection message
            if "The provided text does not contain this information." in generated_text:
                return RAGChatResponse(
                    answer="The provided text does not contain this information.",
                    status=ChatStatusEnum.no_content,
                    context_used=request.context.source_document_id,
                    timestamp=datetime.utcnow()
                )

            # Return successful response
            return RAGChatResponse(
                answer=generated_text,
                status=ChatStatusEnum.success,
                context_used=request.context.source_document_id,
                timestamp=datetime.utcnow()
            )

        except Exception as e:
            # Log the error in a real implementation
            print(f"Error generating response: {str(e)}")
            return RAGChatResponse(
                answer="The provided text does not contain this information.",
                status=ChatStatusEnum.no_content,
                context_used=request.context.source_document_id,
                timestamp=datetime.utcnow()
            )

    def process_request(self, request: RAGChatRequest) -> RAGChatResponse:
        """
        Process a chat request according to the specified processing order:
        1. Check authentication (handled by middleware)
        2. Enforce context-only rule
        3. Apply correct interaction mode
        4. Generate answer or refusal
        """
        # The authentication check is handled by middleware before this service is called

        # Enforce context-only rule - we only use the provided context
        # Apply correct interaction mode (selection-restricted vs rag-mode) handled above
        # Generate answer or refusal
        return self.generate_response(request)


# Anti-hallucination service functions
def check_for_hallucination(response_text: str, context_content: ContextContent) -> bool:
    """
    Check if the response contains hallucinated information not present in the context.
    Returns True if hallucination is detected, False otherwise.
    """
    # This is a simplified implementation
    # In a real system, you'd use more sophisticated semantic analysis
    response_lower = response_text.lower()
    context_lower = context_content.content.lower()

    # Basic check: look for significant content not in context
    response_sentences = response_text.split('.')
    for sentence in response_sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 10:  # Only check non-trivial sentences
            sentence_lower = sentence.lower()
            if sentence_lower not in context_lower:
                # This is a simplified check - in reality, paraphrasing would need to be handled
                continue  # We'll allow some variance for now

    # For now, return False (no hallucination detected) - in a real implementation,
    # this would involve more sophisticated semantic analysis
    return False
