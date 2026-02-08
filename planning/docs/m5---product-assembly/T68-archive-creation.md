---
area: comic
dependsOn:
- T64
effort: 2
iteration: I5
key: T68
milestone: M5 - Product Assembly
priority: p0
title: Archive Creation
type: Feature
---

# Archive Creation

## Acceptance Criteria

- [ ] **Users can generate PDF, CBZ, and EPUB archives from completed comics with proper metadata and page ordering**
  - Verification: Upload a multi-page comic, trigger archive generation for each format, verify downloadable files contain all pages in correct order with comic title/author metadata
- [ ] **Archive generation processes large comics (50+ pages) without memory exhaustion or timeouts**
  - Verification: Create a 100-page comic, monitor server memory usage during archive generation, verify process completes within 5 minutes with <500MB peak memory
- [ ] **Background job system provides real-time progress updates during archive creation**
  - Verification: Start archive generation, verify WebSocket events show progress percentage updates every 10% completion, final success/error notification received
- [ ] **Generated archives are temporarily stored with automatic cleanup after 24 hours**
  - Verification: Generate archive, verify signed download URL works immediately, check Supabase Storage shows TTL metadata, confirm file auto-deleted after 24 hours
- [ ] **Archive generation handles errors gracefully with proper user feedback**
  - Verification: Test with corrupted images, network failures, and invalid comic data - verify error messages displayed in UI and job marked as failed

## Technical Notes

### Approach

Create an archive service that generates multiple comic formats using streaming operations and background jobs. Implement format-specific generators (PDF, CBZ, EPUB) that process comic pages in chunks to manage memory usage. Use BullMQ for job queuing with progress tracking, store temporary archives in Supabase Storage, and provide real-time status updates through WebSocket connections. Include comprehensive validation and cleanup mechanisms.


### Files to Modify

- **path**: apps/api/src/services/storage.service.ts
- **changes**: Add TTL support for temporary file storage, cleanup job scheduling
- **path**: apps/api/src/services/comic.service.ts
- **changes**: Add getComicPagesForArchive method with streaming support
- **path**: apps/api/src/config/queue.ts
- **changes**: Configure archive job queue with BullMQ settings
- **path**: apps/dashboard/src/stores/comic.store.ts
- **changes**: Add archive generation state management

### New Files to Create

- **path**: apps/api/src/services/archive.service.ts
- **purpose**: Core archive generation logic with format-specific handlers
- **path**: apps/api/src/jobs/archive.job.ts
- **purpose**: Background job processor for archive generation with progress tracking
- **path**: apps/api/src/routes/archive/create.ts
- **purpose**: API endpoint to initiate archive generation
- **path**: apps/api/src/routes/archive/status.ts
- **purpose**: API endpoint to check archive generation status
- **path**: apps/api/src/routes/archive/download.ts
- **purpose**: API endpoint to retrieve generated archive
- **path**: apps/api/src/lib/generators/pdf-generator.ts
- **purpose**: PDF-specific archive generation using PDFKit
- **path**: apps/api/src/lib/generators/cbz-generator.ts
- **purpose**: CBZ format generation using JSZip
- **path**: apps/api/src/lib/generators/epub-generator.ts
- **purpose**: EPUB format generation with comic layout
- **path**: apps/api/src/middleware/archive-validation.ts
- **purpose**: Request validation for archive generation endpoints
- **path**: apps/dashboard/src/components/ArchiveGenerator.tsx
- **purpose**: UI component for archive creation with progress tracking
- **path**: apps/dashboard/src/components/ArchiveProgress.tsx
- **purpose**: Progress indicator component with WebSocket integration
- **path**: apps/dashboard/src/hooks/useArchiveGeneration.ts
- **purpose**: React hook for archive generation state and WebSocket handling
- **path**: packages/shared/src/types/archive.ts
- **purpose**: TypeScript definitions for archive-related data structures
- **path**: apps/api/src/jobs/archive-cleanup.job.ts
- **purpose**: Scheduled job to clean up expired archive files

### External Dependencies


- **pdfkit** ^0.14.0

  - PDF generation with comic-specific layouts and metadata support

- **jszip** ^3.10.1

  - CBZ format creation (ZIP archives containing images)

- **epub-gen** ^0.1.0

  - EPUB format generation for e-reader compatibility

- **archiver** ^6.0.1

  - Streaming archive creation with compression options

- **bullmq** ^4.15.0

  - Background job processing with progress tracking and retry logic

