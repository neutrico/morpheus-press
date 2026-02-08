---
area: ecommerce
dependsOn:
- T25
effort: 5
iteration: I6
key: T83
milestone: M6 - Commerce & Distribution
priority: p0
title: Stripe Integration
type: Feature
---

# Stripe Integration

## Acceptance Criteria

- [ ] **Users can successfully purchase comic generation credits using Stripe payment forms**
  - Verification: Manual test: Complete credit purchase flow in dashboard, verify credits added to user account and payment recorded in Stripe
- [ ] **Webhook handlers properly sync payment status changes from Stripe to Supabase**
  - Verification: Integration test: Trigger webhook events in Stripe test mode, verify database updates match payment status
- [ ] **Failed payments display appropriate error messages and don't charge users**
  - Verification: Manual test: Use Stripe test cards for declined payments, verify user sees error and no charge appears in Stripe dashboard
- [ ] **Payment processing handles concurrent requests without data corruption**
  - Verification: Load test: Send 10+ simultaneous payment requests, verify all succeed or fail gracefully with proper error handling
- [ ] **All payment events are logged with sufficient detail for debugging and compliance**
  - Verification: Check logs contain payment_intent_id, user_id, amount, timestamp for all payment operations

## Technical Notes

### Approach

Create a payment service layer in the Fastify backend that wraps Stripe SDK operations with proper error handling and logging. Build React payment components using Stripe Elements for secure card collection in the dashboard. Implement webhook endpoints to process payment confirmations, failed charges, and subscription updates asynchronously. Store essential payment metadata in Supabase while keeping Stripe as the source of truth for sensitive payment data.


### Files to Modify

- **path**: apps/backend/package.json
- **changes**: Add stripe dependency
- **path**: apps/dashboard/package.json
- **changes**: Add @stripe/stripe-js and @stripe/react-stripe-js dependencies
- **path**: packages/database/schema.sql
- **changes**: Add payment_customers, payment_intents, webhook_events tables
- **path**: apps/backend/src/app.ts
- **changes**: Register payment routes and webhook handlers
- **path**: apps/backend/.env.example
- **changes**: Add Stripe API keys and webhook secret variables

### New Files to Create

- **path**: apps/backend/src/services/stripe.ts
- **purpose**: Stripe SDK wrapper with error handling and logging
- **path**: apps/backend/src/routes/payments/index.ts
- **purpose**: Payment API routes (create payment intent, get payment status)
- **path**: apps/backend/src/routes/payments/webhooks.ts
- **purpose**: Stripe webhook handlers for payment events
- **path**: apps/backend/src/types/stripe.ts
- **purpose**: TypeScript interfaces for payment data structures
- **path**: apps/dashboard/src/components/payments/PaymentForm.tsx
- **purpose**: Stripe Elements payment form component
- **path**: apps/dashboard/src/components/payments/CreditPurchase.tsx
- **purpose**: Credit purchase flow with payment integration
- **path**: apps/dashboard/src/hooks/usePayments.ts
- **purpose**: React hook for payment operations and state management
- **path**: apps/backend/src/middleware/stripe-webhook.ts
- **purpose**: Webhook signature verification middleware
- **path**: apps/backend/src/utils/payment-logger.ts
- **purpose**: Structured logging for payment events and compliance

### External Dependencies


- **stripe** ^14.0.0

  - Official Stripe Node.js SDK for backend payment processing and webhook handling

- **@stripe/stripe-js** ^2.0.0

  - Stripe JavaScript SDK for frontend payment element initialization

- **@stripe/react-stripe-js** ^2.0.0

  - React components and hooks for Stripe Elements integration

- **micro** ^10.0.1

  - Lightweight HTTP handler for processing Stripe webhooks with raw body access

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/stripe.test.ts`
  - Scenarios: Create payment intent success, Handle Stripe API errors, Webhook signature verification, Payment metadata formatting
- **File**: `apps/backend/src/__tests__/routes/payments.test.ts`
  - Scenarios: Create payment endpoint validation, Webhook processing logic, Authentication required checks
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/stripe-flow.test.ts`
  - Scenarios: Complete payment flow with webhook confirmation, Failed payment handling and cleanup, User credit balance updates after payment
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

