---
area: comic
dependsOn:
- T66
effort: 3
iteration: I5
key: T67
milestone: M5 - Product Assembly
priority: p0
title: Download Manager
type: Feature
---

# Download Manager

## Acceptance Criteria

- [ ] **Users can download comics in PDF, CBZ, and ZIP (individual images) formats with progress tracking**
  - Verification: Manual testing: Generate comic, select format, verify download completes with progress bar and correct file format
- [ ] **Download system handles files up to 100MB with streaming and memory efficiency under 512MB RAM usage**
  - Verification: Integration test: Download large comic (50+ pages), monitor memory usage with process.memoryUsage() assertions
- [ ] **Failed downloads can be resumed and retried, with queue status visible to users**
  - Verification: Manual testing: Interrupt download mid-process, verify resume functionality and status updates in UI
- [ ] **Download jobs are properly queued and processed with BullMQ, handling up to 10 concurrent downloads per user**
  - Verification: Integration test: Queue multiple downloads, verify rate limiting and proper job processing order
- [ ] **Temporary files are cleaned up within 24 hours and download URLs expire after 1 hour**
  - Verification: Unit test: Verify TTL policies and cleanup job execution, check S3 presigned URL expiration

## Technical Notes

### Approach

Implement a two-phase download system: preparation phase using BullMQ queues to generate requested formats, and delivery phase using Fastify streaming responses. Store download jobs in Supabase with status tracking, generate files using format-specific libraries (PDFKit, JSZip), and stream directly to clients with progress tracking. Use presigned S3 URLs for large files and implement cleanup workers for temporary storage management.


### Files to Modify

- **path**: packages/api/src/server.ts
- **changes**: Register BullMQ queues and download routes
- **path**: packages/api/src/middleware/auth.ts
- **changes**: Add download authorization checks
- **path**: packages/dashboard/src/pages/ComicViewer.tsx
- **changes**: Integrate DownloadManager component
- **path**: packages/shared/src/types/api.ts
- **changes**: Add download-related API types

### New Files to Create

- **path**: packages/api/src/routes/downloads.ts
- **purpose**: Download endpoint handlers and streaming responses
- **path**: packages/api/src/services/download-manager.ts
- **purpose**: Core download orchestration, job management, and queue integration
- **path**: packages/api/src/services/comic-assembler.ts
- **purpose**: Format-specific file generation (PDF, CBZ, ZIP)
- **path**: packages/api/src/workers/download-worker.ts
- **purpose**: BullMQ worker for processing download jobs
- **path**: packages/api/src/workers/cleanup-worker.ts
- **purpose**: Scheduled cleanup of temporary download files
- **path**: packages/dashboard/src/components/DownloadManager.tsx
- **purpose**: Download UI with progress tracking and format selection
- **path**: packages/dashboard/src/hooks/useDownload.ts
- **purpose**: Download state management and progress tracking hook
- **path**: packages/shared/src/types/download.ts
- **purpose**: Download job types, status enums, and format specifications
- **path**: packages/api/src/config/download.ts
- **purpose**: Download configuration (limits, timeouts, file paths)

### External Dependencies


- **bullmq** ^5.0.0

  - Reliable job queue for download preparation tasks

- **pdfkit** ^0.14.0

  - PDF generation from comic pages

- **jszip** ^3.10.1

  - CBZ archive creation and ZIP file generation

- **archiver** ^6.0.1

  - Streaming archive creation for large comics

- **file-type** ^19.0.0

  - MIME type detection for proper Content-Type headers

- **sharp** ^0.33.0

  - Image optimization and format conversion before packaging

## Testing

### Unit Tests

- **File**: `packages/api/src/services/__tests__/download-manager.test.ts`
  - Scenarios: Download job creation and status tracking, Format validation and error handling, Memory limit enforcement, File cleanup scheduling
