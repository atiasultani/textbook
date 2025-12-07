---
description: "Task list for AI-Native Textbook with RAG Chatbot implementation"
---

# Tasks: AI-Native Textbook with RAG Chatbot

**Input**: Design documents from `/specs/001-textbook-gen/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/docusaurus/`
- Paths shown below based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend and frontend directories
- [X] T002 Initialize Python project with FastAPI, Qdrant, Neon dependencies in backend/
- [X] T003 [P] Initialize Docusaurus project in frontend/docusaurus/
- [ ] T004 [P] Configure linting and formatting tools for Python and JavaScript
- [X] T005 Create initial directory structures per plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Setup Neon database schema and migrations framework in backend/
- [ ] T007 [P] Configure Qdrant collection for knowledge embeddings
- [X] T008 [P] Setup API routing and middleware structure in backend/src/api/main.py
- [X] T009 Create base models/entities that all stories depend on in backend/src/models/
- [X] T010 Configure error handling and logging infrastructure in backend/src/
- [X] T011 Setup environment configuration management in backend/src/config/
- [X] T012 [P] Create Docusaurus configuration with auto sidebar in frontend/docusaurus/docusaurus.config.js

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Interactive Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Students can access textbook content and interact with RAG chatbot to get explanations about specific concepts

**Independent Test**: Can access textbook chapters and use the RAG chatbot to answer questions about the content, delivering immediate educational value.

### Implementation for User Story 1

- [X] T013 [P] [US1] Create TextbookChapter model in backend/src/models/textbook.py
- [X] T014 [P] [US1] Create ChatSession model in backend/src/models/chat.py
- [X] T015 [P] [US1] Create UserQuery model in backend/src/models/chat.py
- [X] T016 [US1] Implement TextbookChapter service in backend/src/services/neon_service.py
- [X] T017 [US1] Implement RAG service in backend/src/services/rag_service.py
- [X] T018 [US1] Implement textbook API endpoints in backend/src/api/v1/textbook.py
- [X] T019 [US1] Implement chat API endpoints in backend/src/api/v1/chat.py
- [X] T020 [US1] Create Chatbot component in frontend/docusaurus/src/components/Chatbot.jsx
- [X] T021 [US1] Integrate Chatbot component with textbook pages in frontend/docusaurus/
- [X] T022 [US1] Add validation and error handling for User Story 1

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Navigate Structured Learning Content (Priority: P1)

**Goal**: Learners can navigate through a well-organized textbook with chapters on Physical AI, Robotics, ROS 2, Digital Twins, and Vision-Language-Action Systems following a logical learning progression

**Independent Test**: Can navigate through all chapters and verify the logical flow and organization of content, delivering a complete learning experience.

### Implementation for User Story 2

- [X] T023 [P] [US2] Create textbook content files for 6 chapters in frontend/docusaurus/docs/
- [X] T024 [P] [US2] Generate content for Introduction to Physical AI chapter in frontend/docusaurus/docs/intro-physical-ai/
- [X] T025 [P] [US2] Generate content for Basics of Humanoid Robotics chapter in frontend/docusaurus/docs/basics-humanoid-robotics/
- [X] T026 [P] [US2] Generate content for ROS 2 Fundamentals chapter in frontend/docusaurus/docs/ros-2-fundamentals/
- [X] T027 [P] [US2] Generate content for Digital Twin Simulation chapter in frontend/docusaurus/docs/digital-twin-simulation/
- [X] T028 [P] [US2] Generate content for Vision-Language-Action Systems chapter in frontend/docusaurus/docs/vision-language-action/
- [X] T029 [P] [US2] Generate content for Capstone chapter in frontend/docusaurus/docs/capstone/
- [X] T030 [US2] Configure sidebar navigation to reflect 6-chapter structure in frontend/docusaurus/sidebars.js
- [X] T031 [US2] Implement navigation components for textbook progression in frontend/docusaurus/src/components/
- [X] T032 [US2] Add chapter ordering validation in backend/src/models/textbook.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search and Query Textbook Content (Priority: P2)

**Goal**: Students can search and query the textbook content using natural language to quickly find relevant information and get detailed explanations about specific concepts

**Independent Test**: Can enter various search queries and verify that the RAG system returns relevant textbook content, delivering efficient information retrieval.

### Implementation for User Story 3

- [X] T033 [P] [US3] Create KnowledgeEmbedding model in backend/src/models/embeddings.py
- [X] T034 [P] [US3] Implement Qdrant service in backend/src/services/qdrant_service.py
- [X] T035 [US3] Implement search API endpoint in backend/src/api/v1/search.py
- [X] T036 [US3] Implement embedding generation service in backend/src/services/rag_service.py
- [X] T037 [US3] Create Search component in frontend/docusaurus/src/components/Search.jsx
- [X] T038 [US3] Integrate search functionality with textbook pages in frontend/docusaurus/
- [X] T039 [US3] Add search result display with context in frontend/docusaurus/src/components/

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Foundational Content & Integration

**Purpose**: Populate textbook content and generate embeddings to make RAG functionality complete

- [X] T040 Populate textbook chapters with actual content in backend/src/
- [X] T041 Generate embeddings for all textbook content in backend/src/
- [X] T042 Implement content validation to ensure RAG answers only from textbook content
- [X] T043 Create CLI command to populate textbook content in backend/src/cli/
- [X] T044 Create CLI command to generate embeddings in backend/src/cli/

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Documentation updates in docs/
- [X] T046 Code cleanup and refactoring
- [ ] T047 Performance optimization across all stories
- [ ] T048 [P] Additional unit tests in backend/tests/unit/ and frontend/docusaurus/tests/
- [X] T049 Security hardening
- [X] T050 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Content & Integration (Phase 6)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members
- Models within a story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create TextbookChapter model in backend/src/models/textbook.py"
Task: "Create ChatSession model in backend/src/models/chat.py"
Task: "Create UserQuery model in backend/src/models/chat.py"

# Launch all components for User Story 1 together:
Task: "Create Chatbot component in frontend/docusaurus/src/components/Chatbot.jsx"
Task: "Implement textbook API endpoints in backend/src/api/v1/textbook.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Complete Content & Integration → Full RAG functionality
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3] labels map task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence