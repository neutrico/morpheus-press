---
area: backend
dependsOn:
- T29
effort: 3
iteration: I3
key: T46
milestone: M1 - Backend Services
priority: p0
title: Error Recovery & Retries
type: Task
---

# Error Recovery & Retries

## Acceptance Criteria

- [ ] **HTTP client automatically retries transient failures (network, 5xx errors) with exponential backoff up to 3 attempts**
  - Verification: Unit test simulating network failures shows retry attempts with increasing delays. Integration test with mock server returning 503 then 200 succeeds on retry.
- [ ] **Service-level retries handle API rate limits (429) and quota exceeded errors with appropriate backoff strategies for each provider**
  - Verification: Integration tests with OpenAI/Anthropic/RunPod mock servers returning rate limit errors show provider-specific retry behavior. Verify OpenAI uses 60s backoff, Anthropic uses exponential backoff.
- [ ] **Job queue retries failed comic generation tasks up to 5 times with exponential backoff, maintaining job state and user notifications**
  - Verification: E2E test creating comic generation job that fails 3 times then succeeds shows job retries, state persistence in Supabase, and websocket notifications to user.
- [ ] **Circuit breaker opens after 5 consecutive failures to external service, stays open for 30s, then allows single test request**
  - Verification: Integration test simulating external service downtime shows circuit breaker state transitions logged with metrics. Manual verification of circuit breaker dashboard showing open/closed states.
- [ ] **Comprehensive observability captures retry patterns, failure rates, and costs with structured logs and Prometheus metrics**
  - Verification: Load test generating 100 comics with 20% artificial failure rate produces detailed retry metrics dashboard. Verify retry_attempts_total, circuit_breaker_state, and retry_cost_estimate metrics.

## Technical Notes

### Approach

Create a layered retry system starting with HTTP-level retries via axios-retry for transient failures, service-level retries with custom decorators for business logic failures, and job queue retries for long-running comic generation tasks. Implement circuit breakers to prevent cascade failures and use Redis for shared state across backend instances. Add comprehensive observability with structured logs and metrics to monitor retry patterns and identify problematic external services.


### Files to Modify

- **path**: packages/backend/src/plugins/http-client.ts
- **changes**: Add axios-retry configuration with exponential backoff, service-specific retry conditions
- **path**: packages/backend/src/services/ai/openai-client.ts
- **changes**: Add @Retry decorator with OpenAI-specific retry strategy (rate limits, quota exceeded)
- **path**: packages/backend/src/services/ai/anthropic-client.ts
- **changes**: Add @Retry decorator with Anthropic-specific retry strategy
- **path**: packages/backend/src/services/image/runpod-client.ts
- **changes**: Add @Retry decorator for Stable Diffusion API failures and timeouts
- **path**: packages/backend/src/queues/comic-generation-queue.ts
- **changes**: Configure Bull queue retry settings, add job state persistence, error handling
- **path**: packages/backend/src/plugins/observability.ts
- **changes**: Add retry metrics, structured logging for retry events, cost tracking

### New Files to Create

- **path**: packages/backend/src/lib/retry/retry-decorator.ts
- **purpose**: Decorator factory for service-level retry logic with provider-specific strategies
- **path**: packages/backend/src/lib/retry/circuit-breaker.ts
- **purpose**: Circuit breaker implementation with Redis state sharing across instances
- **path**: packages/backend/src/lib/retry/backoff-strategies.ts
- **purpose**: Exponential backoff, jitter, and provider-specific timing strategies
- **path**: packages/backend/src/lib/retry/dead-letter-queue.ts
- **purpose**: Handler for permanently failed jobs, admin review interface
- **path**: packages/backend/src/lib/retry/retry-config.ts
- **purpose**: Centralized retry configuration for all services and HTTP clients
- **path**: packages/backend/src/lib/retry/cost-tracker.ts
- **purpose**: Track API costs from retry attempts, budget enforcement
- **path**: packages/backend/src/__tests__/fixtures/mock-ai-servers.ts
- **purpose**: Mock HTTP servers simulating various AI service failure modes for testing

### External Dependencies


- **axios-retry** ^4.0.0

  - HTTP-level retry with exponential backoff for API calls

- **p-retry** ^6.2.0

  - Promise-based retry utility for custom service logic

- **ioredis** ^5.3.2

  - Redis client for circuit breaker state and job queue backend

- **@bull-board/api** ^5.10.2

  - Queue monitoring dashboard for retry job inspection

