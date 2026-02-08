---
area: image-gen
dependsOn:
- T50
effort: 2
iteration: I4
key: T56
milestone: M3 - Content Generation Pipeline
priority: p1
title: Prompt Caching & Optimization
type: Task
---

# Prompt Caching & Optimization

## Acceptance Criteria

- [ ] **Cache hit rate of >70% for similar prompts (cosine similarity ≥0.85)**
  - Verification: Check analytics dashboard metrics after 100 test generations with 30% duplicate/similar prompts
- [ ] **Image generation response time reduced by >60% for cached results**
  - Verification: Performance tests showing <500ms response for cache hits vs >2s for API calls
- [ ] **Prompt optimization improves generation quality scores by >15%**
  - Verification: A/B test comparing raw vs optimized prompts using quality scoring endpoint
- [ ] **Cache storage remains under 10GB with TTL-based cleanup**
  - Verification: Monitor Redis memory usage and Supabase storage metrics over 7 days
- [ ] **System gracefully degrades when cache unavailable**
  - Verification: Manual Redis shutdown test - API continues working with direct generation

## Technical Notes

### Approach

Create a PromptCacheService that intercepts image generation requests, computes embeddings for semantic matching, and maintains a Redis-backed cache with Supabase persistence. The service will implement a three-tier lookup: exact hash match, semantic similarity within 0.85 threshold, then fallback to actual generation. Include a PromptOptimizer that standardizes language, adds quality enhancers, and validates against known problematic patterns before caching.


### Files to Modify

- **path**: apps/backend/src/routes/image-gen.ts
- **changes**: Integrate PromptCacheService before RunPod API calls, add cache status to response metadata
- **path**: apps/backend/src/lib/redis.ts
- **changes**: Add cache-specific Redis methods for hash storage, TTL management, and vector operations
- **path**: packages/database/src/migrations/001_initial.sql
- **changes**: Add cache metadata tables via new migration file
- **path**: apps/backend/src/config/index.ts
- **changes**: Add cache configuration (TTL, similarity threshold, size limits)

### New Files to Create

- **path**: apps/backend/src/services/image-gen/prompt-cache.service.ts
- **purpose**: Core caching logic with Redis/Supabase integration and semantic similarity matching
- **path**: apps/backend/src/services/image-gen/prompt-optimizer.service.ts
- **purpose**: Prompt preprocessing, standardization, and quality enhancement
- **path**: packages/database/src/schema/cache.sql
- **purpose**: Cache metadata tables (cache_entries, cache_stats, cache_embeddings)
- **path**: apps/backend/src/lib/embeddings.ts
- **purpose**: OpenAI embedding generation and cosine similarity calculations
- **path**: apps/backend/src/types/cache.types.ts
- **purpose**: TypeScript interfaces for cache entries, metadata, and configuration
- **path**: packages/database/src/migrations/012_cache_tables.sql
- **purpose**: Database migration for cache-related tables and indexes

### External Dependencies


- **ioredis** ^5.3.2

  - High-performance Redis client for Node.js with TypeScript support

- **openai** ^4.24.1

  - Generate text embeddings for semantic prompt similarity matching

- **ml-distance** ^4.0.1

  - Fast cosine similarity calculations for vector comparisons

- **hash-sum** ^2.0.0

  - Consistent hashing for exact prompt match detection

