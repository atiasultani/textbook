# Retrieval Strategy

Key Components:
- Embedding Model
- Vector Database
- Chunk Strategy
- Search Method

Chunking Best Practices:
- 500 to 1500 tokens recommended
- Overlap 50–150 tokens
- Preserve semantic meaning

Retrieval Methods:
- Cosine similarity
- Hybrid: BM25 + Vector Search
- Re-ranking for quality

Always retrieve:
- Top 3 to 8 chunks
- Remove duplicates
- Keep relevant only
