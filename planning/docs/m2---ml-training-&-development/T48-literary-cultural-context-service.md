---
area: ml
dependsOn:
- T40
effort: 5
iteration: I3
key: T48
milestone: M2 - ML Training & Development
priority: p2
title: Literary Cultural Context Service
type: Feature
---

# Literary Cultural Context Service

## Acceptance Criteria

- [ ] **Cultural context service successfully analyzes novel text and extracts structured cultural metadata including time period, geographical setting, cultural references, and literary genre**
  - Verification: POST /api/novels/:id/analyze-context returns structured JSON with cultural_period, geographical_context, literary_genre, and cultural_references fields populated
- [ ] **Service processes novel text in chunks with 90%+ accuracy for major cultural markers (time period, location, genre)**
  - Verification: Run test suite with sample novels from different eras/cultures, verify extracted metadata against ground truth with accuracy >= 90%
- [ ] **Integration with ML pipeline completes end-to-end with cultural metadata flowing to visual generation**
  - Verification: Redis pub/sub message 'cultural-analysis-complete' triggers visual pipeline with cultural context payload, verified in ml-pipeline logs
- [ ] **Service handles concurrent novel processing with rate limiting and progress tracking**
  - Verification: Submit 5 novels simultaneously, verify all complete within 10 minutes with progress updates via WebSocket, no rate limit errors
- [ ] **Cultural bias validation rejects or flags potentially biased/inaccurate cultural interpretations**
  - Verification: Test with novels containing sensitive cultural content, verify validation layer flags or corrects misinterpretations in cultural_validation_notes field

## Technical Notes

### Approach

Build a staged analysis pipeline that processes novel text in overlapping chunks, extracts cultural markers through LLM prompting, validates results against knowledge bases, and generates structured metadata. Use async queue processing to handle multiple novels concurrently while managing API rate limits. Integrate with existing novel processing workflow through event-driven architecture.


### Files to Modify

- **path**: apps/ml/src/services/ml-pipeline.service.ts
- **changes**: Add cultural context integration, subscribe to Redis cultural-analysis-complete events
- **path**: apps/backend/src/routes/novels/index.ts
- **changes**: Add route handlers for cultural context endpoints, WebSocket upgrade handling
- **path**: packages/shared/src/types/novel.types.ts
- **changes**: Extend Novel interface with cultural_context field and metadata structure
- **path**: apps/ml/src/config/redis.config.ts
- **changes**: Add cultural context pub/sub channel configurations

### New Files to Create

- **path**: apps/ml/src/services/cultural-context.service.ts
- **purpose**: Main orchestration service for cultural analysis pipeline with LLM integration
- **path**: apps/ml/src/analyzers/literary-analyzer.ts
- **purpose**: Core NLP analysis logic for genre classification and literary device detection
- **path**: apps/ml/src/analyzers/cultural-validator.ts
- **purpose**: Cultural bias detection and validation against knowledge bases
- **path**: packages/shared/src/types/cultural-context.ts
- **purpose**: TypeScript interfaces for cultural metadata, analysis results, and API contracts
- **path**: apps/backend/src/routes/novels/context.ts
- **purpose**: REST API endpoints for cultural analysis requests and status checking
- **path**: apps/ml/src/processors/text-segmenter.ts
- **purpose**: Sliding window text segmentation with overlap handling for context preservation
- **path**: apps/ml/src/utils/cultural-knowledge.ts
- **purpose**: Integration with external cultural and historical knowledge APIs for validation
- **path**: apps/ml/src/queues/cultural-analysis.queue.ts
- **purpose**: Bull queue processor for async cultural analysis with progress tracking

### External Dependencies


- **@anthropic-ai/sdk** ^0.17.0

  - Primary LLM for cultural and literary analysis

- **natural** ^6.0.0

  - Text processing utilities for tokenization and NLP preprocessing

- **compromise** ^14.0.0

  - Natural language understanding for entity extraction

- **country-list** ^2.3.0

  - Standardized country/culture identification

- **date-fns** ^3.0.0

  - Historical date parsing and normalization

## Testing

### Unit Tests

- **File**: `apps/ml/src/__tests__/cultural-context.service.test.ts`
  - Scenarios: Text segmentation with sliding window, NER extraction for places and dates, Genre classification accuracy, LLM prompt engineering edge cases, Cultural bias detection, Error handling for API failures
