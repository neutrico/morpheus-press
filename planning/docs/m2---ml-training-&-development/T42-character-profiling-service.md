---
area: ml
dependsOn:
- T40
- T22
effort: 5
iteration: I3
key: T42
milestone: M2 - ML Training & Development
priority: p0
title: Character Profiling Service
type: Feature
---

# Character Profiling Service

## Acceptance Criteria

- [ ] **Character extraction accurately identifies and profiles at least 90% of major characters from novel text with physical descriptions, personality traits, and relationships**
  - Verification: Run character extraction on test novels and manually validate against ground truth dataset using `npm test character-profiling.accuracy.test.ts`
- [ ] **Character profile API endpoints support full CRUD operations with sub-200ms response times for profile retrieval**
  - Verification: Execute load tests with `k6 run packages/api/tests/load/character-endpoints.js` and verify 95th percentile < 200ms
- [ ] **Visual consistency validation achieves >0.8 CLIP similarity score between generated character images and stored profiles**
  - Verification: Generate test character images and run validation pipeline: `npm run test:character-validation` with minimum 0.8 similarity threshold
- [ ] **Character relationship mapping correctly identifies and stores character connections with 85% accuracy**
  - Verification: Test relationship extraction on annotated novel samples using `npm test character-relationships.test.ts`
- [ ] **System handles character alias resolution and consolidation without creating duplicate profiles**
  - Verification: Process novels with character aliases and verify single consolidated profile per character in database

## Technical Notes

### Approach

Build a multi-stage character profiling pipeline: (1) Extract character mentions and descriptions from novel text using OpenAI function calling, (2) Consolidate character references and resolve aliases using embedding similarity, (3) Generate comprehensive character profiles with physical descriptions, personality traits, and relationships, (4) Store profiles with vector embeddings for efficient retrieval, (5) Validate generated comic images against character profiles using CLIP similarity scoring.


### Files to Modify

- **path**: packages/database/prisma/schema.prisma
- **changes**: Add Character, CharacterRelationship, and CharacterEmbedding models with proper indexes
- **path**: packages/api/src/app.ts
- **changes**: Register character routes and middleware
- **path**: packages/ml/src/index.ts
- **changes**: Export character profiling service and related utilities

### New Files to Create

- **path**: packages/ml/src/services/character-profiling.service.ts
- **purpose**: Core character extraction, consolidation, and profiling logic
- **path**: packages/ml/src/services/character-validation.service.ts
- **purpose**: CLIP-based visual consistency validation for character images
- **path**: packages/ml/src/models/character.model.ts
- **purpose**: Character data structures, validation schemas, and embedding utilities
- **path**: packages/ml/src/utils/embedding.utils.ts
- **purpose**: Vector embedding generation and similarity calculation utilities
- **path**: packages/api/src/routes/characters.ts
- **purpose**: REST API endpoints for character CRUD operations
- **path**: packages/api/src/controllers/character.controller.ts
- **purpose**: Request handling and business logic for character operations
- **path**: packages/database/migrations/20241201000000_add_character_tables.sql
- **purpose**: Database schema for character profiles, relationships, and embeddings
- **path**: packages/dashboard/src/components/character-editor/CharacterProfile.tsx
- **purpose**: Character profile editing and visualization component
- **path**: packages/dashboard/src/components/character-editor/CharacterList.tsx
- **purpose**: Character listing and management interface
- **path**: packages/dashboard/src/pages/characters/index.tsx
- **purpose**: Main character management page
- **path**: packages/ml/src/prompts/character-extraction.prompt.ts
- **purpose**: LLM prompts for character extraction with few-shot examples

### External Dependencies


- **@openai/openai** ^4.20.0

  - LLM function calling for structured character extraction

- **@langchain/core** ^0.1.0

  - Text chunking and embedding management

- **@supabase/vecs** ^0.4.0

  - Vector similarity search for character matching

- **openai-clip** ^1.2.0

  - Visual-text similarity validation for character consistency

- **compromise** ^14.10.0

  - Natural language processing for entity extraction preprocessing

## Testing

### Unit Tests

