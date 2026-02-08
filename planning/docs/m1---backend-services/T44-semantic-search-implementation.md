---
area: ingestion
dependsOn:
- T43
effort: 5
iteration: I3
key: T44
milestone: M1 - Backend Services
priority: p0
title: Semantic Search Implementation
type: Feature
---

# Semantic Search Implementation

## Acceptance Criteria

- [ ] **Semantic search API returns relevant results for natural language queries**
  - Verification: POST /api/v1/search with query 'dark fantasy novels with dragons' returns novels tagged with fantasy/dragon genres, measured by precision@10 > 0.7
- [ ] **Hybrid search combines semantic and text-based results effectively**
  - Verification: Search for exact title matches appear in top 3 results, while thematically similar content fills remaining positions
- [ ] **Search performance meets latency requirements**
  - Verification: 95th percentile response time < 500ms for queries with 1000+ indexed items, measured via load testing
- [ ] **Background embedding generation processes new content automatically**
  - Verification: New novels/comics get embeddings within 5 minutes of ingestion, verified by checking embedding_status in database
- [ ] **Vector storage and retrieval functions correctly**
  - Verification: pgvector similarity queries return expected nearest neighbors with cosine similarity scores, tested via direct database queries

## Technical Notes

### Approach

Implement a three-layer approach: (1) Embedding generation service that creates vectors for novel/comic content during ingestion, storing them in PostgreSQL with pgvector, (2) Search service that performs hybrid queries combining vector similarity (cosine distance) with traditional full-text search, and (3) Result fusion algorithm that ranks and merges results from both approaches. Include background workers for batch embedding generation and API endpoints for real-time search with proper caching and pagination.


### Files to Modify

- **path**: packages/database/src/schema.sql
- **changes**: Add embedding columns (vector(1536)) to novels and comics tables, create HNSW indexes
- **path**: apps/backend/src/server.ts
- **changes**: Register search routes and embedding worker scheduler
- **path**: packages/database/src/types.ts
- **changes**: Add embedding fields to Novel and Comic type definitions

### New Files to Create

- **path**: apps/backend/src/services/embedding.service.ts
- **purpose**: Generate and manage text embeddings using OpenAI API, handle batching and caching
- **path**: apps/backend/src/services/search.service.ts
- **purpose**: Implement hybrid semantic + text search with result fusion algorithms
- **path**: apps/backend/src/routes/search.ts
- **purpose**: RESTful search endpoints with pagination and filtering
- **path**: apps/backend/src/workers/embedding-indexer.ts
- **purpose**: Background worker to generate embeddings for newly ingested content
- **path**: packages/database/migrations/202401_add_vector_search.sql
- **purpose**: Database migration to add pgvector extension and embedding columns
- **path**: apps/backend/src/lib/search-fusion.ts
- **purpose**: Algorithm to merge and rank results from semantic and text search
- **path**: apps/backend/src/config/search.config.ts
- **purpose**: Search-specific configuration including OpenAI API keys and vector dimensions

### External Dependencies


- **openai** ^4.28.0

  - Generate text embeddings for semantic search

- **pgvector** ^0.5.0

  - PostgreSQL extension for vector similarity search

- **@fastify/schedule** ^2.0.0

  - Background job scheduling for embedding generation

- **postgres** ^3.4.0

  - Direct PostgreSQL queries for vector operations

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/embedding.service.test.ts`
  - Scenarios: Generate embeddings for novel metadata, Handle OpenAI API errors gracefully, Batch embedding requests efficiently, Cache embedding results
- **File**: `apps/backend/src/__tests__/services/search.service.test.ts`
  - Scenarios: Semantic search returns ranked results, Hybrid search merges vector and text results, Query preprocessing and expansion, Empty/invalid query handling
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/search-flow.test.ts`
  - Scenarios: End-to-end search from API to database, Background embedding worker processes queue, Database vector operations with pgvector
### Manual Testing


## Estimates

- **Development**: 4.5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 7.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup pgvector extension and create database migration
- **done**: False
- **task**: Implement embedding service with OpenAI integration
- **done**: False
- **task**: Create vector storage operations and HNSW indexes
- **done**: False
- **task**: Build hybrid search service with result fusion
- **done**: False
- **task**: Implement search API endpoints with pagination
- **done**: False
- **task**: Create background worker for embedding generation
- **done**: False
- **task**: Add comprehensive unit and integration tests
- **done**: False
- **task**: Performance testing and optimization
- **done**: False
- **task**: API documentation and usage examples
- **done**: False
- **task**: Code review and security audit
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Semantic search enables users to find novels, comics, and chapters using natural language queries rather than exact keyword matching. In the context of Morpheus, users should be able to search for "dark fantasy novels with dragons" or "romance stories set in medieval times" and get relevant results based on meaning rather than just text matching. This is crucial for content discovery as the platform scales, especially since novels and comics have rich descriptive metadata (genres, themes, character descriptions, plot summaries) that traditional search can't effectively utilize.

**Technical Approach:**
Implement vector-based semantic search using OpenAI's text-embedding-3-small model for generating embeddings, PostgreSQL's pgvector extension for vector storage and similarity search, and a hybrid approach combining semantic similarity with traditional text search (using PostgreSQL's full-text search). The architecture should include an embedding service for generating vectors, a search service with query expansion capabilities, and background jobs for indexing content as it's ingested.

**Dependencies:**
- External: [@supabase/supabase-js, openai, pgvector (PostgreSQL extension), @fastify/schedule for background jobs]
- Internal: Novel/Comic ingestion pipeline, Content metadata extraction service, Authentication service for user-specific search results

**Risks:**
- Embedding generation costs: OpenAI charges per token, could get expensive with large content volumes - mitigate by batching requests and caching embeddings
- Vector search performance: Large vector datasets can slow queries - mitigate with proper indexing (HNSW) and result pagination
- Embedding model changes: OpenAI model updates could invalidate existing vectors - mitigate by versioning embeddings and planning migration strategies
- Query latency: Vector similarity + traditional search could be slow - mitigate with proper database indexing and result caching

**Complexity Notes:**
More complex than initially estimated due to the hybrid search approach needed. Pure semantic search often misses exact matches users expect, so combining with traditional search requires careful result ranking and fusion algorithms. The embedding generation and storage pipeline also adds operational complexity for content updates.

**Key Files:**
- apps/backend/src/services/embedding.service.ts: Generate and manage embeddings
- apps/backend/src/services/search.service.ts: Hybrid search implementation
- apps/backend/src/routes/search.ts: Search API endpoints
- packages/database/migrations/: Add vector columns and indexes
- apps/backend/src/workers/embedding-indexer.ts: Background embedding generation


### Design Decisions

[{'decision': 'Use OpenAI text-embedding-3-small for embedding generation', 'rationale': 'Cost-effective, good performance for general text, integrates with existing OpenAI usage in the platform', 'alternatives_considered': ['Sentence Transformers (self-hosted)', 'Cohere embeddings', 'OpenAI text-embedding-3-large']}, {'decision': 'Implement hybrid search combining vector similarity with PostgreSQL full-text search', 'rationale': 'Pure semantic search can miss exact keyword matches that users expect, hybrid approach provides better user experience', 'alternatives_considered': ['Pure vector search', 'Elasticsearch with vector plugin', 'Pure PostgreSQL FTS']}, {'decision': 'Use Supabase/PostgreSQL with pgvector extension for vector storage', 'rationale': 'Keeps vector data co-located with relational data, reduces infrastructure complexity, leverages existing Supabase setup', 'alternatives_considered': ['Pinecone vector database', 'Weaviate', 'Qdrant']}]
