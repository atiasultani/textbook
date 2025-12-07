import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.neon_service import get_all_chapters, get_chapter_by_id
from src.services.rag_service import index_chapter_content

async def generate_embeddings():
    """Generate embeddings for all textbook content"""
    print("Generating embeddings for all textbook content...")

    # Get all chapters
    chapters = await get_all_chapters()

    if not chapters:
        print("No chapters found. Please populate the textbook first.")
        return

    for chapter in chapters:
        print(f"Processing chapter: {chapter.title}")

        # Get the full chapter content
        full_chapter = await get_chapter_by_id(chapter.id)
        if full_chapter:
            # Index the chapter content for search
            print(f"Generating embeddings for chapter: {chapter.title}")
            await index_chapter_content(chapter.id, full_chapter.content)
            print(f"Generated embeddings for chapter: {chapter.title}")
        else:
            print(f"Could not retrieve full content for chapter: {chapter.title}")

    print("Embeddings generation completed!")

if __name__ == "__main__":
    asyncio.run(generate_embeddings())