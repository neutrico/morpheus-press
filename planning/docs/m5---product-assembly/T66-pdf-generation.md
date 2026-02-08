---
area: comic
dependsOn:
- T64
- T65
effort: 5
iteration: I5
key: T66
milestone: M5 - Product Assembly
priority: p0
title: PDF Generation
type: Feature
---

# PDF Generation

## Acceptance Criteria

- [ ] **Users can generate PDF downloads of complete comics with all panels properly positioned**
  - Verification: Navigate to comic viewer, click 'Download PDF' button, verify PDF downloads with correct panel layout and readable text
- [ ] **PDF generation handles comics of varying lengths (1-50+ pages) without memory crashes**
  - Verification: Test PDF generation with comics containing 5, 20, and 50+ panels, monitor server memory usage stays below 2GB
- [ ] **Generated PDFs maintain print quality with file sizes under 50MB for typical comics**
  - Verification: Generate PDFs for 3 sample comics, verify file sizes <50MB and images remain crisp when printed at 300dpi
- [ ] **PDF generation provides real-time progress updates and handles failures gracefully**
  - Verification: Start PDF generation, verify progress updates appear in UI, simulate server restart during generation and verify proper error handling
- [ ] **System queues multiple PDF requests and processes them without blocking other operations**
  - Verification: Submit 3 PDF generation requests simultaneously, verify all complete successfully and API remains responsive

## Technical Notes

### Approach

Create a PDF generation service using Puppeteer that renders a specialized comic template optimized for print. Implement job queue processing for async generation with progress tracking. Design print-specific CSS layouts that handle page breaks intelligently between comic panels. Store generated PDFs in Supabase storage with download links returned to users. Include compression and optimization to balance quality with file size.


### Files to Modify

- **path**: apps/api/src/routes/comics/index.ts
- **changes**: Add PDF generation endpoint route registration
- **path**: apps/web/src/pages/comic/[id].tsx
- **changes**: Add PDF download button and progress tracking UI
- **path**: packages/shared/src/types/comic.ts
- **changes**: Add PDF generation status and metadata types

### New Files to Create

- **path**: apps/api/src/services/pdf-generator.ts
- **purpose**: Core PDF generation service using Puppeteer, handles comic rendering and file optimization
- **path**: apps/api/src/routes/comics/pdf.ts
- **purpose**: PDF generation API endpoints for starting jobs and checking status
- **path**: apps/web/src/components/comic/PDFTemplate.tsx
- **purpose**: Print-optimized comic layout component with CSS Grid and print media queries
- **path**: packages/shared/src/types/pdf.ts
- **purpose**: PDF generation request/response types and job status enums
- **path**: apps/api/src/jobs/pdf-generation.ts
- **purpose**: Background job processor for handling PDF generation queue
- **path**: apps/api/src/middleware/pdf-limits.ts
- **purpose**: Rate limiting and resource monitoring for PDF generation requests
- **path**: apps/web/src/hooks/usePDFGeneration.ts
- **purpose**: React hook for managing PDF generation state and progress polling
- **path**: apps/web/src/components/comic/PDFDownloadButton.tsx
- **purpose**: UI component with progress tracking and download functionality

### External Dependencies


- **puppeteer** ^21.5.0

  - Server-side PDF generation using Chrome's rendering engine

- **bullmq** ^4.15.0

  - Job queue for async PDF generation processing

- **sharp** ^0.32.6

  - Image optimization and compression for PDF assets

- **@types/puppeteer** ^5.4.7

  - TypeScript definitions for Puppeteer

## Testing

### Unit Tests

- **File**: `apps/api/src/services/__tests__/pdf-generator.test.ts`
  - Scenarios: Successful PDF generation with mock comic data, Memory limit exceeded error handling, Invalid comic ID error handling, Font fallback when custom fonts unavailable, Image compression and optimization
