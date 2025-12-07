# Quickstart Guide: AI-Native Textbook with RAG Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional, for local Qdrant)
- Access to OpenAI API or compatible embeddings service

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
OPENAI_API_KEY=your-openai-api-key
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

## Testing the RAG Chatbot

1. Navigate to the textbook in your browser
2. Use the chatbot interface to ask questions about the textbook content
3. Verify that responses are based on the textbook content only

## Deployment

1. Build the Docusaurus site:
```bash
cd frontend/docusaurus
npm run build
```

2. Deploy the backend API to your preferred platform (ensure it meets free-tier constraints)

3. Serve the built Docusaurus site (e.g., via GitHub Pages, Netlify, or similar)