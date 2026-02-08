---
area: image-gen
dependsOn:
- T50
effort: 5
iteration: I4
key: T52
milestone: M3 - Content Generation Pipeline
priority: p0
title: Batch Image Generation
type: Feature
---

# Batch Image Generation

## Acceptance Criteria

- [ ] **System can process batch image generation requests with 10-50 images, grouping them efficiently and tracking individual status**
  - Verification: POST /api/image-gen/batch with 20 images returns batch job ID, WebSocket shows progress updates, all images complete within expected time
- [ ] **Real-time progress tracking shows completion status for individual images in a batch job**
  - Verification: WebSocket connection receives progress events with completed/failed/pending counts and individual image status updates
- [ ] **Failed individual images are retried with exponential backoff while successful ones remain completed**
  - Verification: Simulate RunPod API failures for subset of batch, verify retry logic triggers and only failed images are reprocessed
- [ ] **Batch processing handles memory constraints by chunking large requests**
  - Verification: Submit batch of 100 images, verify system processes in chunks of 10-20 and memory usage stays below threshold
- [ ] **System provides cost estimation and budget controls for batch operations**
  - Verification: API returns cost estimate before processing, batch jobs respect user budget limits and fail gracefully when exceeded

## Technical Notes

### Approach

Implement a multi-layered batch processing system with BullMQ handling job orchestration, chunked processing to manage resource usage, and WebSocket connections for real-time progress updates. The system will accept batch requests via REST API, queue them for processing, and use RunPod's batch inference capabilities to generate images in parallel while maintaining granular status tracking for each individual image.


### Files to Modify

- **path**: packages/backend/src/services/image-gen/image-service.ts
- **changes**: Add batch processing hooks and integration with batch processor
- **path**: packages/backend/src/database/models/image-job.ts
- **changes**: Add batch_job_id foreign key and batch-related status fields
- **path**: packages/backend/src/middleware/websocket.ts
- **changes**: Add batch progress event handlers and room management
- **path**: packages/shared/types/api.ts
- **changes**: Add batch request/response types and WebSocket event types

### New Files to Create

- **path**: packages/backend/src/services/image-gen/batch-processor.ts
- **purpose**: Core batch processing logic, chunking, and RunPod integration
- **path**: packages/backend/src/queues/image-batch-queue.ts
- **purpose**: BullMQ job definitions and queue management for batch operations
- **path**: packages/backend/src/routes/image-gen/batch.ts
- **purpose**: REST API endpoints for batch job CRUD operations
- **path**: packages/backend/src/services/cost-estimator.ts
- **purpose**: Calculate costs and enforce budget limits for batch operations
- **path**: packages/backend/src/database/models/batch-job.ts
- **purpose**: Database model for batch job tracking and status
- **path**: packages/frontend/src/components/batch-progress.tsx
- **purpose**: React component for real-time batch progress visualization
- **path**: packages/frontend/src/hooks/use-batch-progress.ts
- **purpose**: Custom hook for WebSocket-based progress tracking
- **path**: packages/shared/types/batch-job.ts
- **purpose**: Shared TypeScript types for batch job data structures

### External Dependencies


- **bullmq** ^5.0.0

  - Redis-based queue for batch job management with built-in retry and progress tracking

- **ioredis** ^5.3.0

  - Redis client for queue state management and caching batch results

- **ws** ^8.16.0

  - WebSocket server for real-time progress updates to frontend clients

- **p-limit** ^5.0.0

  - Control concurrency of RunPod API calls to prevent rate limiting

- **async-retry** ^1.3.3

  - Implement exponential backoff retry logic for failed image generations

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/services/batch-processor.test.ts`
  - Scenarios: Batch job creation and validation, Chunking strategy for different batch sizes, Retry logic with exponential backoff, Progress calculation and status updates, Error handling for RunPod API failures
- **File**: `packages/backend/src/__tests__/queues/image-batch-queue.test.ts`
  - Scenarios: Job enqueueing and dequeuing, Priority handling and batch grouping, Queue failure recovery
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/batch-image-generation.test.ts`
  - Scenarios: End-to-end batch processing with mocked RunPod, WebSocket progress updates during batch execution, Database state consistency across batch lifecycle, Cost calculation and budget enforcement
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

