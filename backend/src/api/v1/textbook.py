from fastapi import APIRouter, HTTPException
from typing import List
from src.models.textbook import TextbookChapter, TextbookChapterWithId
from src.services.neon_service import get_all_chapters, get_chapter_by_id

router = APIRouter()

@router.get("/textbook/chapters", response_model=List[TextbookChapterWithId])
async def get_textbook_chapters():
    """Get all textbook chapters"""
    try:
        chapters = await get_all_chapters()
        return chapters
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chapters: {str(e)}")


@router.get("/textbook/chapters/{chapter_id}", response_model=TextbookChapter)
async def get_textbook_chapter(chapter_id: str):
    """Get a specific textbook chapter"""
    try:
        chapter = await get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return chapter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chapter: {str(e)}")