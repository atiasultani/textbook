# Research: AI-Native Textbook with RAG Chatbot

## Decision: Technology Stack Selection
**Rationale**: Selected Docusaurus + FastAPI + Qdrant + Neon based on free-tier availability, educational use case, and RAG requirements
**Alternatives considered**:
- Next.js + Express vs Docusaurus + FastAPI: Docusaurus is optimized for documentation sites with built-in features like sidebar navigation
- Pinecone vs Qdrant: Qdrant offers a more generous free tier suitable for educational content
- PostgreSQL vs Neon: Neon provides serverless PostgreSQL with free tier and better integration for this use case

## Decision: Architecture Pattern
**Rationale**: Chose separate backend/frontend architecture to maintain clean separation of concerns. Backend handles RAG operations while frontend provides textbook UI
**Alternatives considered**:
- Monolithic approach: Would mix concerns and make scaling harder
- Serverless functions: Would increase complexity and potentially costs

## Decision: Embedding Strategy
**Rationale**: Using OpenAI embeddings or compatible service (like Azure OpenAI) for quality and simplicity. Will implement minimal embedding strategy to stay within free tier limits
**Alternatives considered**:
- Local embeddings (SentenceTransformers): Would require more computational resources
- Alternative providers: OpenAI has the best documentation and reliability for educational use

## Decision: Content Structure
**Rationale**: Docusaurus docs structure with 6 chapters as specified in requirements, auto-generated sidebars for navigation
**Alternatives considered**:
- Custom content management: Would add unnecessary complexity for static textbook content

## Decision: RAG Implementation
**Rationale**: Using Qdrant vector database for semantic search with strict content sourcing from textbook to comply with constitution principle
**Alternatives considered**:
- Elasticsearch: More complex setup, not optimized for vector search
- Custom solution: Would violate simplicity principle