- **File**: `packages/ml/src/services/__tests__/character-profiling.service.test.ts`
  - Scenarios: Character extraction from text passages, Profile consolidation and alias resolution, Embedding generation and similarity matching, Error handling for malformed input, Cache hit/miss scenarios
- **File**: `packages/ml/src/models/__tests__/character.model.test.ts`
  - Scenarios: Character data validation, Profile serialization/deserialization, Relationship mapping validation
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/character-profiling.test.ts`
  - Scenarios: End-to-end character extraction from novel upload to profile storage, Character profile retrieval with relationship data, Visual validation pipeline integration, Batch processing workflow
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2
- **Documentation**: 1
- **Total**: 12.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Design and implement database schema for characters, relationships, and embeddings
- **done**: False
- **task**: Build character extraction service with OpenAI function calling
- **done**: False
- **task**: Implement character consolidation and alias resolution using embeddings
- **done**: False
- **task**: Create CLIP-based visual validation service
- **done**: False
- **task**: Build REST API endpoints for character management
- **done**: False
- **task**: Develop character editor UI components
- **done**: False
- **task**: Implement caching layer with Redis for performance optimization
- **done**: False
- **task**: Create comprehensive test suite including accuracy validation
- **done**: False
- **task**: Write technical documentation and API specifications
- **done**: False
- **task**: Conduct code review and performance optimization
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Character Profiling Service is critical for consistent visual and narrative representation across comic panels. When transforming novels to comics, characters must maintain visual consistency, personality traits, and relationships throughout the story. This service extracts and maintains character profiles from source text, enabling consistent image generation and dialogue adaptation. Without this, characters would appear differently across panels, breaking immersion and narrative coherence.

**Technical Approach:**
Build a character extraction and profiling service using LLMs for text analysis and vector embeddings for character relationship mapping. Use OpenAI's function calling to extract structured character data (physical descriptions, personality traits, relationships). Store character profiles in Supabase with JSONB columns for flexible schema. Implement character embedding similarity search for consistent reference retrieval. Create a character validation service that checks generated images against stored profiles using CLIP embeddings.

**Dependencies:**
- External: @openai/openai, @supabase/supabase-js, @langchain/core, sentence-transformers (via Python bridge), sharp, canvas
- Internal: Novel parsing service, Image generation pipeline, Database schemas, Authentication service

**Risks:**
- Character extraction accuracy: Use few-shot prompting with validated examples and human-in-the-loop validation
- Inconsistent visual representation: Implement CLIP-based similarity scoring between generated images and reference descriptions
- Performance bottlenecks: Cache character profiles with Redis, batch process character extractions
- Storage costs: Compress character embeddings, use efficient vector storage strategies

**Complexity Notes:**
More complex than initially estimated. Requires sophisticated NLP for character relationship mapping, computer vision integration for visual consistency validation, and careful prompt engineering for accurate extraction. The interconnected nature of characters (relationships, mentions, aliases) adds significant complexity to the data modeling and retrieval systems.

**Key Files:**
- packages/ml/src/services/character-profiling.service.ts: Core character extraction logic
- packages/ml/src/models/character.model.ts: Character data structures and validation
- packages/database/migrations/: Character tables and indexes
- packages/api/src/routes/characters.ts: Character CRUD endpoints
- packages/dashboard/src/components/character-editor/: Character management UI


### Design Decisions

[{'decision': 'Use LLM function calling for structured character extraction', 'rationale': 'Provides consistent JSON output format and reduces parsing errors compared to prompt-only approaches', 'alternatives_considered': ['Regex-based extraction', 'Named entity recognition only', 'Custom fine-tuned models']}, {'decision': 'Store character profiles as JSONB in PostgreSQL with vector columns', 'rationale': 'Balances flexibility for evolving character schema with performance for similarity searches using pgvector', 'alternatives_considered': ['Pure vector database', 'Graph database', 'Document store']}, {'decision': 'Implement character visual consistency validation using CLIP embeddings', 'rationale': 'Enables automated quality assurance by comparing generated images to text descriptions', 'alternatives_considered': ['Manual validation only', 'Custom vision model', 'Style transfer approaches']}]
