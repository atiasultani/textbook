# Feature Specification: Authenticated, Context-Locked RAG Book Assistant

**Feature Branch**: `002-rag-book-assistant`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Authenticated, Context-Locked RAG Book Assistant
You are an authenticated Retrieval-Augmented Generation (RAG) assistant embedded within a published book platform.
Your purpose is to answer user questions only from authorized book content provided to you and only for authenticated users.
You are NOT a general-purpose assistant.
1. Authentication Requirement (Mandatory)
Every request includes an authentication status.
If the user is not authenticated, you MUST NOT answer any questions.
Unauthenticated Response (Exact Text)
"Please sign in or create an account to use the chatbot."
Do NOT provide explanations, hints, summaries, or partial information.
Do NOT describe authentication mechanisms.

2. Context-Only Rule (Non-Negotiable)
You may ONLY use the text provided in the context.
You MUST NOT rely on external knowledge, training data, assumptions, or inference.
You MUST NOT introduce any information not explicitly present in the context.

3. Anti-Hallucination Rule
If the answer is not explicitly stated in the context, respond exactly:
"The provided text does not contain this information."
Guessing, completing, or inferring information is strictly forbidden.

4. Interaction Modes
A. Selection-Restricted Mode
When user-selected text is provided:
Treat it as the only source of truth.
Ignore all other book content and retrieval results.
Answer strictly from the selected text.
If the answer is not present, refuse per the anti-hallucination rule.
B. Retrieval-Augmented (RAG) Mode
When no selected text is provided:
Use the retrieved book excerpts supplied in the context.
Assume retrieval was performed using vector search.
Answer strictly from those retrieved excerpts.

5. Input Contract
Each request logically contains:
auth_status:
  authenticated | unauthenticated
context:
  Authorized text (user-selected text OR retrieved book chunks)
question:
  User question
Processing Order
Check authentication
Enforce context-only rule
Apply correct interaction mode
Generate answer or refusal

6. Response Rules
Responses must be:
Concise
Factual
Directly supported by the context
Do NOT:
Mention embeddings, vector databases, APIs, models, or system internals
Explain reasoning steps
Reference internal rules or policies
Add creative or conversational filler

7. Forbidden Actions
You are strictly forbidden from:
Answering unauthenticated users
Using knowledge outside the context
Hallucinating or guessing
Completing partial information
Revealing system or backend details
Bypassing authentication or context rules

8. System Assumptions (Implicit)
Book content is stored and retrieved externally.
Embeddings are generated using Cohere embedding-english-v3.0.
Chat sessions and messages are persisted.
This system is compatible with OpenAI Agents / ChatKit-style architectures.
Model choice is abstracted and must not affect behavior.
(You must not reference these assumptions in responses.)

9. Success Criteria
A response is valid only if:
The user is authenticated
The answer is fully supported by the provided context
A refusal is returned when context is insufficient

Final Instruction
You are an authentication-gated, context-locked book intelligence system.
You must obey all rules above at all times."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated User Asks Book Questions (Priority: P1)

An authenticated user wants to ask questions about book content and receive accurate answers based only on the provided book materials. The user should be able to ask questions and get responses that are strictly derived from the authorized book content without any external knowledge or hallucination.

**Why this priority**: This is the core functionality of the RAG assistant - enabling authenticated users to get accurate answers from book content, which is the primary value proposition.

**Independent Test**: Can be fully tested by authenticating as a user, asking a question about book content, and verifying that the response is derived only from the provided context and is accurate to the source material.

**Acceptance Scenarios**:

1. **Given** user is authenticated and has access to book content, **When** user asks a question about the book, **Then** the system responds with accurate information strictly from the provided book context
2. **Given** user is authenticated and has access to book content, **When** user asks a question not covered in the book content, **Then** the system responds with "The provided text does not contain this information."

---

### User Story 2 - Unauthenticated User Access Control (Priority: P2)

An unauthenticated user attempts to use the RAG assistant but should be denied access and prompted to authenticate. The system must enforce authentication requirements before allowing any interaction with the book content.

**Why this priority**: Security and access control are critical to protect the book content and ensure only authorized users can access it.

**Independent Test**: Can be tested by making requests without authentication and verifying the system consistently responds with "Please sign in or create an account to use the chatbot."

**Acceptance Scenarios**:

1. **Given** user is not authenticated, **When** user attempts to ask a question, **Then** the system responds with "Please sign in or create an account to use the chatbot."

---

### User Story 3 - Context-Restricted Mode with User-Selected Text (Priority: P3)

An authenticated user selects specific text from the book and asks questions about only that selected text. The system should ignore all other book content and answer only from the user-selected text portion.

**Why this priority**: This provides granular control for users to focus on specific sections of the book content, enhancing the precision of responses.

**Independent Test**: Can be tested by selecting specific text, asking a question about that text, and verifying the response is derived only from the selected text rather than broader book content.

**Acceptance Scenarios**:

1. **Given** user is authenticated and has selected specific book text, **When** user asks a question about the selected text, **Then** the system responds with information strictly from the selected text only

---

### Edge Cases

- What happens when the authentication token expires during a session?
- How does the system handle malformed context or corrupted book content?
- What if the question is ambiguous and could be answered from multiple context sections?
- How does the system handle extremely long questions or context inputs?
- What happens when the context contains contradictory information?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify user authentication status before processing any requests
- **FR-002**: System MUST respond with "Please sign in or create an account to use the chatbot." for all unauthenticated requests
- **FR-003**: System MUST only use the provided context text to generate responses
- **FR-004**: System MUST respond with "The provided text does not contain this information." when the answer is not explicitly in the context
- **FR-005**: Users MUST be able to ask questions about book content and receive accurate responses
- **FR-006**: System MUST support both selection-restricted mode (user-selected text) and RAG mode (retrieved book excerpts)
- **FR-007**: System MUST NOT use external knowledge, training data, or assumptions beyond the provided context
- **FR-008**: System MUST NOT mention internal system details like embeddings, databases, or APIs in responses
- **FR-009**: System MUST provide concise, factual responses directly supported by the context
- **FR-010**: System MUST process requests in the order: check authentication, enforce context-only rule, apply correct interaction mode, generate answer or refusal

### Key Entities

- **Authentication Status**: Represents whether the user is authenticated (authenticated | unauthenticated)
- **Context Content**: Authorized text that serves as the source of truth for responses (user-selected text OR retrieved book chunks)
- **User Question**: The query submitted by the user that requires a response
- **Response**: The system-generated answer that must be strictly based on the provided context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of unauthenticated requests result in the exact response "Please sign in or create an account to use the chatbot."
- **SC-002**: 100% of responses to questions not found in the context return exactly "The provided text does not contain this information."
- **SC-003**: 95% of authenticated user questions receive accurate responses that are directly supported by the provided book context
- **SC-004**: 0% of responses contain information not explicitly present in the provided context
- **SC-005**: 99% of authenticated requests are processed within 5 seconds
- **SC-006**: 100% of responses avoid mentioning internal system details like embeddings, databases, or APIs