- **task**: Set up Stripe account and obtain test API keys
- **done**: False
- **task**: Create database schema for payment tracking tables
- **done**: False
- **task**: Implement Stripe service wrapper with core payment operations
- **done**: False
- **task**: Build payment API routes for creating payment intents
- **done**: False
- **task**: Create webhook endpoints with signature verification
- **done**: False
- **task**: Develop React payment form components using Stripe Elements
- **done**: False
- **task**: Integrate payment flow with user credit system
- **done**: False
- **task**: Add comprehensive error handling and user feedback
- **done**: False
- **task**: Implement payment event logging and monitoring
- **done**: False
- **task**: Write unit and integration tests for payment flows
- **done**: False
- **task**: Manual testing with Stripe test cards and scenarios
- **done**: False
- **task**: Security review focusing on PCI compliance and webhook verification
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Stripe integration is crucial for M6 Commerce & Distribution as it enables Morpheus to monetize the novel-to-comic transformation platform. This allows users to purchase comic generation credits, subscribe to premium tiers, or buy finished comic products. Without payment processing, the platform cannot generate revenue or offer tiered services based on usage/quality levels.

**Technical Approach:**
- Use Stripe's official Node.js SDK with TypeScript bindings for backend payment processing
- Implement Stripe Elements/Payment Element in Next.js frontend for secure card collection
- Create webhook endpoints in Fastify to handle payment status updates and subscription changes
- Store payment metadata (customer_id, subscription_id, payment_intent_id) in Supabase
- Use Stripe's test mode during development with proper environment variable configuration
- Implement proper error handling for failed payments, expired cards, and insufficient funds
- Add payment event logging and monitoring for debugging and compliance

**Dependencies:**
- External: stripe (Node.js SDK), @stripe/stripe-js (frontend), @stripe/react-stripe-js (React components)
- Internal: Authentication service (user identification), Credit/subscription management system, Email notification service, Admin dashboard for payment monitoring

**Risks:**
- PCI Compliance: Mitigate by using Stripe Elements (never handle raw card data)
- Webhook security: Verify webhook signatures to prevent fraud/replay attacks  
- Failed payment handling: Implement robust retry logic and user notification systems
- Currency/taxation: Start with USD only, plan for international expansion later
- Subscription edge cases: Handle failed renewals, plan changes, cancellations gracefully

**Complexity Notes:**
This is moderately complex due to multiple integration points (frontend payment forms, backend processing, webhook handling, database updates) and the critical nature of payment processing. The asynchronous nature of webhooks adds complexity for state synchronization. However, Stripe's excellent documentation and SDKs reduce implementation complexity significantly.

**Key Files:**
- apps/backend/src/routes/payments/: Payment API routes and webhook handlers
- apps/backend/src/services/stripe.ts: Stripe service wrapper with error handling
- apps/dashboard/src/components/payments/: Payment forms and subscription management UI
- apps/backend/src/types/stripe.ts: TypeScript interfaces for Stripe objects
- packages/database/schema.sql: Add payment_customers, subscriptions, payment_intents tables


### Design Decisions

[{'decision': 'Use Stripe Payment Element instead of individual Elements', 'rationale': 'Payment Element provides better UX with built-in payment method selection, reduces frontend complexity, and handles international payment methods automatically', 'alternatives_considered': ['Individual Stripe Elements (Card, IBAN, etc.)', 'Stripe Checkout (redirect flow)', 'Alternative payment processor (PayPal, Square)']}, {'decision': 'Implement webhook-first architecture for payment status updates', 'rationale': 'Webhooks provide reliable, asynchronous notification of payment events even if user closes browser. Essential for subscription billing and failed payment handling', 'alternatives_considered': ['Polling Stripe API', 'Frontend-only payment confirmation', 'Hybrid approach with immediate + webhook confirmation']}, {'decision': 'Store Stripe customer ID and subscription metadata in Supabase', 'rationale': 'Enables fast user payment history queries, offline payment status checks, and reduces Stripe API calls. Maintains referential integrity with user accounts', 'alternatives_considered': ['Query Stripe API on-demand', 'Cache payment data in Redis', 'Separate payments microservice']}]
