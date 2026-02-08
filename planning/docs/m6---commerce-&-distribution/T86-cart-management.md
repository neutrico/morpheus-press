---
area: ecommerce
dependsOn:
- T85
effort: 3
iteration: I6
key: T86
milestone: M6 - Commerce & Distribution
priority: p0
title: Cart Management
type: Feature
---

# Cart Management

## Acceptance Criteria

- [ ] **Users can add comics to cart with immediate UI feedback and persistent state across sessions**
  - Verification: Add comic to cart, refresh browser, verify cart persists. Check localStorage for guest users and database for authenticated users
- [ ] **Guest cart seamlessly merges with user cart upon authentication without data loss**
  - Verification: Add items as guest, login, verify all guest items appear in authenticated cart with proper deduplication
- [ ] **Cart operations handle concurrent updates and network failures gracefully with optimistic updates**
  - Verification: Simulate network failure during cart update, verify UI shows loading state and rolls back on failure
- [ ] **Cart validates pricing and availability server-side to prevent manipulation**
  - Verification: Modify cart item price in localStorage/database directly, attempt checkout, verify server rejects with current pricing
- [ ] **Cart performance remains responsive with up to 50 items and implements proper pagination**
  - Verification: Add 50+ items to cart, measure load time <500ms, verify pagination UI appears after 20 items

## Technical Notes

### Approach

Build a cart system with Zustand for client state and Supabase for persistence. Create RESTful cart endpoints in Fastify with proper authentication middleware. Implement optimistic updates with rollback capabilities and real-time price/availability validation. Use React Query for server state synchronization and implement guest cart migration logic on user authentication. Add comprehensive cart validation and inventory checks.


### Files to Modify

- **path**: packages/database/supabase/migrations/20240115000000_create_cart_tables.sql
- **changes**: Add cart and cart_items tables with proper indexes and RLS policies
- **path**: apps/backend/src/types/index.ts
- **changes**: Add Cart, CartItem, and CartOperation type definitions
- **path**: apps/storefront/lib/supabase.ts
- **changes**: Add cart-related database types and queries

### New Files to Create

- **path**: apps/storefront/stores/cart-store.ts
- **purpose**: Zustand store for cart state management with persistence
- **path**: apps/storefront/hooks/use-cart.ts
- **purpose**: React Query hooks for cart operations and server synchronization
- **path**: apps/backend/src/routes/cart/index.ts
- **purpose**: Cart API routes with CRUD operations
- **path**: apps/backend/src/routes/cart/handlers.ts
- **purpose**: Cart route handlers with validation and business logic
- **path**: apps/backend/src/services/cart-service.ts
- **purpose**: Cart business logic, validation, and database operations
- **path**: apps/storefront/components/cart/CartDrawer.tsx
- **purpose**: Sliding cart drawer component with item list
- **path**: apps/storefront/components/cart/CartItem.tsx
- **purpose**: Individual cart item with quantity controls
- **path**: apps/storefront/components/cart/CartSummary.tsx
- **purpose**: Cart totals and checkout button component
- **path**: apps/storefront/components/cart/AddToCartButton.tsx
- **purpose**: Reusable add-to-cart button with loading states
- **path**: packages/shared/schemas/cart.ts
- **purpose**: Zod schemas for cart validation across frontend/backend
- **path**: apps/storefront/utils/cart-persistence.ts
- **purpose**: Guest cart localStorage management utilities
- **path**: apps/backend/src/middleware/cart-validation.ts
- **purpose**: Middleware for validating cart operations and pricing

### External Dependencies


- **zustand** ^4.4.7

  - Lightweight state management for cart operations with persistence middleware

- **@tanstack/react-query** ^5.17.0

  - Server state management and optimistic updates for cart synchronization

- **zod** ^3.22.4

  - Cart data validation schemas for both client and server

- **immer** ^10.0.3

  - Immutable state updates for complex cart operations

## Testing

### Unit Tests

