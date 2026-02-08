---
area: backend
dependsOn:
- T25
effort: 2
iteration: I2
key: T32
milestone: M1 - Backend Services
priority: p1
title: API Documentation & OpenAPI
type: Task
---

# API Documentation & OpenAPI

## Acceptance Criteria

- [ ] **All API endpoints expose comprehensive OpenAPI 3.0 specifications with request/response schemas**
  - Verification: Visit /docs endpoint and verify all routes have complete schema definitions with examples
- [ ] **TypeScript types are automatically generated from OpenAPI specs and used in frontend**
  - Verification: Run `npm run generate:types` and verify packages/shared/types/api.ts contains current API types
- [ ] **API documentation is accessible through interactive Swagger UI with working examples**
  - Verification: Navigate to /docs, test API endpoints directly through the UI with valid authentication
- [ ] **Schema validation enforces documented API contracts on all endpoints**
  - Verification: Send malformed requests to any endpoint and verify proper validation errors with schema references
- [ ] **Public and internal APIs are properly separated in documentation**
  - Verification: Verify /docs shows only public endpoints while /internal/docs shows internal service APIs

## Technical Notes

### Approach

Implement comprehensive API documentation by integrating @fastify/swagger with existing Fastify routes, adding JSON Schema definitions to all endpoints for automatic OpenAPI spec generation. Create a shared schema library for common types (User, Novel, Comic, etc.) that can be reused across routes. Set up automated TypeScript type generation from OpenAPI specs to maintain type safety between frontend and backend. Establish API versioning strategy and documentation hosting through Fastify's swagger-ui plugin.


### Files to Modify

- **path**: packages/backend/src/app.ts
- **changes**: Register @fastify/swagger and @fastify/swagger-ui plugins with configuration
- **path**: packages/backend/src/routes/auth/login.ts
- **changes**: Add comprehensive JSON schemas for login request/response with examples
- **path**: packages/backend/src/routes/novels/upload.ts
- **changes**: Add multipart file upload schema, progress tracking response schema
- **path**: packages/backend/src/routes/novels/process.ts
- **changes**: Add novel processing request schema, ML pipeline status response schemas
- **path**: packages/backend/src/routes/comics/generate.ts
- **changes**: Add comic generation parameters schema, generation status and result schemas
- **path**: packages/backend/src/routes/user/profile.ts
- **changes**: Add user profile schemas with proper field validation and examples
- **path**: packages/backend/package.json
- **changes**: Add type generation scripts and OpenAPI tooling dependencies

### New Files to Create

- **path**: packages/backend/src/plugins/swagger.ts
- **purpose**: Fastify plugin for OpenAPI configuration, custom transformations, and security schemes
- **path**: packages/backend/src/schemas/index.ts
- **purpose**: Centralized JSON schema definitions for User, Novel, Comic, ML job status, etc.
- **path**: packages/backend/src/schemas/auth.ts
- **purpose**: Authentication-related schemas (login, register, tokens, permissions)
- **path**: packages/backend/src/schemas/novel.ts
- **purpose**: Novel entity schemas (metadata, content, processing status, validation rules)
- **path**: packages/backend/src/schemas/comic.ts
- **purpose**: Comic generation schemas (parameters, panels, pages, output formats)
- **path**: packages/backend/src/schemas/common.ts
- **purpose**: Shared/common schemas (pagination, error responses, file uploads, timestamps)
- **path**: packages/backend/src/utils/schema-validation.ts
- **purpose**: Custom schema validators and format checkers for business logic
- **path**: packages/shared/types/api.ts
- **purpose**: Generated TypeScript types from OpenAPI specs for frontend consumption
- **path**: scripts/generate-types.js
- **purpose**: Script to generate TypeScript types from OpenAPI spec using openapi-typescript

### External Dependencies


- **@fastify/swagger** ^8.0.0

  - Automatic OpenAPI 3.0 specification generation from Fastify JSON schemas

- **@fastify/swagger-ui** ^4.0.0

  - Interactive API documentation interface hosted within the application

- **@apidevtools/swagger-parser** ^10.1.0

  - OpenAPI spec validation and dereferencing for build-time checks

- **openapi-typescript** ^7.0.0

  - Generate TypeScript types from OpenAPI specs for frontend consumption

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/plugins/swagger.test.ts`
  - Scenarios: OpenAPI spec generation from route schemas, Schema validation for request/response objects, Custom transformations and security definitions, Error handling for malformed schemas
- **File**: `packages/backend/src/__tests__/schemas/index.test.ts`
  - Scenarios: Shared schema definitions validate correctly, Schema composition and inheritance, Custom format validators
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/api-docs.test.ts`
  - Scenarios: Generated OpenAPI spec matches actual API behavior, Swagger UI renders correctly with authentication, Type generation produces valid TypeScript, API versioning works across different spec versions
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

