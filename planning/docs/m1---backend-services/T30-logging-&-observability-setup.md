---
area: backend
dependsOn: []
effort: 2
iteration: I2
key: T30
milestone: M1 - Backend Services
priority: p0
title: Logging & Observability Setup
type: Task
---

# Logging & Observability Setup

## Acceptance Criteria

- [ ] **All HTTP requests have correlation IDs that propagate through ML pipeline stages and external API calls**
  - Verification: Check logs for correlation_id field in request/response pairs, verify same ID appears in RunPod/OpenAI API call logs
- [ ] **Health check endpoint returns detailed status of all dependencies (Supabase, RunPod, OpenAI/Anthropic APIs) with <100ms response time**
  - Verification: GET /health returns 200 with dependency statuses, measure response time with wrk or similar tool
- [ ] **Prometheus metrics are exposed for ML pipeline performance (request duration, API costs, error rates) with proper labels**
  - Verification: GET /metrics shows morpheus_* metrics with service/operation/status labels, verify in Grafana dashboard
- [ ] **Structured logs exclude sensitive data (API keys, user content, novel text) while maintaining debugging capability**
  - Verification: Search logs for patterns matching API keys/PII, verify no sensitive data leakage in production logs
- [ ] **Log levels are configurable per environment with production using INFO+ and development using DEBUG**
  - Verification: Set LOG_LEVEL=debug in dev, verify debug logs appear; set LOG_LEVEL=info in prod, verify debug logs filtered

## Technical Notes

### Approach

Create a comprehensive observability stack using Fastify plugins that integrate Pino structured logging, OpenTelemetry tracing, and Prometheus metrics. Implement correlation ID propagation from HTTP requests through ML pipeline stages, with custom instrumentation for RunPod and LLM API calls. Build health check endpoints that monitor all dependencies (Supabase, external APIs, ML services) and provide detailed system status. Use environment-based configuration to control log levels and sampling rates for optimal performance in production.


### Files to Modify

- **path**: packages/backend/src/server.ts
- **changes**: Register logging, metrics, and tracing plugins before routes
- **path**: packages/backend/src/services/ml/text-generation.ts
- **changes**: Add correlation ID propagation and metrics tracking to LLM calls
- **path**: packages/backend/src/services/ml/image-generation.ts
- **changes**: Instrument RunPod API calls with tracing and error logging
- **path**: packages/backend/src/services/database.ts
- **changes**: Add database connection health checks and query performance metrics

### New Files to Create

- **path**: packages/backend/src/plugins/logging.ts
- **purpose**: Fastify plugin for Pino structured logging with correlation IDs
- **path**: packages/backend/src/plugins/metrics.ts
- **purpose**: Prometheus metrics collection for ML operations and system health
- **path**: packages/backend/src/plugins/tracing.ts
- **purpose**: OpenTelemetry distributed tracing setup for microservice correlation
- **path**: packages/backend/src/lib/logger.ts
- **purpose**: Logger configuration and sensitive data redaction utilities
- **path**: packages/backend/src/routes/health.ts
- **purpose**: Health check endpoint with dependency monitoring
- **path**: packages/backend/src/lib/observability/correlation.ts
- **purpose**: Correlation ID management and async context propagation
- **path**: packages/backend/src/lib/observability/metrics.ts
- **purpose**: Custom metrics definitions for ML pipeline operations
- **path**: packages/shared/src/types/telemetry.ts
- **purpose**: Shared types for telemetry data structures and configuration
- **path**: packages/backend/src/config/observability.ts
- **purpose**: Environment-based configuration for logging, metrics, and tracing

### External Dependencies


- **pino** ^8.17.0

  - High-performance structured logging with minimal overhead for ML workloads

- **@opentelemetry/api** ^1.7.0

  - Distributed tracing across novel transformation pipeline stages

- **@opentelemetry/auto-instrumentations-node** ^0.40.0

  - Automatic instrumentation for HTTP, database, and external API calls

- **prom-client** ^15.1.0

  - Prometheus metrics collection for performance monitoring and alerting

- **@fastify/under-pressure** ^8.3.0

  - Health checks and circuit breaker functionality for ML service dependencies

