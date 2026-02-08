---
area: ingestion
dependsOn:
- T25
effort: 3
iteration: I3
key: T38
milestone: M1 - Backend Services
priority: p0
title: Book Upload Handler
type: Feature
---

# Book Upload Handler

## Acceptance Criteria

- [ ] **System accepts and processes PDF, EPUB, TXT, and DOCX files up to 100MB**
  - Verification: Upload test files of each format via POST /api/books/upload and verify 200 response with extracted content
- [ ] **File validation rejects invalid formats and oversized files with appropriate error messages**
  - Verification: Upload invalid file types and >100MB files, verify 400 responses with specific error codes
- [ ] **Extracted text content is stored in database with proper metadata (title, author, word count)**
  - Verification: Query books table after upload to verify content field populated and metadata fields accurate
- [ ] **Original files are securely stored in Supabase Storage with proper access controls**
  - Verification: Check storage bucket for uploaded files and verify they're only accessible to authenticated users
- [ ] **Large file processing happens asynchronously without blocking the upload response**
  - Verification: Upload 50MB+ file and verify immediate response with job_id, then check job completion via status endpoint

## Technical Notes

### Approach

Create a Fastify multipart upload route that streams files to temporary storage while validating format and size. Implement dedicated service classes for content extraction using format-specific parsers (pdf-parse, epub2, mammoth). Store original files in Supabase Storage and extracted metadata/content in PostgreSQL with proper foreign key relationships. Use async job processing for heavy operations like full-text extraction and initial chapter detection to prevent request timeouts.


### Files to Modify

- **path**: packages/api/src/app.ts
- **changes**: Register multipart plugin and book upload routes
- **path**: packages/api/src/middleware/auth.ts
- **changes**: Add user context extraction for file ownership
- **path**: packages/shared/types/api.ts
- **changes**: Add upload response types and error codes
- **path**: packages/database/schema.sql
- **changes**: Add books table and file_uploads tracking table

### New Files to Create

- **path**: packages/api/src/routes/books/upload.ts
- **purpose**: Main upload endpoint with multipart handling
- **path**: packages/api/src/routes/books/status.ts
- **purpose**: Upload job status checking endpoint
- **path**: packages/api/src/services/BookUploadService.ts
- **purpose**: Core upload orchestration and file management
- **path**: packages/api/src/services/ContentExtractorService.ts
- **purpose**: Format-specific content parsing and extraction
- **path**: packages/api/src/services/FileValidatorService.ts
- **purpose**: Security validation and format verification
- **path**: packages/api/src/lib/validators/book-upload.ts
- **purpose**: Zod schemas for upload validation
- **path**: packages/api/src/lib/storage/SupabaseStorageAdapter.ts
- **purpose**: File storage abstraction layer
- **path**: packages/api/src/lib/jobs/BookProcessingJob.ts
- **purpose**: Async job handler for content processing
- **path**: packages/shared/types/book.ts
- **purpose**: Book entity types and upload interfaces
- **path**: packages/api/src/lib/errors/UploadErrors.ts
- **purpose**: Custom error classes for upload scenarios

### External Dependencies


- **@fastify/multipart** ^8.0.0

  - Native Fastify multipart form support with streaming

- **pdf-parse** ^1.1.1

  - Reliable PDF text extraction with metadata support

- **epub2** ^3.0.2

  - EPUB file parsing and chapter extraction

- **mammoth** ^1.6.0

  - DOCX file processing with formatting preservation

- **mime-types** ^2.1.35

  - File type validation and MIME type detection

- **file-type** ^19.0.0

  - File signature validation for security

## Testing

### Unit Tests

- **File**: `packages/api/src/__tests__/services/BookUploadService.test.ts`
  - Scenarios: Valid file upload flow, File size validation, MIME type validation, Storage service integration, Database persistence
- **File**: `packages/api/src/__tests__/services/ContentExtractorService.test.ts`
  - Scenarios: PDF text extraction, EPUB content parsing, DOCX document processing, TXT file handling, Malformed file error handling