- **File**: `packages/api/src/services/__tests__/comic-assembler.test.ts`
  - Scenarios: PDF generation with metadata, CBZ archive creation, Image optimization and compression, Invalid comic data handling
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/downloads.test.ts`
  - Scenarios: Complete download workflow from request to delivery, Queue processing with BullMQ integration, S3 presigned URL generation and access, Rate limiting and concurrent download management
- **File**: `packages/dashboard/src/components/__tests__/DownloadManager.test.tsx`
  - Scenarios: Progress tracking and status updates, Error state handling and retry UI, Format selection and download triggering
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 7

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup BullMQ configuration and Redis connection for download queues
- **done**: False
- **task**: Implement download job types and Supabase schema for job tracking
- **done**: False
- **task**: Create comic-assembler service with PDF, CBZ, and ZIP generation
- **done**: False
- **task**: Build download-manager service with queue integration and streaming
- **done**: False
- **task**: Implement download API routes with authentication and rate limiting
- **done**: False
- **task**: Create BullMQ workers for job processing and file cleanup
- **done**: False
- **task**: Build DownloadManager React component with progress tracking
- **done**: False
- **task**: Implement client-side download hook with resume capability
- **done**: False
- **task**: Add comprehensive error handling and retry mechanisms
- **done**: False
- **task**: Write unit and integration tests, conduct manual testing
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Download Manager is essential for the comic generation workflow, allowing users to download their completed comics in various formats (PDF, CBZ, individual images). This is a critical user-facing feature that completes the novel-to-comic transformation journey. Users need reliable, resumable downloads with progress tracking, especially for multi-page comics that can be large files. This also supports different use cases - casual readers wanting PDFs, comic enthusiasts preferring CBZ format, and creators needing individual page assets.

**Technical Approach:**
Implement a robust download system using streaming responses with Fastify's built-in streaming capabilities. Use a queue-based approach with BullMQ for handling download preparation (comic assembly, format conversion). Store download metadata in Supabase with status tracking. Implement client-side download progress with fetch API and ReadableStream. For file generation, use libraries like PDFKit for PDF creation and JSZip for CBZ archives. Implement presigned URLs for direct S3 downloads when files are pre-generated.

**Dependencies:**
- External: BullMQ, PDFKit, JSZip, file-type, archiver, sharp (image processing)
- Internal: Comic storage service, user authentication, file upload/storage infrastructure, comic generation pipeline

**Risks:**
- Memory issues with large files: Use streaming and temporary file cleanup
- Concurrent download limits: Implement rate limiting and queue management
- File corruption during generation: Add checksums and retry mechanisms
- Storage costs for temporary files: Implement TTL cleanup policies
- Browser download failures: Add resumable download support

**Complexity Notes:**
Initially seems straightforward but complexity increases with format variety, large file handling, and user experience requirements. The streaming implementation and queue management add significant architectural complexity. Integration with existing comic storage and the need for format conversion make this a medium-high complexity task.

**Key Files:**
- packages/api/src/routes/downloads.ts: Download endpoint handlers
- packages/api/src/services/download-manager.ts: Core download logic
- packages/api/src/services/comic-assembler.ts: Comic format generation
- packages/dashboard/src/components/DownloadManager.tsx: UI component
- packages/shared/src/types/download.ts: Type definitions


### Design Decisions

[{'decision': 'Use streaming responses with queue-based file preparation', 'rationale': 'Handles large files efficiently, provides progress tracking, and scales with multiple concurrent downloads', 'alternatives_considered': ['Direct file serving', 'Pre-generated files only', 'Client-side assembly']}, {'decision': 'Support PDF, CBZ, and ZIP formats', 'rationale': 'Covers main use cases - PDF for reading, CBZ for comic apps, ZIP for individual assets', 'alternatives_considered': ['PDF only', 'Custom format', 'EPUB support']}, {'decision': 'Temporary file generation with TTL cleanup', 'rationale': 'Balances performance (no regeneration) with storage costs and allows customization per download', 'alternatives_considered': ['Always stream generate', 'Permanent file caching', 'Client-side generation']}]
