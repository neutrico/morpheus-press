---
area: ingestion
dependsOn:
- T38
effort: 5
iteration: I3
key: T39
milestone: M1 - Backend Services
priority: p0
title: Chapter Extraction & Parsing
type: Feature
---

# Chapter Extraction & Parsing

## Acceptance Criteria

- [ ] **System successfully extracts and parses chapters from TXT, DOCX, PDF, and EPUB files up to 50MB**
  - Verification: Upload test files via POST /api/v1/ingestion/chapters and verify 200 response with structured chapter data
- [ ] **Chapter detection accuracy >90% for common formats (Chapter N, Ch. N, numbered sections)**
  - Verification: Run test suite with 20+ sample novels, measure detected vs expected chapter count
- [ ] **Memory usage stays under 512MB when processing large files (20MB+)**
  - Verification: Monitor memory with --max-old-space-size=512 during load tests
- [ ] **Processing completes within 30 seconds for files under 5MB, 2 minutes for files under 50MB**
  - Verification: Automated performance tests measuring end-to-end processing time
- [ ] **API returns proper error responses for unsupported formats, corrupted files, and oversized uploads**
  - Verification: Test error scenarios and verify appropriate HTTP status codes and error messages

## Technical Notes

### Approach

Build a Fastify plugin that accepts file uploads and returns structured chapter data. Use strategy pattern for different file formats (TXT/DOCX/PDF/EPUB), each with specific extraction logic. Implement a two-pass system: first pass uses regex to identify likely chapter boundaries, second pass validates with LLM for ambiguous cases. Stream large files in chunks to prevent memory issues and store results in Supabase with proper indexing.


### Files to Modify

- **path**: packages/backend/src/app.ts
- **changes**: Register chapter-parser plugin
- **path**: packages/backend/src/lib/database.types.ts
- **changes**: Add Chapter table types from Supabase schema

### New Files to Create

- **path**: packages/backend/src/plugins/chapter-parser.ts
- **purpose**: Main Fastify plugin for chapter extraction API endpoints
- **path**: packages/backend/src/services/ingestion/chapter-extractor.ts
- **purpose**: Core extraction service with strategy pattern for file formats
- **path**: packages/backend/src/services/ingestion/extractors/txt-extractor.ts
- **purpose**: Plain text file extraction strategy
- **path**: packages/backend/src/services/ingestion/extractors/docx-extractor.ts
- **purpose**: DOCX file extraction using mammoth library
- **path**: packages/backend/src/services/ingestion/extractors/pdf-extractor.ts
- **purpose**: PDF text extraction using pdf-parse library
- **path**: packages/backend/src/services/ingestion/extractors/epub-extractor.ts
- **purpose**: EPUB file extraction using epub2 library
- **path**: packages/backend/src/services/ingestion/chapter-detector.ts
- **purpose**: Chapter boundary detection with regex patterns and LLM fallback
- **path**: packages/backend/src/models/chapter.ts
- **purpose**: Zod schemas and database models for chapter data
- **path**: packages/backend/src/routes/ingestion/chapters.ts
- **purpose**: HTTP route handlers for chapter ingestion endpoints
- **path**: packages/backend/src/lib/streaming-utils.ts
- **purpose**: Utilities for chunked file processing and memory management
- **path**: packages/backend/src/jobs/chapter-processing.ts
- **purpose**: Background job handlers for async chapter processing

### External Dependencies


- **mammoth** ^1.6.0

  - Extract text content from DOCX files while preserving structure

- **pdf-parse** ^1.1.1

  - Parse PDF files and extract text content reliably

- **epub2** ^3.0.2

  - Extract chapters and metadata from EPUB format novels

- **natural** ^6.10.0

  - Text processing utilities for sentence tokenization and content analysis

- **iconv-lite** ^0.6.3

  - Handle various text encodings and normalize to UTF-8

