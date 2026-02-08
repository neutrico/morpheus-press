---
area: image-gen
dependsOn:
- T41
effort: 3
iteration: I4
key: T55
milestone: M3 - Content Generation Pipeline
priority: p1
title: Mood & Atmosphere Service
type: Feature
---

# Mood & Atmosphere Service

## Acceptance Criteria

- [ ] **Mood analysis extracts structured emotional tone, atmosphere, and visual descriptors from novel text with 90% consistency across identical inputs**
  - Verification: Run integration test with sample novel chapters, verify mood taxonomy fields populated correctly
- [ ] **Generated mood profiles integrate seamlessly with Stable Diffusion pipeline, producing visually consistent images that match extracted mood descriptors**
  - Verification: Generate 10 images from same mood profile, manually verify visual consistency and mood alignment
- [ ] **System maintains mood continuity across chapter boundaries with smooth transitions (mood drift < 20% between adjacent scenes)**
  - Verification: Process multi-chapter novel, measure mood similarity scores between consecutive chapters
- [ ] **Mood analysis performance stays under 2 seconds per chapter with Redis caching achieving 80% hit rate after initial analysis**
  - Verification: Load test with performance monitoring, check Redis metrics dashboard
- [ ] **Service handles failures gracefully with fallback to previous mood profiles and comprehensive error logging**
  - Verification: Simulate LLM API failures, verify image generation continues with cached mood data

## Technical Notes

### Approach

Build a mood analysis pipeline that processes novel chapters through LLM APIs to extract structured mood data using Zod schemas. Implement a hierarchical mood taxonomy that maps to Stable Diffusion prompt modifiers. Cache mood profiles in Redis with intelligent invalidation. Integrate as preprocessing step in existing image generation pipeline with fallback mechanisms for service failures.


### Files to Modify

- **path**: packages/image-gen/src/pipeline/image-generator.ts
- **changes**: Add mood preprocessing step, integrate mood descriptors into SD prompts
- **path**: packages/services/src/llm/llm-service.ts
- **changes**: Add mood analysis prompt templates and response parsing
- **path**: packages/db/src/schema/index.ts
- **changes**: Export mood profile schema definitions
- **path**: packages/api/src/routes/index.ts
- **changes**: Register mood service routes

### New Files to Create

- **path**: packages/services/src/mood/mood-analyzer.ts
- **purpose**: Core mood analysis service with LLM integration
- **path**: packages/services/src/mood/mood-taxonomy.ts
- **purpose**: Standardized mood descriptor system and SD prompt mapping
- **path**: packages/services/src/mood/mood-cache.ts
- **purpose**: Redis-based caching layer for mood profiles
- **path**: packages/services/src/mood/mood-interpolation.ts
- **purpose**: Smooth mood transitions between scenes/chapters
- **path**: packages/services/src/mood/types.ts
- **purpose**: TypeScript interfaces and Zod schemas for mood data
- **path**: packages/db/src/schema/mood-profiles.sql
- **purpose**: Database schema for mood profile persistence
- **path**: packages/image-gen/src/pipeline/mood-integration.ts
- **purpose**: Mood data integration with Stable Diffusion pipeline
- **path**: packages/api/src/routes/mood.ts
- **purpose**: REST endpoints for mood analysis operations
- **path**: packages/api/src/middleware/mood-validation.ts
- **purpose**: Request validation for mood service endpoints

### External Dependencies


- **openai** ^4.20.0

  - Primary LLM for mood analysis with structured output support

- **anthropic** ^0.7.0

  - Fallback LLM for mood analysis redundancy

- **redis** ^4.6.0

  - High-performance caching for mood profiles and analysis results

- **zod** ^3.22.0

  - Runtime validation of LLM-generated mood data structures

- **natural** ^6.7.0

  - Text preprocessing and sentiment analysis utilities

## Testing

### Unit Tests

- **File**: `packages/services/src/__tests__/mood/mood-analyzer.test.ts`
  - Scenarios: Text analysis with various mood types, Mood taxonomy mapping validation, Caching layer interactions, Error handling for malformed input, Mood interpolation calculations
