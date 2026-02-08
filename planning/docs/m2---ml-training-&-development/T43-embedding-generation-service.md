---
area: ml
dependsOn:
- T41
- T42
effort: 3
iteration: I3
key: T43
milestone: M2 - ML Training & Development
priority: p0
title: Embedding Generation Service
type: Task
---

# Embedding Generation Service

## Acceptance Criteria

- [ ] **Text embedding generation produces 3072-dimension vectors for novel content with <2s response time for single chapters**
  - Verification: POST /api/embeddings/text with chapter content returns vector array of length 3072 within 2000ms
- [ ] **Image embedding generation using CLIP models processes comic panels and stores results in pgvector**
  - Verification: POST /api/embeddings/image with comic panel returns embedding ID and SELECT from embeddings table shows stored vector
- [ ] **Batch processing queue handles full novel embedding (50+ chapters) without memory issues or rate limit failures**
  - Verification: POST /api/embeddings/batch with novel ID completes successfully and all chapters have embeddings in database
- [ ] **Vector similarity search returns relevant content with >0.8 cosine similarity for semantic queries**
  - Verification: GET /api/embeddings/search with query text returns ranked results with similarity scores >0.8
- [ ] **Redis caching reduces embedding lookup time by >50% for frequently accessed content**
  - Verification: Performance test shows cached embedding requests <100ms vs >200ms for uncached

## Technical Notes

### Approach

Create a dedicated embedding service in the Fastify backend that exposes REST endpoints for generating, storing, and querying text/image embeddings. Implement a job queue system for batch processing large novels while supporting real-time embedding generation for interactive features. Use Supabase's pgvector extension for efficient vector similarity search, with Redis caching for frequently accessed embeddings. Design the service to handle both OpenAI text embeddings and CLIP image embeddings from RunPod instances.


### Files to Modify

- **path**: apps/api/src/app.ts
- **changes**: Register embedding routes and initialize BullMQ connection
- **path**: packages/database/src/schema/index.ts
- **changes**: Add embeddings table schema with vector column and indexes
- **path**: packages/shared/src/types/index.ts
- **changes**: Export embedding types and API interfaces
- **path**: apps/api/src/config/index.ts
- **changes**: Add OpenAI, Anthropic, and RunPod API configuration

### New Files to Create

- **path**: apps/api/src/services/embedding/embedding-service.ts
- **purpose**: Core embedding generation service with OpenAI and CLIP integration
- **path**: apps/api/src/services/embedding/vector-store.ts
- **purpose**: Supabase pgvector operations and similarity search
- **path**: apps/api/src/services/embedding/cache-manager.ts
- **purpose**: Redis caching layer for embeddings and search results
- **path**: apps/api/src/services/embedding/embedding-queue.ts
- **purpose**: BullMQ job processor for batch embedding generation
- **path**: apps/api/src/routes/embeddings/index.ts
- **purpose**: REST API routes for embedding CRUD operations
- **path**: apps/api/src/routes/embeddings/text.ts
- **purpose**: Text embedding generation endpoints
- **path**: apps/api/src/routes/embeddings/image.ts
- **purpose**: Image embedding generation via RunPod
- **path**: apps/api/src/routes/embeddings/search.ts
- **purpose**: Vector similarity search endpoints
- **path**: apps/api/src/routes/embeddings/batch.ts
- **purpose**: Batch processing endpoints for novels
- **path**: packages/database/src/types/embedding.ts
- **purpose**: TypeScript types for embedding data structures
- **path**: packages/shared/src/ml/embedding-utils.ts
- **purpose**: Shared utilities for vector operations and preprocessing
- **path**: apps/api/src/middleware/rate-limit.ts
- **purpose**: Rate limiting middleware for embedding endpoints
- **path**: packages/database/migrations/20241201_create_embeddings_table.sql
- **purpose**: Database migration for embeddings table with pgvector support

### External Dependencies


- **@openai/openai** ^4.20.0

  - Text embedding generation for novel content

- **@anthropic-ai/anthropic-sdk** ^0.17.0

  - Alternative text embedding provider for redundancy

- **bullmq** ^4.15.0

  - Job queue for batch embedding processing

- **ioredis** ^5.3.0

  - Redis client for embedding cache and job queue

- **@tensorflow/tfjs-node** ^4.15.0

  - CLIP model inference for image embeddings

- **pgvector** ^0.1.8

  - PostgreSQL extension for vector similarity search