- **sharp** ^0.33.1

  - Image processing for cache thumbnail generation and optimization

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/prompt-cache.service.test.ts`
  - Scenarios: Exact hash match retrieval, Semantic similarity matching within threshold, Cache miss fallback to generation, TTL expiration handling, Redis connection failure, Invalid embedding responses
- **File**: `apps/backend/src/__tests__/services/prompt-optimizer.service.test.ts`
  - Scenarios: Prompt standardization and enhancement, Problematic content filtering, Quality enhancer injection, Character limit handling
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/image-gen-cache.test.ts`
  - Scenarios: Full generation pipeline with caching, Cache invalidation workflows, Supabase metadata persistence, OpenAI embedding integration
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 7

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Redis configuration and connection utilities
- **done**: False
- **task**: Create database schema and migration for cache tables
- **done**: False
- **task**: Implement OpenAI embeddings service with similarity calculations
- **done**: False
- **task**: Build PromptOptimizer service with standardization rules
- **done**: False
- **task**: Develop PromptCacheService with three-tier lookup logic
- **done**: False
- **task**: Integrate caching into existing image-gen route handlers
- **done**: False
- **task**: Add cache analytics and monitoring endpoints
- **done**: False
- **task**: Implement cache invalidation and cleanup jobs
- **done**: False
- **task**: Create comprehensive test suite with mocked dependencies
- **done**: False
- **task**: Performance testing and threshold tuning
- **done**: False

## Agent Notes

### Research Findings

**Context:**
In Morpheus's image generation pipeline, users frequently request similar visual content (character descriptions, scene compositions, art styles). Without caching, every generation hits RunPod's Stable Diffusion API, leading to unnecessary costs, slower response times, and potential rate limiting. Prompt caching optimizes this by storing generated images and reusing semantically similar prompts, while prompt optimization ensures we get the best possible outputs with minimal API calls.

**Technical Approach:**
Implement a multi-layered caching strategy:
1. **Exact Match Cache**: Hash-based storage for identical prompts using Redis
2. **Semantic Similarity Cache**: Vector embeddings (OpenAI text-embedding-ada-002) to find similar prompts within threshold
3. **Prompt Optimization**: Pre-processing pipeline to standardize, enhance, and validate prompts before generation
4. **Cache Invalidation**: TTL-based expiry with manual purging capabilities
5. **Supabase Integration**: Store cache metadata, usage stats, and image references in PostgreSQL

**Dependencies:**
- External: redis, ioredis, @supabase/supabase-js, openai, crypto, sharp
- Internal: image-gen service, database schemas, storage service, analytics pipeline

**Risks:**
- **Storage Costs**: Large image cache could inflate storage costs - mitigate with aggressive TTL and size limits
- **Cache Poisoning**: Bad generations cached permanently - implement quality scoring and manual review flags
- **Memory Leaks**: Vector embeddings consuming excessive RAM - use lazy loading and periodic cleanup
- **Consistency Issues**: Cache/DB sync problems - implement eventual consistency with reconciliation jobs

**Complexity Notes:**
This is more complex than initially estimated. Semantic similarity requires ML pipeline integration, vector storage, and similarity threshold tuning. The caching layer adds significant architectural complexity requiring careful error handling, fallback mechanisms, and monitoring.

**Key Files:**
- apps/backend/src/services/image-gen/prompt-cache.service.ts: Core caching logic
- apps/backend/src/services/image-gen/prompt-optimizer.service.ts: Prompt preprocessing
- apps/backend/src/lib/redis.ts: Redis connection and utilities
- packages/database/src/schema/cache.sql: Cache metadata tables
- apps/backend/src/routes/image-gen.ts: Integration with generation endpoints


### Design Decisions

[{'decision': 'Use Redis for hot cache + Supabase for metadata persistence', 'rationale': 'Redis provides sub-millisecond lookup for frequent requests, while Supabase handles durable storage, analytics, and complex queries', 'alternatives_considered': ['Pure PostgreSQL with materialized views', 'In-memory LRU cache only', 'External cache service (Elasticache)']}, {'decision': 'Implement semantic similarity using OpenAI embeddings with cosine similarity', 'rationale': 'Leverages existing OpenAI integration, provides good semantic understanding, and cosine similarity is computationally efficient', 'alternatives_considered': ['Local sentence transformers', 'Fuzzy string matching', 'Custom trained embeddings']}, {'decision': 'Cache final generated images, not intermediate states', 'rationale': 'Reduces storage complexity while maximizing reuse value for end users', 'alternatives_considered': ['Cache all pipeline steps', 'Cache only prompt embeddings', 'Cache generation parameters only']}]
