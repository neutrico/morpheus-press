---
area: ingestion
dependsOn:
- T25
effort: 3
iteration: I3
key: T37
milestone: M1 - Backend Services
priority: p0
title: Wolne Lektury API Integration
type: Feature
---

# Wolne Lektury API Integration

## Acceptance Criteria

- [ ] **Successfully fetch and store book metadata from Wolne Lektury API with proper schema validation**
  - Verification: Run `npm test -- wolne-lektury.test.ts` and verify API integration tests pass. Check Supabase books table contains expected fields: title, author, publication_date, genre, language, etc.
- [ ] **Process and chunk full-text content for books with progress tracking and error handling**
  - Verification: Trigger import via POST /admin/ingestion/wolne-lektury endpoint, monitor job queue status, verify book content is stored in chunks table with proper text segmentation
- [ ] **Implement rate limiting and exponential backoff to respect API limits without failures**
  - Verification: Run load test importing 100+ books simultaneously, verify no 429 errors and exponential backoff logs appear. Check Redis rate limiter keys.
- [ ] **Support incremental sync to update existing books and add new releases**
  - Verification: Run initial import, then run sync again - verify only new/updated books are processed. Check sync_metadata table for last_sync timestamps.
- [ ] **Admin interface displays import progress, statistics, and error handling**
  - Verification: Access /admin/ingestion dashboard, trigger import, verify real-time progress updates, job status display, and error reporting UI

## Technical Notes

### Approach

Create a Fastify plugin that wraps the Wolne Lektury REST API with proper error handling, rate limiting, and response validation using Zod schemas. Implement a job queue system using BullMQ to process book imports asynchronously, storing metadata in Supabase and full text content in chunked format optimized for LLM processing. Build admin endpoints for triggering imports and monitoring progress, with incremental sync capabilities to efficiently handle catalog updates.


### Files to Modify

- **path**: apps/backend/src/app.ts
- **changes**: Register wolne-lektury ingestion plugin and admin routes
- **path**: packages/database/src/schema.sql
- **changes**: Add books, book_chunks, and sync_metadata tables with indexes
- **path**: apps/backend/package.json
- **changes**: Add dependencies: axios, bullmq, cheerio, ioredis, zod

### New Files to Create

- **path**: apps/backend/src/plugins/ingestion/wolne-lektury.ts
- **purpose**: Main Fastify plugin with API client, rate limiting, and job queue setup
- **path**: apps/backend/src/services/wolne-lektury-api.ts
- **purpose**: API client service with request/response handling and validation
- **path**: apps/backend/src/services/content-processor.ts
- **purpose**: Text processing, chunking, and content optimization for LLM consumption
- **path**: apps/backend/src/routes/admin/ingestion.ts
- **purpose**: Admin endpoints for triggering imports, monitoring progress, and managing sync
- **path**: apps/backend/src/jobs/wolne-lektury-import.ts
- **purpose**: BullMQ job processors for handling book import tasks
- **path**: apps/backend/src/schemas/wolne-lektury.ts
- **purpose**: Zod schemas for API response validation and type safety
- **path**: packages/database/src/migrations/003_wolne_lektury_tables.sql
- **purpose**: Database migration for book-related tables and indexes
- **path**: apps/frontend/src/pages/admin/ingestion.tsx
- **purpose**: Admin UI for managing ingestion processes and monitoring status

### External Dependencies


- **axios** ^1.6.0

  - HTTP client for Wolne Lektury API calls with retry capabilities

- **zod** ^3.22.0

  - Runtime validation of API responses and data transformation

- **bullmq** ^5.0.0

  - Redis-based job queue for async book processing

- **cheerio** ^1.0.0-rc.12

  - HTML parsing if API returns formatted content that needs cleaning

