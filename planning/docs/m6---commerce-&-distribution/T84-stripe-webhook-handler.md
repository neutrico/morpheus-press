---
area: ecommerce
dependsOn:
- T83
effort: 3
iteration: I6
key: T84
milestone: M6 - Commerce & Distribution
priority: p0
title: Stripe Webhook Handler
type: Task
---

# Stripe Webhook Handler

## Acceptance Criteria

- [ ] **Webhook endpoint successfully receives and verifies Stripe webhook signatures**
  - Verification: Test with stripe CLI: `stripe listen --forward-to localhost:3000/webhooks/stripe` and trigger test events
- [ ] **Payment successful events create orders and deliver comics without duplicates**
  - Verification: Send duplicate payment_intent.succeeded events and verify only one order is created in database
- [ ] **Subscription events properly update user subscription status and permissions**
  - Verification: Trigger customer.subscription.updated event and verify user access changes in database
- [ ] **Failed webhook processing is logged and queued for retry**
  - Verification: Simulate handler failure and verify error logging and retry queue entry
- [ ] **All webhook events are idempotent and can be safely replayed**
  - Verification: Replay the same webhook event multiple times and verify system state remains consistent

## Technical Notes

### Approach

Create a Fastify route at /webhooks/stripe that verifies webhook signatures using Stripe's SDK. Parse the raw request body and route events to specific handlers based on event type. Each handler will be idempotent by checking against a webhook_events table in Supabase before processing. Use database transactions to ensure consistency between webhook processing and business logic updates. Queue heavy operations like email notifications and comic delivery asynchronously.


### Files to Modify

- **path**: apps/api/src/app.ts
- **changes**: Register @fastify/raw-body plugin and webhook route
- **path**: packages/database/src/migrations/000X_webhook_events.sql
- **changes**: Create webhook_events table for idempotency tracking
- **path**: apps/api/src/config/env.ts
- **changes**: Add STRIPE_WEBHOOK_SECRET environment variable validation

### New Files to Create

- **path**: apps/api/src/routes/webhooks/stripe.ts
- **purpose**: Main webhook endpoint with signature verification and event routing
- **path**: apps/api/src/services/stripe-webhook-handler.ts
- **purpose**: Core webhook processing logic with idempotency and error handling
- **path**: apps/api/src/services/webhook-handlers/index.ts
- **purpose**: Export all individual event handlers
- **path**: apps/api/src/services/webhook-handlers/payment-intent.ts
- **purpose**: Handle payment_intent.* events for order processing
- **path**: apps/api/src/services/webhook-handlers/subscription.ts
- **purpose**: Handle customer.subscription.* events for subscription management
- **path**: apps/api/src/services/webhook-handlers/invoice.ts
- **purpose**: Handle invoice.* events for billing notifications
- **path**: apps/api/src/types/stripe-events.ts
- **purpose**: TypeScript types and Zod schemas for webhook event validation
- **path**: apps/api/src/utils/webhook-idempotency.ts
- **purpose**: Utility functions for idempotency key generation and checking
- **path**: apps/api/src/middleware/webhook-auth.ts
- **purpose**: Stripe webhook signature verification middleware

### External Dependencies


- **stripe** ^14.0.0

  - Official Stripe SDK for webhook signature verification and type definitions

- **@fastify/raw-body** ^4.0.0

  - Required to access raw request body for Stripe signature verification

- **zod** ^3.22.0

  - Runtime validation of webhook payloads to ensure data integrity

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/stripe-webhook-handler.test.ts`
  - Scenarios: Event signature verification success/failure, Idempotency key handling, Each event type handler logic, Database transaction rollback on errors, Invalid event payload handling
- **File**: `apps/api/src/__tests__/routes/webhooks/stripe.test.ts`
  - Scenarios: Valid webhook request processing, Invalid signature rejection, Malformed payload handling, Rate limiting behavior
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/stripe-webhooks.test.ts`
  - Scenarios: End-to-end payment flow with order creation, Subscription lifecycle management, Failed payment handling and user notification, Comic delivery pipeline trigger
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

- **task**: Setup Stripe webhook configuration and environment variables
- **done**: False
- **task**: Create database migration for webhook_events tracking table
- **done**: False
- **task**: Implement webhook signature verification middleware
- **done**: False
- **task**: Create main webhook endpoint with event routing
- **done**: False
- **task**: Implement individual event handlers (payment_intent, subscription, invoice)
- **done**: False
- **task**: Add idempotency checking and database transaction handling
- **done**: False
- **task**: Implement error handling, logging, and retry queue integration
- **done**: False
- **task**: Create comprehensive unit and integration tests
- **done**: False
- **task**: Add monitoring and alerting for webhook failures
- **done**: False
- **task**: Documentation and deployment configuration
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Stripe webhook handlers are essential for maintaining data consistency between Stripe's payment system and Morpheus's database. When users purchase comics, subscribe to services, or payment states change, Stripe sends webhooks to notify our system. Without proper webhook handling, we'd have inconsistent payment states, failed order fulfillment, and poor user experience. This is critical for the commerce milestone as it enables real-time payment processing, subscription management, and automated comic delivery.

**Technical Approach:**
Use Fastify's raw body parsing with Stripe's webhook signature verification for security. Implement idempotent event processing using Supabase to store processed webhook IDs. Create dedicated handlers for each event type (payment_intent.succeeded, customer.subscription.updated, etc.) following the command pattern. Use Fastify's async/await with proper error handling and dead letter queues for failed webhooks. Leverage TypeScript's strict typing with Stripe's official types for type safety.

**Dependencies:**
- External: stripe ^14.0.0, @fastify/raw-body ^4.0.0, zod ^3.22.0 for validation
- Internal: Supabase client, order processing service, user management service, email notification service, comic delivery pipeline

**Risks:**
- Duplicate processing: Use idempotency keys and database constraints to prevent duplicate order fulfillment
- Webhook replay attacks: Implement proper signature verification and timestamp validation
- Event ordering issues: Design handlers to be order-independent where possible, use database transactions
- Performance bottlenecks: Queue heavy operations (image processing, email) asynchronously
- Failed webhook delivery: Implement retry logic and monitoring for webhook failures

**Complexity Notes:**
More complex than initially estimated due to the need for robust idempotency, error handling, and integration with multiple Morpheus services (orders, users, comics, notifications). The variety of Stripe events and their interdependencies adds significant complexity.

**Key Files:**
- apps/api/src/routes/webhooks/stripe.ts: Main webhook endpoint
- apps/api/src/services/stripe-webhook-handler.ts: Event processing logic
- apps/api/src/types/stripe-events.ts: TypeScript types for webhook payloads
- packages/database/src/schema.sql: Webhook events tracking table


### Design Decisions

[{'decision': 'Use event-driven architecture with dedicated handlers per event type', 'rationale': 'Provides separation of concerns, easier testing, and allows for independent scaling of different webhook types', 'alternatives_considered': ['Single monolithic handler', 'Queue-based processing with workers']}, {'decision': 'Store webhook events in database for idempotency and audit trail', 'rationale': 'Prevents duplicate processing, enables debugging, and provides audit compliance for financial transactions', 'alternatives_considered': ['In-memory cache', 'Redis-based deduplication']}]
