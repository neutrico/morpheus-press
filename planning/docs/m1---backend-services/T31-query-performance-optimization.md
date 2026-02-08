---
area: backend
dependsOn:
- T24
effort: 3
iteration: I2
key: T31
milestone: M1 - Backend Services
priority: p1
title: Query Performance Optimization
type: Task
---

# Query Performance Optimization

## Acceptance Criteria

- [ ] **Database queries execute within performance thresholds: <100ms for simple queries, <500ms for complex joins, <2s for full-text search**
  - Verification: Run performance test suite with `npm run test:perf` and check metrics dashboard shows all queries under thresholds
- [ ] **Redis caching reduces database load by >70% for frequently accessed data (user sessions, comic thumbnails, novel metadata)**
  - Verification: Monitor cache hit ratio in Redis CLI with `redis-cli info stats` and verify hit_rate > 0.7
- [ ] **Connection pooling handles concurrent load without connection exhaustion up to 100 simultaneous users**
  - Verification: Load test with `k6 run tests/load/concurrent-users.js` and verify no connection timeout errors
- [ ] **Cursor-based pagination efficiently handles large datasets (>10k novels, >50k comic panels) with consistent response times**
  - Verification: Test pagination endpoints with large datasets and verify response times remain <300ms across all pages
- [ ] **Query monitoring captures performance metrics and identifies slow queries automatically**
  - Verification: Check Fastify metrics endpoint `/metrics` shows query duration histograms and slow query alerts trigger for queries >1s

## Technical Notes

### Approach

Implement a three-layer optimization strategy: database-level indexing and RLS policies in Supabase, application-level caching with Redis integrated through Fastify plugins, and connection pooling for efficient resource utilization. Focus on optimizing the most frequent queries first (user authentication, novel parsing status, comic thumbnails) using cursor-based pagination and prepared statements. Add comprehensive monitoring to identify bottlenecks before they impact user experience.


### Files to Modify

- **path**: apps/backend/src/app.ts
- **changes**: Register database and cache plugins, add metrics collection
- **path**: apps/backend/src/routes/novels/index.ts
- **changes**: Implement cursor pagination, add caching for novel metadata
- **path**: apps/backend/src/routes/novels/[id]/status.ts
- **changes**: Add Redis caching for processing status with 30s TTL
- **path**: apps/backend/src/routes/comics/index.ts
- **changes**: Implement cursor pagination for comic gallery, cache thumbnails
- **path**: apps/backend/src/routes/users/profile.ts
- **changes**: Add session caching and optimized user data queries
- **path**: supabase/migrations/001_initial_schema.sql
- **changes**: Add performance indexes for novels.title, comics.created_at, users.email

### New Files to Create

- **path**: apps/backend/src/plugins/database.ts
- **purpose**: Database connection pooling, prepared statements, query optimization setup
- **path**: apps/backend/src/plugins/cache.ts
- **purpose**: Redis integration plugin with Fastify, caching strategies
- **path**: apps/backend/src/services/cache.ts
- **purpose**: Cache service with invalidation patterns, TTL management
- **path**: apps/backend/src/middleware/metrics.ts
- **purpose**: Query performance monitoring, slow query detection
- **path**: apps/backend/src/utils/pagination.ts
- **purpose**: Cursor-based pagination utilities for large datasets
- **path**: apps/backend/src/types/cache.ts
- **purpose**: TypeScript interfaces for cache keys, TTL configurations
- **path**: supabase/migrations/002_performance_indexes.sql
- **purpose**: Database indexes for optimized query performance
- **path**: apps/backend/src/__tests__/fixtures/large-dataset.ts
- **purpose**: Test data generators for performance testing scenarios
- **path**: tests/load/query-performance.js
- **purpose**: K6 load testing scripts for database performance validation

### External Dependencies


- **ioredis** ^5.3.2

  - High-performance Redis client for caching novel processing status and comic metadata

- **@fastify/redis** ^6.1.1

  - Official Fastify Redis plugin for seamless integration with existing backend architecture

- **@fastify/caching** ^8.0.1

  - Built-in Fastify caching mechanisms for HTTP response caching

- **pg-pool** ^3.6.1

  - PostgreSQL connection pooling to prevent connection exhaustion during high load

