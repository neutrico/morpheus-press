---
area: image-gen
dependsOn:
- T41
effort: 3
iteration: I4
key: T53
milestone: M3 - Content Generation Pipeline
priority: p0
title: Location & Environment Service
type: Feature
---

# Location & Environment Service

## Acceptance Criteria

- [ ] **Location extraction from novel text achieves >85% accuracy with confidence scoring**
  - Verification: Run test suite with annotated novel excerpts: npm run test:location-extraction -- --coverage
- [ ] **Environment consistency maintained across sequential panels with <0.3 embedding distance**
  - Verification: Integration test verifies similar scenes use consistent environments: npm run test:integration -- --grep 'environment consistency'
- [ ] **API responds within 200ms for cached locations and 2s for new extractions**
  - Verification: Load test endpoints: k6 run tests/performance/location-api.js
- [ ] **Generated prompts include location-specific details and pass safety validation**
  - Verification: Manual review of 20 generated prompts + automated safety checks in test suite
- [ ] **Service integrates seamlessly with image generation pipeline without breaking existing flows**
  - Verification: End-to-end test generates comic panel with location context: npm run test:e2e -- --spec comic-generation

## Technical Notes

### Approach

Implement a three-layer architecture: extraction layer using LLMs to parse locations from novel text, classification layer that categorizes and matches environments using vector embeddings, and generation layer that produces Stable Diffusion prompts with location-specific details. Use Supabase for persistent storage of location templates and scene continuity, Redis for caching frequently used environments, and integrate with the existing image generation pipeline through standardized prompt injection patterns.


### Files to Modify

- **path**: packages/image-gen/src/prompt-builders/base-prompt.builder.ts
- **changes**: Add location context injection methods and environment template integration
- **path**: packages/api/src/config/database.config.ts
- **changes**: Add Redis configuration for location caching
- **path**: packages/shared/src/types/index.ts
- **changes**: Export location-related type definitions

### New Files to Create

- **path**: packages/api/src/services/location-environment.service.ts
- **purpose**: Core service for location extraction, classification, and environment management
- **path**: packages/api/src/routes/locations/index.ts
- **purpose**: Route handler registration and middleware setup
- **path**: packages/api/src/routes/locations/locations.routes.ts
- **purpose**: RESTful endpoints for location CRUD operations
- **path**: packages/api/src/routes/locations/environments.routes.ts
- **purpose**: Environment template and preset management endpoints
- **path**: packages/shared/src/types/location.types.ts
- **purpose**: TypeScript interfaces for locations, environments, and scene continuity
- **path**: packages/database/supabase/migrations/20241201_create_locations_tables.sql
- **purpose**: Database schema for locations, environments, and scene tracking
- **path**: packages/api/src/utils/location-extractor.util.ts
- **purpose**: NLP utilities for parsing locations from text using LLMs
- **path**: packages/api/src/utils/environment-matcher.util.ts
- **purpose**: Vector embedding utilities for environment similarity matching
- **path**: packages/image-gen/src/prompt-builders/environment.builder.ts
- **purpose**: Location-aware prompt generation for Stable Diffusion
- **path**: packages/api/src/cache/location.cache.ts
- **purpose**: Redis caching layer for location analyses and environment data
- **path**: packages/api/src/validators/location.validators.ts
- **purpose**: Zod schemas for input validation and sanitization

### External Dependencies


- **compromise** ^14.10.0

  - Natural language processing for location entity extraction

- **ioredis** ^5.3.2

  - Redis client for caching location and environment data

- **sentence-transformers** ^1.0.0

  - Vector embeddings for location similarity matching

- **@xenova/transformers** ^2.17.1

  - Client-side transformer models for location classification

## Testing

### Unit Tests

- **File**: `packages/api/src/services/__tests__/location-environment.service.test.ts`
  - Scenarios: Location extraction from various text formats, Environment classification and matching, Confidence scoring accuracy, Cache hit/miss scenarios, Error handling for malformed input, LLM API failure graceful degradation
