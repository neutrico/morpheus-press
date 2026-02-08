---
area: ingestion
dependsOn:
- T39
effort: 5
iteration: I3
key: T40
milestone: M1 - Backend Services
priority: p0
title: Text Preprocessing Pipeline
type: Task
---

# Text Preprocessing Pipeline

## Acceptance Criteria

- [ ] **Pipeline processes uploaded text files (TXT, PDF, DOCX) and extracts structured content including characters, dialogue, narrative segments, and scene boundaries**
  - Verification: Upload test novel file via POST /api/ingestion/process-text, verify response contains extracted characters array, dialogue/narrative segments with proper tags, and scene boundary markers
- [ ] **System handles large files (>10MB) without memory exhaustion using streaming and background job processing**
  - Verification: Upload 50MB+ text file, monitor memory usage stays under 500MB, verify WebSocket progress updates, confirm job completes successfully
- [ ] **Character detection identifies main characters with 90%+ accuracy and handles name variations/aliases through fuzzy matching**
  - Verification: Process test novel with known character list, verify detected characters match expected list within 90% accuracy, test aliases like 'John' vs 'Johnny' are grouped correctly
- [ ] **Scene segmentation preserves context at boundaries using overlapping windows and semantic similarity scoring**
  - Verification: Verify adjacent scenes share contextual elements, check overlap regions contain relevant context, validate scene transitions maintain narrative flow
- [ ] **Pipeline is resumable from any stage failure and caches intermediate results for re-processing**
  - Verification: Interrupt processing mid-stage, restart pipeline, verify it resumes from cached checkpoint without re-processing completed stages

## Technical Notes

### Approach

Build a multi-stage pipeline service that accepts raw text files, processes them through cleaning/normalization, NLP analysis for character/dialogue extraction, semantic segmentation into scenes, and outputs structured data ready for LLM comic generation prompts. Use PostgreSQL for intermediate storage, WebSocket for progress updates, and implement as background jobs for large files. Each stage is modular and resumable to handle failures gracefully.


### Files to Modify

- **path**: apps/api/src/models/index.ts
- **changes**: Add imports for new ProcessedText, TextSegment, and CharacterEntity models
- **path**: apps/api/src/services/index.ts
- **changes**: Export TextProcessorService and register with dependency injection
- **path**: apps/api/src/routes/index.ts
- **changes**: Register ingestion routes with main router
- **path**: packages/shared/types/index.ts
- **changes**: Export text processing types for frontend consumption

### New Files to Create

- **path**: apps/api/src/services/text-processor.ts
- **purpose**: Main preprocessing pipeline orchestrator with stage management
- **path**: apps/api/src/models/processed-text.ts
- **purpose**: Database schema for storing processed text segments and metadata
- **path**: apps/api/src/models/character-entity.ts
- **purpose**: Character extraction and management with alias resolution
- **path**: apps/api/src/models/text-segment.ts
- **purpose**: Individual text segments with type classification and scene boundaries
- **path**: apps/api/src/routes/ingestion.ts
- **purpose**: REST endpoints for file upload, processing triggers, and status queries
- **path**: apps/api/src/utils/text-chunker.ts
- **purpose**: Token-aware text segmentation with overlap and boundary detection
- **path**: apps/api/src/utils/nlp-processor.ts
- **purpose**: NLP utilities for character extraction, dialogue detection, and scene analysis
- **path**: apps/api/src/utils/file-parser.ts
- **purpose**: Multi-format file parsing (PDF, DOCX, TXT) with encoding normalization
- **path**: packages/shared/types/text-processing.ts
- **purpose**: TypeScript interfaces for text processing pipeline data structures
- **path**: apps/api/src/jobs/text-processing-job.ts
- **purpose**: Background job implementation for large file processing
- **path**: apps/api/src/services/websocket-progress.ts
- **purpose**: Real-time progress updates via WebSocket for processing status

### External Dependencies


- **spacy** ^3.7.0

  - NER for character detection, sentence segmentation, and dialogue attribution

- **tiktoken** ^1.0.10

  - Accurate token counting for LLM context window management

- **sentence-transformers** ^2.2.2

  - Semantic similarity for intelligent scene boundary detection

- **pdf-parse** ^1.1.1

  - Extract text content from PDF novel uploads

- **mammoth** ^1.6.0

  - Convert DOCX files to clean text while preserving structure

