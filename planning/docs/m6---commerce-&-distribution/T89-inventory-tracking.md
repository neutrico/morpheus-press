---
area: ecommerce
dependsOn:
- T88
effort: 2
iteration: I6
key: T89
milestone: M6 - Commerce & Distribution
priority: p1
title: Inventory Tracking
type: Task
---

# Inventory Tracking

## Acceptance Criteria

- [ ] **Inventory system accurately tracks stock levels for digital assets (unlimited/licensed), physical books (finite), and print-on-demand capacity across all operations**
  - Verification: Run integration tests that simulate purchases, reservations, and stock updates - verify database consistency and Redis cache alignment
- [ ] **Concurrent purchase attempts cannot oversell inventory, even under high load (100+ simultaneous requests)**
  - Verification: Execute load test with artillery targeting checkout endpoints - verify no negative stock levels in database
- [ ] **Inventory reservations during checkout automatically expire after 15 minutes with stock returned to available pool**
  - Verification: Create reservation, wait 15+ minutes, verify stock returned via GET /api/inventory/products/{id} endpoint
- [ ] **Real-time inventory updates are pushed to admin dashboard and storefront within 2 seconds of stock changes**
  - Verification: Monitor WebSocket connections while making inventory changes - measure update latency with browser dev tools
- [ ] **Inventory reconciliation job detects and fixes discrepancies between Redis cache and PostgreSQL within 5 minutes**
  - Verification: Manually corrupt Redis cache data, run reconciliation job, verify corrections logged and data restored

## Technical Notes

### Approach

Build a dual-layer inventory system with PostgreSQL as the source of truth and Redis for real-time operations. Create separate inventory pools for digital assets, physical stock, and print-on-demand capacity, each with specialized business logic. Implement event-driven stock updates using Supabase real-time features and background job processing. Use distributed locking for checkout reservations with automatic TTL cleanup. Integrate tightly with the order management system and provide real-time stock visibility through WebSocket connections to both admin dashboard and storefront.


### Files to Modify

- **path**: packages/database/supabase/migrations/20240115000000_inventory_system.sql
- **changes**: Add inventory_pools, inventory_items, inventory_reservations, inventory_logs tables with RLS policies
- **path**: packages/shared/src/types/index.ts
- **changes**: Export inventory types for cross-package usage
- **path**: apps/api/src/middleware/auth.ts
- **changes**: Add inventory management permissions for admin users
- **path**: apps/dashboard/src/components/layout/navigation.tsx
- **changes**: Add inventory management navigation items
- **path**: apps/storefront/src/components/product/ProductCard.tsx
- **changes**: Display real-time stock status and availability

### New Files to Create

- **path**: packages/shared/src/types/inventory.ts
- **purpose**: TypeScript definitions for inventory entities, enums, and API responses
- **path**: packages/database/supabase/migrations/20240115000000_inventory_system.sql
- **purpose**: Database schema for multi-tier inventory system with constraints
- **path**: apps/api/src/services/inventory/inventory-service.ts
- **purpose**: Core inventory management business logic and operations
- **path**: apps/api/src/services/inventory/inventory-pools.ts
- **purpose**: Specialized handlers for digital, physical, and POD inventory types
- **path**: apps/api/src/services/inventory/inventory-cache.ts
- **purpose**: Redis caching layer with distributed locking mechanisms
- **path**: apps/api/src/services/inventory/inventory-reconciliation.ts
- **purpose**: Background job for detecting and fixing inventory discrepancies
- **path**: apps/api/src/routes/inventory/index.ts
- **purpose**: REST API endpoints for inventory operations and queries
- **path**: apps/api/src/routes/inventory/admin.ts
- **purpose**: Administrative inventory management endpoints
- **path**: apps/api/src/routes/inventory/public.ts
- **purpose**: Public inventory status endpoints for storefront
- **path**: apps/api/src/jobs/inventory-cleanup.ts
- **purpose**: Background job for cleaning expired reservations
- **path**: apps/dashboard/src/components/inventory/InventoryDashboard.tsx
- **purpose**: Main inventory management interface for administrators
- **path**: apps/dashboard/src/components/inventory/StockLevels.tsx
- **purpose**: Real-time stock level monitoring component
- **path**: apps/dashboard/src/components/inventory/InventoryAlerts.tsx
- **purpose**: Low stock and out-of-stock alert system
- **path**: apps/dashboard/src/hooks/useInventorySubscription.ts
- **purpose**: Real-time inventory updates via Supabase subscriptions
- **path**: apps/storefront/src/components/product/StockIndicator.tsx
- **purpose**: Customer-facing stock availability display
- **path**: apps/storefront/src/hooks/useProductAvailability.ts
- **purpose**: Real-time product availability tracking for customers

### External Dependencies


- **ioredis** ^5.3.0

  - Redis client for real-time inventory caching and distributed locking

- **pg-boss** ^9.0.0

  - PostgreSQL-based job queue for inventory reconciliation and cleanup tasks

- **decimal.js** ^10.4.0

  - Precise decimal arithmetic for inventory quantities and financial calculations

- **date-fns** ^2.30.0

  - Date manipulation for reservation TTL and inventory reporting time ranges

## Testing

### Unit Tests