- **File**: `apps/ml/src/__tests__/literary-analyzer.test.ts`
  - Scenarios: Literary device identification, Historical context scoring, Cultural reference validation, Batch processing logic
### Integration Tests

- **File**: `apps/ml/src/__tests__/integration/cultural-pipeline.test.ts`
  - Scenarios: End-to-end novel text to cultural metadata pipeline, Redis pub/sub integration with ML queue, Database persistence of cultural context, WebSocket progress updates
- **File**: `apps/backend/src/__tests__/integration/context-api.test.ts`
  - Scenarios: REST API endpoints for cultural analysis, Authentication and authorization, Rate limiting behavior
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

- **task**: Set up project structure and install dependencies (@anthropic-ai/sdk, openai, natural, compromise)
- **done**: False
- **task**: Implement text segmentation service with sliding window approach and context overlap
- **done**: False
- **task**: Build literary analyzer with NER, genre classification, and cultural reference extraction
- **done**: False
- **task**: Create cultural validation layer with bias detection and knowledge base cross-referencing
- **done**: False
- **task**: Implement main cultural context service with LLM orchestration and prompt engineering
- **done**: False
- **task**: Set up Redis pub/sub integration and Bull queue for async processing with progress tracking
- **done**: False
- **task**: Build REST API endpoints with authentication, rate limiting, and WebSocket support
- **done**: False
- **task**: Integrate with existing ML pipeline and database schema updates
- **done**: False
- **task**: Implement comprehensive test suite including cultural sensitivity test cases
- **done**: False
- **task**: Performance optimization, caching strategy, and API rate limit management
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Literary Cultural Context Service analyzes novels to extract cultural, historical, and literary context that influences visual adaptation decisions. When converting novels to comics, understanding the cultural setting, time period, literary genre conventions, and thematic elements is crucial for generating appropriate visual styles, character designs, and scene compositions. This service feeds contextual metadata to the visual generation pipeline, ensuring cultural authenticity and genre-appropriate artistic choices.

**Technical Approach:**
Implement a multi-stage NLP pipeline using LLMs for cultural analysis:
1. Text segmentation and context extraction using sliding window approach
2. Named Entity Recognition for places, time periods, cultural references
3. Genre classification and literary device identification
4. Cultural context scoring and metadata generation
5. Integration with existing ML pipeline through Redis pub/sub
Built as a microservice within the ML workspaces, exposing REST + WebSocket APIs

**Dependencies:**
- External: @anthropic-ai/sdk, openai, natural, compromise, date-fns, country-list
- Internal: shared/types, ml/text-processor, ml/analysis-queue, database/novel-metadata

**Risks:**
- Cultural bias in LLM responses: Implement validation against cultural knowledge bases
- High token consumption: Use caching and batch processing strategies
- Latency impact on novel processing: Implement async processing with progress tracking
- Accuracy of historical context: Cross-reference with structured historical data APIs

**Complexity Notes:**
More complex than initially estimated due to need for cultural sensitivity validation and integration with multiple knowledge sources. Requires careful prompt engineering and result validation.

**Key Files:**
- apps/ml/src/services/cultural-context.service.ts: Main service implementation
- apps/ml/src/analyzers/literary-analyzer.ts: Core analysis logic
- packages/shared/src/types/cultural-context.ts: Type definitions
- apps/backend/src/routes/novels/context.ts: API endpoint integration


### Design Decisions

[{'decision': 'Use Anthropic Claude for cultural analysis with OpenAI as fallback', 'rationale': 'Claude shows better performance on nuanced cultural and literary analysis tasks', 'alternatives_considered': ['OpenAI GPT-4 only', 'Hybrid ensemble approach', 'Fine-tuned local model']}, {'decision': 'Implement sliding window text analysis with overlap', 'rationale': 'Preserves context across chunk boundaries while managing token limits', 'alternatives_considered': ['Chapter-based analysis', 'Full text analysis', 'Sentence-level processing']}, {'decision': 'Cache cultural context results in Redis with novel content hash', 'rationale': 'Expensive LLM operations should be cached, hash ensures cache invalidation on content changes', 'alternatives_considered': ['Database caching', 'Memory-only caching', 'No caching']}]
