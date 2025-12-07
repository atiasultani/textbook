# Implementation Plan: AI-Native Textbook with RAG Chatbot

**Branch**: `001-textbook-gen` | **Date**: 2025-12-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-textbook-gen/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a Docusaurus-based textbook with 6 chapters on Physical AI and Humanoid Robotics, featuring an integrated RAG chatbot using Qdrant vector database and Neon for storage. The system will provide natural language search and Q&A capabilities based strictly on textbook content, with free-tier architecture constraints.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for Docusaurus
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant, Neon, OpenAI API (or compatible embeddings service), Pydantic
**Storage**: Neon PostgreSQL for metadata, Qdrant vector database for embeddings, Docusaurus static files
**Testing**: pytest for backend, Jest for frontend components
**Target Platform**: Web application (Linux server deployment, GitHub Pages compatible)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 second response time for RAG queries, <3 second page load times, support 100 concurrent users
**Constraints**: Free-tier compatible services only, minimal embeddings to reduce costs, no heavy GPU usage
**Scale/Scope**: 6 textbook chapters, thousands of users, educational content delivery

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**: Architecture uses minimal components (Docusaurus + FastAPI + Qdrant + Neon)
**Accuracy**: RAG answers will be strictly derived from textbook content (no hallucination)
**Minimalism**: Focus on core textbook and RAG functionality, avoiding feature bloat
**Fast Builds**: Docusaurus static site generation optimized for quick builds
**Free-tier Architecture**: All components (Qdrant Cloud free tier, Neon free tier, OpenAI API) compatible with free usage
**RAG Answers ONLY from Book Text**: Implementation will ensure strict content sourcing from textbook

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-gen/
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
│   ├── models/
│   │   ├── textbook.py
│   │   ├── chat.py
│   │   └── embeddings.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── qdrant_service.py
│   │   └── neon_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── textbook.py
│   │   │   ├── chat.py
│   │   │   └── search.py
│   │   └── main.py
│   └── config/
│       └── settings.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── docusaurus/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.jsx
│   │   │   ├── Search.jsx
│   │   │   └── TextbookContent.jsx
│   │   ├── pages/
│   │   └── css/
│   ├── docs/
│   │   ├── intro-physical-ai/
│   │   ├── basics-humanoid-robotics/
│   │   ├── ros-2-fundamentals/
│   │   ├── digital-twin-simulation/
│   │   ├── vision-language-action/
│   │   └── capstone/
│   ├── static/
│   ├── docusaurus.config.js
│   ├── sidebars.js
│   └── package.json
└── tests/
    └── e2e/
```

**Structure Decision**: Web application structure selected with separate backend (FastAPI) and frontend (Docusaurus) to maintain clean separation of concerns. The backend handles RAG operations and API, while Docusaurus frontend provides textbook UI with integrated chatbot component.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