- **File**: `apps/api/src/services/inventory/__tests__/inventory-service.test.ts`
  - Scenarios: Stock allocation and deallocation, Reservation creation and expiry, Multi-format inventory handling, Concurrency control with locks, Cache invalidation logic
- **File**: `apps/api/src/services/inventory/__tests__/inventory-pools.test.ts`
  - Scenarios: Digital asset pool operations, Physical stock pool operations, Print-on-demand capacity checks, Pool-specific business rules
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/inventory-flow.test.ts`
  - Scenarios: Complete purchase flow with stock deduction, Checkout reservation and timeout handling, Real-time updates via Supabase subscriptions, Redis cache consistency after operations, Inventory reconciliation process
- **File**: `apps/api/src/__tests__/integration/concurrent-purchases.test.ts`
  - Scenarios: Race condition prevention during simultaneous checkouts, Distributed lock behavior under load
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

- **task**: Design and implement database schema with inventory tables, constraints, and RLS policies
- **done**: False
- **task**: Create core inventory service with multi-pool architecture and business logic
- **done**: False
- **task**: Implement Redis caching layer with distributed locking for concurrency control
- **done**: False
- **task**: Build REST API endpoints for inventory operations (admin and public)
- **done**: False
- **task**: Develop real-time subscription system for live inventory updates
- **done**: False
- **task**: Create admin dashboard components for inventory management and monitoring
- **done**: False
- **task**: Implement storefront components for displaying product availability
- **done**: False
- **task**: Build background jobs for reservation cleanup and inventory reconciliation
- **done**: False
- **task**: Integrate inventory system with checkout flow and order management
- **done**: False
- **task**: Comprehensive testing including load testing for concurrency scenarios
- **done**: False
- **task**: Documentation for API endpoints, admin workflows, and system architecture
- **done**: False
- **task**: Code review and security audit of inventory operations
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Inventory tracking is essential for the Morpheus commerce platform to manage physical comic book stock, digital asset availability, and print-on-demand fulfillment. This system needs to track comic book inventory across multiple formats (digital downloads, physical prints, limited editions), prevent overselling, handle reservation/hold periods during checkout, and provide real-time stock visibility to both customers and administrators. Given the novel-to-comic transformation workflow, inventory must also account for generated assets and their licensing/usage rights.

**Technical Approach:**
Implement a multi-tier inventory system using PostgreSQL with row-level security, Redis for real-time stock caching, and event-driven architecture for stock updates. Use Supabase real-time subscriptions for live inventory updates in the dashboard. Implement optimistic concurrency control with database constraints to prevent race conditions during high-traffic scenarios. Design separate inventory pools for digital assets (unlimited/licensed), physical stock (finite quantities), and print-on-demand (capacity-based availability). Integration with payment processing should include inventory reservation during checkout flow with TTL-based automatic release.

**Dependencies:**
- External: ioredis, pg-boss, decimal.js, date-fns
- Internal: Supabase client, authentication middleware, order management system, payment processing service, admin dashboard components, storefront product pages

**Risks:**
- Race conditions during concurrent purchases: Use database-level constraints and Redis distributed locks
- Cache invalidation complexity: Implement event-driven cache updates with fallback to database queries  
- Inventory reservation abuse: Add rate limiting and automated cleanup of expired reservations
- Complex multi-format tracking: Design clear separation of concerns between digital/physical/POD inventory types
- Real-time sync failures: Build reconciliation jobs to detect and fix inventory discrepancies

**Complexity Notes:**
This task is more complex than initially estimated due to the need to handle multiple inventory types (digital assets, physical books, print-on-demand capacity), real-time synchronization across distributed systems, and integration with both the creative workflow (asset generation) and commerce pipeline (orders, payments, fulfillment). The event-driven architecture required for proper inventory management adds significant complexity.

**Key Files:**
- packages/database/supabase/migrations/: Add inventory tables schema
- apps/api/src/services/inventory/: Core inventory management service
- apps/api/src/routes/inventory/: REST API endpoints for inventory operations
- apps/dashboard/src/components/inventory/: Admin inventory management UI
- apps/storefront/src/components/product/: Product availability display
- packages/shared/src/types/inventory.ts: Shared inventory type definitions


### Design Decisions

[{'decision': 'Use hybrid SQL + Redis architecture for inventory tracking', 'rationale': 'PostgreSQL provides ACID guarantees and complex queries needed for reporting, while Redis enables real-time stock checking and reservation management with sub-millisecond latency', 'alternatives_considered': ['Pure SQL with aggressive caching', 'Event sourcing with separate read/write models', 'Third-party inventory service integration']}, {'decision': 'Implement three distinct inventory pools (digital, physical, POD)', 'rationale': 'Different inventory types have fundamentally different constraints and business rules - digital has licensing limits, physical has finite stock, POD has capacity/queue management', 'alternatives_considered': ['Single unified inventory table with type flags', 'Completely separate microservices per type']}, {'decision': 'Use pessimistic locking with TTL for checkout reservations', 'rationale': 'Prevents overselling during payment processing while automatically cleaning up abandoned carts, critical for limited edition releases', 'alternatives_considered': ['Optimistic concurrency with retry logic', 'No reservation system with real-time availability checks']}]
