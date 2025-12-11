# Quickstart Guide: AI-Native Textbook with Enhanced RAG Chatbot and UI/UX

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for local Qdrant)
- Cohere API key (free tier available)
- Git

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up backend environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend environment:
```bash
cd frontend/docusaurus
npm install
```

4. Create environment files:
```bash
# backend/.env
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
NEON_DATABASE_URL=your-neon-database-url
COHERE_API_KEY=your-cohere-api-key
```

## Running Locally

1. Start the backend API:
```bash
cd backend
python -m src.api.main
```

2. In a separate terminal, start the Docusaurus frontend:
```bash
cd frontend/docusaurus
npm start
```

3. The textbook will be available at `http://localhost:3000`
4. The backend API will be available at `http://localhost:8000`

## Initial Setup

1. Populate the textbook content:
```bash
python -m src.cli.populate_textbook
```

2. Generate embeddings for the textbook content:
```bash
python -m src.cli.generate_embeddings
```

## Key Features

### Cohere-Powered RAG Chatbot
- Navigate to the textbook in your browser
- Use the enhanced chatbot interface to ask questions about the textbook content
- Verify that responses are based strictly on textbook content only
- Try the select-text → Ask AI functionality by selecting text and asking specific questions about it

### Animated UI/UX
- Experience engaging, animated elements throughout the textbook
- Animations are optimized for performance and won't impact page load times
- Interactive elements provide visual feedback to enhance learning

## API Endpoints

### Textbook API
- `GET /api/v1/textbook/chapters` - Get all textbook chapters
- `GET /api/v1/textbook/chapters/{chapterId}` - Get specific chapter
- `GET /api/v1/textbook/chapters/{chapterId}/blocks` - Get content blocks
- `GET /api/v1/textbook/chapters/{chapterId}/animated-elements` - Get animated UI elements
- `POST /api/v1/textbook/search` - Search textbook content

### Chat API
- `POST /api/v1/chat/start` - Start new chat session
- `POST /api/v1/chat/{sessionId}/query` - Send query to Cohere-powered chatbot
- `GET /api/v1/chat/cohere-config` - Get Cohere configuration

## Adding New Content

1. Add new chapters to `frontend/docusaurus/docs/`
2. Update `frontend/docusaurus/sidebars.js` to include navigation
3. Run the content population script: `python -m src.cli.populate_textbook`
4. Regenerate embeddings: `python -m src.cli.generate_embeddings`

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend/docusaurus
npm test
```

## Deployment

1. Build the Docusaurus site:
```bash
cd frontend/docusaurus
npm run build
```

2. Deploy the backend API to your preferred platform (ensure it meets free-tier constraints)

3. Serve the built Docusaurus site (e.g., via GitHub Pages, Netlify, or similar)

4. Configure environment variables for production deployment