import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.neon_service import create_chapter
from src.services.rag_service import index_chapter_content

# Sample textbook content
SAMPLE_CHAPTERS = [
    {
        "title": "Introduction to Physical AI",
        "slug": "intro-physical-ai",
        "order": 1,
        "content": "# Introduction to Physical AI\n\nPhysical AI is an interdisciplinary field that combines robotics, machine learning, and physics to create intelligent systems that can interact with the physical world. Unlike traditional AI that operates primarily in digital spaces, Physical AI focuses on embodied intelligence that can perceive, reason, and act in physical environments.\n\n## Key Concepts\n\n- **Embodied Intelligence**: Intelligence that emerges from the interaction between an agent and its physical environment\n- **Sensorimotor Learning**: Learning through sensing and acting in the physical world\n- **Physics-Informed AI**: AI systems that incorporate physical laws and constraints\n\n## Applications\n\nPhysical AI has applications in various domains:\n\n- Robotics and automation\n- Healthcare and assistive technologies\n- Manufacturing and logistics\n- Autonomous vehicles\n- Human-robot interaction\n\n## Challenges\n\nCreating effective Physical AI systems presents unique challenges:\n\n- Real-time perception and decision making\n- Uncertainty in physical environments\n- Safety and reliability requirements\n- Integration of multiple sensory modalities"
    },
    {
        "title": "Basics of Humanoid Robotics",
        "slug": "basics-humanoid-robotics",
        "order": 2,
        "content": "# Basics of Humanoid Robotics\n\nHumanoid robots are robots with human-like features and capabilities. They are designed to mimic human appearance and behavior, making them ideal for human-robot interaction and tasks that require human-like dexterity and mobility.\n\n## Anatomy of Humanoid Robots\n\nHumanoid robots typically feature:\n\n- **Bipedal locomotion**: Two legs for walking\n- **Upper body**: Arms and hands for manipulation\n- **Head**: With sensors for perception\n- **Torso**: Connecting all components\n\n## Key Technologies\n\n- **Actuators**: Motors and servos for movement\n- **Sensors**: Cameras, microphones, touch sensors\n- **Control systems**: Algorithms for balance and coordination\n- **AI systems**: For perception and decision making\n\n## Applications\n\nHumanoid robots are used in:\n\n- Healthcare assistance\n- Customer service\n- Education\n- Research\n- Entertainment"
    },
    {
        "title": "ROS 2 Fundamentals",
        "slug": "ros-2-fundamentals",
        "order": 3,
        "content": "# ROS 2 Fundamentals\n\nROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior.\n\n## Core Concepts\n\n- **Nodes**: Processes that perform computation\n- **Topics**: Named buses over which nodes exchange messages\n- **Services**: Synchronous request/response communication\n- **Actions**: Asynchronous goal-oriented communication\n\n## Architecture\n\nROS 2 uses a DDS (Data Distribution Service) implementation for communication between nodes, providing:\n\n- Real-time performance\n- Distributed systems support\n- Language independence\n- Platform independence\n\n## Key Features\n\n- Improved security\n- Better real-time support\n- Cross-platform compatibility\n- Deterministic behavior"
    },
    {
        "title": "Digital Twin Simulation (Gazebo + Isaac)",
        "slug": "digital-twin-simulation",
        "order": 4,
        "content": "# Digital Twin Simulation (Gazebo + Isaac)\n\nDigital twin simulation involves creating a virtual replica of a physical system. This allows for testing, validation, and optimization of robotic systems in a safe virtual environment before deployment in the real world.\n\n## Gazebo Simulation\n\nGazebo provides:\n\n- Realistic physics simulation\n- High-quality graphics\n- Multiple sensors simulation\n- Robot models library\n- Plugin system for custom functionality\n\n## Isaac Sim\n\nIsaac Sim offers:\n\n- Photorealistic rendering\n- Synthetic data generation\n- AI training environments\n- Integration with robotics frameworks\n\n## Benefits\n\n- Reduced development time and costs\n- Safe testing environment\n- Rapid prototyping\n- Training data generation"
    },
    {
        "title": "Vision-Language-Action Systems",
        "slug": "vision-language-action",
        "order": 5,
        "content": "# Vision-Language-Action Systems\n\nVision-Language-Action systems integrate visual perception, natural language understanding, and physical action to create robots that can understand and respond to human commands in natural language.\n\n## Components\n\n- **Visual Perception**: Understanding the environment through cameras and sensors\n- **Language Understanding**: Processing natural language commands\n- **Action Execution**: Performing physical tasks based on understanding\n\n## Applications\n\n- Assistive robotics\n- Industrial automation\n- Domestic robots\n- Educational robots\n\n## Challenges\n\n- Multimodal integration\n- Real-time processing\n- Context understanding\n- Safety and reliability"
    },
    {
        "title": "Capstone: Simple AI-Robot Pipeline",
        "slug": "capstone",
        "order": 6,
        "content": "# Capstone: Simple AI-Robot Pipeline\n\nThis capstone project integrates all concepts learned in previous chapters to build a complete AI-robot pipeline that demonstrates the principles of Physical AI in action.\n\n## Project Overview\n\nThe capstone project combines:\n\n- Physical AI principles\n- Humanoid robotics concepts\n- ROS 2 framework\n- Digital twin simulation\n- Vision-language-action systems\n\n## Implementation Steps\n\n1. Design the robot architecture\n2. Implement perception systems\n3. Create decision-making algorithms\n4. Integrate action systems\n5. Test in simulation\n6. Deploy to physical robot\n\n## Learning Outcomes\n\nBy completing this capstone, you will have:\n\n- Integrated multiple AI and robotics technologies\n- Built a complete AI-robot pipeline\n- Applied Physical AI principles in practice\n- Developed a working prototype"
    }
]

async def populate_textbook():
    """Populate the textbook with sample content"""
    print("Populating textbook with sample content...")

    for chapter_data in SAMPLE_CHAPTERS:
        print(f"Creating chapter: {chapter_data['title']}")
        chapter = await create_chapter(chapter_data)
        print(f"Created chapter with ID: {chapter.id}")

        # Index the chapter content for search
        print(f"Indexing content for search...")
        await index_chapter_content(chapter.id, chapter.content)
        print(f"Indexed content for chapter: {chapter.title}")

    print("Textbook population completed!")

if __name__ == "__main__":
    asyncio.run(populate_textbook())