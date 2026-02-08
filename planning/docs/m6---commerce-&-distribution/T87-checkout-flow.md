---
area: ecommerce
dependsOn:
- T83
- T86
effort: 5
iteration: I6
key: T87
milestone: M6 - Commerce & Distribution
priority: p0
title: Checkout Flow
type: Feature
---

# Checkout Flow

## Acceptance Criteria

- [ ] **User can complete end-to-end checkout for digital comic purchase with cart review, customer info, payment, and order confirmation steps**
  - Verification: E2E test covers full flow from cart to delivered digital asset download link
- [ ] **Payment processing handles success, failure, and pending states with proper error messages and retry mechanisms**
  - Verification: Integration tests with Stripe test cards (4242424242424242 success, 4000000000000002 decline) verify all payment states
- [ ] **Order state machine transitions correctly through pending → paid → processing → delivered with real-time updates**
  - Verification: Unit tests verify state transitions and integration tests confirm Supabase real-time subscriptions update UI
- [ ] **Cart abandonment recovery allows users to resume checkout within 24 hours of session creation**
  - Verification: Manual test: start checkout, close browser, return within 24h and verify cart/progress restoration
- [ ] **Digital asset delivery provides download link within 5 minutes of successful payment for pre-generated comics**
  - Verification: Performance test measures time from webhook receipt to email delivery with download link

## Technical Notes

### Approach

Build a 4-step checkout flow (Cart Review → Customer Info → Payment → Confirmation) using React Hook Form with Zod schemas for validation. Integrate Stripe Elements for PCI-compliant payment collection, with Next.js API routes handling server-side payment intent creation and webhook processing. Implement order state machine in Fastify backend to track order lifecycle from pending → paid → processing → delivered. Use Supabase Row Level Security for order access control and real-time subscriptions for order status updates.


### Files to Modify

- **path**: apps/backend/src/app.ts
- **changes**: Register order routes and Stripe webhook endpoints
- **path**: packages/database/src/schema/index.ts
- **changes**: Add orders, order_items, payments, and digital_deliveries tables
- **path**: apps/storefront/src/pages/_app.tsx
- **changes**: Add React Query client configuration for checkout state
- **path**: apps/backend/src/plugins/auth.ts
- **changes**: Add guest checkout session handling

### New Files to Create

- **path**: apps/storefront/src/components/checkout/CheckoutFlow.tsx
- **purpose**: Main checkout component orchestrating 4-step process
- **path**: apps/storefront/src/components/checkout/CartReview.tsx
- **purpose**: Step 1: Cart items display and quantity modification
- **path**: apps/storefront/src/components/checkout/CustomerInfo.tsx
- **purpose**: Step 2: Billing/shipping information collection
- **path**: apps/storefront/src/components/checkout/PaymentStep.tsx
- **purpose**: Step 3: Stripe Elements integration for payment
- **path**: apps/storefront/src/components/checkout/OrderConfirmation.tsx
- **purpose**: Step 4: Order success and digital delivery status
- **path**: apps/storefront/src/hooks/useCheckout.ts
- **purpose**: Checkout state management with React Hook Form
- **path**: apps/storefront/src/pages/api/checkout/create-payment-intent.ts
- **purpose**: Create Stripe payment intent with order details
- **path**: apps/storefront/src/pages/api/checkout/confirm-payment.ts
- **purpose**: Confirm payment and create order record
- **path**: apps/storefront/src/pages/api/webhooks/stripe.ts
- **purpose**: Handle Stripe webhook events for payment status
- **path**: apps/backend/src/routes/orders/index.ts
- **purpose**: Order CRUD operations and status management
- **path**: apps/backend/src/services/OrderService.ts
- **purpose**: Business logic for order lifecycle management
- **path**: apps/backend/src/services/PaymentService.ts
- **purpose**: Stripe integration and payment processing
- **path**: apps/backend/src/services/DigitalDeliveryService.ts
- **purpose**: Coordinate asset generation and delivery
- **path**: apps/backend/src/lib/order-state-machine.ts
- **purpose**: Define order state transitions and validation
- **path**: packages/shared/src/types/checkout.ts
- **purpose**: TypeScript interfaces for checkout flow
- **path**: packages/shared/src/schemas/checkout.ts
- **purpose**: Zod validation schemas for checkout forms

### External Dependencies


- **@stripe/stripe-js** ^2.1.0

  - Client-side Stripe integration for secure payment processing

- **@stripe/react-stripe-js** ^2.3.0

  - React components for Stripe Elements integration

- **stripe** ^14.0.0

  - Server-side Stripe SDK for payment processing and webhooks

- **react-hook-form** ^7.47.0

  - Form state management with excellent TypeScript support

- **@hookform/resolvers** ^3.3.0

  - Zod integration for form validation schemas

- **zod** ^3.22.0

  - Runtime type validation for checkout forms and API endpoints

- **@tanstack/react-query** ^5.0.0

  - API state management for cart and order operations

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/order-service.test.ts`
  - Scenarios: Order creation with valid cart items, Order state transitions, Payment intent creation and updates, Digital asset linking, Tax calculation integration
- **File**: `apps/storefront/src/hooks/__tests__/useCheckout.test.ts`
  - Scenarios: Form validation with Zod schemas, Step navigation and persistence, Error state handling, Cart total calculations
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/checkout-flow.test.ts`
  - Scenarios: Complete checkout flow with Stripe test environment, Webhook processing for payment events, Order fulfillment pipeline integration, Email notification delivery
- **File**: `apps/storefront/src/__tests__/integration/checkout-ui.test.ts`
  - Scenarios: Multi-step form progression, Real-time order status updates, Payment error handling UI
### E2E Tests

- **File**: `apps/storefront/src/__tests__/e2e/checkout.spec.ts`
  - Scenarios: Guest checkout with email receipt, Authenticated user checkout with order history, Cart abandonment and recovery, Failed payment retry flow
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

- **task**: Setup database schema for orders, payments, and digital deliveries
- **done**: False
- **task**: Implement order state machine and business logic services
- **done**: False
- **task**: Create Stripe integration for payment processing and webhooks
- **done**: False
- **task**: Build React checkout flow components with form validation
- **done**: False
- **task**: Implement Next.js API routes for payment orchestration
- **done**: False
- **task**: Add digital asset delivery coordination with ML pipeline
- **done**: False
- **task**: Implement cart persistence and abandonment recovery
- **done**: False
- **task**: Add real-time order status updates with Supabase subscriptions
- **done**: False
- **task**: Create comprehensive test suite covering unit, integration, and e2e
- **done**: False
- **task**: Document checkout API endpoints and integration patterns
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Checkout Flow is a critical ecommerce component that enables users to purchase comic books generated from novels on the Morpheus platform. This solves the monetization challenge by providing a secure, user-friendly payment experience that converts browsers into customers. Given this is in the Commerce & Distribution milestone, it's essential for the platform's business viability and must handle various payment methods, tax calculations, digital delivery, and order management.

**Technical Approach:**
Implement a multi-step checkout process using React Hook Form for state management, Stripe for payment processing, and Supabase for order persistence. Use Next.js API routes as a backend-for-frontend (BFF) pattern to orchestrate between Fastify backend services, Stripe webhooks, and order fulfillment. Implement optimistic UI updates with proper error boundaries and loading states. Follow atomic transaction patterns for order creation to ensure data consistency.

**Dependencies:**
- External: Stripe SDK, React Hook Form, Zod validation, React Query for API state
- Internal: Authentication service, Product catalog service, User management, Email service, Digital asset delivery service

**Risks:**
- Payment processing failures: Implement idempotency keys and webhook retry logic
- Cart abandonment: Add session persistence and recovery mechanisms
- Tax calculation complexity: Use Stripe Tax or integrate with tax service APIs
- Digital delivery issues: Implement robust asset generation status tracking
- PCI compliance: Ensure all payment data flows through Stripe, never store card details

**Complexity Notes:**
Higher complexity than initially estimated due to digital goods delivery requirements. Unlike physical products, comic delivery involves coordinating with ML pipeline completion, asset generation, and potential re-generation requests. Multi-tenant considerations for white-label storefronts add additional complexity layers.

**Key Files:**
- apps/storefront/src/components/checkout/: Checkout flow components
- apps/storefront/src/pages/api/checkout/: Payment processing APIs
- apps/backend/src/routes/orders/: Order management endpoints
- packages/database/src/schema/: Order and payment tables
- apps/storefront/src/hooks/useCheckout.ts: Checkout state management


### Design Decisions

[{'decision': 'Use Stripe Checkout vs Custom Implementation', 'rationale': 'Custom implementation provides better UX integration with comic previews and allows for complex digital delivery workflows', 'alternatives_considered': ['Stripe Checkout (hosted)', 'PayPal Smart Buttons', 'Square Web Payments SDK']}, {'decision': 'Multi-step vs Single-page checkout', 'rationale': 'Multi-step reduces cognitive load for digital goods and allows progressive validation of complex comic customization options', 'alternatives_considered': ['Single-page accordion', 'Modal-based checkout', 'Separate checkout page']}, {'decision': 'Optimistic UI updates for cart operations', 'rationale': 'Improves perceived performance for cart modifications while maintaining data consistency through conflict resolution', 'alternatives_considered': ['Pessimistic updates', 'Real-time sync with WebSockets', 'Periodic polling']}]