- **file-type** ^18.7.0

  - Detect file formats reliably from buffer content

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/services/chapter-extractor.test.ts`
  - Scenarios: Text extraction from each file format, Chapter boundary detection with various markers, Metadata extraction (titles, numbers, word counts), Error handling for corrupted files, Memory management with large inputs
- **File**: `packages/backend/src/__tests__/plugins/chapter-parser.test.ts`
  - Scenarios: Plugin registration and configuration, Request validation and sanitization, Response formatting
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/chapter-ingestion.test.ts`
  - Scenarios: End-to-end file upload and chapter extraction, Database persistence of chapter data, Queue integration for async processing, Error propagation through pipeline
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

- **task**: Setup dependencies (mammoth, pdf-parse, epub2, natural) and update package.json
- **done**: False
- **task**: Create database schema for chapters table in Supabase migration
- **done**: False
- **task**: Implement file format detection and base extractor interface
- **done**: False
- **task**: Build format-specific extractors (TXT, DOCX, PDF, EPUB)
- **done**: False
- **task**: Implement chapter boundary detection with regex patterns
- **done**: False
- **task**: Add LLM integration for ambiguous chapter detection
- **done**: False
- **task**: Create streaming utilities and memory management
- **done**: False
- **task**: Build main chapter-extractor service with strategy pattern
- **done**: False
- **task**: Implement Fastify plugin and API routes with validation
- **done**: False
- **task**: Add Redis caching for repeated operations
- **done**: False
- **task**: Setup background job processing for large files
- **done**: False
- **task**: Write comprehensive test suites and run coverage analysis
- **done**: False
- **task**: Performance testing with large files and memory profiling
- **done**: False
- **task**: Create API documentation and usage examples
- **done**: False
- **task**: Code review and refactoring based on feedback
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Chapter extraction and parsing is fundamental to the novel-to-comic transformation pipeline. This service needs to intelligently segment uploaded novel text into logical chapters, handling various formats (plain text, EPUB, DOCX, PDF) and inconsistent chapter markers. It's critical for M1 as downstream services (scene analysis, character extraction, comic generation) depend on properly segmented content. Without this, the entire transformation pipeline fails.

**Technical Approach:**
Implement a multi-stage parsing pipeline using Fastify plugins:
1. File format detection and content extraction (different strategies per format)
2. Text preprocessing and normalization 
3. Chapter boundary detection using regex patterns + LLM validation
4. Metadata extraction (chapter titles, numbers, word counts)
5. Content validation and error handling

Use streaming for large files, implement caching for repeated operations, and design for extensibility as chapter formats vary widely across novels.

**Dependencies:**
- External: mammoth (DOCX), pdf-parse (PDF), epub2 (EPUB), natural (NLP), zod (validation)
- Internal: file-upload service, database models, queue system for async processing

**Risks:**
- Memory issues with large novels: Use streaming and chunked processing
- Inconsistent chapter formats: Implement fallback strategies and LLM-assisted detection
- Performance bottlenecks: Add Redis caching and background job processing
- Character encoding issues: Normalize to UTF-8 early in pipeline

**Complexity Notes:**
Initially appears straightforward but complexity emerges from format diversity and edge cases. Novels have inconsistent chapter markers ("Chapter 1", "Ch. 1", "ONE", etc.) and some lack clear boundaries. The LLM integration for ambiguous cases adds async complexity but is necessary for quality.

**Key Files:**
- packages/backend/src/plugins/chapter-parser.ts: Main parser plugin
- packages/backend/src/services/ingestion/: Core extraction logic
- packages/backend/src/models/chapter.ts: Database schema
- packages/backend/src/routes/ingestion/chapters.ts: API endpoints


### Design Decisions

[{'decision': 'Use multi-format parser with strategy pattern', 'rationale': 'Different file formats require different extraction methods. Strategy pattern allows easy extension and testing of each format independently.', 'alternatives_considered': ['Single parser for all formats', 'External service for parsing']}, {'decision': 'Hybrid regex + LLM approach for chapter detection', 'rationale': 'Regex handles common patterns efficiently, LLM provides fallback for ambiguous cases and validation. Balances performance with accuracy.', 'alternatives_considered': ['Pure regex approach', 'LLM-only approach', 'Rule-based heuristics']}, {'decision': 'Streaming processing with chunked analysis', 'rationale': 'Prevents memory issues with large novels while maintaining processing speed. Critical for scalability.', 'alternatives_considered': ['Load entire file in memory', 'External processing service']}]