- **File**: `apps/api/src/jobs/__tests__/pdf-generation.test.ts`
  - Scenarios: Job queue processing, Progress tracking updates, Job failure and retry logic
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/pdf-workflow.test.ts`
  - Scenarios: End-to-end PDF generation from API request to file storage, Queue system integration with multiple concurrent jobs, Supabase storage upload and retrieval
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

- **task**: Setup Puppeteer, BullMQ dependencies and configure PDF generation queue
- **done**: False
- **task**: Implement core PDF generator service with memory management and optimization
- **done**: False
- **task**: Create print-optimized comic template component with CSS media queries
- **done**: False
- **task**: Build PDF generation API endpoints with job creation and status checking
- **done**: False
- **task**: Implement background job processing with progress tracking and error handling
- **done**: False
- **task**: Add PDF download UI components with progress indicators to comic viewer
- **done**: False
- **task**: Configure Supabase storage integration for PDF file management
- **done**: False
- **task**: Implement rate limiting and resource monitoring middleware
- **done**: False
- **task**: Write comprehensive test suite covering unit, integration, and performance scenarios
- **done**: False
- **task**: Create API documentation and user guide for PDF generation feature
- **done**: False

## Agent Notes

### Research Findings

**Context:**
PDF Generation is critical for delivering the final comic product to users. After comics are assembled from generated panels, users need a high-quality, printable PDF format for reading offline, printing, or sharing. This is the final step in the novel-to-comic transformation pipeline and represents the primary deliverable users expect. Without PDF generation, Morpheus would only exist as a web viewer, limiting distribution and user experience.

**Technical Approach:**
Recommended using Puppeteer for server-side PDF generation, leveraging Chrome's native PDF rendering capabilities. Create a dedicated comic viewer template optimized for PDF output with proper page breaks, margins, and print styles. Implement as a background job using a queue system to handle potentially long-running operations. Store generated PDFs in Supabase storage with metadata tracking. Use CSS Grid/Flexbox for precise panel positioning and @media print queries for PDF-specific styling.

**Dependencies:**
- External: puppeteer (PDF generation), bullmq (job queue), sharp (image optimization)
- Internal: Comic assembly service, panel storage system, user authentication, file storage service

**Risks:**
- Memory usage: Puppeteer can consume significant RAM with large comics; implement pagination and memory monitoring
- Generation time: Complex comics may take minutes to render; use job queues and progress tracking
- Font licensing: Ensure comic fonts are licensed for PDF distribution; fallback to web-safe fonts
- File size: High-res images can create massive PDFs; implement compression and optimization

**Complexity Notes:**
More complex than initially estimated due to print-specific layout challenges, memory management requirements, and the need for robust error handling. Comic panel positioning must translate perfectly from web to print dimensions, requiring careful CSS media queries and possibly different layout algorithms.

**Key Files:**
- apps/api/src/services/pdf-generator.ts: Core PDF generation service
- apps/api/src/routes/comics/pdf.ts: PDF generation endpoints
- apps/web/src/components/comic/PDFTemplate.tsx: Print-optimized comic layout
- packages/shared/src/types/pdf.ts: PDF generation types
- apps/api/src/jobs/pdf-generation.ts: Background job processing


### Design Decisions

[{'decision': 'Use Puppeteer over jsPDF/PDFKit', 'rationale': "Puppeteer leverages Chrome's mature rendering engine, handles complex CSS layouts better, and provides consistent output quality. Easier to maintain print styles alongside web styles.", 'alternatives_considered': ['jsPDF (limited layout capabilities)', 'PDFKit (requires manual positioning)', '@react-pdf/renderer (React-specific but limited styling)']}, {'decision': 'Implement as background job with queue system', 'rationale': 'PDF generation for multi-page comics can take 30+ seconds, requiring async processing to avoid request timeouts. Enables progress tracking and retry mechanisms.', 'alternatives_considered': ['Synchronous generation (timeout risk)', 'Client-side generation (performance issues)']}, {'decision': 'Create dedicated PDF template component', 'rationale': 'Print layouts have different requirements than web viewing - page breaks, margins, print-safe colors, and DPI considerations require specialized styling.', 'alternatives_considered': ['Reuse existing comic viewer (suboptimal print output)', 'Pure HTML templates (harder to maintain)']}]
