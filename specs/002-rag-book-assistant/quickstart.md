# Quickstart: Authenticated, Context-Locked RAG Book Assistant

## Overview
This guide provides quick setup instructions for the authenticated, context-locked RAG book assistant feature.

## Prerequisites
- Python 3.11+
- FastAPI
- Cohere Agents/ChatKit SDKs
- Neon PostgreSQL
- Qdrant vector database
- JWT authentication enabled

## Environment Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] cohere psycopg2-binary qdrant-client
```

2. Set up environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your values
COHERE_API_KEY=your_cohere_api_key
NEON_DATABASE_URL=your_neon_database_url
QDRANT_URL=your_qdrant_url
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/v1/chat` - Process user questions with RAG assistant

Example request:
```json
{
  "question": "What are the key principles of humanoid robotics?",
  "context": {
    "type": "retrieved-excerpt",
    "content": "Humanoid robotics involves creating robots with human-like characteristics...",
    "source_document_id": "intro-to-humanoid-robotics-chapter-1"
  },
  "mode": "rag-mode"
}
```

### Authentication Endpoint
- **POST** `/api/v1/auth/verify` - Verify authentication status

## Running the Service

1. Start the FastAPI server:
```bash
cd backend
uvicorn src.api.main:app --reload --port 8000
```

2. Test the endpoints:
```bash
# Test chat endpoint (with valid JWT token)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key principles?",
    "context": {
      "type": "retrieved-excerpt",
      "content": "The key principles include...",
      "source_document_id": "document-id"
    },
    "mode": "rag-mode"
  }'
```

## Key Features

1. **Authentication Required**: All chat requests must include a valid JWT token
2. **Context-Locked Responses**: Answers are strictly derived from provided context
3. **Anti-Hallucination**: System responds with "The provided text does not contain this information" when content is not available in context
4. **Dual Modes**: Supports both selection-restricted and RAG modes
5. **Response Validation**: All responses are validated to ensure they only contain context-based information

## Testing

Run the test suite:
```bash
pytest tests/unit/test_rag_service.py
pytest tests/integration/test_chat_endpoints.py
```

## Configuration

The service can be configured through environment variables in the `.env` file:
- `COHERE_API_KEY`: API key for Cohere integration
- `NEON_DATABASE_URL`: Connection string for Neon PostgreSQL
- `QDRANT_URL`: URL for Qdrant vector database
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `MAX_CONTEXT_LENGTH`: Maximum length of context content (default: 4096 characters)
- `RESPONSE_TIMEOUT`: Timeout for response generation (default: 30 seconds)