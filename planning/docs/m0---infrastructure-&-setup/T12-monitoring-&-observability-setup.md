---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T12
milestone: M0 - Infrastructure & Setup
priority: p0
title: Monitoring & Observability Setup
type: Task
---

# Monitoring & Observability Setup

## Acceptance Criteria

- [ ] **All API endpoints and ML service calls are instrumented with OpenTelemetry traces**
  - Verification: Run `curl -X POST http://localhost:3000/api/comics/transform` and verify traces appear in Grafana with spans for LLM calls, image generation, and database operations
- [ ] **Correlation IDs track user requests across the entire comic transformation pipeline**
  - Verification: Generate a comic and verify the same correlation ID appears in logs from frontend, API, ML services, and database operations
- [ ] **Custom business metrics are collected for ML operations including cost tracking**
  - Verification: Check Prometheus metrics endpoint `/metrics` contains `morpheus_openai_tokens_total`, `morpheus_comic_generation_duration_seconds`, and `morpheus_transformation_success_rate`
- [ ] **Error tracking captures and correlates failures across services**
  - Verification: Trigger an OpenAI API failure and verify Sentry shows the error with full context including user ID, comic ID, and request traces
- [ ] **Grafana dashboards display system health and business metrics**
  - Verification: Access Grafana at http://localhost:3001 and verify dashboards show API response times, ML service costs, comic generation success rates, and system resource usage

## Technical Notes

### Approach

Set up OpenTelemetry SDK in both Fastify backend and Next.js applications with auto-instrumentation for HTTP, database, and external API calls. Create custom spans for ML operations (LLM requests, image generation) with cost and performance metrics. Implement correlation IDs to trace user requests across comic transformation pipelines. Deploy Prometheus for metrics collection, Grafana for dashboards, and integrate Sentry for real-time error tracking and performance monitoring.


### Files to Modify

- **path**: apps/api/src/app.ts
- **changes**: Add OpenTelemetry plugin registration and correlation ID middleware
- **path**: apps/api/src/routes/comics.ts
- **changes**: Add custom spans for comic transformation pipeline with business metrics
- **path**: apps/dashboard/next.config.js
- **changes**: Add instrumentation configuration and Sentry integration
- **path**: apps/storefront/next.config.js
- **changes**: Add basic telemetry for public-facing metrics
- **path**: packages/ml-clients/src/openai.ts
- **changes**: Instrument LLM calls with token usage and cost tracking
- **path**: packages/ml-clients/src/stable-diffusion.ts
- **changes**: Add tracing for image generation requests with performance metrics
- **path**: packages/supabase/src/client.ts
- **changes**: Add database operation instrumentation and query performance tracking

### New Files to Create

- **path**: packages/observability/src/index.ts
- **purpose**: Main observability package exports and initialization
- **path**: packages/observability/src/instrumentation.ts
- **purpose**: OpenTelemetry SDK configuration and auto-instrumentation setup
- **path**: packages/observability/src/metrics.ts
- **purpose**: Custom business metrics definitions and collection utilities
- **path**: packages/observability/src/tracing.ts
- **purpose**: Distributed tracing utilities and span helpers
- **path**: packages/observability/src/logging.ts
- **purpose**: Structured logging configuration with correlation ID support
- **path**: packages/observability/src/sanitization.ts
- **purpose**: Data sanitization middleware to prevent secret exposure
- **path**: apps/api/src/plugins/telemetry.ts
- **purpose**: Fastify plugin for OpenTelemetry integration
- **path**: apps/dashboard/instrumentation.ts
- **purpose**: Next.js instrumentation configuration for frontend telemetry
- **path**: apps/storefront/instrumentation.ts
- **purpose**: Storefront-specific observability setup
- **path**: docker-compose.monitoring.yml
- **purpose**: Local development stack for Prometheus, Grafana, and Jaeger
- **path**: grafana/dashboards/morpheus-system.json
- **purpose**: System health and performance dashboard configuration
- **path**: grafana/dashboards/morpheus-business.json
- **purpose**: Business metrics dashboard for comic generation analytics
- **path**: prometheus/prometheus.yml
- **purpose**: Prometheus configuration for metrics collection

### External Dependencies


- **@opentelemetry/api** ^1.7.0

  - Core OpenTelemetry API for instrumentation

- **@opentelemetry/sdk-node** ^0.45.0

  - Node.js OpenTelemetry SDK with auto-instrumentation

- **@sentry/node** ^7.80.0

  - Error tracking and APM for Fastify backend

- **@sentry/nextjs** ^7.80.0

  - Error tracking and performance monitoring for Next.js apps

- **pino** ^8.16.0

  - High-performance structured logging for Node.js

- **prometheus-api-metrics** ^3.2.2

  - Prometheus metrics middleware for Fastify

## Testing

### Unit Tests

