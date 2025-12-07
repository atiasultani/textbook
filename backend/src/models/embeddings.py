from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class KnowledgeEmbeddingBase(BaseModel):
    chapter_id: str
    content_chunk: str
    embedding_vector: List[float]
    chunk_index: int
    metadata: Optional[dict] = None


class KnowledgeEmbeddingCreate(KnowledgeEmbeddingBase):
    pass


class KnowledgeEmbedding(KnowledgeEmbeddingBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    chapter_id: str
    chapter_title: str
    content: str
    similarity_score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]