- **iconv-lite** ^0.6.3

  - Character encoding handling for Polish text content

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/wolne-lektury-api.test.ts`
  - Scenarios: API response parsing and validation, Rate limiting logic, Error handling for network failures, Text chunking algorithms, Incremental sync logic
- **File**: `apps/backend/src/__tests__/services/content-processor.test.ts`
  - Scenarios: Text chunking with proper boundaries, Polish character encoding handling, Large content streaming
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/wolne-lektury-ingestion.test.ts`
  - Scenarios: End-to-end book import flow, Job queue processing with Redis, Database transactions and rollbacks, File storage integration for covers
- **File**: `apps/backend/src/__tests__/integration/admin-ingestion-routes.test.ts`
  - Scenarios: Admin endpoint authentication, Import triggering and status monitoring, Bulk operations handling
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

- **task**: Setup database schema and migrations for books, chunks, and sync metadata
- **done**: False
- **task**: Implement Wolne Lektury API client with rate limiting and error handling
- **done**: False
- **task**: Create content processor service for text chunking and optimization
- **done**: False
- **task**: Build BullMQ job queue system for async processing
- **done**: False
- **task**: Develop admin API endpoints for import management
- **done**: False
- **task**: Create admin UI for monitoring and controlling imports
- **done**: False
- **task**: Implement incremental sync logic and scheduling
- **done**: False
- **task**: Add comprehensive error handling and logging
- **done**: False
- **task**: Write unit and integration tests with high coverage
- **done**: False
- **task**: Document API endpoints and admin procedures
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Wolne Lektury (wolnelektury.pl) is Poland's largest free digital library containing public domain Polish literature classics. This integration enables Morpheus to automatically ingest high-quality literary works as source material for comic transformation, providing users with a curated catalog of classic novels, poems, and stories. This solves the cold-start problem by pre-populating the platform with culturally significant content while ensuring copyright compliance.

**Technical Approach:**
Implement a robust ingestion service using Fastify's plugin architecture with dedicated routes for Wolne Lektury API integration. Use their REST API (wolnelektury.pl/api/) to fetch book metadata, full text content, and cover images. Design an ETL pipeline with queue-based processing using Redis/BullMQ for handling bulk imports. Store normalized book data in Supabase with proper indexing for search and filtering. Implement incremental sync to handle updates and new releases from their catalog.

**Dependencies:**
- External: axios/node-fetch for API calls, zod for API response validation, bull/bullmq for job queuing, cheerio for HTML parsing if needed
- Internal: Database schemas in Supabase, content ingestion service, search indexing service, file storage service for cover images

**Risks:**
- Rate limiting: Wolne Lektury API may have undocumented limits; implement exponential backoff and respect headers
- Data format changes: API responses may evolve; use schema validation and graceful degradation
- Large content volumes: Full book texts can be massive; implement streaming and chunked processing
- Character encoding: Polish diacritics require proper UTF-8 handling throughout the pipeline

**Complexity Notes:**
Initially seems straightforward but complexity increases with scale. The API is well-documented but lacks official rate limits documentation. Text processing for comic adaptation will require sophisticated chunking strategies. Integration touches multiple system components (ingestion, storage, search, user content).

**Key Files:**
- apps/backend/src/plugins/ingestion/wolne-lektury.ts: Main API integration service
- apps/backend/src/routes/admin/ingestion.ts: Admin endpoints for triggering imports
- packages/database/src/schemas/books.sql: Book metadata schema
- apps/backend/src/services/content-processor.ts: Text processing and chunking logic


### Design Decisions

[{'decision': 'Use incremental sync with last-modified tracking', 'rationale': 'Wolne Lektury updates their catalog regularly; full re-imports would be wasteful and slow', 'alternatives_considered': ['Full periodic sync', 'Webhook-based updates (not available)', 'Manual imports only']}, {'decision': 'Store full text in PostgreSQL with proper chunking', 'rationale': 'Enables fast search and comic generation without external dependencies; PostgreSQL handles large text well', 'alternatives_considered': ['External text storage service', 'File-based storage', 'Vector database for embeddings']}, {'decision': 'Queue-based processing with job priorities', 'rationale': 'Large catalog requires async processing; priorities allow featuring popular books first', 'alternatives_considered': ['Synchronous processing', 'Batch processing without queues', 'Stream processing']}]
