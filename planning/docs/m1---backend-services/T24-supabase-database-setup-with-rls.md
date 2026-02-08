---
area: backend
dependsOn: []
effort: 5
iteration: I2
key: T24
milestone: M1 - Backend Services
priority: p0
title: Supabase Database Setup with RLS
type: Task
---

# Supabase Database Setup with RLS

## Acceptance Criteria

- [ ] **Supabase database schema with all core tables (users, novels, comic_pages, transformations, subscriptions) deployed with proper relationships and constraints**
  - Verification: Run 'npx supabase db describe' and verify all tables exist with correct schema
- [ ] **RLS policies enforce user ownership - users can only access their own novels and comic pages, admins can access all data**
  - Verification: Execute test queries with different user JWT tokens and verify access restrictions work correctly
- [ ] **TypeScript types generated from database schema are available and properly typed**
  - Verification: Import types from packages/database/types.ts and verify TypeScript compilation with proper type checking
- [ ] **Supabase client configured for both server-side and client-side usage with proper environment variable setup**
  - Verification: Test database connections from apps/web and apps/backend with different auth contexts
- [ ] **Audit logging and soft delete functionality working for all major tables**
  - Verification: Perform create/update/delete operations and verify audit_logs table populated and soft deletes preserve data

## Technical Notes

### Approach

Set up Supabase project with structured migrations for core tables (users, novels, comic_pages, transformations). 
Implement RLS policies that enforce user ownership while allowing admin access. Create TypeScript types from schema 
and configure Supabase client for both server and client-side usage. Include audit logging and soft delete patterns 
for data integrity. Test RLS policies thoroughly with different user roles and edge cases.


### Files to Modify

- **path**: package.json
- **changes**: Add Supabase CLI scripts and database-related dependencies
- **path**: .env.example
- **changes**: Add Supabase URL, anon key, and service role key templates

### New Files to Create

- **path**: supabase/config.toml
- **purpose**: Supabase project configuration
- **path**: supabase/migrations/20241201000001_initial_schema.sql
- **purpose**: Initial database schema with core tables
- **path**: supabase/migrations/20241201000002_rls_policies.sql
- **purpose**: Row Level Security policies for all tables
- **path**: supabase/migrations/20241201000003_audit_system.sql
- **purpose**: Audit logging triggers and soft delete functions
- **path**: packages/database/src/client.ts
- **purpose**: Supabase client configuration and initialization
- **path**: packages/database/src/types.ts
- **purpose**: Generated TypeScript types from database schema
- **path**: packages/database/src/policies.ts
- **purpose**: RLS policy helper functions and constants
- **path**: packages/database/package.json
- **purpose**: Database package dependencies and scripts
- **path**: apps/backend/src/lib/supabase.ts
- **purpose**: Backend-specific Supabase client with service role
- **path**: apps/web/src/lib/supabase.ts
- **purpose**: Client-side Supabase client configuration
- **path**: scripts/db-reset.sh
- **purpose**: Development database reset and seeding script
- **path**: scripts/generate-types.sh
- **purpose**: Script to regenerate TypeScript types from schema

### External Dependencies


- **@supabase/supabase-js** ^2.38.0

  - Official Supabase client for database operations and real-time subscriptions

- **@supabase/cli** ^1.123.0

  - Database migrations, type generation, and local development environment

- **pg** ^8.11.0

  - PostgreSQL client for direct database operations and connection pooling

- **zod** ^3.22.0

  - Runtime validation for database schemas and API input validation

## Testing

### Unit Tests

- **File**: `packages/database/src/__tests__/client.test.ts`
  - Scenarios: Supabase client initialization, Environment variable validation, Connection error handling
- **File**: `packages/database/src/__tests__/types.test.ts`
  - Scenarios: Type generation validation, Schema relationship types, Enum type definitions
### Integration Tests

- **File**: `packages/database/src/__tests__/integration/rls.test.ts`
  - Scenarios: User can only read their own novels, User cannot access other users' comic pages, Admin can access all resources, Unauthenticated requests properly blocked
- **File**: `packages/database/src/__tests__/integration/audit.test.ts`
  - Scenarios: Audit logs created on data changes, Soft delete preserves data but hides from queries, Admin can view deleted records
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

- **task**: Initialize Supabase project and configure local development environment
- **done**: False
- **task**: Create initial migration with core table schema (users, novels, comic_pages, transformations, subscriptions)
- **done**: False
- **task**: Implement RLS policies migration with comprehensive user ownership rules
- **done**: False
- **task**: Set up audit logging system with triggers and soft delete functions
- **done**: False
- **task**: Create database package with TypeScript client and type generation
- **done**: False
- **task**: Configure Supabase clients for backend and frontend applications
- **done**: False
- **task**: Write comprehensive integration tests for RLS policies and audit system
- **done**: False
- **task**: Create development scripts for database management and type generation
- **done**: False
- **task**: Document database schema, RLS policies, and development workflows
- **done**: False
- **task**: Deploy to staging and validate all functionality end-to-end
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task establishes the foundational database infrastructure for Morpheus, setting up Supabase with PostgreSQL and implementing Row Level Security (RLS) policies. This is critical for the novel-to-comic platform as it needs to securely manage user accounts, novel content, comic transformations, and billing data. RLS ensures users can only access their own content while allowing for proper admin access patterns and multi-tenant architecture.

**Technical Approach:**
- Use Supabase CLI for schema management and migrations
- Implement RLS policies using PostgreSQL's native security features
- Create TypeScript types from database schema using Supabase's type generation
- Design tables for users, novels, comic_pages, transformations, subscriptions, and audit logs
- Use Supabase's built-in auth integration for user management
- Implement soft deletes and audit trails for data integrity
- Create views for complex queries and reporting

**Dependencies:**
- External: @supabase/supabase-js, @supabase/cli, dotenv, pg (for local dev)
- Internal: Will be consumed by authentication service, novel processing service, and API routes

**Risks:**
- RLS policy complexity: Start simple, iterate; use policy templates and thorough testing
- Migration rollback challenges: Always create reversible migrations; test on staging first
- Performance with RLS: Monitor query plans; create appropriate indexes; consider materialized views for heavy queries
- Auth integration leaks: Validate RLS policies in isolation; use security-focused code reviews

**Complexity Notes:**
Higher complexity than typical database setup due to multi-tenant RLS requirements and the need to handle large binary assets (comic images). The ML integration for storing transformation metadata adds additional schema complexity.

**Key Files:**
- supabase/migrations/: SQL migration files for schema and RLS policies
- packages/database/: TypeScript types and client configuration
- apps/backend/src/lib/supabase.ts: Supabase client setup
- .env.example: Environment variable templates


### Design Decisions

[{'decision': 'Use Supabase RLS instead of application-level authorization', 'rationale': "Database-level security provides defense in depth, reduces code complexity, and leverages PostgreSQL's battle-tested security features", 'alternatives_considered': ['Application-level auth middleware', 'API Gateway authorization', 'Custom RBAC system']}, {'decision': 'Implement soft deletes for user content', 'rationale': 'Novel and comic data represents significant user investment; soft deletes enable recovery and comply with data retention policies', 'alternatives_considered': ['Hard deletes with backups', 'Archive tables', 'Event sourcing']}, {'decision': "Use Supabase's built-in auth with custom user profiles", 'rationale': 'Leverages proven auth system while allowing custom user metadata for subscription tiers and preferences', 'alternatives_considered': ['Custom JWT auth', 'Auth0 integration', 'NextAuth.js']}]
