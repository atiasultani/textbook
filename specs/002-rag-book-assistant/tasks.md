# Tasks: Authenticated, Context-Locked RAG Book Assistant

**Feature**: Authenticated, Context-Locked RAG Book Assistant
**Branch**: `002-rag-book-assistant`
**Input**: Feature specification from `/specs/002-rag-book-assistant/spec.md`

## Implementation Strategy

This feature implements an authenticated, context-locked RAG (Retrieval-Augmented Generation) book assistant that strictly responds to authenticated users with information derived only from provided book content. The implementation follows a phased approach with user stories in priority order (P1, P2, P3), where each phase builds on the previous one but remains independently testable.

**MVP Scope**: User Story 1 (authenticated users asking book questions) with basic authentication and RAG functionality.

## Dependencies

User stories follow priority order where:
- User Story 1 (P1) - Core RAG functionality for authenticated users
- User Story 2 (P2) - Authentication enforcement for all users
- User Story 3 (P3) - Context-restricted mode for selected text

User Story 2 is foundational and should be completed before User Story 1 for security reasons, though both are needed for full functionality.

## Parallel Execution Examples

Each user story phase can have parallel tasks for:
- [P] Model implementations (different files)
- [P] Service implementations (independent services)
- [P] Test implementations (independent test files)

## Phase 1: Setup

Setup tasks for project initialization and configuration.

- [X] T001 Create feature branch `002-rag-book-assistant` from main
- [X] T002 Update requirements.txt with new dependencies (cohere, python-jose, passlib)
- [X] T003 Create backend/src/models/chat.py with Pydantic models
- [X] T004 Create backend/src/models/textbook.py with textbook-related models
- [X] T005 Create backend/src/models/embeddings.py with embedding models
- [X] T006 Create backend/src/services/auth_service.py for JWT authentication
- [X] T007 Create backend/src/services/rag_service.py for RAG functionality
- [X] T008 Create backend/src/services/neon_service.py for database operations
- [X] T009 Create backend/src/services/qdrant_service.py for vector operations
- [X] T010 Create backend/src/api/v1/auth.py with authentication endpoints
- [X] T011 Create backend/src/api/v1/chat.py with chat endpoints
- [X] T012 Update backend/src/config/settings.py with new configuration

## Phase 2: Foundational

Foundational tasks that block all user stories.

- [X] T013 [P] Implement JWT authentication models in backend/src/models/chat.py
- [X] T014 [P] Implement context content models in backend/src/models/chat.py
- [X] T015 [P] Implement user question models in backend/src/models/chat.py
- [X] T016 [P] Implement response models in backend/src/models/chat.py
- [X] T017 [P] Implement authentication service in backend/src/services/auth_service.py
- [X] T018 [P] Implement JWT token validation functionality in backend/src/services/auth_service.py
- [X] T019 [P] Create authentication middleware in backend/src/services/auth_service.py
- [X] T020 [P] Update backend/src/config/settings.py with JWT configuration
- [X] T021 [P] Add JWT secret key to .env.example file
- [X] T022 [P] Create unit tests for authentication service in backend/tests/unit/test_auth_service.py
- [X] T023 Update backend/src/api/main.py to include new API routes
- [X] T024 Create authentication verification endpoint in backend/src/api/v1/auth.py

## Phase 3: User Story 2 - Unauthenticated User Access Control (Priority: P2)

Implement authentication enforcement for all users before core RAG functionality.

**Story Goal**: An unauthenticated user attempts to use the RAG assistant but should be denied access and prompted to authenticate. The system must enforce authentication requirements before allowing any interaction with the book content.

**Independent Test Criteria**: Can be tested by making requests without authentication and verifying the system consistently responds with "Please sign in or create an account to use the chatbot."

**Acceptance Scenarios**:
1. **Given** user is not authenticated, **When** user attempts to ask a question, **Then** the system responds with "Please sign in or create an account to use the chatbot."

