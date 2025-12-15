# Research: Authenticated, Context-Locked RAG Book Assistant

## Overview

This research document addresses the technical approach for implementing an authenticated, context-locked RAG book assistant that strictly responds to authenticated users with information derived only from provided book content.

## Authentication Implementation

### Decision: JWT-based authentication with middleware
### Rationale:
JWT tokens provide stateless authentication that works well with API services and can be easily validated on each request. This approach is compatible with the existing backend structure and provides good performance.

### Alternatives considered:
- Session-based authentication: Requires server-side storage and doesn't scale well
- API keys: Less secure and harder to manage for user-specific access
- OAuth: Overly complex for this use case

## RAG Service Architecture

### Decision: FastAPI service with Cohere integration
### Rationale:
The existing backend already uses FastAPI, so extending it with new endpoints maintains consistency. Cohere Agents/ChatKit SDKs are specified in the project constitution as required technology.

### Alternatives considered:
- OpenAI API: Constitution specifically mentions Cohere Agents/ChatKit SDKs
- Self-hosted models: Would violate free-tier architecture principle
- Alternative vector databases: Qdrant is already specified in constitution

## Context-Locking Implementation

### Decision: Context validation service that enforces content-only responses
### Rationale:
A dedicated service can validate that responses only contain information from the provided context, preventing hallucination and enforcing the context-only rule.

### Implementation approach:
- Pre-process responses to compare against source context
- Use similarity checking to ensure content alignment
- Return standard response when content not found in context

## Anti-Hallucination Strategy

### Decision: Rule-based validation with fallback response
### Rationale:
The requirements specifically state that when content is not in the context, the system must respond with "The provided text does not contain this information." This requires a rule-based approach rather than probabilistic methods.

### Implementation:
- Content matching algorithms to verify information comes from context
- Confidence thresholds to determine if information is sufficiently supported
- Strict fallback mechanism when content verification fails

## Interaction Modes Support

### Decision: Mode detection based on request context structure
### Rationale:
The system needs to support both selection-restricted mode (user-selected text) and RAG mode (retrieved book excerpts). This can be determined by the structure and source of the provided context in the request.

### Implementation:
- Check if context comes from user selection vs. retrieved excerpts
- Apply appropriate processing rules based on mode
- Maintain consistent response format across both modes

## Response Rules Compliance

### Decision: Response filtering middleware
### Rationale:
To ensure responses never mention internal system details like embeddings, databases, or APIs, implement a filtering mechanism that sanitizes responses before delivery.

### Implementation:
- Text analysis to detect internal system references
- Content replacement for any detected system details
- Validation that responses are concise and factual

## Performance Considerations

### Decision: Caching for authentication tokens and frequently accessed content
### Rationale:
To meet performance goals of <5s response time and <200ms p95 latency for authentication, implement strategic caching.

### Implementation:
- JWT token validation caching
- Frequently accessed book content caching
- Response caching for common queries