- **pino-pretty** ^10.3.0

  - Development-friendly log formatting (dev dependency)

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/plugins/logging.test.ts`
  - Scenarios: Correlation ID generation and propagation, Sensitive data redaction, Log level filtering, Request/response logging format
- **File**: `packages/backend/src/__tests__/plugins/metrics.test.ts`
  - Scenarios: Prometheus metrics registration, Custom metrics for ML operations, Metric labels and values, Performance overhead measurement
- **File**: `packages/backend/src/__tests__/lib/logger.test.ts`
  - Scenarios: Logger configuration per environment, Structured log format validation, Child logger creation with context
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/observability.test.ts`
  - Scenarios: End-to-end request tracing through ML pipeline, Health check with real dependency calls, Metrics collection during ML operations, OpenTelemetry span creation and propagation
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

- **task**: Install dependencies (@opentelemetry/*, pino, prometheus-client, fastify plugins)
- **done**: False
- **task**: Create logger configuration with environment-based levels and sensitive data redaction
- **done**: False
- **task**: Implement Fastify logging plugin with correlation ID generation and request/response logging
- **done**: False
- **task**: Setup Prometheus metrics plugin with custom ML operation metrics
- **done**: False
- **task**: Configure OpenTelemetry tracing for distributed request correlation
- **done**: False
- **task**: Build health check endpoint with dependency monitoring (Supabase, external APIs)
- **done**: False
- **task**: Instrument ML services with correlation ID propagation and performance metrics
- **done**: False
- **task**: Add sensitive data redaction to all log outputs
- **done**: False
- **task**: Create comprehensive test suite for all observability components
- **done**: False
- **task**: Document observability configuration and debugging procedures
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Morpheus processes complex ML workloads (LLM text generation, Stable Diffusion image generation) with external API dependencies and async operations. Without proper logging and observability, debugging production issues, monitoring performance bottlenecks, tracking API costs, and ensuring SLA compliance becomes nearly impossible. This is critical for M1 as it establishes the foundation for reliable backend services before adding more complex features.

**Technical Approach:**
- Structured logging with correlation IDs for request tracing across microservices
- OpenTelemetry for distributed tracing (especially important for ML pipeline observability)
- Prometheus metrics + Grafana dashboards for real-time monitoring
- Custom Fastify plugins for request logging, error tracking, and performance metrics
- Supabase integration for application-level audit logs
- Health check endpoints with dependency status monitoring
- Log aggregation with different levels (DEBUG for dev, INFO+ for production)

**Dependencies:**
- External: @opentelemetry/*, pino, prometheus-client, @fastify/sensible
- Internal: Database connection pool monitoring, ML service status checks, authentication middleware integration

**Risks:**
- Performance overhead: excessive logging can impact ML processing latency
- Log volume explosion: unstructured logs from ML operations could overwhelm storage
- Sensitive data leakage: novel content, API keys, user data in logs
- Missing context: async ML jobs losing trace correlation
- Cost implications: verbose logging increasing infrastructure costs

**Complexity Notes:**
Higher complexity than typical logging setup due to:
1. ML pipeline observability requirements (RunPod, OpenAI/Anthropic API monitoring)
2. Cross-service correlation (backend → ML services → external APIs)
3. Performance-sensitive operations requiring selective instrumentation
4. Multi-tenant data isolation in logs

**Key Files:**
- packages/backend/src/plugins/logging.ts: Core logging plugin
- packages/backend/src/plugins/metrics.ts: Prometheus metrics
- packages/backend/src/plugins/tracing.ts: OpenTelemetry setup
- packages/backend/src/lib/logger.ts: Logger configuration
- packages/backend/src/routes/health.ts: Health check endpoint
- packages/shared/src/types/telemetry.ts: Shared telemetry types


### Design Decisions

[{'decision': 'Use Pino for structured logging with OpenTelemetry for tracing', 'rationale': 'Pino offers excellent performance for high-throughput ML operations, OpenTelemetry provides vendor-neutral observability for complex async workflows', 'alternatives_considered': ['Winston + Jaeger', 'Built-in console logging', 'DataDog APM only']}, {'decision': 'Implement correlation ID propagation through ML pipeline', 'rationale': 'Essential for debugging failed transformations across novel→analysis→image generation→comic assembly stages', 'alternatives_considered': ['Service-level logging only', 'Database-based tracking', 'External correlation service']}, {'decision': 'Custom Fastify plugins for telemetry integration', 'rationale': 'Provides seamless integration with existing Fastify 5 architecture and allows fine-grained control over what gets instrumented', 'alternatives_considered': ['Express.js middleware patterns', 'Global instrumentation', 'Route-level manual logging']}]