- **task**: Install and configure @fastify/swagger, @fastify/swagger-ui, openapi-typescript dependencies
- **done**: False
- **task**: Create swagger plugin with OpenAPI 3.0 configuration, security schemes, and custom transforms
- **done**: False
- **task**: Build comprehensive schema library for all entity types (User, Novel, Comic, etc.)
- **done**: False
- **task**: Retrofit all existing route handlers with proper JSON schemas for validation and documentation
- **done**: False
- **task**: Implement API versioning strategy and separate public/internal documentation endpoints
- **done**: False
- **task**: Set up automated TypeScript type generation from OpenAPI specs with build scripts
- **done**: False
- **task**: Add comprehensive examples and descriptions to all schema definitions
- **done**: False
- **task**: Implement schema validation testing and contract testing between frontend/backend
- **done**: False
- **task**: Configure CI/CD pipeline to validate OpenAPI specs and detect breaking changes
- **done**: False
- **task**: Update developer documentation with API usage examples and SDK generation instructions
- **done**: False

## Agent Notes

### Research Findings

**Context:**
API documentation and OpenAPI specification is crucial for Morpheus as a platform that will have multiple consumers - the Next.js dashboard/storefront frontends, potential mobile apps, third-party integrations, and developer partners. Given that Morpheus transforms novels to comics using ML services, having well-documented APIs ensures smooth integration between services and enables future scaling. This task provides the foundation for API contracts, client SDK generation, and developer onboarding.

**Technical Approach:**
Leverage Fastify's excellent OpenAPI ecosystem with @fastify/swagger and @fastify/swagger-ui for automatic spec generation from route schemas. Use JSON Schema for request/response validation that doubles as documentation. Implement a documentation-first approach where schemas drive both validation and API docs. Generate TypeScript types from OpenAPI specs to ensure type safety across frontend/backend boundaries. Consider using @apidevtools/swagger-parser for spec validation and potentially @openapitools/openapi-generator-cli for client SDK generation.

**Dependencies:**
- External: @fastify/swagger, @fastify/swagger-ui, @apidevtools/swagger-parser, @openapitools/openapi-generator-cli
- Internal: All existing Fastify route handlers, authentication middleware, database schemas (Supabase types), ML service integration endpoints

**Risks:**
- Schema drift: API implementations diverging from docs over time - mitigation: automated schema validation in CI/CD
- Performance overhead: Large OpenAPI specs affecting startup time - mitigation: lazy loading and spec caching
- Breaking changes: Unintentional API changes breaking frontends - mitigation: semantic versioning and contract testing
- Security exposure: Accidentally documenting internal endpoints - mitigation: separate public/internal API documentation

**Complexity Notes:**
This is moderately complex due to the need to retrofit existing routes with proper schemas and the interconnected nature of Morpheus APIs (novel processing, comic generation, user management, ML orchestration). The task becomes more complex when considering client SDK generation and maintaining documentation across multiple API versions.

**Key Files:**
- packages/backend/src/app.ts: Register swagger plugins and configure OpenAPI options
- packages/backend/src/routes/**: Add comprehensive JSON schemas to all route definitions
- packages/backend/src/schemas/**: Create shared schema definitions for common types
- packages/backend/src/plugins/swagger.ts: Custom swagger configuration and transformations
- packages/shared/types/**: Generated TypeScript types from OpenAPI specs


### Design Decisions

[{'decision': "Use Fastify's native JSON Schema integration with @fastify/swagger", 'rationale': 'Provides automatic OpenAPI generation from existing route schemas, reduces maintenance burden, and ensures documentation stays in sync with implementation', 'alternatives_considered': ['Manual OpenAPI spec writing', 'External tools like Stoplight', 'GraphQL with introspection']}, {'decision': 'Generate TypeScript client types from OpenAPI specs', 'rationale': 'Ensures type safety between frontend and backend, catches breaking changes at compile time, and improves developer experience', 'alternatives_considered': ['Manual type definitions', 'Runtime type checking only', 'Separate frontend/backend types']}, {'decision': 'Implement API versioning through URL paths (/v1/, /v2/)', 'rationale': 'Explicit versioning supports backward compatibility as Morpheus evolves, essential for platform stability', 'alternatives_considered': ['Header-based versioning', 'No versioning', 'Query parameter versioning']}]