- **File**: `packages/services/src/__tests__/mood/mood-taxonomy.test.ts`
  - Scenarios: Taxonomy validation and structure, Stable Diffusion prompt generation, Mood descriptor normalization
### Integration Tests

- **File**: `packages/services/src/__tests__/integration/mood-pipeline.test.ts`
  - Scenarios: End-to-end mood analysis pipeline, Redis caching and retrieval, Database persistence operations, LLM service integration, Image generation pipeline integration
- **File**: `packages/api/src/__tests__/integration/mood-endpoints.test.ts`
  - Scenarios: REST API mood analysis requests, Batch mood processing, Authentication and rate limiting
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

- **task**: Design mood taxonomy structure and validate with sample content
- **done**: False
- **task**: Implement core mood analyzer with LLM prompt engineering
- **done**: False
- **task**: Build Redis caching layer with intelligent invalidation
- **done**: False
- **task**: Create database schema and persistence layer
- **done**: False
- **task**: Integrate mood preprocessing into image generation pipeline
- **done**: False
- **task**: Implement mood interpolation for scene transitions
- **done**: False
- **task**: Build REST API endpoints with validation middleware
- **done**: False
- **task**: Write comprehensive test suites (unit + integration)
- **done**: False
- **task**: Performance testing and optimization
- **done**: False
- **task**: Documentation and API specs
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Mood & Atmosphere Service is critical for generating cohesive visual narratives in comics. It analyzes novel text to extract emotional tone, setting atmosphere, and visual mood descriptors that guide Stable Diffusion image generation. This ensures panels maintain consistent visual themes (dark/gritty, whimsical, romantic, etc.) and that character emotions are visually represented accurately. Without this service, generated images would lack narrative coherence and emotional depth.

**Technical Approach:**
- Implement a microservice architecture with mood analysis pipeline using LLM prompt engineering
- Create mood taxonomy system with standardized descriptors for Stable Diffusion
- Build context-aware analysis that considers chapter/scene continuity
- Use caching layer for mood profiles to optimize repeated generations
- Integrate with existing image-gen pipeline as preprocessing step
- Implement mood interpolation for smooth transitions between scenes

**Dependencies:**
- External: openai@^4.20.0, anthropic@^0.7.0, redis@^4.6.0, zod@^3.22.0
- Internal: LLM service wrapper, image generation pipeline, content analysis service, database models for mood persistence

**Risks:**
- Subjective interpretation: LLMs may interpret mood inconsistently - mitigate with structured prompts and validation
- Performance bottleneck: Real-time mood analysis could slow generation - mitigate with background processing and caching
- Mood drift: Long novels may have inconsistent atmosphere detection - mitigate with sliding window context analysis
- Cost escalation: Additional LLM calls increase operational costs - mitigate with intelligent caching and batching

**Complexity Notes:**
More complex than initially estimated due to need for contextual continuity tracking and mood taxonomy standardization. Requires sophisticated prompt engineering and validation systems.

**Key Files:**
- packages/services/src/mood/mood-analyzer.ts: Core mood analysis logic
- packages/services/src/mood/mood-taxonomy.ts: Standardized mood descriptors
- packages/db/src/schema/mood-profiles.sql: Mood persistence layer
- packages/image-gen/src/pipeline/mood-integration.ts: Integration with SD pipeline
- packages/api/src/routes/mood.ts: REST endpoints for mood operations


### Design Decisions

[{'decision': 'Use structured LLM prompts with Zod validation for mood extraction', 'rationale': 'Ensures consistent, type-safe mood data that integrates reliably with Stable Diffusion prompts', 'alternatives_considered': ['Pre-trained sentiment models', 'Rule-based mood detection', 'Hybrid ML approach']}, {'decision': 'Implement Redis-based mood profile caching with TTL', 'rationale': 'Reduces LLM API calls for repeated generations while allowing mood evolution updates', 'alternatives_considered': ['Database-only caching', 'In-memory caching', 'No caching']}, {'decision': 'Create hierarchical mood taxonomy (primary/secondary/tertiary)', 'rationale': 'Allows granular control over visual generation while maintaining simplicity for basic use cases', 'alternatives_considered': ['Flat mood tags', 'Emotion wheel mapping', 'Continuous mood vectors']}]