- [X] T025 [US2] Implement authentication middleware to intercept all chat requests
- [X] T026 [US2] Create authentication check function that validates JWT tokens
- [X] T027 [US2] Implement 401 Unauthorized response with exact message for unauthenticated requests
- [X] T028 [US2] Add authentication verification endpoint to return authentication status
- [X] T029 [US2] Create unit tests for authentication middleware in backend/tests/unit/test_auth_service.py
- [X] T030 [US2] Create integration tests for unauthenticated requests in backend/tests/integration/test_chat_endpoints.py

## Phase 4: User Story 1 - Authenticated User Asks Book Questions (Priority: P1)

Implement core RAG functionality for authenticated users.

**Story Goal**: An authenticated user wants to ask questions about book content and receive accurate answers based only on the provided book materials. The user should be able to ask questions and get responses that are strictly derived from the authorized book content without any external knowledge or hallucination.

**Independent Test Criteria**: Can be fully tested by authenticating as a user, asking a question about book content, and verifying that the response is derived only from the provided context and is accurate to the source material.

**Acceptance Scenarios**:
1. **Given** user is authenticated and has access to book content, **When** user asks a question about the book, **Then** the system responds with accurate information strictly from the provided book context
2. **Given** user is authenticated and has access to book content, **When** user asks a question not covered in the book content, **Then** the system responds with "The provided text does not contain this information."

- [X] T031 [US1] Implement RAG service initialization in backend/src/services/rag_service.py
- [X] T032 [US1] Create context validation function to ensure responses only use provided context
- [X] T033 [US1] Implement Cohere integration for response generation in backend/src/services/rag_service.py
- [X] T034 [US1] Create anti-hallucination check function to validate response content
- [X] T035 [US1] Implement response generation that follows processing order: check authentication, enforce context-only rule, apply correct interaction mode, generate answer or refusal
- [X] T036 [US1] Create chat endpoint that processes authenticated user questions in backend/src/api/v1/chat.py
- [X] T037 [US1] Implement logic to return exact message "The provided text does not contain this information." when content not found
- [X] T038 [US1] Create unit tests for RAG service in backend/tests/unit/test_rag_service.py
- [X] T039 [US1] Create integration tests for authenticated chat requests in backend/tests/integration/test_chat_endpoints.py
- [X] T040 [US1] Create tests for anti-hallucination functionality in backend/tests/unit/test_rag_service.py

## Phase 5: User Story 3 - Context-Restricted Mode with User-Selected Text (Priority: P3)

Implement context-restricted mode for selected text.

**Story Goal**: An authenticated user selects specific text from the book and asks questions about only that selected text. The system should ignore all other book content and answer only from the user-selected text portion.

**Independent Test Criteria**: Can be tested by selecting specific text, asking a question about that text, and verifying the response is derived only from the selected text rather than broader book content.

**Acceptance Scenarios**:
1. **Given** user is authenticated and has selected specific book text, **When** user asks a question about the selected text, **Then** the system responds with information strictly from the selected text only

- [X] T041 [US3] Update RAG service to support selection-restricted mode in backend/src/services/rag_service.py
- [X] T042 [US3] Implement mode detection to distinguish between selection-restricted and RAG modes
- [X] T043 [US3] Create function to process user-selected text as exclusive context
- [X] T044 [US3] Update chat endpoint to handle mode parameter and route to appropriate processing logic
- [X] T045 [US3] Create unit tests for selection-restricted mode in backend/tests/unit/test_rag_service.py
- [X] T046 [US3] Create integration tests for selection-restricted functionality in backend/tests/integration/test_chat_endpoints.py

## Phase 6: Polish & Cross-Cutting Concerns

Final tasks for production readiness.

- [X] T047 Add comprehensive error handling for edge cases (token expiration, malformed context, etc.)
- [X] T048 Implement performance optimizations for response times under 5 seconds
- [X] T049 Add logging for authentication and RAG operations
- [X] T050 Create comprehensive integration tests covering all user stories
- [X] T051 Update API documentation with new endpoints
- [X] T052 Add input validation for all API endpoints
- [X] T053 Implement caching for frequently accessed content
- [X] T054 Add monitoring and metrics for authentication and RAG operations
- [X] T055 Create load testing for concurrent user scenarios
- [X] T056 Finalize security review of authentication implementation