- **File**: `apps/storefront/stores/__tests__/cart-store.test.ts`
  - Scenarios: Add/remove/update cart items, Cart total calculations, Optimistic updates and rollbacks, Guest cart persistence
- **File**: `apps/backend/src/services/__tests__/cart-service.test.ts`
  - Scenarios: Cart CRUD operations, Price validation, Cart merging logic, Inventory checks
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/cart-api.test.ts`
  - Scenarios: Full cart lifecycle with authentication, Guest to authenticated user cart migration, Concurrent cart updates handling
- **File**: `apps/storefront/components/cart/__tests__/cart-integration.test.ts`
  - Scenarios: Cart UI with real API calls, Error state handling, Loading states
### E2E Tests

- **File**: `apps/storefront/__tests__/e2e/cart-flow.spec.ts`
  - Scenarios: Complete add-to-cart to checkout flow, Cross-device cart synchronization, Cart abandonment and recovery
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 8.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Create database schema and migrations for cart tables
- **done**: False
- **task**: Implement Zustand cart store with persistence logic
- **done**: False
- **task**: Build cart API endpoints with authentication and validation
- **done**: False
- **task**: Create cart service layer with business logic
- **done**: False
- **task**: Develop React Query hooks for cart operations
- **done**: False
- **task**: Build cart UI components (drawer, items, summary)
- **done**: False
- **task**: Implement guest-to-authenticated cart migration
- **done**: False
- **task**: Add optimistic updates with error handling
- **done**: False
- **task**: Implement cart validation and inventory checks
- **done**: False
- **task**: Write comprehensive tests and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Cart Management is essential for Morpheus's comic storefront, allowing users to add transformed comics to their cart, modify quantities, persist cart state across sessions, and proceed to checkout. This enables the core monetization flow where users purchase their AI-generated comics. Without robust cart functionality, users cannot complete purchases, making this critical for the commerce milestone.

**Technical Approach:**
Implement a hybrid cart system with client-side state management (Zustand) for immediate UX and server-side persistence for logged-in users. Use optimistic updates for cart operations with rollback on failure. Store cart data in Supabase with proper user association and guest cart handling via localStorage/cookies. Implement cart validation to ensure comic availability and pricing accuracy.

**Dependencies:**
- External: [@tanstack/react-query, zustand, @supabase/supabase-js, stripe, zod]
- Internal: [authentication service, comic catalog API, user management, pricing engine]

**Risks:**
- Cart abandonment due to session loss: implement robust persistence with guest cart migration
- Race conditions on concurrent cart updates: use optimistic locking with version numbers
- Price manipulation attacks: server-side price validation on every cart operation
- Performance with large carts: implement cart item limits and pagination

**Complexity Notes:**
More complex than initially estimated due to guest/authenticated user cart merging, real-time price updates, inventory management integration, and cross-device cart synchronization requirements.

**Key Files:**
- apps/storefront/stores/cart-store.ts: Zustand cart state management
- apps/backend/src/routes/cart/: Cart API endpoints (CRUD operations)
- packages/database/migrations/: Cart and cart_items table schemas
- apps/storefront/components/cart/: Cart UI components
- apps/storefront/hooks/use-cart.ts: Cart operations hook with react-query


### Design Decisions

[{'decision': 'Hybrid client/server cart with Zustand + Supabase persistence', 'rationale': 'Provides immediate UX with optimistic updates while ensuring data persistence and cross-device synchronization', 'alternatives_considered': ['Pure server-side cart', 'Redux Toolkit with RTK Query', 'Context API only']}, {'decision': 'Guest cart migration on authentication', 'rationale': 'Prevents cart loss when users sign up/login mid-session, improving conversion rates', 'alternatives_considered': ['Force login before adding to cart', 'Separate guest/user carts permanently']}, {'decision': 'Server-side price and availability validation', 'rationale': 'Prevents price manipulation and ensures data integrity at checkout', 'alternatives_considered': ['Client-side validation only', 'Validation only at checkout']}]
