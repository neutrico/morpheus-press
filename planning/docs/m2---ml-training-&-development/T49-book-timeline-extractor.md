---
area: ml
dependsOn:
- T41
effort: 3
iteration: I3
key: T49
milestone: M2 - ML Training & Development
priority: p2
title: Book Timeline Extractor
type: Feature
---

# Book Timeline Extractor

## Acceptance Criteria

- [ ] **Timeline extractor processes novels in streaming chunks and extracts chronological events with 90%+ accuracy on test corpus**
  - Verification: Run test suite with sample novels, verify extracted events match manually annotated timelines
- [ ] **System handles novels up to 500MB with <16GB memory usage and provides progress updates every 30 seconds**
  - Verification: Load test with large novels, monitor memory usage with htop, verify WebSocket progress events
- [ ] **Background job processing completes within 2x estimated time and recovers from failures**
  - Verification: Submit timeline extraction jobs via API, verify completion and retry behavior in job queue dashboard
- [ ] **API endpoints return proper responses with timeline data and validation errors**
  - Verification: Test POST /books/:id/timeline and GET /books/:id/timeline endpoints with curl/Postman
- [ ] **Timeline coherence validation catches 95% of inconsistent temporal references**
  - Verification: Test with novels containing timeline inconsistencies, verify validation layer flags them

## Technical Notes

### Approach

Build a streaming timeline extraction service that processes novels in configurable chunks (2000-4000 tokens). Each chunk gets analyzed by LLM for key events, then correlated with spaCy's temporal and entity extraction. Events are stored with timestamps, character references, and confidence scores in PostgreSQL. A validation layer ensures timeline coherence by cross-referencing extracted events. The service integrates with the existing job queue for background processing and provides real-time progress updates via WebSocket connections to the dashboard.


### Files to Modify

- **path**: packages/database/src/schema/index.ts
- **changes**: Export timeline table schemas and types
- **path**: apps/api/src/config/openai.ts
- **changes**: Add timeline extraction prompts and model configurations
- **path**: apps/api/src/middleware/validation.ts
- **changes**: Add timeline request validation schemas
- **path**: apps/api/src/routes/books/index.ts
- **changes**: Import and mount timeline routes
- **path**: apps/api/src/jobs/index.ts
- **changes**: Register timeline extraction job handlers

### New Files to Create

- **path**: packages/database/src/schema/timelines.sql
- **purpose**: Database schema for timeline events, metadata, and processing status
- **path**: apps/api/src/services/ml/timeline-extractor.ts
- **purpose**: Core timeline extraction service with streaming and LLM integration
- **path**: apps/api/src/services/ml/timeline-validator.ts
- **purpose**: Timeline coherence validation and event correlation logic
- **path**: apps/api/src/services/ml/text-chunker.ts
- **purpose**: Intelligent text chunking with context preservation
- **path**: apps/api/src/routes/books/timeline.ts
- **purpose**: REST API endpoints for timeline extraction and retrieval
- **path**: apps/api/src/jobs/timeline-extraction.ts
- **purpose**: Background job processing for timeline extraction
- **path**: apps/api/src/types/timeline.ts
- **purpose**: TypeScript types and Zod schemas for timeline data
- **path**: apps/api/src/utils/temporal-parser.ts
- **purpose**: Utility functions for parsing temporal expressions with date-fns

### External Dependencies


- **spacy** ^3.7.0

  - Advanced NLP for named entity recognition, temporal expressions, and linguistic analysis

- **tiktoken** ^1.0.0

  - Accurate token counting for LLM API calls and chunk size management

- **date-fns** ^3.0.0

  - Robust temporal expression parsing and timeline sequencing

- **zod** ^3.22.0

  - Runtime validation for timeline event schemas and LLM response parsing

## Testing

### Unit Tests

- **File**: `apps/api/src/services/ml/__tests__/timeline-extractor.test.ts`
  - Scenarios: Chunk processing with valid novel text, Event extraction and temporal parsing, Error handling for malformed text, Memory management and streaming, LLM response parsing and validation
