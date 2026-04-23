# Advanced Retrieval + Context Engineering

This module upgrades the RAG system with **advanced retrieval strategies**:

- Hybrid retrieval (**FAISS + BM25**)
- Rank fusion using **Reciprocal Rank Fusion (RRF)**
- Cross-encoder **reranking**
- Chunk deduplication
- Structured context building for LLMs

---

## Architecture Diagram

```mermaid
sequenceDiagram
    participant User
    participant Hybrid
    participant Reranker
    participant Context

    User->>Hybrid: Query
    Hybrid->>Hybrid: Dense + BM25 Search
    Hybrid->>Hybrid: RRF Combine
    Hybrid->>Reranker: Top Results
    Reranker->>Reranker: Score pairs
    Reranker->>Context: Ranked Results
    Context->>User: Final Context
```

## Tasks Performed
- **Implemented hybrid retrieval (dense + BM25)**
- **Built RRF ranking mechanism**
- **Integrated cross-encoder reranker**
- **Added deduplication logic**
- **Built context construction**
- **Enabled source traceability**

## RRF Flow

```mermaid
graph TD
    A[Dense Results] --> C[Score Aggregation]
    B[BM25 Results] --> C
    C --> D[Combined Ranking]
```
```javascript
Rank Fusion (RRF)
score = score + weight * (1 / (k + rank))
```

## Learning Outcomes
- **Learned hybrid retrieval systems (semantic + keyword)**
- **Implemented Reciprocal Rank Fusion (RRF)**
- **Understood reranking with cross-encoders**
- **Implemented deduplication strategies**
- **Built traceableity**