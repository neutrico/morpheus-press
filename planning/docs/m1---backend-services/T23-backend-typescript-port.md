---
area: backend
dependsOn: []
effort: 8
iteration: I2
key: T23
milestone: M1 - Backend Services
priority: p0
title: Backend TypeScript Port
type: Task
---

# Backend TypeScript Port

## Acceptance Criteria

- [ ] **All TypeScript compilation passes with strict mode enabled and zero errors**
  - Verification: Run `npm run type-check` in backend directory with exit code 0
- [ ] **All existing API endpoints maintain functionality with proper TypeScript types**
  - Verification: Run integration test suite with 100% endpoint coverage and all tests passing
- [ ] **Supabase client operations are fully typed with generated schema types**
  - Verification: Database queries show proper IntelliSense and compile-time type checking
- [ ] **ML service integrations (OpenAI/Anthropic/RunPod) have complete type coverage**
  - Verification: All ML API calls have typed request/response interfaces with runtime validation
- [ ] **Development experience improvements are measurable**
  - Verification: IDE shows proper autocomplete, error detection, and refactoring support across all TypeScript files

## Technical Notes

### Approach

Start by setting up strict TypeScript configuration and converting core server setup. Implement Zod schemas for all API endpoints with type inference for request/response validation. Generate Supabase types from database schema and create typed client wrapper. Convert ML service integrations with proper typing for complex nested responses. Finally, implement Fastify type providers for end-to-end type safety across all routes. Use incremental migration approach to maintain functionality throughout the port.


### Files to Modify