- **prom-client** ^15.1.0

  - Prometheus metrics for retry rates, success/failure ratios

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/lib/retry.test.ts`
  - Scenarios: Exponential backoff calculation with jitter, Retry decorator success after failures, Circuit breaker state transitions, Dead letter queue job handling
- **File**: `packages/backend/src/__tests__/services/ai-client.test.ts`
  - Scenarios: OpenAI rate limit retry with 60s backoff, Anthropic exponential backoff retry, Permanent failure after max retries, Successful retry after transient failure
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/retry-system.test.ts`
  - Scenarios: End-to-end comic generation with AI service failures and recovery, Circuit breaker prevents cascade failures during service outage, Dead letter queue captures permanently failed jobs, Job queue maintains state across retries
- **File**: `packages/backend/src/__tests__/integration/external-services.test.ts`
  - Scenarios: HTTP client retry behavior with real external service failures, Service-specific retry strategies for each AI provider
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 7.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Install retry dependencies (axios-retry, p-retry, ioredis circuit breaker)
- **done**: False
- **task**: Implement core retry utilities and backoff strategies
- **done**: False
- **task**: Create retry decorator with provider-specific configurations
- **done**: False
- **task**: Add HTTP client retry configuration to Fastify plugin
- **done**: False
- **task**: Implement circuit breaker with Redis shared state
- **done**: False
- **task**: Configure Bull queue retry strategies for comic generation
- **done**: False
- **task**: Add service-level retry decorators to AI clients
- **done**: False
- **task**: Implement dead letter queue and cost tracking
- **done**: False
- **task**: Add comprehensive observability (metrics, structured logs)
- **done**: False
- **task**: Create unit and integration tests with mock failure scenarios
- **done**: False
- **task**: Perform manual testing with real external service failures
- **done**: False
- **task**: Update API documentation with retry behavior details
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Error recovery & retries are critical for Morpheus due to its heavy reliance on external services (OpenAI/Anthropic APIs, RunPod Stable Diffusion, Supabase) and the long-running nature of novel-to-comic transformations. Users expect resilient processing when API rate limits are hit, network issues occur, or ML services are temporarily unavailable. Without proper retry mechanisms, failed transformations would require manual intervention and create poor user experience.

**Technical Approach:**
Implement a multi-layered retry strategy using exponential backoff with jitter:
1. **HTTP Client Level**: Axios interceptors for transient failures (network, 5xx errors)
2. **Service Level**: Custom retry decorators for business logic (rate limits, quota exceeded)
3. **Job Queue Level**: Bull Queue with job retry configuration for long-running tasks
4. **Circuit Breaker**: Prevent cascade failures when external services are down
5. **Dead Letter Queue**: Capture permanently failed jobs for manual review
6. **Observability**: Structured logging and metrics for retry patterns

**Dependencies:**
- External: axios-retry, p-retry, bullmq, ioredis, pino logger
- Internal: Existing Fastify plugins, Supabase client, OpenAI/Anthropic service wrappers

**Risks:**
- **API Cost Explosion**: Aggressive retries could multiply API costs; mitigation via retry budgets and circuit breakers
- **Resource Exhaustion**: Too many concurrent retries; mitigation via queue concurrency limits and backpressure
- **Data Inconsistency**: Partial failures in multi-step operations; mitigation via idempotent operations and transaction boundaries
- **Observability Gaps**: Hard to debug retry storms; mitigation via detailed metrics and distributed tracing

**Complexity Notes:**
Higher complexity than initially estimated due to the heterogeneous nature of external services (each has different failure modes, rate limits, and optimal retry strategies). The async nature of comic generation adds complexity as retries need to maintain job state and user notifications.

**Key Files:**
- packages/backend/src/lib/retry/: Core retry utilities and decorators
- packages/backend/src/services/ai/: Add retry logic to LLM clients  
- packages/backend/src/services/image/: Add retry logic to Stable Diffusion client
- packages/backend/src/queues/: Configure Bull queue retry strategies
- packages/backend/src/plugins/http-client.ts: Axios retry configuration


### Design Decisions

[{'decision': 'Use Bull Queue built-in retry with custom exponential backoff', 'rationale': 'Leverages existing queue infrastructure, provides job persistence, and allows per-job retry configuration', 'alternatives_considered': ['Custom retry service', 'AWS SQS with DLQ', 'Simple setTimeout recursion']}, {'decision': 'Implement service-specific retry strategies rather than generic approach', 'rationale': 'OpenAI rate limits differ from RunPod availability issues - each needs tailored backoff and circuit breaking', 'alternatives_considered': ['Single unified retry service', 'Client-side retry only', 'No retries, fail fast']}, {'decision': 'Use circuit breaker pattern with Redis state storage', 'rationale': 'Prevents retry storms across multiple backend instances and provides fast failure when services are known to be down', 'alternatives_considered': ['In-memory circuit breaker', 'No circuit breaking', 'Database-backed state']}]
