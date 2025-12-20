# RAG Architecture Knowledge

RAG = Retrieval Augmented Generation

Pipeline:
1️⃣ Receive user question
2️⃣ Convert to embedding
3️⃣ Retrieve top-k relevant chunks
4️⃣ Rank + filter results
5️⃣ Build context window
6️⃣ Generate answer using LLM
7️⃣ Provide citations if needed

Must:
- Reduce hallucination
- Provide factual responses
- Indicate uncertainty honestly

Supports:
- Document QA
- Knowledge bots
- Product chatbots
- Educational bots
