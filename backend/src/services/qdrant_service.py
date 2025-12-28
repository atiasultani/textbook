from typing import List, Optional
from src.config.settings import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import asyncio
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Qdrant client
if settings.qdrant_api_key:
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
else:
    client = QdrantClient(host="localhost", port=6333)


def get_embedding_size():
    """Get the expected embedding size based on the configured provider"""
    if settings.embedding_provider.lower() == "gemini":
        return 768  # Gemini embedding size
    elif settings.embedding_provider.lower() == "cohere":
        return 1024  # Cohere embed-english-v3.0 size
    else:
        # Default to 1536 to maintain backward compatibility with existing setup
        return 1536

def get_collection_name():
    """Get the appropriate collection name based on embedding provider to avoid dimension conflicts"""
    size = get_embedding_size()
    if size == 768:
        return "textbook_embeddings_gemini"
    elif size == 1024:
        return "textbook_embeddings_cohere"
    else:
        return "textbook_embeddings"  # Original collection name

async def create_collection():
    """Create the embeddings collection in Qdrant if it doesn't exist"""
    collection_name = get_collection_name()
    expected_size = get_embedding_size()
    try:
        collection_info = client.get_collection(collection_name)
        # Check if the existing collection has the correct vector size
        if collection_info.config.params.vectors.size != expected_size:
            logger.warning(f"Collection {collection_name} exists but has wrong dimension ({collection_info.config.params.vectors.size}), expected {expected_size}. This may cause issues.")
        else:
            logger.info(f"Collection {collection_name} already exists with correct dimension {expected_size}")
    except:
        # Collection doesn't exist, create it
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=expected_size, distance=models.Distance.COSINE),  # Embedding size
        )
        logger.info(f"Created collection {collection_name} with dimension {expected_size}")


async def store_embeddings(chapter_id: str, content_chunks: List[dict]):
    """Store embeddings for a chapter in Qdrant"""
    collection_name = get_collection_name()
    points = []
    for i, chunk in enumerate(content_chunks):
        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=chunk["embedding"],
            payload={
                "chapter_id": chapter_id,
                "content": chunk["content"],
                "chunk_index": i
            }
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points
    )


async def search_embeddings(query_embedding: List[float], top_k: int = 5) -> List[dict]:
    """Search for similar embeddings in Qdrant"""
    collection_name = get_collection_name()
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,
    )

    results = []
    for result in search_results:
        results.append({
            "chapter_id": result.payload["chapter_id"],
            "content": result.payload["content"],
            "similarity_score": result.score
        })

    return results


async def get_all_embeddings(chapter_id: str) -> List[dict]:
    """Get all embeddings for a specific chapter"""
    collection_name = get_collection_name()
    scroll_result = client.scroll(
        collection_name=collection_name,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="chapter_id",
                    match=models.MatchValue(value=chapter_id),
                ),
            ]
        ),
        limit=10000,  # Adjust as needed
    )

    results = []
    for point in scroll_result[0]:
        results.append({
            "id": point.id,
            "content": point.payload["content"],
            "chunk_index": point.payload["chunk_index"]
        })

    return results