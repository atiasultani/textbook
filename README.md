# AI-Native Textbook: Physical AI & Humanoid Robotics

An interactive textbook with RAG-powered chatbot for learning Physical AI and Humanoid Robotics concepts.

## Features

- Interactive textbook with 6 chapters on Physical AI and Humanoid Robotics
- RAG (Retrieval-Augmented Generation) chatbot that answers questions based on textbook content
- Natural language search functionality
- Auto-generated sidebar navigation
- Responsive design for cross-device accessibility

## Chapters

1. Introduction to Physical AI
2. Basics of Humanoid Robotics
3. ROS 2 Fundamentals
4. Digital Twin Simulation (Gazebo + Isaac)
5. Vision-Language-Action Systems
6. Capstone: Simple AI-Robot Pipeline

## Architecture

The application follows a web application architecture with:

- **Frontend**: Docusaurus-based textbook interface with integrated chatbot component
- **Backend**: FastAPI service handling RAG operations and API endpoints
- **Storage**:
  - Neon PostgreSQL for metadata
  - Qdrant vector database for embeddings
  - Docusaurus static files for content

## Technologies Used

- **Backend**: Python 3.11, FastAPI, Pydantic
- **Frontend**: Docusaurus, React
- **Database**: Neon PostgreSQL, Qdrant vector database
- **AI/ML**: OpenAI embeddings API
- **Other**: Docker, Pytest, Jest

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for local Qdrant)
- Access to OpenAI API or compatible embeddings service

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file with your API keys:
   ```bash
   # backend/.env
   NEON_DATABASE_URL=your-neon-database-url
   QDRANT_URL=your-qdrant-url
   QDRANT_API_KEY=your-qdrant-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

5. Start the backend server:
   ```bash
   python -m src.api.main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/docusaurus
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. The textbook will be available at `http://localhost:3000`
2. The backend API will be available at `http://localhost:8000`
3. Use the chatbot interface to ask questions about the textbook content
4. Use the search functionality to find specific information
5. Navigate through chapters using the sidebar

## API Endpoints

- `GET /api/v1/textbook/chapters` - Get all textbook chapters
- `GET /api/v1/textbook/chapters/{chapterId}` - Get a specific textbook chapter
- `POST /api/v1/textbook/search` - Search textbook content
- `POST /api/v1/chat/start` - Start a new chat session
- `POST /api/v1/chat/{sessionId}/query` - Send a query to the RAG chatbot

## CLI Commands

- Populate textbook content:
  ```bash
  python -m src.cli.populate_textbook
  ```

- Generate embeddings for textbook content:
  ```bash
  python -m src.cli.generate_embeddings
  ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.