- **File**: `packages/api/src/__tests__/lib/validators/book-upload.test.ts`
  - Scenarios: Valid upload payload validation, File type validation, Size limit validation, Required field validation
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/book-upload.test.ts`
  - Scenarios: Complete upload flow with database persistence, File upload with Supabase Storage integration, Authentication middleware integration, Error handling across service boundaries
### E2E Tests

- **File**: `packages/e2e/tests/book-upload.spec.ts`
  - Scenarios: Dashboard file upload workflow, Upload progress tracking, File processing status updates
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 9

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup database schema and migrations for books and file_uploads tables
- **done**: False
- **task**: Install and configure required dependencies (@fastapi/multipart, pdf-parse, epub2, mammoth)
- **done**: False
- **task**: Implement FileValidatorService with MIME type and size validation
- **done**: False
- **task**: Create ContentExtractorService with format-specific parsers
- **done**: False
- **task**: Build BookUploadService orchestrating validation, extraction, and storage
- **done**: False
- **task**: Implement upload route with streaming multipart support
- **done**: False
- **task**: Add Supabase Storage integration for file persistence
- **done**: False
- **task**: Create job queue system for async processing of large files
- **done**: False
- **task**: Implement comprehensive error handling and custom error classes
- **done**: False
- **task**: Add authentication middleware integration and user context
- **done**: False
- **task**: Create status endpoint for tracking upload job progress
- **done**: False
- **task**: Write comprehensive test suites (unit, integration, e2e)
- **done**: False
- **task**: Add API documentation and usage examples
- **done**: False
- **task**: Performance testing with large files and concurrent uploads
- **done**: False
- **task**: Security review and penetration testing
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Book Upload Handler is a critical component for content ingestion that enables users to upload novel files (PDF, EPUB, TXT, DOCX) through the dashboard and processes them for comic transformation. This solves the core problem of getting user content into the Morpheus pipeline, validating file integrity, extracting text content, and preparing it for chapter segmentation and comic generation. Without this, users cannot feed their novels into the transformation system.

**Technical Approach:**
Implement a multi-part file upload endpoint using Fastify's multipart plugin with streaming support. Use a service-oriented architecture with dedicated classes for FileValidator, ContentExtractor, and BookProcessor. Leverage Supabase Storage for file persistence and PostgreSQL for metadata storage. Implement async processing with job queues for large files to prevent request timeouts. Use strong typing with Zod schemas for validation and proper error handling with custom error classes.

**Dependencies:**
- External: @fastify/multipart, pdf-parse, epub2, mammoth (DOCX), zod, mime-types, sharp (thumbnails)
- Internal: database service, storage service, job queue system, user authentication middleware

**Risks:**
- Large file uploads (>100MB): Implement streaming uploads with progress tracking and chunked processing
- Memory exhaustion from PDF/EPUB parsing: Use streaming parsers and implement memory limits
- File format security vulnerabilities: Strict MIME type validation, file signature verification, sandboxed processing
- Concurrent upload limits: Implement rate limiting and queue management per user
- Storage costs from abandoned uploads: Implement cleanup jobs and upload expiration

**Complexity Notes:**
More complex than initially estimated due to multiple file format support requirements and the need for robust content extraction. The streaming aspects and proper error recovery add significant complexity. However, the well-defined scope and existing Fastify/Supabase infrastructure reduce integration complexity.

**Key Files:**
- packages/api/src/routes/books/upload.ts: Main upload endpoint
- packages/api/src/services/BookUploadService.ts: Core upload logic
- packages/api/src/services/ContentExtractorService.ts: File parsing logic
- packages/api/src/lib/validators/book-upload.ts: Zod validation schemas
- packages/shared/types/book.ts: Type definitions


### Design Decisions

[{'decision': 'Use streaming multipart uploads with Fastify native support', 'rationale': 'Handles large files efficiently, integrates well with existing Fastify setup, provides progress tracking capabilities', 'alternatives_considered': ['Direct base64 upload', 'External upload service (AWS S3 direct)', 'Chunked upload implementation']}, {'decision': 'Implement synchronous upload + asynchronous processing pattern', 'rationale': 'Provides immediate feedback to users while preventing timeout issues for large file processing', 'alternatives_considered': ['Fully synchronous processing', 'Fully asynchronous with webhooks', 'WebSocket real-time updates']}, {'decision': 'Store original files in Supabase Storage with extracted content in PostgreSQL', 'rationale': 'Leverages existing infrastructure, keeps large binary data separate from searchable text content, enables efficient queries', 'alternatives_considered': ['Store everything in PostgreSQL', 'Use separate S3 bucket', 'Store extracted text as files']}]
