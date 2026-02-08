---
area: ml
dependsOn:
- T40
- T21
effort: 5
iteration: I3
key: T41
milestone: M2 - ML Training & Development
priority: p0
title: Scene Extraction Service
type: Feature
---

# Scene Extraction Service

## Acceptance Criteria

- [ ] **Service successfully processes novels of varying lengths (1K-100K words) and identifies scene boundaries with >80% accuracy against manually labeled test data**
  - Verification: Run automated test suite against labeled dataset: `npm test apps/ml-service/src/__tests__/scene-extraction-accuracy.test.ts`
- [ ] **API returns structured scene metadata including characters, setting, actions, dialogue, and mood with confidence scores for each field**
  - Verification: POST request to `/api/ml/scenes/extract` returns JSON with required fields and confidence scores 0-1
- [ ] **Service handles token limits gracefully by chunking large novels while preserving narrative context across boundaries**
  - Verification: Process 150K word novel and verify no scenes are lost at chunk boundaries, check logs for successful chunking
- [ ] **Scene extraction completes within 2 minutes per 10K words of input text**
  - Verification: Performance test measuring processing time: `npm run perf-test:scene-extraction`
- [ ] **All extracted scenes are properly stored in Supabase with correct relationships and indexing**
  - Verification: Query database after extraction to verify scene records, relationships, and run index performance tests

## Technical Notes

### Approach

Build a FastAPI-style service within the ML microservice that processes novel text in configurable chunks while preserving narrative context. Use LLM few-shot prompting to identify scene boundaries and extract structured metadata (characters, setting, actions, dialogue, mood). Implement confidence scoring based on boundary clarity and metadata completeness. Store extracted scenes with relationship mapping in Supabase, enabling efficient querying for comic generation pipeline.


### Files to Modify

- **path**: packages/database/src/schema.sql
- **changes**: Add scenes table, scene_metadata table, and indexes for novel_id and scene_order
- **path**: apps/ml-service/src/app.ts
- **changes**: Register scene extraction routes and middleware
- **path**: packages/shared/src/types/api.ts
- **changes**: Add SceneExtractionRequest and SceneExtractionResponse types

### New Files to Create

- **path**: apps/ml-service/src/services/scene-extraction.ts
- **purpose**: Core scene extraction service with LLM integration and chunking logic
- **path**: apps/ml-service/src/routes/scenes.ts
- **purpose**: REST API endpoints for scene extraction operations
- **path**: packages/database/src/types/scene.ts
- **purpose**: TypeScript types and Zod schemas for scene data models
- **path**: apps/ml-service/src/prompts/scene-detection.ts
- **purpose**: LLM prompt templates and few-shot examples for different genres
- **path**: apps/ml-service/src/utils/text-chunking.ts
- **purpose**: Smart text chunking with context preservation utilities
- **path**: apps/ml-service/src/services/confidence-scoring.ts
- **purpose**: Confidence scoring algorithms for scene boundaries and metadata
- **path**: apps/ml-service/src/config/extraction-config.ts
- **purpose**: Configuration for chunk sizes, token limits, and model parameters
- **path**: apps/ml-service/src/__tests__/fixtures/sample-novels.ts
- **purpose**: Test data with manually labeled scene boundaries for accuracy testing

### External Dependencies


- **@anthropic-ai/sdk** ^0.24.0

  - Primary LLM for scene analysis with strong instruction following

- **openai** ^4.20.0

  - Fallback LLM and embedding generation for scene similarity

- **natural** ^6.0.0

  - Text preprocessing, tokenization, and linguistic analysis

- **compromise** ^14.10.0

  - Named entity recognition for character and location extraction

- **tiktoken** ^1.0.10

  - Accurate token counting for LLM request optimization

## Testing

### Unit Tests

- **File**: `apps/ml-service/src/__tests__/services/scene-extraction.test.ts`
  - Scenarios: Single scene extraction with all metadata fields, Multi-scene novel processing, Edge cases: dialogue-heavy scenes, action sequences, flashbacks, Error handling: invalid text, API failures, token limits, Confidence scoring accuracy
