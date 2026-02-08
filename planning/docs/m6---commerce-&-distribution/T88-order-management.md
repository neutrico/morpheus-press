---
area: ecommerce
dependsOn:
- T87
effort: 3
iteration: I6
key: T88
milestone: M6 - Commerce & Distribution
priority: p0
title: Order Management
type: Feature
---

# Order Management

## Acceptance Criteria

- [ ] **Complete order lifecycle from cart creation to digital delivery with state transitions (pending → processing → paid → fulfilled → delivered)**
  - Verification: Integration test creating order, processing payment via Stripe, and generating secure download link
- [ ] **Stripe payment integration with webhook handling for payment status updates and idempotent operations**
  - Verification: Webhook endpoint processes duplicate events safely, payment failures rollback order state
- [ ] **Multi-tenant order isolation with row-level security ensuring users only access their orders**
  - Verification: Database query with different user tokens returns only user-specific orders
- [ ] **Admin dashboard displays order management with filtering, status updates, and refund processing**
  - Verification: Manual testing of admin UI showing order list, detail view, and status change actions
- [ ] **Digital asset delivery through secure tokenized download links with 24-hour expiration**
  - Verification: Download link works within expiration window, returns 403 after expiration

## Technical Notes

### Approach

Build a comprehensive order management system centered around a PostgreSQL-backed state machine. Integrate Stripe for payment processing with webhook-driven status updates. Create admin dashboards for order monitoring and customer-facing checkout flows. Implement secure digital delivery through tokenized download links with expiration. Use event-driven architecture to trigger notifications, analytics, and fulfillment processes.


### Files to Modify

- **path**: packages/database/migrations/001_initial.sql
- **changes**: Add orders, order_items, order_state_history tables with RLS policies
- **path**: apps/api/src/lib/database.ts
- **changes**: Add order-related database types and helper functions
- **path**: apps/api/src/middleware/auth.ts
- **changes**: Extend authentication to support order access validation

### New Files to Create

- **path**: apps/api/src/services/order-service.ts
- **purpose**: Core order management logic, state machine, business rules
- **path**: apps/api/src/services/payment-service.ts
- **purpose**: Stripe integration, payment processing, webhook handling
- **path**: apps/api/src/services/digital-delivery-service.ts
- **purpose**: Secure download link generation, asset delivery management
- **path**: apps/api/src/routes/orders/index.ts
- **purpose**: Order CRUD API endpoints with JSON:API compliance
- **path**: apps/api/src/routes/orders/checkout.ts
- **purpose**: Checkout flow endpoints, cart to order conversion
- **path**: apps/api/src/routes/orders/downloads.ts
- **purpose**: Digital asset download endpoints with token validation
- **path**: apps/api/src/routes/webhooks/stripe.ts
- **purpose**: Stripe webhook endpoint for payment status updates
- **path**: apps/api/src/schemas/order-schemas.ts
- **purpose**: Zod validation schemas for order operations
- **path**: apps/dashboard/src/pages/orders/index.tsx
- **purpose**: Admin order list view with filtering and pagination
- **path**: apps/dashboard/src/pages/orders/[id].tsx
- **purpose**: Admin order detail view with status management
- **path**: apps/dashboard/src/components/orders/OrderStateMachine.tsx
- **purpose**: Visual order state machine component for admin
- **path**: apps/storefront/src/components/checkout/CheckoutFlow.tsx
- **purpose**: Customer checkout flow with Stripe Elements integration
- **path**: apps/storefront/src/components/checkout/OrderConfirmation.tsx
- **purpose**: Order confirmation page with download access
- **path**: apps/storefront/src/pages/orders/[id]/download.tsx
- **purpose**: Secure download page with token validation
- **path**: packages/shared/src/types/order.ts
- **purpose**: Shared TypeScript types for order entities
- **path**: packages/shared/src/constants/order-states.ts
- **purpose**: Order state machine constants and transitions

### External Dependencies


- **stripe** ^14.0.0

  - Payment processing and subscription management

- **zod** ^3.22.0

  - Order payload validation and type safety

- **uuid** ^9.0.0

  - Generate unique order IDs and download tokens

- **date-fns** ^2.30.0

  - Order date handling and token expiration logic

## Testing

### Unit Tests

- **File**: `apps/api/src/services/__tests__/order-service.test.ts`
  - Scenarios: Order state machine transitions, Payment webhook processing, Order validation and error handling, Digital delivery token generation
- **File**: `apps/api/src/routes/orders/__tests__/orders.test.ts`
  - Scenarios: Order CRUD operations, Authentication and authorization, Input validation with zod schemas
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/order-flow.test.ts`
  - Scenarios: Complete order lifecycle with Stripe test mode, Webhook processing with order state updates, Multi-user order isolation
- **File**: `apps/api/src/__tests__/integration/payment-webhooks.test.ts`
  - Scenarios: Stripe webhook signature validation, Duplicate webhook handling, Failed payment processing
### E2E Tests

- **File**: `apps/storefront/cypress/e2e/checkout-flow.cy.ts`
  - Scenarios: Customer checkout with Stripe payment, Order confirmation and download access, Failed payment handling
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2
- **Documentation**: 1
- **Total**: 12.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Design and create database schema with orders, order_items, and state_history tables
- **done**: False
- **task**: Implement core order service with state machine logic and validation
- **done**: False
- **task**: Set up Stripe integration with payment processing and webhook handling
- **done**: False
- **task**: Create order management API endpoints with proper authentication and RLS
- **done**: False
- **task**: Implement digital delivery service with secure tokenized downloads
- **done**: False
- **task**: Build admin dashboard for order management and monitoring
- **done**: False
- **task**: Create customer checkout flow with Stripe Elements integration
- **done**: False
- **task**: Add comprehensive error handling and edge case management
- **done**: False
- **task**: Implement unit and integration tests for all order flows
- **done**: False
- **task**: Add monitoring, logging, and analytics for order processing
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Order Management is the core engine for handling comic purchases in Morpheus. It needs to manage the complete order lifecycle from cart creation through payment processing, fulfillment tracking, and digital delivery of comic assets. This is critical for monetizing the platform and providing users with a seamless purchasing experience for generated comics.

**Technical Approach:**
Implement a state machine-based order system with clear transitions (pending → processing → paid → fulfilled → delivered). Use Supabase RLS for multi-tenant order isolation, integrate Stripe for payments, and leverage event-driven architecture with PostgreSQL triggers for order state changes. Design RESTful APIs following JSON:API spec for consistency with existing Morpheus patterns.

**Dependencies:**
- External: Stripe SDK, zod validation, date-fns for date handling, uuid for order IDs
- Internal: User authentication service, Comic catalog service, Notification system, Email service

**Risks:**
- Payment processing failures: Implement idempotent operations and webhook handling
- Race conditions on inventory: Use PostgreSQL row-level locking and atomic transactions  
- Order state corruption: Strict state machine validation with database constraints
- Digital asset delivery: Secure token-based download links with expiration

**Complexity Notes:**
More complex than initially appears due to payment flow edge cases, refund handling, and digital rights management. The state machine logic and webhook processing add significant complexity beyond basic CRUD operations.

**Key Files:**
- apps/api/src/routes/orders/: Order management endpoints
- packages/database/migrations/: Order tables and triggers
- apps/dashboard/src/pages/orders/: Admin order management UI
- apps/storefront/src/components/checkout/: Customer checkout flow


### Design Decisions

[{'decision': 'Use PostgreSQL enum for order status with state machine validation', 'rationale': 'Ensures data integrity and prevents invalid state transitions at the database level', 'alternatives_considered': ['String status field', 'Separate order_events table', 'Redis state storage']}, {'decision': 'Implement Stripe webhooks for payment confirmation rather than polling', 'rationale': 'Real-time payment updates and reduced API calls, following Stripe best practices', 'alternatives_considered': ['Payment polling', 'Client-side confirmation only', 'Dual webhook + polling']}, {'decision': 'Generate secure download tokens for digital comic delivery', 'rationale': 'Prevents unauthorized access while allowing legitimate purchases to download', 'alternatives_considered': ['Direct file URLs', 'Session-based access', 'JWT tokens']}]
