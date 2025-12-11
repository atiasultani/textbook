from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
import uuid


class ContentBlockBase(BaseModel):
    chapter_id: str
    content: str
    block_type: str  # Type of content (paragraph, code, heading, etc.)
    position: int  # Order within the chapter
    embedding_id: Optional[str] = None  # Reference to vector embedding in Qdrant

    @field_validator('position')
    @classmethod
    def validate_position(cls, v):
        if v < 0:
            raise ValueError('Position must be non-negative')
        return v


class ContentBlockCreate(ContentBlockBase):
    pass


class ContentBlockUpdate(BaseModel):
    content: Optional[str] = None
    block_type: Optional[str] = None
    position: Optional[int] = None
    embedding_id: Optional[str] = None


class ContentBlock(ContentBlockBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TextbookChapterBase(BaseModel):
    title: str
    content: str
    slug: str
    order: int
    metadata: Optional[dict] = None
    content_blocks: Optional[List[ContentBlock]] = None

    @field_validator('order')
    @classmethod
    def validate_order(cls, v):
        if v < 1 or v > 6:
            raise ValueError('Chapter order must be between 1 and 6')
        return v


class TextbookChapterCreate(TextbookChapterBase):
    pass


class TextbookChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    order: Optional[int] = None
    metadata: Optional[dict] = None


class TextbookChapter(TextbookChapterBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TextbookChapterWithId(BaseModel):
    id: str
    title: str
    slug: str
    order: int