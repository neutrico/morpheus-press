---
area: image-gen
dependsOn:
- T52
effort: 2
iteration: I4
key: T57
milestone: M3 - Content Generation Pipeline
priority: p0
title: Generation Progress Tracking
type: Task
---

# Generation Progress Tracking

## Acceptance Criteria

- [ ] **Real-time progress updates are delivered to clients within 500ms of state changes during comic generation**
  - Verification: WebSocket message timestamps show <500ms latency between progress events in browser dev tools
- [ ] **Progress tracking survives service restarts and maintains state consistency**
  - Verification: Restart backend service during generation, verify client reconnects and receives correct progress state from Redis
- [ ] **Fallback to SSE works when WebSocket connections fail**
  - Verification: Block WebSocket connections in browser, verify SSE endpoint delivers same progress data
- [ ] **All generation phases (QUEUED, ANALYZING, GENERATING, POST_PROCESSING, COMPLETE) report progress percentages**
  - Verification: Generate comic and verify progress events contain phase and percentage fields for each stage
- [ ] **RunPod webhook integration updates progress for external ML operations**
  - Verification: Mock RunPod webhook calls update Redis state and propagate to connected clients

## Technical Notes

### Approach

Create a centralized ProgressTracker service that manages job states in Redis with unique job IDs. Implement WebSocket endpoints for real-time client subscriptions and integrate RunPod webhook handlers for external progress updates. Use a structured event system with phases (QUEUED, ANALYZING, GENERATING, POST_PROCESSING, COMPLETE) and percentage completion within each phase. Build React hooks and components for seamless frontend integration with automatic reconnection handling.


### Files to Modify

- **path**: packages/backend/src/services/image-generation.service.ts
- **changes**: Integrate ProgressTracker calls at generation milestones
- **path**: packages/backend/src/routes/generation/index.ts
- **changes**: Add WebSocket and SSE progress endpoints
- **path**: packages/backend/src/config/redis.ts
- **changes**: Add progress-specific Redis configuration and TTL settings
- **path**: packages/frontend/src/pages/GenerationPage.tsx
- **changes**: Integrate ProgressTracker component and useGenerationProgress hook

### New Files to Create

- **path**: packages/backend/src/services/progress-tracker.service.ts
- **purpose**: Core progress management, Redis operations, client subscription handling
- **path**: packages/backend/src/routes/generation/progress.routes.ts
- **purpose**: WebSocket and SSE endpoint definitions for real-time progress updates
- **path**: packages/backend/src/types/generation.types.ts
- **purpose**: TypeScript definitions for progress events, job states, and phase enums
- **path**: packages/backend/src/integrations/runpod-webhook.handler.ts
- **purpose**: Handle RunPod webhook callbacks and translate to internal progress events
- **path**: packages/backend/src/middleware/progress-auth.middleware.ts
- **purpose**: Authentication middleware for WebSocket connections using JWT tokens
- **path**: packages/frontend/src/hooks/useGenerationProgress.ts
- **purpose**: React hook for WebSocket subscription, reconnection logic, and state management
- **path**: packages/frontend/src/components/ProgressTracker.tsx
- **purpose**: UI component with progress bar, phase indicators, and time estimates
- **path**: packages/frontend/src/utils/websocket-client.ts
- **purpose**: WebSocket client with automatic reconnection and SSE fallback logic
- **path**: packages/backend/src/utils/progress-calculator.ts
- **purpose**: Algorithms for calculating overall progress across multiple generation phases

### External Dependencies


- **socket.io** ^4.7.5

  - WebSocket server implementation with built-in fallbacks and room management

- **ioredis** ^5.3.2

  - Redis client for fast progress state storage and pub/sub capabilities

- **@fastify/websocket** ^8.3.0

  - Native Fastify WebSocket support for lightweight real-time communication

- **uuid** ^9.0.1

  - Generate unique job IDs for progress tracking correlation

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/services/progress-tracker.service.test.ts`
  - Scenarios: Job creation and state initialization, Progress updates and phase transitions, Client subscription management, Redis state persistence and retrieval, Job completion and cleanup
- **File**: `packages/backend/src/__tests__/integrations/runpod-webhook.handler.test.ts`
  - Scenarios: Valid webhook payload processing, Invalid webhook handling, Progress calculation from RunPod status
- **File**: `packages/frontend/src/__tests__/hooks/useGenerationProgress.test.ts`
  - Scenarios: WebSocket connection and subscription, Automatic reconnection on disconnect, SSE fallback activation, Progress state updates
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/progress-tracking.test.ts`
  - Scenarios: End-to-end WebSocket progress flow, Redis persistence across service restart, RunPod webhook to client propagation, Multiple client subscription handling
