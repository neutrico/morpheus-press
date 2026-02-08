---
area: ingestion
dependsOn:
- T38
effort: 3
iteration: I3
key: T45
milestone: M1 - Backend Services
priority: p0
title: Book Status & Progress Tracking
type: Feature
---

# Book Status & Progress Tracking

## Acceptance Criteria

- [ ] **Book status progresses through defined states (UPLOADED → ANALYZING → GENERATING_SCENES → CREATING_ARTWORK → COMPLETED) with atomic state transitions**
  - Verification: Run integration test `npm run test -- BookStatusService.integration.test.ts` and verify state machine transitions work correctly
- [ ] **Real-time progress updates are delivered to frontend clients within 500ms of backend state changes**
  - Verification: Manual test: Upload book, monitor WebSocket messages in browser dev tools, measure time between backend log and frontend update
- [ ] **System recovers from failures and resumes processing from last known good state without data loss**
  - Verification: Integration test simulating service crashes at each state, verify resume functionality with `npm run test -- failure-recovery.test.ts`
- [ ] **Progress tracking shows overall percentage (0-100%) and detailed substep information for each processing stage**
  - Verification: Check API response at `GET /api/books/{id}/status` contains `overall_progress`, `current_stage`, and `substeps` fields
- [ ] **System handles concurrent status updates for multiple books without race conditions**
  - Verification: Load test with `k6 run tests/load/concurrent-status-updates.js` processing 10+ books simultaneously

## Technical Notes

### Approach

Create a BookStatusService that manages a finite state machine with states like UPLOADED, ANALYZING, GENERATING_SCENES, CREATING_ARTWORK, COMPLETED, FAILED. Each ML processing service publishes progress events to Redis, which the status service consumes to update PostgreSQL state and trigger Supabase real-time notifications. Implement progress tracking with both overall percentage and detailed substep information, using database transactions for atomic state updates and retry mechanisms for failed transitions.


### Files to Modify

- **path**: packages/backend/src/app.ts
- **changes**: Add BookStatusService initialization and Redis connection setup
- **path**: packages/backend/src/routes/books/index.ts
- **changes**: Import and mount status routes at /books/:id/status
- **path**: packages/backend/src/services/MLProcessingService.ts
- **changes**: Add progress event publishing to Redis at each processing step
- **path**: packages/shared/src/types/Book.ts
- **changes**: Add BookStatus enum and BookProgress interface definitions
- **path**: packages/frontend/src/hooks/useBookStatus.ts
- **changes**: Add Supabase subscription for real-time status updates

### New Files to Create

- **path**: packages/backend/src/services/BookStatusService.ts
- **purpose**: Core status management with finite state machine logic and Redis integration
- **path**: packages/backend/src/models/BookStatus.ts
- **purpose**: PostgreSQL schema definitions and database operations for book status
- **path**: packages/backend/src/routes/books/status.ts
- **purpose**: REST API endpoints for status queries and manual status operations
- **path**: packages/backend/src/events/BookStatusEvents.ts
- **purpose**: Event type definitions and Redis pub/sub message schemas
- **path**: packages/database/migrations/20240115_add_book_status_tables.sql
- **purpose**: Create book_status and book_progress tables with indexes
- **path**: packages/frontend/src/components/ProgressTracker.tsx
- **purpose**: Real-time progress visualization with progress bars and status messages
- **path**: packages/frontend/src/components/StatusIndicator.tsx
- **purpose**: Book status badge/indicator component with state-specific styling
- **path**: packages/backend/src/lib/StateMachine.ts
- **purpose**: Generic finite state machine implementation with validation and guards

### External Dependencies


- **@xstate/fsm** ^2.0.0

  - Lightweight finite state machine for managing book processing states

- **ioredis** ^5.3.2

  - Redis client for high-frequency progress updates and pub/sub

- **bullmq** ^4.15.0

  - Queue management with built-in progress tracking and job state persistence

