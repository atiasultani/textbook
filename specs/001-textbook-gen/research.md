# Research: AI-Native Textbook with Enhanced RAG Chatbot and UI/UX

## Decision: Technology Stack Selection
**Rationale**: Selected Docusaurus + Cohere Agents/ChatKit SDKs + FastAPI + Qdrant + Neon based on free-tier availability, educational use case, and enhanced RAG requirements per updated constitution
**Alternatives considered**:
- Next.js + Express vs Docusaurus + FastAPI: Docusaurus is optimized for documentation sites with built-in features like sidebar navigation
- OpenAI API vs Cohere: Cohere was specifically required in updated constitution and offers competitive free tier
- Pinecone vs Qdrant: Qdrant offers a more generous free tier suitable for educational content
- PostgreSQL vs Neon: Neon provides serverless PostgreSQL with free tier and better integration for this use case

## Decision: Architecture Pattern
**Rationale**: Chose separate backend/frontend architecture to maintain clean separation of concerns. Backend handles RAG operations, Cohere integration and API services while frontend provides textbook UI with integrated chatbot, animated UI elements, and text selection functionality
**Alternatives considered**:
- Monolithic approach: Would mix concerns and make scaling harder
- Serverless functions: Would increase complexity and potentially costs

## Decision: AI Model Integration
**Rationale**: Using Cohere Agents/ChatKit SDKs instead of OpenAI API as specified in updated constitution. Cohere provides enterprise-grade language models with reliable performance and free tier compliance.
**Alternatives considered**:
- OpenAI API: Previously considered but replaced by Cohere per updated constitution
- Hugging Face Transformers: Self-hosted option but increases complexity beyond free-tier architecture
- Anthropic Claude: Another alternative but Cohere was specifically mentioned in constitution

## Decision: Embedding Strategy
**Rationale**: Using Cohere-compatible embeddings or Cohere's own embedding services for quality and consistency with the language model. Will implement minimal embedding strategy to stay within free tier limits.
**Alternatives considered**:
- OpenAI embeddings: No longer primary choice due to Cohere integration
- Local embeddings (SentenceTransformers): Would require more computational resources
- Cohere embeddings: Preferred for consistency with Cohere language model

## Decision: Content Structure
**Rationale**: Docusaurus docs structure with 6 chapters as specified in requirements, auto-generated sidebars for navigation
**Alternatives considered**:
- Custom content management: Would add unnecessary complexity for static textbook content

## Decision: RAG Implementation
**Rationale**: Using Qdrant vector database for semantic search with Cohere integration for response generation, with strict content sourcing from textbook to comply with constitution principle
**Alternatives considered**:
- Elasticsearch: More complex setup, not optimized for vector search
- Custom solution: Would violate simplicity principle

## Decision: Select-text → Ask AI Implementation
**Rationale**: Using JavaScript text selection APIs in the frontend to capture user selections and send to Cohere-powered backend for context-specific responses
**Technical approach**:
- Use window.getSelection() API to capture user text selections
- Pass selected text as context to Cohere API
- Ensure responses are strictly based on provided context to maintain accuracy principle

## Decision: Animated UI/UX Implementation
**Rationale**: Using CSS animations and React-based animation libraries like Framer Motion for complex interactions to achieve attractive UI while maintaining performance
**Constraints**: Animations must be lightweight to maintain fast page load times and not interfere with educational content readability.
**Alternatives considered**:
- Heavy JavaScript animations: Rejected due to performance impact
- GIFs/videos: Rejected due to file size and control limitations
- CSS animations: Chosen for performance and simplicity

## Decision: Cohere vs Qdrant Integration Strategy
**Rationale**: Maintain the Qdrant vector database for storing textbook embeddings while using Cohere for the language model responses. The RAG service will retrieve relevant textbook content from Qdrant and pass it to Cohere for response generation.
**Architecture**:
- Qdrant: Store and retrieve textbook content embeddings
- Cohere: Generate responses based on retrieved context
- Neon: Store metadata and session information