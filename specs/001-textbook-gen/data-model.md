# Data Model: AI-Native Textbook with RAG Chatbot

## Entities

### TextbookChapter
- **id**: string (UUID) - Unique identifier for each chapter
- **title**: string - Title of the chapter
- **content**: string - Full text content of the chapter
- **slug**: string - URL-friendly identifier
- **order**: integer - Chapter sequence number (1-6)
- **created_at**: datetime - Timestamp of creation
- **updated_at**: datetime - Timestamp of last update
- **metadata**: JSON - Additional chapter-specific metadata

### UserQuery
- **id**: string (UUID) - Unique identifier for each query
- **query_text**: string - The original user query
- **user_id**: string (optional) - Identifier for the user (if tracking)
- **timestamp**: datetime - When the query was made
- **session_id**: string - Identifier for the chat session
- **language**: string - Language of the query (default: English)

### KnowledgeEmbedding
- **id**: string (UUID) - Unique identifier for each embedding
- **chapter_id**: string - Reference to the textbook chapter
- **content_chunk**: string - The text chunk that was embedded
- **embedding_vector**: array<float> - The vector representation of the content
- **chunk_index**: integer - Position of the chunk within the chapter
- **metadata**: JSON - Additional metadata about the chunk

### ChatSession
- **id**: string (UUID) - Unique identifier for each session
- **user_id**: string (optional) - Identifier for the user (if tracking)
- **created_at**: datetime - When the session started
- **updated_at**: datetime - Last interaction timestamp
- **context_window**: array<JSON> - The conversation history

## Relationships

- TextbookChapter 1---* KnowledgeEmbedding (One chapter has many embeddings)
- ChatSession 1---* UserQuery (One session has many queries)
- UserQuery 1---* KnowledgeEmbedding (One query may reference multiple embeddings via RAG)

## Validation Rules

- TextbookChapter.order must be between 1 and 6
- TextbookChapter.title and content cannot be empty
- UserQuery.query_text must be between 5 and 500 characters
- KnowledgeEmbedding.embedding_vector must have consistent dimensions (1536 for OpenAI ada-002)
- ChatSession context_window has maximum size of 20 messages to prevent memory issues

## State Transitions

N/A - All entities are immutable once created, representing snapshots of data at a point in time.