- **@fastify/metrics** ^10.3.0

  - Performance monitoring and query timing metrics for optimization insights

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/cache.test.ts`
  - Scenarios: Cache hit/miss scenarios, Cache invalidation patterns, Redis connection failures, TTL expiration handling
- **File**: `apps/backend/src/__tests__/plugins/database.test.ts`
  - Scenarios: Connection pool initialization, Query execution with prepared statements, Connection pool exhaustion handling, Database reconnection logic
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/query-optimization.test.ts`
  - Scenarios: Novel content queries with caching, Comic pagination with cursor-based navigation, User authentication with session caching, Real-time status updates with cache invalidation
- **File**: `apps/backend/src/__tests__/integration/performance.test.ts`
  - Scenarios: Concurrent query execution under load, Memory usage during large dataset operations, Cache performance with high throughput
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

- **task**: Setup Redis configuration and Fastify plugins integration
- **done**: False
- **task**: Implement database connection pooling with pg-pool
- **done**: False
- **task**: Create cache service with invalidation strategies
- **done**: False
- **task**: Add performance indexes to Supabase schema
- **done**: False
- **task**: Implement cursor-based pagination for novels and comics routes
- **done**: False
- **task**: Add query monitoring middleware with metrics collection
- **done**: False
- **task**: Optimize authentication and user session queries with caching
- **done**: False
- **task**: Create performance testing suite with load scenarios
- **done**: False
- **task**: Document caching strategies and performance guidelines
- **done**: False
- **task**: Code review and performance validation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Query Performance Optimization is critical for Morpheus as the platform will handle computationally expensive operations like novel parsing, comic panel generation, and user management at scale. Poor database performance will directly impact user experience during story processing, dashboard loading, and storefront browsing. This task establishes foundational performance patterns before M1 backend services go live, preventing costly refactoring later.

**Technical Approach:**
- Implement Supabase query optimization with proper indexing strategies for novel content, user data, and comic metadata
- Use Fastify 5's built-in caching mechanisms with Redis for frequent queries (user sessions, comic thumbnails, processing status)
- Implement connection pooling with pg-pool for PostgreSQL connections
- Add query monitoring with @supabase/postgrest-js optimization patterns
- Implement cursor-based pagination for large datasets (novel chapters, comic panels)
- Use prepared statements and parameterized queries to prevent injection and improve performance
- Add database query logging and performance monitoring with Fastify metrics

**Dependencies:**
- External: ioredis, @fastify/redis, @supabase/supabase-js, pg-pool, @fastify/caching
- Internal: Database schema design, authentication service, file storage service

**Risks:**
- Over-optimization: Premature optimization could add complexity without measurable benefits
- Cache invalidation: Stale data in Redis could show outdated processing status or comic content
- Index bloat: Too many indexes could slow down write operations for novel uploads
- Connection limits: PostgreSQL connection exhaustion under high concurrent loads

**Complexity Notes:**
Higher complexity than initially estimated due to Morpheus's unique data patterns - novel text processing creates variable-length content, comic generation involves large binary data, and real-time status updates require careful cache management. The ML integration adds another layer of query complexity for training data and model outputs.

**Key Files:**
- packages/backend/src/plugins/database.ts: Connection pooling and query optimization setup
- packages/backend/src/services/cache.ts: Redis caching layer implementation
- packages/backend/src/routes/novels/: Query optimization for novel content endpoints
- packages/backend/src/routes/comics/: Pagination and caching for comic data
- packages/backend/src/middleware/metrics.ts: Query performance monitoring
- supabase/migrations/: Database indexes and constraints optimization


### Design Decisions

[{'decision': "Use Redis for caching with Fastify's built-in caching plugin", 'rationale': "Fastify 5's native caching integrates seamlessly with the existing architecture and provides better performance than external solutions", 'alternatives_considered': ['Memcached', 'In-memory Map-based caching', 'Supabase Edge Functions caching']}, {'decision': 'Implement cursor-based pagination over offset-based', 'rationale': 'Cursor pagination performs consistently well with large datasets and prevents page drift during novel processing', 'alternatives_considered': ['Offset-based pagination', 'Numbered pagination', 'Infinite scroll without pagination']}, {'decision': 'Use Supabase RLS policies for query optimization', 'rationale': 'Row Level Security policies push filtering to the database level, reducing data transfer and improving security', 'alternatives_considered': ['Application-level filtering', 'View-based access control', 'Separate read/write databases']}]
