# Implementation Plan: Authenticated, Context-Locked RAG Book Assistant

**Branch**: `002-rag-book-assistant` | **Date**: 2025-12-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-rag-book-assistant/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an authenticated, context-locked RAG (Retrieval-Augmented Generation) book assistant that strictly responds to authenticated users with information derived only from provided book content. The system will verify user authentication status before processing requests, enforce context-only rules to prevent hallucination, and support both selection-restricted mode (user-selected text) and RAG mode (retrieved book excerpts). The assistant will respond with "Please sign in or create an account to use the chatbot" for unauthenticated requests and "The provided text does not contain this information" when answers aren't explicitly in the context.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Cohere Agents/ChatKit SDKs, Pydantic, Qdrant, Neon PostgreSQL
**Storage**: Neon PostgreSQL (metadata), Qdrant vector database (embeddings)
**Testing**: pytest with integration and unit tests
**Target Platform**: Linux server (backend API)
**Project Type**: web (backend API service for RAG chatbot)
**Performance Goals**: <5s response time for authenticated requests, handle 1000+ concurrent users
**Constraints**: Free-tier service compatibility, <200ms p95 latency for authentication checks, no external knowledge usage
**Scale/Scope**: 10k+ authenticated users, 1M+ book content chunks, multi-modal textbook integration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Compliance Verification

**I. Simplicity** ✅
- RAG chatbot will use straightforward architecture with clear request flow
- Authentication checks will be simple and direct
- Response generation will follow a linear process

**II. Accuracy** ✅
- System will strictly derive answers from provided book content only
- Anti-hallucination rules enforced in all responses
- Context-only rule prevents external knowledge usage

**III. Minimalism** ✅
- Focused on core RAG functionality without unnecessary features
- Minimal dependencies to maintain system efficiency
- Clean API endpoints for essential functionality only

**IV. Fast Builds** ✅
- Backend API will be lightweight with minimal dependencies
- Optimized for fast response times as specified in requirements

**V. Free-tier Architecture** ✅
- Using FastAPI, Neon PostgreSQL, and Qdrant - all free-tier compatible
- Architecture designed to work within free-tier limitations
- No heavy GPU usage as per constitution constraints

**VI. RAG Answers ONLY from Book Text** ✅
- System will strictly adhere to context-only rule
- Will respond with "The provided text does not contain this information" when content not available
- No external knowledge or hallucination allowed

**VII. Modern UI/UX Excellence** ✅
- Backend API designed to support frontend with animated UI elements
- Will provide clean, responsive interface for chat functionality

### Post-Design Compliance Verification

**I. Simplicity** ✅
- API endpoints are straightforward with clear request/response patterns
- Authentication middleware provides simple token validation
- Context validation service ensures clear separation of concerns

**II. Accuracy** ✅
- Data models enforce content validation at the schema level
- Response model includes confidence scoring and hallucination detection
- API contract specifies strict content validation requirements

**III. Minimalism** ✅
- Data models contain only essential fields for the feature
- API contract defines minimal but complete interface
- No unnecessary dependencies added to the system

**IV. Fast Builds** ✅
- Extended existing backend structure rather than creating new projects
- Leveraged existing FastAPI infrastructure for efficiency
- Caching strategies included for performance optimization

**V. Free-tier Architecture** ✅
- All specified technologies (FastAPI, Neon, Qdrant) remain free-tier compatible
- No new heavy dependencies introduced that would violate constraints
- Architecture maintains compatibility with free-tier service limits

**VI. RAG Answers ONLY from Book Text** ✅
- Context Content model enforces source document tracking
- Response model includes context_used field for verification
- API contract specifies content validation requirements

**VII. Modern UI/UX Excellence** ✅
- API contract supports frontend features needed for animated UI
- Response model includes metadata needed for rich UI experiences
- Authentication integration enables personalized user experiences

**CONCLUSION**: All constitutional requirements are satisfied by the implemented design approach.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-book-assistant/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── v1/
│   │       ├── chat.py          # New chat endpoints for RAG assistant
│   │       ├── auth.py          # Authentication endpoints
│   │       └── textbook.py      # Textbook content endpoints
│   ├── models/
│   │   ├── chat.py            # Chat session and message models
│   │   ├── textbook.py        # Textbook content models
│   │   └── embeddings.py      # Embedding models
│   ├── services/
│   │   ├── rag_service.py     # RAG assistant service
│   │   ├── neon_service.py    # Neon PostgreSQL service
│   │   ├── qdrant_service.py  # Qdrant vector database service
│   │   └── auth_service.py    # Authentication service
│   ├── config/
│   │   └── settings.py        # Configuration settings
│   └── cli/
│       └── populate_textbook.py # CLI tools for textbook management
├── tests/
│   ├── unit/
│   │   ├── test_chat.py
│   │   └── test_rag_service.py
│   └── integration/
│       └── test_chat_endpoints.py
├── requirements.txt
└── .env.example
```

**Structure Decision**: The existing backend structure is extended with new authentication and RAG services. The chat API will be enhanced to support the context-locked RAG assistant functionality while maintaining compatibility with existing textbook features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
