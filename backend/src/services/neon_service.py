from typing import List, Optional
from src.models.textbook import TextbookChapter, TextbookChapterWithId
import asyncio
import uuid
from datetime import datetime

# In-memory storage for now - will be replaced with Neon database in the future
textbook_storage = {}

# Sample textbook chapters
SAMPLE_CHAPTERS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Introduction to Physical AI",
        "slug": "intro-physical-ai",
        "order": 1,
        "content": "# Introduction to Physical AI\n\nPhysical AI is an interdisciplinary field that combines robotics, machine learning, and physics to create intelligent systems that can interact with the physical world...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Basics of Humanoid Robotics",
        "slug": "basics-humanoid-robotics",
        "order": 2,
        "content": "# Basics of Humanoid Robotics\n\nHumanoid robots are robots with human-like features and capabilities. They are designed to mimic human appearance and behavior...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "ROS 2 Fundamentals",
        "slug": "ros-2-fundamentals",
        "order": 3,
        "content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Digital Twin Simulation (Gazebo + Isaac)",
        "slug": "digital-twin-simulation",
        "order": 4,
        "content": "# Digital Twin Simulation (Gazebo + Isaac)\n\nDigital twin simulation involves creating a virtual replica of a physical system. This allows for testing, validation, and optimization of robotic systems in a safe virtual environment...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Vision-Language-Action Systems",
        "slug": "vision-language-action",
        "order": 5,
        "content": "# Vision-Language-Action Systems\n\nVision-Language-Action systems integrate visual perception, natural language understanding, and physical action to create robots that can understand and respond to human commands in natural language...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Capstone: Simple AI-Robot Pipeline",
        "slug": "capstone",
        "order": 6,
        "content": "# Capstone: Simple AI-Robot Pipeline\n\nThis capstone project integrates all concepts learned in previous chapters to build a complete AI-robot pipeline that demonstrates the principles of Physical AI in action...",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Initialize the sample chapters
for chapter in SAMPLE_CHAPTERS:
    textbook_storage[chapter["id"]] = chapter


async def get_all_chapters() -> List[TextbookChapterWithId]:
    """Get all textbook chapters with basic info"""
    chapters = []
    for chapter_data in textbook_storage.values():
        chapter = TextbookChapterWithId(
            id=chapter_data["id"],
            title=chapter_data["title"],
            slug=chapter_data["slug"],
            order=chapter_data["order"]
        )
        chapters.append(chapter)
    # Sort by order
    chapters.sort(key=lambda x: x.order)
    return chapters


async def get_chapter_by_id(chapter_id: str) -> Optional[TextbookChapter]:
    """Get a specific textbook chapter by ID"""
    if chapter_id in textbook_storage:
        chapter_data = textbook_storage[chapter_id]
        return TextbookChapter(
            id=chapter_data["id"],
            title=chapter_data["title"],
            content=chapter_data["content"],
            slug=chapter_data["slug"],
            order=chapter_data["order"],
            created_at=chapter_data["created_at"],
            updated_at=chapter_data["updated_at"],
            metadata=chapter_data.get("metadata")
        )
    return None


async def create_chapter(chapter_data: dict) -> TextbookChapter:
    """Create a new textbook chapter"""
    chapter_id = str(uuid.uuid4())
    new_chapter = {
        "id": chapter_id,
        "title": chapter_data["title"],
        "content": chapter_data["content"],
        "slug": chapter_data["slug"],
        "order": chapter_data["order"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "metadata": chapter_data.get("metadata", {})
    }
    textbook_storage[chapter_id] = new_chapter

    return TextbookChapter(
        id=new_chapter["id"],
        title=new_chapter["title"],
        content=new_chapter["content"],
        slug=new_chapter["slug"],
        order=new_chapter["order"],
        created_at=new_chapter["created_at"],
        updated_at=new_chapter["updated_at"],
        metadata=new_chapter["metadata"]
    )