### E2E Tests

- **File**: `packages/e2e/src/generation-progress.spec.ts`
  - Scenarios: Full comic generation with progress tracking, Network interruption recovery, Multiple concurrent generations
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

- **task**: Setup Redis progress key structure and TTL configuration
- **done**: False
- **task**: Implement ProgressTracker service with job lifecycle management
- **done**: False
- **task**: Create WebSocket endpoints with authentication middleware
- **done**: False
- **task**: Build SSE fallback endpoint with same progress data
- **done**: False
- **task**: Implement RunPod webhook handler with progress translation
- **done**: False
- **task**: Create React hook with reconnection and fallback logic
- **done**: False
- **task**: Build ProgressTracker UI component with phase visualization
- **done**: False
- **task**: Integrate progress tracking into existing image generation flow
- **done**: False
- **task**: Implement comprehensive test suite (unit, integration, e2e)
- **done**: False
- **task**: Add monitoring and error logging for production debugging
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Generation Progress Tracking is critical for the comic generation pipeline where users need real-time feedback on long-running AI operations (text-to-image generation via RunPod Stable Diffusion, panel layout processing, story analysis). Without proper progress tracking, users face a black box experience during 30-60 second generation cycles, leading to abandonment and poor UX. This directly impacts user retention and platform credibility.

**Technical Approach:**
Implement a multi-layered progress system using WebSockets for real-time updates, Redis for progress state persistence, and a structured event system. Use Server-Sent Events (SSE) as WebSocket fallback. Create a progress management service that tracks generation jobs through distinct phases (queuing, processing, post-processing, completion) with percentage completion and estimated time remaining. Integrate with RunPod webhooks for external ML pipeline updates.

**Dependencies:**
- External: socket.io@4.7.5, ioredis@5.3.2, @fastify/websocket@8.3.0, uuid@9.0.1
- Internal: Supabase job tracking tables, authentication middleware, existing image generation service, notification system

**Risks:**
- WebSocket connection drops: Implement automatic reconnection with exponential backoff and SSE fallback
- Progress state inconsistency: Use Redis TTL with database backup for persistence across service restarts
- RunPod webhook reliability: Implement polling fallback mechanism for critical progress updates
- Memory leaks from uncleaned progress listeners: Proper cleanup on job completion/cancellation

**Complexity Notes:**
More complex than initially estimated due to need for fault-tolerant real-time communication, integration with external RunPod webhooks, and maintaining progress state across potential service restarts. The multi-phase nature of comic generation (story analysis → panel planning → image generation → post-processing) requires sophisticated progress calculation algorithms.

**Key Files:**
- packages/backend/src/services/progress-tracker.service.ts: Core progress management
- packages/backend/src/routes/generation/progress.routes.ts: WebSocket endpoints
- packages/backend/src/types/generation.types.ts: Progress event type definitions
- packages/frontend/src/hooks/useGenerationProgress.ts: React hook for progress subscription
- packages/frontend/src/components/ProgressTracker.tsx: UI component
- packages/backend/src/integrations/runpod-webhook.handler.ts: External progress updates


### Design Decisions

[{'decision': 'Use Redis for progress state with database backup', 'rationale': 'Provides fast real-time updates while ensuring persistence across service restarts', 'alternatives_considered': ['Memory-only storage', 'Database-only storage', 'Event sourcing pattern']}, {'decision': 'WebSockets with SSE fallback for client communication', 'rationale': 'WebSockets offer lowest latency for real-time updates, SSE ensures compatibility with restrictive networks', 'alternatives_considered': ['Polling-based updates', 'WebSockets only', 'SSE only']}, {'decision': 'Structured phase-based progress tracking', 'rationale': 'Comic generation has distinct phases with different time characteristics, allowing better user communication', 'alternatives_considered': ['Simple percentage completion', 'Time-based estimates only', 'Binary status updates']}]