- **compromise** ^14.10.0

  - Lightweight NLP for text normalization and basic entity recognition

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/text-processor.test.ts`
  - Scenarios: Text cleaning and normalization, Character extraction with NER, Dialogue vs narrative classification, Scene boundary detection, Error handling for malformed input, Memory management for large texts
- **File**: `apps/api/src/__tests__/utils/text-chunker.test.ts`
  - Scenarios: Token-aware chunking with tiktoken, Overlap window calculations, Boundary detection accuracy, Memory efficient streaming
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/text-pipeline.test.ts`
  - Scenarios: Full pipeline: file upload to structured output, Background job processing with progress tracking, WebSocket progress updates, Database persistence of processed segments, Resume from failure scenarios
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

- **task**: Setup NLP dependencies (spacy, sentence-transformers, tiktoken) and configure model downloads
- **done**: False
- **task**: Create database models and migrations for processed text storage
- **done**: False
- **task**: Implement file parsing utilities for PDF, DOCX, TXT formats
- **done**: False
- **task**: Build text chunking service with token counting and overlap logic
- **done**: False
- **task**: Develop NLP processor for character extraction and dialogue classification
- **done**: False
- **task**: Create scene segmentation using semantic similarity
- **done**: False
- **task**: Implement main text processor service with pipeline orchestration
- **done**: False
- **task**: Build REST API endpoints and WebSocket progress service
- **done**: False
- **task**: Add background job queue integration for large file processing
- **done**: False
- **task**: Create comprehensive test suite and performance benchmarks
- **done**: False
- **task**: Write API documentation and usage examples
- **done**: False
- **task**: Conduct code review and security analysis
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The text preprocessing pipeline is crucial for transforming raw novel text into structured, ML-ready content for comic generation. This involves cleaning text, segmenting into scenes/panels, extracting dialogue vs narrative, identifying characters, and preparing prompts for LLM scene analysis. Without proper preprocessing, downstream AI models receive inconsistent input, leading to poor comic panel generation and character continuity issues. This is a foundational component that directly impacts the quality of the entire novel-to-comic transformation process.

**Technical Approach:**
- Use a modular pipeline architecture with discrete processing stages
- Implement text chunking with overlap for context preservation using tiktoken for token counting
- Natural Language Processing via spaCy for NER (character detection) and sentence segmentation
- Regex patterns for dialogue extraction and formatting cleanup
- Scene boundary detection using ML-based sentence similarity (sentence-transformers)
- Streaming processing for large novels to manage memory efficiently
- Cache intermediate results in PostgreSQL for resumability
- Expose via Fastify REST endpoints with real-time WebSocket progress updates

**Dependencies:**
- External: spacy, tiktoken, sentence-transformers, compromise, pdf-parse, mammoth (for docx)
- Internal: Database models for storing processed segments, WebSocket service, file upload service

**Risks:**
- Memory exhaustion with large files: Use streaming and chunked processing
- Character name variations/aliases: Build fuzzy matching with Levenshtein distance
- Context loss at chunk boundaries: Implement overlapping windows with smart boundary detection
- Processing time for large novels: Implement background job queue with progress tracking
- Text encoding issues: Normalize to UTF-8 early in pipeline

**Complexity Notes:**
This is more complex than initially apparent due to the need for semantic understanding rather than just text manipulation. Character consistency across scenes, maintaining narrative flow, and handling various input formats (PDF, DOCX, TXT) adds significant complexity. The ML components for scene segmentation require careful prompt engineering and model selection.

**Key Files:**
- apps/api/src/services/text-processor.ts: Main preprocessing service
- apps/api/src/models/processed-text.ts: Database schema for segments
- apps/api/src/routes/ingestion.ts: API endpoints for text upload/processing
- packages/shared/types/text-processing.ts: Shared TypeScript interfaces
- apps/api/src/utils/text-chunker.ts: Token-aware text segmentation


### Design Decisions

[{'decision': 'Use spaCy for NLP tasks instead of lighter alternatives', 'rationale': 'Provides robust NER for character detection, dependency parsing for dialogue attribution, and proven performance with literary text', 'alternatives_considered': ['Natural (compromise.js)', 'NLTK.js', 'Custom regex-based solution']}, {'decision': 'Implement streaming pipeline with PostgreSQL staging tables', 'rationale': 'Enables processing of large novels without memory issues, provides resumability, and allows real-time progress tracking for frontend', 'alternatives_considered': ['In-memory processing', 'File-based intermediate storage', 'Redis-based caching']}, {'decision': 'Use sentence-transformers for semantic scene boundary detection', 'rationale': 'Provides better scene transitions than rule-based approaches, understands context shifts that indicate panel boundaries', 'alternatives_considered': ['Rule-based chapter/paragraph splitting', 'Custom BERT fine-tuning', 'OpenAI embeddings API']}]
