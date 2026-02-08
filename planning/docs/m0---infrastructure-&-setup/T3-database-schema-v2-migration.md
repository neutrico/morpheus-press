---
area: setup
dependsOn: []
effort: 5
iteration: I1
key: T3
milestone: M0 - Infrastructure & Setup
priority: p0
title: Database Schema v2 Migration
type: Task
---

# Database Schema v2 Migration

## Acceptance Criteria

- [ ] **All database tables (users, projects, novels, chapters, panels, transformation_jobs, ai_assets) are created with proper relationships and constraints**
  - Verification: Run `supabase db describe` and verify all tables exist with correct foreign keys and constraints
- [ ] **Row Level Security policies enable proper multi-tenant access control for all tables**
  - Verification: Execute test queries as different user roles and verify data isolation using `supabase test db`
- [ ] **Migration can be applied and rolled back without data loss**
  - Verification: Run migration, seed test data, rollback, re-apply migration and verify data integrity
- [ ] **TypeScript types are generated and match database schema**
  - Verification: Run `supabase gen types typescript` and verify generated types in packages/shared/types/database.ts compile without errors
- [ ] **Database service layer provides type-safe CRUD operations for all entities**
  - Verification: Unit tests pass for all service methods and TypeScript compilation succeeds without type errors

## Technical Notes

### Approach

Create Supabase migration files defining core tables (users, projects, novels, chapters, panels, transformation_jobs, ai_assets) with proper relationships and constraints. Implement Row Level Security policies for multi-tenant access control. Generate TypeScript types from schema using Supabase CLI. Create database service layer in backend with type-safe query builders using Drizzle ORM. Test migration rollback scenarios and seed development data.


### Files to Modify

- **path**: supabase/config.toml
- **changes**: Add RLS configuration and environment-specific settings
- **path**: packages/shared/types/index.ts
- **changes**: Export new database types and update existing interfaces
- **path**: apps/backend/src/lib/supabase.ts
- **changes**: Update client configuration for new schema

### New Files to Create

- **path**: supabase/migrations/20240101000000_schema_v2.sql
- **purpose**: Main migration file with all table definitions and constraints
- **path**: supabase/migrations/20240101000001_rls_policies.sql
- **purpose**: Row Level Security policies for all tables
- **path**: supabase/migrations/20240101000002_functions_triggers.sql
- **purpose**: Database functions and triggers for audit trails and business logic
- **path**: supabase/seed.sql
- **purpose**: Development seed data for testing
- **path**: packages/shared/types/database.ts
- **purpose**: Generated TypeScript interfaces for all database tables
- **path**: apps/backend/src/services/database/base.ts
- **purpose**: Base database service with common CRUD operations
- **path**: apps/backend/src/services/database/users.ts
- **purpose**: User-specific database operations
- **path**: apps/backend/src/services/database/projects.ts
- **purpose**: Project and novel management database operations
- **path**: apps/backend/src/services/database/transformations.ts
- **purpose**: AI transformation job database operations
- **path**: apps/backend/src/services/database/index.ts
- **purpose**: Database service exports and initialization
- **path**: supabase/scripts/backup.sh
- **purpose**: Automated backup script for migration safety
- **path**: supabase/scripts/test-migration.sh
- **purpose**: Migration testing script for CI/CD

### External Dependencies


- **@supabase/supabase-js** ^2.38.0

  - Official Supabase client for database operations

- **drizzle-orm** ^0.29.0

  - Type-safe SQL query builder with Supabase integration

- **zod** ^3.22.0

  - Runtime schema validation for API inputs/outputs

- **supabase** ^1.113.0

  - Supabase CLI for migration management and type generation

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/database.test.ts`
  - Scenarios: CRUD operations for each table, Foreign key constraint validation, Soft delete functionality, Query builder type safety
- **File**: `apps/backend/src/__tests__/services/user-service.test.ts`
  - Scenarios: User creation and authentication, RLS policy enforcement, Profile updates
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/migration.test.ts`
  - Scenarios: Full migration apply/rollback cycle, Data seeding and retrieval, Cross-table relationship queries, RLS policy integration with auth
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

- **task**: Set up Supabase CLI and verify connection to development environment
- **done**: False
- **task**: Design and document database schema with entity relationship diagram
- **done**: False
- **task**: Create migration files for tables, constraints, and indexes
- **done**: False
- **task**: Implement Row Level Security policies for multi-tenant access
- **done**: False
- **task**: Create database functions and triggers for audit trails
- **done**: False
- **task**: Generate TypeScript types and update shared package
- **done**: False
- **task**: Implement database service layer with Drizzle ORM integration
- **done**: False
- **task**: Create comprehensive test suite for all database operations
- **done**: False
- **task**: Test migration rollback scenarios and backup procedures
- **done**: False
- **task**: Document schema changes and update API documentation
- **done**: False
- **task**: Code review and security audit of RLS policies
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Database Schema v2 Migration represents the evolution from initial MVP schemas to production-ready database architecture for the novel-to-comic platform. This task is critical for establishing proper data relationships between users, novels, comic panels, transformation jobs, and AI-generated assets. It enables core business features like user authentication, content management, billing integration, and ML pipeline data persistence. Without this foundation, subsequent development tasks cannot proceed.

**Technical Approach:**
Leverage Supabase's migration system with PostgreSQL-native features including row-level security (RLS), triggers, and functions. Implement schema versioning with proper rollback capabilities using Supabase CLI. Design normalized tables for users, projects, novels, chapters, panels, transformation_jobs, and ai_assets with proper foreign key constraints. Use PostgreSQL enums for status fields and JSONB for flexible metadata storage. Implement audit trails with created_at/updated_at timestamps and soft deletes where appropriate.

**Dependencies:**
- External: @supabase/supabase-js ^2.38.0, drizzle-orm for type-safe queries, zod for schema validation
- Internal: Backend authentication service, file storage service, ML pipeline integration points

**Risks:**
- Data loss during migration: Implement comprehensive backup strategy and test migrations in staging
- Performance degradation: Index key columns and implement proper query optimization
- Breaking changes to existing code: Version API endpoints and maintain backward compatibility
- RLS policy complexity: Start with simple policies and iterate, extensive testing required

**Complexity Notes:**
More complex than initially estimated due to Supabase RLS requirements and the need to support both dashboard and storefront access patterns. The interconnected nature of novel content, comic panels, and AI transformation jobs requires careful foreign key design and cascading delete strategies.

**Key Files:**
- supabase/migrations/: New migration files with CREATE TABLE statements
- packages/shared/types/database.ts: TypeScript interfaces for all tables
- apps/backend/src/services/: Database service layer implementations
- supabase/config.toml: Environment and RLS configuration


### Design Decisions

[{'decision': 'Use Supabase native migrations over ORM migrations', 'rationale': 'Better integration with Supabase dashboard, RLS policies, and edge functions', 'alternatives_considered': ['Drizzle migrations', 'Prisma migrations', 'Custom migration scripts']}, {'decision': 'Implement soft deletes for user content', 'rationale': 'Enables content recovery and maintains referential integrity for AI training data', 'alternatives_considered': ['Hard deletes with cascade', 'Archive tables', 'Versioned records']}, {'decision': 'JSONB for AI model parameters and metadata', 'rationale': 'Flexible schema for different AI model configurations without schema changes', 'alternatives_considered': ['Separate parameter tables', 'Text fields with JSON', 'EAV pattern']}]
