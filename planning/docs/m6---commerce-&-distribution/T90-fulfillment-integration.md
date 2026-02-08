---
area: ecommerce
dependsOn:
- T88
effort: 3
iteration: I6
key: T90
milestone: M6 - Commerce & Distribution
priority: p1
title: Fulfillment Integration
type: Task
---

# Fulfillment Integration

## Acceptance Criteria

- [ ] **Orders can be automatically processed and routed to optimal fulfillment providers based on cost and availability**
  - Verification: Create test order via API, verify provider selection logic in logs, confirm order submitted to correct provider with proper specifications
- [ ] **Comic assets are automatically optimized for print with correct specifications (300 DPI, CMYK, bleed areas)**
  - Verification: Upload test comic, trigger fulfillment, verify generated print-ready PDF meets provider requirements using automated validation
- [ ] **Real-time order status updates are synchronized from providers and displayed in dashboard**
  - Verification: Place order, simulate provider webhooks, confirm status updates appear in dashboard within 5 seconds
- [ ] **Failed fulfillment requests are automatically retried with exponential backoff and fallback providers**
  - Verification: Simulate provider API failures, verify retry attempts logged with increasing delays, confirm fallback to secondary provider
- [ ] **Order tracking information is accurate and includes shipping details, estimated delivery, and provider tracking numbers**
  - Verification: Complete order fulfillment flow, verify tracking data matches provider response, test tracking URL generation

## Technical Notes

### Approach

Create a fulfillment service that abstracts multiple print-on-demand providers behind a unified interface. Orders are queued for processing, where comic assets are optimized for print, fulfillment providers are selected based on cost/availability, and orders are submitted via provider APIs. Implement webhook endpoints to receive status updates and sync order states back to the database. Provide real-time order tracking through WebSocket connections to the dashboard.


### Files to Modify

- **path**: packages/database/schema.sql
- **changes**: Add fulfillment_orders, fulfillment_providers, and order_tracking tables
- **path**: apps/api/src/routes/orders.ts
- **changes**: Add fulfillment trigger endpoints and status retrieval
- **path**: apps/dashboard/src/components/orders/OrderList.tsx
- **changes**: Add fulfillment status column and tracking links

### New Files to Create

- **path**: apps/api/src/services/fulfillment/fulfillment-service.ts
- **purpose**: Core fulfillment orchestration and provider management
- **path**: apps/api/src/services/fulfillment/providers/printful-adapter.ts
- **purpose**: Printful API integration and order submission
- **path**: apps/api/src/services/fulfillment/providers/gooten-adapter.ts
- **purpose**: Gooten API integration and order submission
- **path**: apps/api/src/services/fulfillment/providers/base-provider.ts
- **purpose**: Abstract base class for fulfillment provider implementations
- **path**: apps/api/src/services/fulfillment/comic-optimizer.ts
- **purpose**: Comic asset optimization for print specifications
- **path**: apps/api/src/services/fulfillment/cost-calculator.ts
- **purpose**: Multi-provider cost comparison and optimization
- **path**: apps/api/src/queues/fulfillment-queue.ts
- **purpose**: BullMQ implementation for order processing pipeline
- **path**: apps/api/src/routes/webhooks/fulfillment.ts
- **purpose**: Provider webhook handlers for status updates
- **path**: apps/api/src/middleware/webhook-validator.ts
- **purpose**: Webhook signature validation for security
- **path**: apps/dashboard/src/components/orders/OrderTracking.tsx
- **purpose**: Real-time order status and tracking display
- **path**: apps/dashboard/src/hooks/useOrderStatus.ts
- **purpose**: WebSocket hook for real-time order updates
- **path**: packages/database/migrations/20241201_fulfillment_tables.sql
- **purpose**: Database schema for fulfillment system

### External Dependencies


- **@printful/printful-sdk** ^1.5.0

  - Official SDK for Printful print-on-demand integration

- **bullmq** ^4.15.0

  - Redis-based queue system for reliable order processing

- **ioredis** ^5.3.2

  - Redis client for queue management and caching

- **sharp** ^0.33.0

  - Image processing for print optimization (DPI, color profiles)

- **pdf2pic** ^3.1.0

  - Convert generated comic PDFs to print-ready formats

