# Data Model: Authenticated, Context-Locked RAG Book Assistant

## Overview

This document defines the data models for the authenticated, context-locked RAG book assistant feature. The models support authentication verification, context management, and response generation while enforcing the context-only rule.

## Core Entities

### Authentication Status
Represents whether the user is authenticated (authenticated | unauthenticated)

**Fields:**
- `status`: Enum (authenticated | unauthenticated)
- `user_id`: Optional string (present when authenticated)
- `token`: Optional JWT token string
- `expires_at`: Optional datetime

**Validation:**
- If status is 'authenticated', user_id must be present
- Token must be valid JWT when present
- expires_at must be in the future when present

### Context Content
Authorized text that serves as the source of truth for responses (user-selected text OR retrieved book chunks)

**Fields:**
- `type`: Enum (user-selected | retrieved-excerpt)
- `content`: String (the actual text content)
- `source_document_id`: String (identifier for the source document)
- `section_reference`: Optional string (page number, chapter, etc.)
- `retrieval_metadata`: Optional object (confidence scores, relevance, etc.)

**Validation:**
- content must not be empty
- source_document_id must be valid reference
- type must be one of the defined enum values

### User Question
The query submitted by the user that requires a response

**Fields:**
- `id`: String (unique identifier)
- `question_text`: String (the actual question)
- `user_id`: String (identifier for the authenticated user)
- `timestamp`: DateTime (when the question was submitted)
- `context_id`: String (reference to the associated context content)

**Validation:**
- question_text must not be empty
- user_id must be valid authenticated user
- timestamp must be current or past
- context_id must reference valid context content

### Response
The system-generated answer that must be strictly based on the provided context

**Fields:**
- `id`: String (unique identifier)
- `answer_text`: String (the generated answer)
- `question_id`: String (reference to the associated question)
- `context_used`: String (the context that was used to generate the response)
- `confidence_score`: Float (0.0 to 1.0, how confident the system is in the response)
- `was_hallucinated`: Boolean (whether the response contained information not in the context)
- `timestamp`: DateTime (when the response was generated)

**Validation:**
- answer_text must not contain information not present in context_used
- confidence_score must be between 0.0 and 1.0
- was_hallucinated must be false if answer_text contains only context-based information

## Relationships

```
User Question (1) -> (1) Context Content
User Question (1) -> (1) Response
Authentication Status (1) -> (*) User Question
```

## State Transitions

### Authentication Status
- `unauthenticated` -> `authenticated`: When valid JWT token is provided
- `authenticated` -> `unauthenticated`: When token expires or is invalid

### Response Generation
- `pending` -> `processing`: When question is received and context is being analyzed
- `processing` -> `completed`: When response is generated from context
- `processing` -> `no-content`: When no relevant content is found in context
- `completed` -> `validated`: After response is verified to contain only context-based information

## API Request/Response Models

### Request Model
```python
class ChatRequest(BaseModel):
    question: str
    context: ContextContent
    auth_status: AuthenticationStatus
    mode: str  # "selection-restricted" | "rag-mode"
```

### Response Model
```python
class ChatResponse(BaseModel):
    answer: str
    status: str  # "success" | "no-content" | "unauthorized"
    context_used: Optional[str]
    timestamp: datetime
```

### Authentication Check Model
```python
class AuthCheckRequest(BaseModel):
    token: str

class AuthCheckResponse(BaseModel):
    authenticated: bool
    user_id: Optional[str]
    message: str
```