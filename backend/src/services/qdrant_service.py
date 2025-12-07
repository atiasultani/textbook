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

COLLECTION_NAME = "textbook_embeddings"

async def create_collection():
    """Create the embeddings collection in Qdrant if it doesn't exist"""
    try:
        client.get_collection(COLLECTION_NAME)
        logger.info(f"Collection {COLLECTION_NAME} already exists")
    except:
        # Collection doesn't exist, create it
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # OpenAI ada-002 embedding size
        )
        logger.info(f"Created collection {COLLECTION_NAME}")


async def store_embeddings(chapter_id: str, content_chunks: List[dict]):
    """Store embeddings for a chapter in Qdrant"""
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
        collection_name=COLLECTION_NAME,
        points=points
    )


async def search_embeddings(query_embedding: List[float], top_k: int = 5) -> List[dict]:
    """Search for similar embeddings in Qdrant"""
    search_results = client.search(
        collection_name=COLLECTION_NAME,
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
    scroll_result = client.scroll(
        collection_name=COLLECTION_NAME,
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