- **File**: `packages/api/src/routes/locations/__tests__/locations.routes.test.ts`
  - Scenarios: CRUD operations for locations, Bulk processing endpoints, Authentication and authorization, Input validation and sanitization
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/location-pipeline.test.ts`
  - Scenarios: Novel text to environment prompt generation flow, Redis caching integration, Supabase persistence and retrieval, Integration with prompt-engineering service
- **File**: `packages/image-gen/src/__tests__/integration/environment-prompts.test.ts`
  - Scenarios: Location-aware prompt injection, Environment consistency across panel sequence
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 8

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup database schema and migrations for locations/environments
- **done**: False
- **task**: Implement core LocationEnvironmentService with LLM integration
- **done**: False
- **task**: Create Redis caching layer for performance optimization
- **done**: False
- **task**: Build RESTful API endpoints with proper validation
- **done**: False
- **task**: Implement environment prompt builder for image generation
- **done**: False
- **task**: Integrate with existing prompt-engineering service
- **done**: False
- **task**: Add vector embedding system for environment matching
- **done**: False
- **task**: Write comprehensive test suite (unit + integration)
- **done**: False
- **task**: Performance testing and optimization
- **done**: False
- **task**: Documentation and API reference
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Location & Environment Service is critical for generating consistent, contextually appropriate comic panel backgrounds. When transforming novels to comics, the system needs to intelligently extract and manage location information from text, then generate appropriate visual environments that maintain consistency across panels. This solves the problem of having characters appear in random or inconsistent backgrounds, which breaks narrative flow. The service provides structured location data to the image generation pipeline, ensuring visual continuity and proper scene setting.

**Technical Approach:**
Build a TypeScript service that combines NLP for location extraction with a structured environment database. Use OpenAI/Anthropic LLMs for semantic location understanding and classification. Implement a caching layer with Redis for frequently used environments. Create a RESTful API with Fastify that serves location metadata to the image generation pipeline. Use Supabase for persistent storage of location templates, environment presets, and scene continuity tracking. Integrate with the existing prompt engineering system to inject location-specific details into Stable Diffusion prompts.

**Dependencies:**
- External: @supabase/supabase-js, openai, @anthropic-ai/sdk, natural, compromise, ioredis, zod
- Internal: prompt-engineering service, image-gen pipeline, novel-analysis service, database schemas

**Risks:**
- Location extraction accuracy: Implement confidence scoring and fallback to manual tagging
- Environment consistency drift: Use embedding-based similarity matching for related scenes  
- Performance bottlenecks: Cache location analyses and implement batching for bulk processing
- Prompt injection vulnerabilities: Sanitize all location descriptions before passing to LLMs

**Complexity Notes:**
This is more complex than initially apparent due to the need for semantic understanding of implicit locations (e.g., "the old oak tree where they first met" requires context memory). The service needs sophisticated NLP capabilities and state management for scene transitions. However, the modular architecture makes it manageable by separating extraction, classification, and generation concerns.

**Key Files:**
- packages/api/src/services/location-environment.service.ts: Core service implementation
- packages/api/src/routes/locations/: RESTful API endpoints
- packages/database/supabase/migrations/: Location and environment tables
- packages/shared/src/types/location.types.ts: TypeScript interfaces
- packages/image-gen/src/prompt-builders/environment.builder.ts: Location-aware prompt generation


### Design Decisions

[{'decision': 'Use hybrid NLP approach with LLM + rule-based extraction', 'rationale': 'LLMs provide semantic understanding while rule-based systems catch explicit location mentions reliably', 'alternatives_considered': ['Pure LLM approach', 'Pure NLP library approach', 'Manual annotation only']}, {'decision': 'Implement vector embeddings for location similarity matching', 'rationale': 'Enables intelligent environment reuse and consistency checking across similar scenes', 'alternatives_considered': ['Keyword matching', 'Manual categorization', 'No similarity matching']}, {'decision': 'Cache environment data in Redis with Supabase as source of truth', 'rationale': 'Balances performance with data persistence for frequently accessed location metadata', 'alternatives_considered': ['Pure database approach', 'In-memory only', 'File-based caching']}]