- **sharp** ^0.33.0

  - Image optimization and format standardization before archiving

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/archive.service.test.ts`
  - Scenarios: PDF generation with valid comic data, CBZ creation with image optimization, EPUB generation with metadata, Error handling for missing images, Memory stream processing, Format validation
- **File**: `apps/api/src/__tests__/jobs/archive.job.test.ts`
  - Scenarios: Job progress tracking, Job failure handling, Cleanup on completion, Memory management
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/archive.integration.test.ts`
  - Scenarios: End-to-end archive generation flow, Storage service integration, Job queue processing, WebSocket progress updates, File cleanup scheduling
- **File**: `apps/dashboard/src/__tests__/components/ArchiveGenerator.test.tsx`
  - Scenarios: UI state management during generation, Progress bar updates, Download link handling, Error message display
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 8.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup external dependencies (PDFKit, JSZip, Sharp, BullMQ, epub-gen)
- **done**: False
- **task**: Create archive service with streaming architecture and format generators
- **done**: False
- **task**: Implement BullMQ job processing with progress tracking and memory management
- **done**: False
- **task**: Build API endpoints for archive creation, status checking, and download
- **done**: False
- **task**: Add temporary storage with TTL and cleanup jobs to Supabase integration
- **done**: False
- **task**: Create React components with WebSocket progress updates and download handling
- **done**: False
- **task**: Implement comprehensive error handling and validation across all layers
- **done**: False
- **task**: Add unit and integration tests with memory usage monitoring
- **done**: False
- **task**: Performance testing with large comics and concurrent archive generation
- **done**: False
- **task**: Documentation for API endpoints, job configuration, and deployment considerations
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Archive Creation enables users to package completed comics into distributable formats (PDF, EPUB, CBZ/CBR) for offline reading, sharing, or selling. This is essential for the product assembly milestone as it transforms individual comic pages into consumable final products. Users need archives to distribute their comics on platforms, share with readers, or create physical prints.

**Technical Approach:**
- Use PDFKit for PDF generation with proper comic layout and metadata
- Implement JSZip for CBZ (Comic Book ZIP) format creation
- Leverage Sharp for image optimization and format standardization before archiving
- Create streaming archive generation to handle large comics without memory issues
- Implement background job processing with BullMQ for async archive creation
- Store archives temporarily in Supabase Storage with signed URLs for download
- Add progress tracking for long-running archive operations

**Dependencies:**
- External: pdfkit, jszip, sharp, bullmq, archiver, epub-gen
- Internal: comic service, page service, storage service, job queue system, notification service

**Risks:**
- Memory exhaustion: Large comics could overwhelm server memory during archive creation
  Mitigation: Stream processing, chunk-based operations, memory monitoring
- Storage costs: Archives consume significant storage space
  Mitigation: Temporary storage with TTL, compression optimization, cleanup jobs
- Generation timeouts: Complex comics may exceed request timeouts
  Mitigation: Background processing with progress updates via WebSocket/SSE
- Format compatibility: Different readers support different features
  Mitigation: Format validation, fallback options, comprehensive testing

**Complexity Notes:**
More complex than initially estimated due to multiple output formats, memory management requirements, and need for background processing. The streaming and optimization aspects add significant technical complexity.

**Key Files:**
- apps/api/src/services/archive.service.ts: Core archive generation logic
- apps/api/src/jobs/archive.job.ts: Background job handler
- apps/api/src/routes/archive/: API endpoints for archive operations
- apps/dashboard/src/components/ArchiveGenerator.tsx: UI for archive creation
- packages/shared/src/types/archive.ts: Archive type definitions


### Design Decisions

[{'decision': 'Use background job processing for archive generation', 'rationale': 'Archive creation is resource-intensive and time-consuming, requiring async processing to avoid request timeouts and improve user experience', 'alternatives_considered': ['Synchronous generation', 'Client-side processing', 'External service integration']}, {'decision': 'Support multiple archive formats (PDF, CBZ, EPUB)', 'rationale': 'Different use cases require different formats - PDF for printing, CBZ for comic readers, EPUB for broader e-reader compatibility', 'alternatives_considered': ['PDF only', 'Single universal format', 'User-selectable single format']}, {'decision': 'Implement streaming archive generation', 'rationale': 'Prevents memory exhaustion with large comics and enables real-time progress tracking', 'alternatives_considered': ['In-memory generation', 'Disk-based temporary files', 'Chunked processing']}]
