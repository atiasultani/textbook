---
description: "Task list for AI-Native Textbook with Enhanced RAG Chatbot and UI/UX implementation"
---

# Tasks: AI-Native Textbook with Enhanced RAG Chatbot and UI/UX

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
- [X] T002 Initialize Python project with Cohere Agents/ChatKit SDKs, FastAPI, Qdrant, Neon dependencies in backend/
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

## Phase 3: User Story 1 - Access Interactive Textbook Content with Enhanced UI (Priority: P1) 🎯 MVP

**Goal**: Students can access textbook content with attractive, animated UI elements and interact with Cohere-powered RAG chatbot to get explanations about specific concepts, including asking about selected text

**Independent Test**: Can access textbook chapters with animated UI elements and use the Cohere-powered RAG chatbot to answer questions about the content (including selected text), delivering immediate educational value with an engaging user experience.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create TextbookChapter model in backend/src/models/textbook.py
- [ ] T014 [P] [US1] Create ChatSession model in backend/src/models/chat.py
- [ ] T015 [P] [US1] Create UserQuery model with selected_text field in backend/src/models/chat.py
- [ ] T016 [P] [US1] Create ChatResponse model in backend/src/models/chat.py
- [ ] T017 [P] [US1] Create ContentBlock model in backend/src/models/textbook.py
- [ ] T018 [US1] Implement TextbookChapter service in backend/src/services/neon_service.py
- [X] T019 [US1] Implement Cohere service in backend/src/services/cohere_service.py
- [X] T020 [US1] Enhance RAG service to integrate with Cohere in backend/src/services/rag_service.py
- [ ] T021 [US1] Implement textbook API endpoints in backend/src/api/v1/textbook.py
- [X] T022 [US1] Implement Cohere API endpoints in backend/src/api/v1/cohere.py
- [X] T023 [US1] Enhance chat API endpoints to support Cohere integration in backend/src/api/v1/chat.py
- [X] T024 [US1] Create Chatbot component with enhanced UI in frontend/docusaurus/src/components/Chatbot.jsx
- [X] T025 [US1] Create TextSelection component for select-text functionality in frontend/docusaurus/src/components/TextSelection.jsx
- [X] T026 [US1] Create AnimatedUI component for engaging animations in frontend/docusaurus/src/components/AnimatedUI.jsx
- [X] T027 [US1] Integrate Chatbot and TextSelection components with textbook pages in frontend/docusaurus/
- [X] T028 [US1] Add validation and error handling for User Story 1

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Navigate Structured Learning Content with Engaging UI (Priority: P1)

**Goal**: Learners can navigate through a well-organized textbook with animated UI elements and chapters on Physical AI, Robotics, ROS 2, Digital Twins, and Vision-Language-Action Systems following a logical learning progression with sustained engagement

**Independent Test**: Can navigate through all chapters with animated UI elements and verify the logical flow and organization of content with engaging visual feedback, delivering a complete learning experience with enhanced visual appeal.

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create textbook content files for 6 chapters in frontend/docusaurus/docs/
- [ ] T030 [P] [US2] Generate content for Introduction to Physical AI chapter in frontend/docusaurus/docs/intro-physical-ai/
- [ ] T031 [P] [US2] Generate content for Basics of Humanoid Robotics chapter in frontend/docusaurus/docs/basics-humanoid-robotics/
- [ ] T032 [P] [US2] Generate content for ROS 2 Fundamentals chapter in frontend/docusaurus/docs/ros-2-fundamentals/
- [ ] T033 [P] [US2] Generate content for Digital Twin Simulation chapter in frontend/docusaurus/docs/digital-twin-simulation/
- [ ] T034 [P] [US2] Generate content for Vision-Language-Action Systems chapter in frontend/docusaurus/docs/vision-language-action/
- [ ] T035 [P] [US2] Generate content for Capstone chapter in frontend/docusaurus/docs/capstone/
- [ ] T036 [US2] Configure sidebar navigation to reflect 6-chapter structure with animations in frontend/docusaurus/sidebars.js
- [ ] T037 [US2] Implement navigation components with animations for textbook progression in frontend/docusaurus/src/components/
- [ ] T038 [US2] Add chapter ordering validation in backend/src/models/textbook.py
- [ ] T039 [US2] Create animation configuration for textbook chapters in frontend/docusaurus/src/animations/
- [ ] T040 [US2] Implement animated UI elements for enhanced engagement in frontend/docusaurus/src/components/

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Enhanced RAG Chatbot with Cohere Integration (Priority: P1)

**Goal**: Students can use an advanced RAG chatbot powered by Cohere Agents/ChatKit SDKs to search and query textbook content using natural language to quickly find relevant information and get detailed explanations about specific concepts

**Independent Test**: Can enter various search queries and verify that the Cohere-powered RAG system returns relevant textbook content with accurate answers, delivering efficient and reliable information retrieval.

### Implementation for User Story 3

- [ ] T041 [P] [US3] Create KnowledgeEmbedding model in backend/src/models/embeddings.py
- [ ] T042 [P] [US3] Implement Qdrant service in backend/src/services/qdrant_service.py
- [ ] T043 [US3] Implement search API endpoint with Cohere integration in backend/src/api/v1/search.py
- [ ] T044 [US3] Implement embedding generation service with Cohere compatibility in backend/src/services/rag_service.py
- [ ] T045 [US3] Create Search component with enhanced UI in frontend/docusaurus/src/components/Search.jsx
- [ ] T046 [US3] Integrate search functionality with textbook pages in frontend/docusaurus/
- [ ] T047 [US3] Add search result display with context and animations in frontend/docusaurus/src/components/
- [ ] T048 [US3] Implement Cohere configuration API endpoint in backend/src/api/v1/cohere.py
- [ ] T049 [US3] Add source attribution for Cohere responses in frontend components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Foundational Content & Integration

**Purpose**: Populate textbook content and generate embeddings to make RAG functionality complete

- [ ] T050 Populate textbook chapters with actual content in backend/src/
- [ ] T051 Generate embeddings for all textbook content in backend/src/
- [ ] T052 Implement content validation to ensure Cohere responses only from textbook content
- [ ] T053 Create CLI command to populate textbook content in backend/src/cli/
- [ ] T054 Create CLI command to generate embeddings in backend/src/cli/
- [ ] T055 Create CLI command to generate content blocks in backend/src/cli/

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T056 [P] Documentation updates in docs/
- [ ] T057 Code cleanup and refactoring
- [ ] T058 Performance optimization across all stories
- [ ] T059 [P] Additional unit tests in backend/tests/unit/ and frontend/docusaurus/tests/
- [ ] T060 Security hardening
- [ ] T061 Run quickstart.md validation
- [ ] T062 Animation performance optimization to ensure smooth experience

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
Task: "Create UserQuery model with selected_text field in backend/src/models/chat.py"

# Launch all components for User Story 1 together:
Task: "Create Chatbot component with enhanced UI in frontend/docusaurus/src/components/Chatbot.jsx"
Task: "Create TextSelection component for select-text functionality in frontend/docusaurus/src/components/TextSelection.jsx"
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