- **File**: `apps/ml-service/src/__tests__/prompts/scene-detection.test.ts`
  - Scenarios: Prompt template generation with different genres, Few-shot example selection logic, Context window optimization
### Integration Tests

- **File**: `apps/ml-service/src/__tests__/integration/scene-extraction-flow.test.ts`
  - Scenarios: End-to-end: novel upload → scene extraction → database storage, API authentication and authorization, Batch processing workflow, Error recovery and retry logic
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

- **task**: Set up database schema and types for scene storage
- **done**: False
- **task**: Implement core text chunking with context preservation
- **done**: False
- **task**: Create LLM prompt templates for scene detection and metadata extraction
- **done**: False
- **task**: Build scene extraction service with confidence scoring
- **done**: False
- **task**: Implement REST API endpoints with proper validation
- **done**: False
- **task**: Add batch processing capabilities for large novels
- **done**: False
- **task**: Create comprehensive test suite with labeled datasets
- **done**: False
- **task**: Performance optimization and caching implementation
- **done**: False
- **task**: Integration testing with ML pipeline orchestrator
- **done**: False
- **task**: Documentation and API specification
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Scene Extraction Service is a critical ML component that automatically identifies and segments distinct narrative scenes from novel text. This solves the fundamental problem of breaking down long-form prose into visually coherent comic panels. Each extracted scene becomes a potential comic panel with its own visual composition, characters, and setting. This service provides the foundation for subsequent image generation and panel layout by creating structured scene metadata including dialogue, character positions, setting descriptions, and emotional tone.

**Technical Approach:**
Implement a multi-stage NLP pipeline using OpenAI/Anthropic LLMs for semantic scene understanding combined with rule-based text analysis. Use a hybrid approach: 1) Text preprocessing with paragraph/dialogue boundaries 2) LLM-based scene boundary detection using few-shot prompting 3) Scene metadata extraction (characters, setting, actions, mood) 4) Confidence scoring and human review flagging. Build as a dedicated microservice within the ML pipeline, exposing REST endpoints for batch and real-time processing. Store results in Supabase with proper indexing for scene relationships.

**Dependencies:**
- External: @anthropic-ai/sdk, openai, natural, compromise, tiktoken
- Internal: ML pipeline orchestrator, authentication service, database models for scenes/novels

**Risks:**
- LLM inconsistency: implement confidence scoring and fallback rules
- Scene boundary ambiguity: provide manual override interface
- Token limits with large novels: implement chunking with context preservation
- Cost explosion: implement caching and incremental processing

**Complexity Notes:**
More complex than initially estimated due to narrative structure variety across genres. Literary fiction requires different scene detection than action/romance. Need to handle flashbacks, dream sequences, and non-linear narratives. Consider this a P0 foundational service that other ML components depend on.

**Key Files:**
- apps/ml-service/src/services/scene-extraction.ts: core extraction logic
- apps/ml-service/src/routes/scenes.ts: API endpoints
- packages/database/src/types/scene.ts: scene data models
- apps/ml-service/src/prompts/scene-detection.ts: LLM prompt templates


### Design Decisions

[{'decision': 'Hybrid LLM + rule-based approach rather than pure ML', 'rationale': 'Provides deterministic fallbacks when LLMs fail, enables cost optimization through rule pre-filtering, and allows domain-specific customization per genre', 'alternatives_considered': ['Pure LLM approach', 'Traditional NLP only', 'Custom trained transformer model']}, {'decision': 'Scene confidence scoring with human review queue', 'rationale': 'Ensures quality control for ambiguous scenes while maintaining automation for clear boundaries, critical for downstream image generation accuracy', 'alternatives_considered': ['Fully automated with no review', 'Manual scene marking only']}, {'decision': 'Incremental processing with scene relationship tracking', 'rationale': 'Enables efficient re-processing when users edit novels, maintains narrative continuity context between scenes', 'alternatives_considered': ['Full reprocessing on changes', 'Stateless scene extraction']}]