- **webhook-validator** ^2.1.0

  - Validate incoming webhooks from fulfillment providers

## Testing

### Unit Tests

- **File**: `apps/api/src/services/fulfillment/__tests__/fulfillment-service.test.ts`
  - Scenarios: Provider selection algorithm, Comic asset optimization, Error handling and retries, Cost calculation accuracy
- **File**: `apps/api/src/services/fulfillment/__tests__/provider-adapter.test.ts`
  - Scenarios: Printful API integration, Gooten API integration, Webhook signature validation
- **File**: `apps/api/src/queues/__tests__/fulfillment-queue.test.ts`
  - Scenarios: Queue job processing, Job failure handling, Priority queue management
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/fulfillment-flow.test.ts`
  - Scenarios: End-to-end order fulfillment, Webhook processing and status sync, Multi-provider fallback, Real-time status updates
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2.5
- **Documentation**: 1
- **Total**: 13

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Set up database schema and migrations for fulfillment tables
- **done**: False
- **task**: Implement base provider interface and abstract classes
- **done**: False
- **task**: Create Printful and Gooten API adapters with authentication
- **done**: False
- **task**: Build comic asset optimization service for print specifications
- **done**: False
- **task**: Implement fulfillment service with provider selection logic
- **done**: False
- **task**: Set up BullMQ queue system for order processing
- **done**: False
- **task**: Create webhook endpoints and signature validation
- **done**: False
- **task**: Build dashboard components for order tracking
- **done**: False
- **task**: Implement WebSocket connections for real-time updates
- **done**: False
- **task**: Add comprehensive error handling and retry mechanisms
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Fulfillment Integration enables Morpheus to automatically process and ship physical comic book orders to customers. This is critical for the commerce platform as it bridges the gap between digital comic generation and physical product delivery. Without this, the platform would be limited to digital-only sales, significantly reducing revenue potential and market reach. The integration needs to handle order routing, inventory management, print job specifications, shipping calculations, and tracking updates.

**Technical Approach:**
Implement a fulfillment service layer that integrates with print-on-demand providers (Printful, Gooten) and traditional fulfillment centers via webhooks and REST APIs. Use a queue-based architecture with BullMQ for order processing, implement fulfillment provider abstraction layer for multi-vendor support, and create order status synchronization with real-time updates via WebSocket connections to the dashboard. Leverage Supabase edge functions for webhook processing and implement retry mechanisms with exponential backoff for failed fulfillment requests.

**Dependencies:**
- External: [@printful/printful-sdk, axios, bullmq, ioredis, zod, webhook-validator]
- Internal: [orders service, payment service, notification service, comic generation pipeline, user dashboard components]

**Risks:**
- Provider API downtime: Implement circuit breaker pattern with multiple provider fallbacks
- Print quality issues: Add pre-flight validation for comic assets and print specifications
- Inventory sync delays: Cache inventory data with TTL and implement real-time webhooks
- Cost calculation errors: Create comprehensive testing suite for pricing logic and validate against provider APIs

**Complexity Notes:**
More complex than initially estimated due to multi-provider integration requirements and the need for robust error handling across the fulfillment pipeline. The comic-to-print specification mapping adds additional complexity, as generated comics need to be optimized for physical printing (color profiles, DPI, bleed areas).

**Key Files:**
- apps/api/src/services/fulfillment/: Core fulfillment service implementation
- apps/api/src/queues/fulfillment-queue.ts: Order processing queue management
- apps/api/src/routes/webhooks/fulfillment.ts: Provider webhook handlers
- apps/dashboard/src/components/orders/OrderTracking.tsx: Real-time order status UI
- packages/database/migrations/: Order fulfillment tables and indexes


### Design Decisions

[{'decision': 'Multi-provider abstraction layer with primary/fallback routing', 'rationale': 'Reduces vendor lock-in, improves reliability, and enables cost optimization by routing to best provider per order type', 'alternatives_considered': ['Single provider integration', 'Manual fulfillment workflow', 'Direct provider SDK usage']}, {'decision': 'Queue-based order processing with Redis/BullMQ', 'rationale': 'Handles high order volumes, provides retry mechanisms, and enables distributed processing across multiple API instances', 'alternatives_considered': ['Synchronous processing', 'Database-based queues', 'Cloud pub/sub services']}]