- **File**: `apps/api/src/services/ml/__tests__/timeline-validator.test.ts`
  - Scenarios: Timeline coherence validation, Event correlation and deduplication, Confidence score calculation
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/timeline-extraction.test.ts`
  - Scenarios: End-to-end timeline extraction flow, Database persistence and retrieval, Job queue integration, WebSocket progress updates
- **File**: `apps/api/src/__tests__/integration/timeline-api.test.ts`
  - Scenarios: API endpoint responses, Authentication and authorization, Error handling and validation
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

- **task**: Create database schema and migrations for timeline storage
- **done**: False
- **task**: Implement text chunking service with context preservation
- **done**: False
- **task**: Build core timeline extractor with LLM integration
- **done**: False
- **task**: Develop timeline validation and coherence checking
- **done**: False
- **task**: Create REST API endpoints with proper validation
- **done**: False
- **task**: Implement background job processing with progress tracking
- **done**: False
- **task**: Add WebSocket integration for real-time updates
- **done**: False
- **task**: Write comprehensive test suite
- **done**: False
- **task**: Performance testing and optimization
- **done**: False
- **task**: Documentation and code review
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Book Timeline Extractor is essential for converting novels into comics by identifying and sequencing key narrative events. This component analyzes full-text novels to extract a chronological timeline of major plot points, character interactions, and scene changes. This structured timeline becomes the foundation for panel generation, ensuring the comic adaptation maintains narrative coherence and proper pacing. Without this, the ML pipeline would struggle to create coherent visual sequences from unstructured text.

**Technical Approach:**
Implement a hybrid approach combining LLM-based content analysis with rule-based text processing. Use OpenAI/Anthropic models for semantic understanding of plot progression, while leveraging spaCy for linguistic analysis (named entity recognition, temporal expressions, dialogue detection). Design as a streaming pipeline to handle large novels efficiently, with chunked processing and intermediate result storage in PostgreSQL. Integrate with existing ML workflow infrastructure and provide REST endpoints for dashboard monitoring.

**Dependencies:**
- External: spacy (NLP), tiktoken (token counting), date-fns (temporal parsing), zod (validation)
- Internal: ML service infrastructure, database models, OpenAI/Anthropic integration layer, job queue system

**Risks:**
- Memory exhaustion with large novels: implement streaming with configurable chunk sizes and Redis caching
- LLM inconsistency across chunks: use few-shot prompting with consistent examples and validation schemas
- Processing time/cost: implement smart caching, result reuse, and progress tracking with user notifications
- Timeline coherence issues: add validation layer that cross-references extracted events for logical consistency

**Complexity Notes:**
Higher complexity than initially apparent due to need for maintaining narrative coherence across large text volumes. Requires sophisticated prompt engineering, temporal reasoning, and robust error handling. The streaming architecture and result validation add significant engineering overhead beyond basic text processing.

**Key Files:**
- apps/api/src/services/ml/timeline-extractor.ts: core extraction service
- apps/api/src/routes/books/timeline.ts: API endpoints  
- packages/database/src/schema/timelines.sql: timeline data models
- apps/api/src/jobs/timeline-extraction.ts: background job processing


### Design Decisions

[{'decision': 'Hybrid LLM + NLP approach with streaming architecture', 'rationale': 'LLMs provide semantic understanding while spaCy handles structured linguistic analysis. Streaming prevents memory issues with large novels and enables progress tracking.', 'alternatives_considered': ['Pure LLM approach', 'Rule-based only', 'Vector embedding similarity']}, {'decision': 'PostgreSQL storage with JSON timeline format', 'rationale': 'Leverages existing Supabase infrastructure while providing flexible schema for timeline events. JSON columns allow complex event metadata without rigid structure.', 'alternatives_considered': ['Separate timeline database', 'Redis-only caching', 'File-based storage']}]