- **sharp** ^0.33.0

  - Image preprocessing before embedding generation

## Testing

### Unit Tests

- **File**: `apps/api/src/services/embedding/__tests__/embedding-service.test.ts`
  - Scenarios: Text embedding generation success, Image embedding processing, Cache hit/miss scenarios, Rate limit handling with exponential backoff, Vector storage and retrieval, Batch job creation and processing
- **File**: `apps/api/src/services/embedding/__tests__/vector-store.test.ts`
  - Scenarios: Vector insertion and similarity search, Embedding versioning and lifecycle, Database connection handling
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/embedding-flow.test.ts`
  - Scenarios: End-to-end text embedding to vector search, Novel batch processing pipeline, Cache integration with Redis, External API integration (OpenAI/RunPod)
- **File**: `apps/api/src/__tests__/integration/embedding-queue.test.ts`
  - Scenarios: BullMQ job processing and error handling, Concurrent embedding generation
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 1
- **Total**: 9

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup database schema and pgvector extension configuration
- **done**: False
- **task**: Implement core embedding service with OpenAI text-embedding-3-large integration
- **done**: False
- **task**: Create CLIP image embedding service with RunPod API integration
- **done**: False
- **task**: Build vector store service with Supabase pgvector operations
- **done**: False
- **task**: Implement Redis caching layer with configurable TTL and eviction policies
- **done**: False
- **task**: Create BullMQ job queue for batch processing with retry logic and monitoring
- **done**: False
- **task**: Build REST API endpoints with input validation and error handling
- **done**: False
- **task**: Implement rate limiting and exponential backoff for external APIs
- **done**: False
- **task**: Add comprehensive logging and monitoring for embedding operations
- **done**: False
- **task**: Create integration with content parsing service for novel processing pipeline
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The embedding generation service is crucial for Morpheus's ability to understand and process novel content semantically. This service will convert text chunks (chapters, scenes, character descriptions) and generated comic panels into high-dimensional vector representations that enable:
- Semantic search across novel content for comic panel generation
- Character consistency tracking across scenes
- Style transfer matching between text descriptions and visual outputs
- Content recommendation and similarity matching in the storefront
- Training data preparation for fine-tuning custom models

**Technical Approach:**
Implement a dedicated embedding microservice using Fastify that handles both text and image embeddings:
- Text embeddings: OpenAI text-embedding-3-large or Anthropic's embedding models for novel content
- Image embeddings: CLIP models via RunPod for generated comic panels
- Vector storage in Supabase using pgvector extension
- Batch processing queue for large novels using BullMQ
- Caching layer with Redis for frequently accessed embeddings
- RESTful API with streaming support for real-time embedding generation

**Dependencies:**
- External: @openai/openai, @anthropic-ai/anthropic-sdk, @supabase/supabase-js, bullmq, ioredis, @tensorflow/tfjs (for CLIP), sharp (image processing)
- Internal: Depends on content parsing service (T41), needs integration with novel processing pipeline, comic generation service will consume embeddings

**Risks:**
- Rate limiting from OpenAI/Anthropic APIs: implement exponential backoff and request queuing
- Vector storage costs scaling with content: implement embedding lifecycle management and archival
- CLIP model memory usage on RunPod: batch processing and memory monitoring
- Embedding drift affecting consistency: version embeddings and maintain model consistency

**Complexity Notes:**
Higher complexity than initially estimated due to multi-modal requirements (text + images) and the need for real-time + batch processing modes. The vector similarity search optimization and embedding versioning add significant architectural complexity.

**Key Files:**
- apps/api/src/services/embedding/: new service directory
- apps/api/src/routes/embeddings/: API routes for embedding CRUD
- packages/database/src/types/: embedding schema types
- packages/shared/src/ml/: shared ML utilities and types


### Design Decisions

[{'decision': 'Use hybrid embedding approach with OpenAI for text and CLIP for images', 'rationale': 'OpenAI embeddings excel at semantic text understanding while CLIP provides superior text-image alignment for comic generation consistency', 'alternatives_considered': ['Single model approach with multimodal transformers', 'Custom trained embeddings', 'Sentence transformers only']}, {'decision': 'Store embeddings in Supabase with pgvector for similarity search', 'rationale': 'Keeps vector data co-located with relational data, leverages existing Supabase infrastructure, and pgvector provides excellent performance for similarity queries', 'alternatives_considered': ['Dedicated vector DB like Pinecone', 'Redis with vector search', 'Elasticsearch with dense vectors']}]