- **zod** ^3.22.4

  - Runtime validation for status transitions and progress data

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/services/BookStatusService.test.ts`
  - Scenarios: State machine transitions (happy path), Invalid state transition rejection, Progress update calculations, Event emission on state changes, Error handling and rollback
- **File**: `packages/backend/src/__tests__/models/BookStatus.test.ts`
  - Scenarios: Database schema validation, Status enum type safety, Progress percentage bounds checking
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/book-status-flow.test.ts`
  - Scenarios: Complete book processing pipeline with status updates, Redis event publishing and consumption, Supabase real-time notification delivery, Database transaction rollback on failures, Concurrent book processing status isolation
- **File**: `packages/backend/src/__tests__/integration/status-api.test.ts`
  - Scenarios: REST API endpoints return correct status data, WebSocket subscription receives real-time updates
### Manual Testing


## Estimates

- **Development**: 4.5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 7.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Create database migration for book_status and book_progress tables
- **done**: False
- **task**: Implement BookStatus model with PostgreSQL operations
- **done**: False
- **task**: Build BookStatusService with finite state machine logic
- **done**: False
- **task**: Create Redis event publishing/subscription system
- **done**: False
- **task**: Implement REST API endpoints for status queries
- **done**: False
- **task**: Add Supabase real-time subscription integration
- **done**: False
- **task**: Build frontend ProgressTracker component with WebSocket updates
- **done**: False
- **task**: Integrate status updates into existing ML processing services
- **done**: False
- **task**: Write comprehensive unit and integration tests
- **done**: False
- **task**: Add error handling and failure recovery mechanisms
- **done**: False
- **task**: Create API documentation and usage examples
- **done**: False
- **task**: Conduct load testing and performance optimization
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Book status & progress tracking is critical for the novel-to-comic transformation pipeline. Users need visibility into where their book is in the processing workflow (uploaded, analyzing, generating scenes, creating artwork, etc.), while the system needs robust state management to handle failures, retries, and resume operations. This enables better UX through progress indicators and reliable processing through state persistence.

**Technical Approach:**
Implement a state machine pattern using a PostgreSQL-backed status system with real-time updates via Supabase subscriptions. Create an event-driven architecture where each processing stage emits progress events that update both database state and notify frontend clients. Use enum-based status types for type safety and implement progress tracking with percentage completion and detailed substep information.

**Dependencies:**
- External: [@xstate/fsm, ioredis, bull/bullmq]
- Internal: [supabase client, ML processing services, ingestion pipeline, dashboard components]

**Risks:**
- State inconsistency: Implement atomic updates and event sourcing with rollback capabilities
- Real-time update performance: Use Redis for high-frequency updates, batch database writes
- Complex state transitions: Define clear FSM with validation rules and transition guards
- Long-running process failures: Implement heartbeat mechanism and timeout detection

**Complexity Notes:**
More complex than initially estimated due to need for robust failure handling, real-time updates, and coordination across multiple async ML services. The state machine aspect adds architectural complexity but provides better reliability.

**Key Files:**
- packages/backend/src/services/BookStatusService.ts: Core status management logic
- packages/backend/src/models/BookStatus.ts: Database schema and types
- packages/backend/src/routes/books/status.ts: REST API endpoints
- packages/database/migrations/: New status and progress tables
- packages/frontend/src/components/ProgressTracker.tsx: Real-time progress UI


### Design Decisions

[{'decision': 'Use finite state machine pattern with PostgreSQL persistence', 'rationale': 'Provides predictable state transitions, easy debugging, and reliable persistence with ACID guarantees', 'alternatives_considered': ['Event sourcing only', 'Simple status flags', 'Redis-only state']}, {'decision': 'Hybrid real-time updates (Redis + Supabase subscriptions)', 'rationale': 'Redis handles high-frequency ML progress updates, Supabase provides reliable real-time UI updates', 'alternatives_considered': ['Supabase only', 'WebSocket implementation', 'Polling-based updates']}, {'decision': 'Hierarchical progress tracking (stage + substeps)', 'rationale': 'Provides detailed progress visibility while maintaining simple high-level status', 'alternatives_considered': ['Simple percentage only', 'Event log based', 'Milestone checkpoints']}]