- **File**: `packages/observability/src/__tests__/instrumentation.test.ts`
  - Scenarios: OpenTelemetry span creation and attributes, Correlation ID generation and propagation, Metric collection and labeling, Log sanitization for sensitive data
- **File**: `packages/observability/src/__tests__/metrics.test.ts`
  - Scenarios: Custom metric registration, Business metric calculation, Cost tracking accuracy
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/observability.test.ts`
  - Scenarios: End-to-end trace propagation through comic generation, Database operation instrumentation, External ML service call tracing
- **File**: `apps/dashboard/src/__tests__/integration/telemetry.test.ts`
  - Scenarios: Frontend trace collection and export, User interaction tracking, Error boundary integration with Sentry
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

- **task**: Create observability package with OpenTelemetry SDK configuration
- **done**: False
- **task**: Implement correlation ID middleware and propagation utilities
- **done**: False
- **task**: Set up structured logging with Pino and log sanitization
- **done**: False
- **task**: Instrument Fastify API with custom spans and business metrics
- **done**: False
- **task**: Configure Next.js applications with frontend telemetry
- **done**: False
- **task**: Add instrumentation to ML service clients (OpenAI, Stable Diffusion)
- **done**: False
- **task**: Integrate Sentry for error tracking and performance monitoring
- **done**: False
- **task**: Create Docker Compose stack for local monitoring services
- **done**: False
- **task**: Build Grafana dashboards for system and business metrics
- **done**: False
- **task**: Configure Prometheus metrics collection and alerting rules
- **done**: False
- **task**: Test end-to-end observability pipeline with sample comic generation
- **done**: False
- **task**: Document observability setup and troubleshooting guide
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Monitoring & observability is critical for a production ML/AI platform like Morpheus that processes novel-to-comic transformations. This task solves visibility into system health, performance bottlenecks, error tracking, and user behavior across the complex pipeline involving LLM calls, image generation, database operations, and multi-service architecture. Without proper observability, debugging production issues, optimizing expensive ML operations, and ensuring SLA compliance becomes nearly impossible.

**Technical Approach:**
Implement a three-pillar observability stack: metrics (Prometheus/OpenTelemetry), logs (structured JSON with correlation IDs), and traces (distributed tracing across Fastify backend, Next.js frontend, and external ML services). Use OpenTelemetry as the unified collection layer, with Grafana for dashboards and AlertManager for notifications. Integrate application performance monitoring (APM) specifically for expensive operations like LLM calls and Stable Diffusion requests. Include business metrics like transformation success rates, processing times per comic page, and cost tracking for OpenAI/RunPod usage.

**Dependencies:**
- External: @opentelemetry/api, @opentelemetry/sdk-node, @sentry/node, @sentry/nextjs, pino (structured logging), prometheus-api-metrics, grafana/faro-web-sdk
- Internal: Authentication middleware (for user correlation), ML service wrappers, Supabase client adapters, shared types package

**Risks:**
- Performance overhead: OpenTelemetry instrumentation can add 5-15ms latency; mitigate with sampling strategies and async batching
- Data volume explosion: ML operations generate verbose logs; implement log level filtering and retention policies
- Secret exposure: API keys/tokens in traces; use sanitization middleware and secure trace exporters
- Vendor lock-in: Avoid proprietary agents; stick to OpenTelemetry standard for portability

**Complexity Notes:**
More complex than initially estimated due to distributed tracing across external ML services (OpenAI, RunPod) and correlation of async comic generation pipelines. The multi-tenant nature (users, comics, pages) requires sophisticated tagging strategies. However, the TypeScript monorepo structure simplifies shared observability utilities.

**Key Files:**
- packages/observability/: Shared instrumentation utilities and types
- apps/api/src/plugins/telemetry.ts: Fastify OpenTelemetry plugin
- apps/dashboard/instrumentation.ts: Next.js OpenTelemetry configuration
- apps/storefront/instrumentation.ts: Storefront observability setup
- packages/ml-clients/: Add instrumentation to LLM and SD wrappers
- docker-compose.monitoring.yml: Local Prometheus/Grafana stack


### Design Decisions

[{'decision': 'OpenTelemetry as primary observability framework', 'rationale': 'Vendor-neutral, comprehensive tracing/metrics, excellent TypeScript support, works across Fastify/Next.js', 'alternatives_considered': ['Datadog APM (expensive)', 'New Relic (vendor lock-in)', 'Custom Prometheus setup (limited tracing)']}, {'decision': 'Sentry for error tracking and performance monitoring', 'rationale': 'Best-in-class error tracking, React/Next.js integration, reasonable pricing for startups', 'alternatives_considered': ['Bugsnag', 'Rollbar', 'Self-hosted error tracking']}, {'decision': 'Grafana + Prometheus for metrics visualization', 'rationale': 'Industry standard, excellent dashboard ecosystem, cost-effective self-hosting option', 'alternatives_considered': ['Datadog dashboards', 'CloudWatch', 'Custom visualization']}]
