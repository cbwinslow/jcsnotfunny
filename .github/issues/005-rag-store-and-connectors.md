# RAG store & index connectors (FAISS local + managed)

Summary

Provide a robust approach for storing transcript embeddings and supporting retrieval for RAG workflows: local FAISS index with JSON fallback, and optional connectors for managed vector stores (Pinecone, Weaviate). Provide CLI to build and query indexes.

Acceptance criteria (measurable)

- Implement local FAISS index creation from transcript sentences and store an ids->metadata mapping JSON.
- Add an adapter layer and config allowing users to select `faiss` or `pinecone` or `weaviate` with clear environment variable docs.
- Add unit tests that build a small index from sample transcripts and assert NN lookup returns expected nearest sentence for a query.

Subtasks / microgoals

- Implement `scripts/rag/indexer.py` with `build_index` and `query_index` functions.
- Add CLI `scripts/rag/cli.py` and tests (`tests/test_rag_indexer.py`).
- Add docs for configuring Pinecone / Weaviate and migration guide.

Labels: type/automation, area/editing, priority/medium

Estimate: 2–4 days