- **task**: Set up BullMQ infrastructure and Redis configuration for batch queues
- **done**: False
- **task**: Implement batch job database models and migrations
- **done**: False
- **task**: Create batch processor service with chunking and RunPod integration
- **done**: False
- **task**: Build REST API endpoints for batch job management
- **done**: False
- **task**: Implement WebSocket handlers for real-time progress updates
- **done**: False
- **task**: Create cost estimation service with budget controls
- **done**: False
- **task**: Build frontend batch progress UI components
- **done**: False
- **task**: Add retry logic with exponential backoff for failed generations
- **done**: False
- **task**: Implement comprehensive error handling and cleanup mechanisms
- **done**: False
- **task**: Write unit and integration tests
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Batch image generation is critical for the comic creation pipeline where multiple panels need to be generated simultaneously for a chapter or scene. Instead of generating images one-by-one (which is slow and expensive), batch processing allows for parallel generation, better resource utilization, and cost optimization through RunPod's batch inference capabilities. This is essential for production comics which may have 20-50 panels per chapter.

**Technical Approach:**
- Queue-based architecture using BullMQ for job management and Redis for state
- Implement batch grouping strategy (group by style, model, or user preference)
- Use RunPod's batch inference API with async/await patterns for parallel processing
- Implement progress tracking with WebSocket updates to frontend
- Add retry mechanisms with exponential backoff for failed generations
- Use streaming responses to show partial results as they complete
- Implement resource pooling to manage RunPod endpoint scaling

**Dependencies:**
- External: bullmq, ioredis, ws (WebSocket), p-limit, async-retry
- Internal: existing image-gen service, notification system, database models for batch jobs

**Risks:**
- Rate limiting: RunPod API limits could cause bottlenecks (implement queue throttling)
- Memory issues: Large batch processing could exhaust memory (implement chunking)
- Partial failures: Some images succeed, others fail (implement granular status tracking)
- Cost explosion: Batch jobs could rack up unexpected costs (implement budget controls)
- Timeout handling: Long-running batches may exceed request timeouts (use background processing)

**Complexity Notes:**
More complex than initially expected due to state management across multiple async operations, error recovery strategies, and the need for real-time progress updates. The queue management and WebSocket integration add significant architectural complexity.

**Key Files:**
- packages/backend/src/services/image-gen/batch-processor.ts: Core batch processing logic
- packages/backend/src/queues/image-batch-queue.ts: BullMQ job definitions
- packages/backend/src/routes/image-gen/batch.ts: API endpoints
- packages/frontend/src/components/batch-progress.tsx: Progress tracking UI
- packages/shared/types/batch-job.ts: Shared type definitions


### Design Decisions

[{'decision': 'Use BullMQ with Redis for job queue management', 'rationale': 'Provides robust job scheduling, retry logic, and progress tracking with minimal setup. Integrates well with existing Redis infrastructure.', 'alternatives_considered': ['AWS SQS', 'Custom queue implementation', 'PostgreSQL-based queue']}, {'decision': 'Implement chunked batch processing (max 10 images per chunk)', 'rationale': 'Prevents memory exhaustion and allows for better error isolation. RunPod performs better with smaller batches.', 'alternatives_considered': ['Single large batch', 'Dynamic chunk sizing', 'User-configurable chunks']}, {'decision': 'WebSocket-based progress updates', 'rationale': 'Real-time feedback is essential for user experience with long-running batch jobs. WebSockets provide low-latency updates.', 'alternatives_considered': ['Server-sent events', 'Polling-based updates', 'Email notifications only']}]
