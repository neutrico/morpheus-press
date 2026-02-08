---
area: image-gen
dependsOn:
- T42
effort: 3
iteration: I4
key: T51
milestone: M3 - Content Generation Pipeline
priority: p0
title: Character Description Service
type: Feature
---

# Character Description Service

## Acceptance Criteria

- [ ] **Service extracts character descriptions from novel text with 90%+ accuracy**
  - Verification: Run test suite with sample novel chapters containing 20+ characters and verify extraction completeness
- [ ] **Character deduplication identifies same characters across chapters with <5% false positives**
  - Verification: Test with Harry Potter sample data - 'Harry', 'Harry Potter', 'the boy wizard' should merge to single profile
- [ ] **API responds to character lookup requests within 200ms for cached data**
  - Verification: Load test GET /api/characters/{id} endpoint with 100 concurrent requests
- [ ] **Generated character profiles include required fields: physical_description, personality_traits, relationships**
  - Verification: Validate API responses against Zod schema in packages/shared/src/types/character.types.ts
- [ ] **Character profiles maintain consistency across comic panel generation**
  - Verification: Generate 5 panels with same character and verify visual consistency using image similarity metrics

## Technical Notes

### Approach

Build a multi-stage pipeline: (1) Extract character mentions from novel text using LLM prompts, (2) Generate structured character profiles with physical descriptions, personality traits, and relationships, (3) Use vector embeddings to detect and merge duplicate characters across chapters, (4) Store normalized profiles in PostgreSQL with caching layer, (5) Provide REST API for image generation service to retrieve consistent character descriptions.


### Files to Modify

- **path**: packages/database/supabase/migrations/20241201000000_create_characters_tables.sql
- **changes**: Add characters, character_profiles, character_embeddings tables with indexes
- **path**: packages/shared/src/types/index.ts
- **changes**: Export character types for cross-package usage
- **path**: apps/dashboard/src/pages/characters/index.tsx
- **changes**: Add character management page with list, edit, merge functionality

### New Files to Create

- **path**: packages/api/src/services/character-description.service.ts
- **purpose**: Core service for character extraction, normalization, and deduplication
- **path**: packages/api/src/controllers/character.controller.ts
- **purpose**: REST API endpoints for character CRUD operations
- **path**: packages/api/src/lib/character-embeddings.ts
- **purpose**: Vector embedding utilities for character similarity detection
- **path**: packages/shared/src/types/character.types.ts
- **purpose**: TypeScript schemas and Zod validation for character data structures
- **path**: packages/api/src/events/character-events.ts
- **purpose**: Event handlers for character updates from novel processing pipeline
- **path**: packages/api/src/routes/characters.ts
- **purpose**: Express routes for character API endpoints
- **path**: apps/dashboard/src/components/character-editor/CharacterEditor.tsx
- **purpose**: React component for editing individual character profiles
- **path**: apps/dashboard/src/components/character-editor/CharacterMerge.tsx
- **purpose**: React component for merging duplicate character profiles
- **path**: packages/api/src/services/llm-prompts/character-extraction.ts
- **purpose**: Structured prompts for LLM-based character extraction

### External Dependencies


- **openai** ^4.28.0

  - GPT-4 for character extraction and description standardization

- **@anthropic-ai/sdk** ^0.17.0

  - Claude as fallback LLM for character analysis

- **zod** ^3.22.0

  - Runtime validation for character profile schemas

- **@supabase/vecs** ^0.2.0

  - Vector similarity search for character deduplication

- **ioredis** ^5.3.0

  - Caching frequently accessed character profiles

## Testing

### Unit Tests

- **File**: `packages/api/src/services/__tests__/character-description.service.test.ts`
  - Scenarios: Character extraction from novel text, Profile normalization and validation, Vector embedding generation, Cache hit/miss scenarios, Error handling for malformed input, LLM service failures
- **File**: `packages/api/src/controllers/__tests__/character.controller.test.ts`
  - Scenarios: CRUD operations via REST API, Query parameter validation, Authentication/authorization
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/character-pipeline.test.ts`
  - Scenarios: End-to-end novel processing to character extraction, Database persistence and retrieval, Cache layer integration, Event-driven character updates
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

- **task**: Create database schema and migrations for character storage
- **done**: False
- **task**: Implement TypeScript types and Zod schemas for character data
- **done**: False
- **task**: Build core CharacterDescriptionService with LLM integration
- **done**: False
- **task**: Implement vector embedding pipeline for character deduplication
- **done**: False
- **task**: Create REST API controllers and routes
- **done**: False
- **task**: Add Redis caching layer for character profiles
- **done**: False
- **task**: Build character management UI components
- **done**: False
- **task**: Integrate with novel processing pipeline via events
- **done**: False
- **task**: Connect character service to image generation pipeline
- **done**: False
- **task**: Write comprehensive test suites and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Character Description Service is a critical component for the image generation pipeline that extracts, standardizes, and maintains consistent character descriptions from novel text. This service ensures visual consistency across comic panels by providing detailed, structured character profiles that can be fed to Stable Diffusion models. Without this, generated characters would vary wildly between panels, breaking narrative immersion.

**Technical Approach:**
Implement as a dedicated service within the content generation pipeline using:
- LLM-based character extraction from novel chapters using structured prompts
- Character profile normalization and deduplication using vector embeddings
- PostgreSQL storage with JSONB fields for flexible character attributes
- Caching layer (Redis/Upstash) for frequently accessed character data
- Event-driven updates when new chapters are processed
- RESTful API with TypeScript schemas for type safety

**Dependencies:**
- External: openai@^4.28.0, @anthropic-ai/sdk@^0.17.0, @supabase/supabase-js@^2.39.0, zod@^3.22.0, ioredis@^5.3.0
- Internal: LLM service abstraction, novel processing pipeline, image generation service, database schemas

**Risks:**
- Character inconsistency: Implement semantic similarity checks and manual override capabilities
- LLM hallucination: Use structured prompts with examples and validation schemas
- Performance bottleneck: Cache character profiles and batch process multiple characters
- Storage bloat: Implement character profile versioning with cleanup policies

**Complexity Notes:**
More complex than initially estimated due to character deduplication challenges (same character described differently across chapters) and the need for semantic understanding of character relationships and variations.

**Key Files:**
- packages/api/src/services/character-description.service.ts: Core service implementation
- packages/database/migrations/: Character tables and indexes
- packages/shared/src/types/character.types.ts: TypeScript definitions
- apps/dashboard/src/components/character-editor/: Admin UI for character management


### Design Decisions

[{'decision': 'Use LLM-based extraction with structured prompts rather than NLP libraries', 'rationale': 'LLMs provide better context understanding for nuanced character descriptions and handle varied writing styles more effectively', 'alternatives_considered': ['spaCy/NLTK entity extraction', 'Rule-based pattern matching', 'Hybrid LLM + NLP approach']}, {'decision': 'Store character data as JSONB in PostgreSQL with semantic search via embeddings', 'rationale': 'Flexible schema for varied character attributes while maintaining ACID properties and enabling similarity searches for deduplication', 'alternatives_considered': ['Separate NoSQL database', 'Rigid relational schema', 'Vector database only']}]