- **path**: apps/backend/package.json
- **changes**: Add TypeScript dependencies, update build scripts to use tsx/tsc
- **path**: apps/backend/src/server.js
- **changes**: Rename to server.ts, add strict typing for Fastify instance and plugins
- **path**: apps/backend/src/routes/*.js
- **changes**: Convert all route files to TypeScript with Zod schemas and type providers
- **path**: apps/backend/src/lib/supabase.js
- **changes**: Convert to TypeScript with generated database types and typed client wrapper
- **path**: apps/backend/src/middleware/*.js
- **changes**: Add TypeScript typing for auth middleware and request context

### New Files to Create

- **path**: apps/backend/tsconfig.json
- **purpose**: Strict TypeScript configuration with path mapping and modern target
- **path**: apps/backend/src/types/index.ts
- **purpose**: Global type definitions and re-exports
- **path**: apps/backend/src/types/ml-services.ts
- **purpose**: Typed interfaces for OpenAI, Anthropic, and RunPod API contracts
- **path**: apps/backend/src/types/database.ts
- **purpose**: Generated Supabase types and custom database interfaces
- **path**: apps/backend/src/schemas/api.ts
- **purpose**: Zod schemas for all API endpoints with type inference
- **path**: apps/backend/src/lib/validation.ts
- **purpose**: Utility functions for runtime validation and error handling
- **path**: apps/backend/src/lib/type-guards.ts
- **purpose**: Type guard functions for runtime type checking

### External Dependencies


- **zod** ^3.22.4

  - Runtime validation with TypeScript inference for API schemas and ML service payloads

- **@fastify/type-provider-typebox** ^4.0.0

  - Fastify's recommended type provider for end-to-end type safety

- **tsx** ^4.7.0

  - Fast TypeScript execution for development and testing

- **supabase** ^2.38.0

  - Latest Supabase client with improved TypeScript support and type generation

- **@types/node** ^20.10.0

  - Node.js type definitions compatible with current LTS

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/types/ml-services.test.ts`
  - Scenarios: OpenAI response type validation, Anthropic message format typing, RunPod job state transitions, Type inference from Zod schemas
- **File**: `apps/backend/src/__tests__/lib/supabase.test.ts`
  - Scenarios: Generated type compatibility, Query result type inference, Error handling with typed responses
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/api-routes.test.ts`
  - Scenarios: End-to-end type safety from request to response, Zod validation integration with Fastify, Error response type consistency
- **File**: `apps/backend/src/__tests__/integration/ml-workflows.test.ts`
  - Scenarios: Complete ML pipeline with typed data flow, File upload processing with proper types
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 8

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup TypeScript configuration and development tooling
- **done**: False
- **task**: Install dependencies and configure build scripts
- **done**: False
- **task**: Convert core server setup and plugin registration to TypeScript
- **done**: False
- **task**: Generate and integrate Supabase database types
- **done**: False
- **task**: Create Zod schemas for all API endpoints with validation
- **done**: False
- **task**: Convert ML service integrations with proper typing
- **done**: False
- **task**: Implement Fastify type providers for end-to-end type safety
- **done**: False
- **task**: Convert all route handlers and middleware to TypeScript
- **done**: False
- **task**: Add comprehensive type testing and validation tests
- **done**: False
- **task**: Update documentation and development setup guides
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task involves porting the existing backend from JavaScript to TypeScript to improve type safety, developer experience, and maintainability. Given Morpheus handles complex ML workflows, file uploads, and integrates with multiple external services (OpenAI/Anthropic, RunPod, Supabase), strong typing will prevent runtime errors and improve API contract enforcement. This is critical for M1 as all subsequent backend development will build on this foundation.

**Technical Approach:**
- Implement strict TypeScript configuration with Fastify 5's native TypeScript support
- Use Zod for runtime validation and type inference for API schemas
- Implement proper typing for Supabase client with generated types
- Create typed interfaces for ML service integrations (OpenAI/Anthropic responses, RunPod API)
- Use Fastify's type providers for end-to-end type safety
- Implement proper error handling with typed error responses
- Set up path mapping for clean imports and module resolution

**Dependencies:**
- External: [@fastify/type-provider-typebox, zod, @types/node, tsx, supabase (with generated types)]
- Internal: Database schema definitions, API route structure, authentication middleware

**Risks:**
- Type complexity explosion: Start with interfaces, gradually add generics. Use utility types sparingly.
- Migration breaking existing functionality: Implement incrementally with comprehensive test coverage using Vitest
- Performance overhead from TypeScript compilation: Use SWC or esbuild for faster builds in development
- Supabase type generation issues: Pin Supabase CLI version and use generated types as base with manual overrides

**Complexity Notes:**
More complex than initial estimate due to ML service integrations requiring complex nested types for prompts, responses, and image generation parameters. The async nature of RunPod jobs will need careful typing for state management and webhook handling.

**Key Files:**
- src/server.ts: Main Fastify server setup with TypeScript configuration
- src/types/: Global type definitions for ML services, database models
- src/routes/: Convert all route handlers to TypeScript with proper typing
- src/lib/supabase.ts: Typed Supabase client configuration
- src/lib/ml-services.ts: Typed interfaces for OpenAI/Anthropic/RunPod
- tsconfig.json: Strict TypeScript configuration
- package.json: Add TypeScript build scripts


### Design Decisions

[{'decision': 'Use Zod for schema validation with TypeScript inference', 'rationale': 'Provides runtime validation and compile-time types from single source of truth, essential for ML API integrations where payload structure is critical', 'alternatives_considered': ['Joi with separate TypeScript interfaces', 'Pure TypeScript without runtime validation', "Fastify's built-in validation"]}, {'decision': 'Generate Supabase types from database schema', 'rationale': 'Ensures backend types stay in sync with database schema changes, critical for novel processing workflow data integrity', 'alternatives_considered': ['Manual type definitions', 'Generic database interfaces', 'ORM with built-in typing']}, {'decision': 'Implement Fastify type providers for end-to-end safety', 'rationale': 'Ensures request/response types are enforced from route definition to handler implementation, preventing API contract violations', 'alternatives_considered': ['Manual typing per route', 'Shared interfaces without enforcement', 'OpenAPI schema generation']}]
