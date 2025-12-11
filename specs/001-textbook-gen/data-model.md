# Data Model: AI-Native Textbook with Enhanced RAG Chatbot and UI/UX

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

### ContentBlock
- **id**: string (UUID) - Unique identifier for each content block
- **chapter_id**: string - Reference to the textbook chapter
- **content**: string - The text content of the block
- **block_type**: string - Type of content (paragraph, code, heading, etc.)
- **position**: integer - Order within the chapter
- **embedding_id**: string - Reference to vector embedding in Qdrant

### UserQuery
- **id**: string (UUID) - Unique identifier for each query
- **query_text**: string - The original user query
- **selected_text**: string (optional) - Text selected by user for targeted questioning
- **user_id**: string (optional) - Identifier for the user (if tracking)
- **timestamp**: datetime - When the query was made
- **session_id**: string - Identifier for the chat session
- **language**: string - Language of the query (default: English)

### ChatResponse
- **id**: string (UUID) - Unique identifier for each response
- **query_id**: string - Reference to the original query
- **response_text**: string - The AI-generated response
- **source_chunks**: array<string> - IDs of source content blocks used to generate response
- **confidence_score**: float - Confidence level of the response (0-1)
- **created_at**: datetime - When the response was generated
- **is_hallucinated**: boolean - Flag if response was not based on textbook content

### KnowledgeEmbedding
- **id**: string (UUID) - Unique identifier for each embedding
- **content_block_id**: string - Reference to the source content block
- **chapter_id**: string - Reference to the textbook chapter
- **content_chunk**: string - The text chunk that was embedded
- **embedding_vector**: array<float> - The vector representation of the content
- **chunk_index**: integer - Position of the chunk within the chapter
- **metadata**: JSON - Additional metadata about the chunk

### ChatSession
- **id**: string (UUID) - Unique identifier for each session
- **user_id**: string (optional) - Identifier for the user (if tracking)
- **session_token**: string - Anonymous session identifier
- **created_at**: datetime - When the session started
- **updated_at**: datetime - Last interaction timestamp
- **is_active**: boolean - Whether the session is currently active
- **context_window**: array<JSON> - The conversation history

### AnimatedUIElement
- **id**: string (UUID) - Unique identifier for each animated element
- **element_type**: string - Type of animated element (tooltip, highlight, transition, etc.)
- **target_selector**: string - CSS selector for the target element
- **animation_type**: string - Type of animation (fade, slide, bounce, etc.)
- **trigger_event**: string - Event that triggers the animation
- **enabled**: boolean - Whether the animation is currently enabled
- **chapter_id**: string (optional) - Reference to specific chapter if applicable

### SelectedText
- **id**: string (UUID) - Unique identifier for each text selection
- **session_id**: string - Reference to the chat session
- **content_block_id**: string - Reference to the content block containing the selection
- **selected_text**: string - The actual selected text
- **start_position**: integer - Start position within the content block
- **end_position**: integer - End position within the content block
- **created_at**: datetime - When the selection was made

## Relationships

- TextbookChapter 1---* ContentBlock (One chapter has many content blocks)
- ContentBlock 1---* KnowledgeEmbedding (One content block has one embedding)
- TextbookChapter 1---* AnimatedUIElement (One chapter may have many animated elements)
- ChatSession 1---* UserQuery (One session has many queries)
- UserQuery 1---* ChatResponse (One query has one response)
- UserQuery 1---* SelectedText (One query may have selected text)
- UserQuery *---* KnowledgeEmbedding (One query may reference multiple embeddings via RAG)

## Validation Rules

- TextbookChapter.order must be between 1 and 6
- TextbookChapter.title and content cannot be empty
- UserQuery.query_text must be between 5 and 500 characters
- UserQuery.selected_text must not exceed 1000 characters to prevent large context windows
- KnowledgeEmbedding.embedding_vector must have consistent dimensions
- ChatSession context_window has maximum size of 20 messages to prevent memory issues
- ChatResponse.is_hallucinated must be validated against source_chunks to ensure accuracy
- SelectedText.start_position must be less than end_position

## State Transitions

N/A - All entities are immutable once created, representing snapshots of data at a point in time.