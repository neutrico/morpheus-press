---
area: backend
dependsOn:
- T23
- T24
effort: 5
iteration: I2
key: T25
milestone: M1 - Backend Services
priority: p0
title: API Routes Implementation
type: Task
---

# API Routes Implementation

## Acceptance Criteria

- [ ] **All core API routes (/v1/auth, /v1/projects, /v1/novels, /v1/comics, /v1/assets) respond with proper HTTP status codes and follow RESTful conventions**
  - Verification: Run integration tests with `npm run test:integration` and verify all routes return expected status codes (200, 201, 400, 401, 404, 500)
- [ ] **Request/response validation works correctly using Zod schemas with comprehensive error messages**
  - Verification: Send malformed requests to each endpoint and verify proper 400 responses with detailed validation errors
- [ ] **JWT authentication protects all secured endpoints and integrates with Supabase**
  - Verification: Test authenticated and unauthenticated requests; verify JWT tokens are validated against Supabase users
- [ ] **OpenAPI documentation is auto-generated and accessible at /documentation endpoint**
  - Verification: Navigate to http://localhost:3001/documentation and verify all routes are documented with request/response schemas
- [ ] **Rate limiting prevents abuse with configurable limits per endpoint**
  - Verification: Send burst requests exceeding rate limits and verify 429 responses are returned

## Technical Notes

### Approach

Create domain-specific Fastify plugins (auth, projects, novels, comics, assets) with dedicated route handlers. 
Implement comprehensive Zod schemas for request validation and response serialization. 
Use middleware chains for authentication, rate limiting, and error handling. 
Structure routes following RESTful conventions with proper HTTP methods and status codes. 
Integrate with Supabase for data persistence and authentication, with ML services for async processing workflows.


### Files to Modify

- **path**: apps/backend/src/app.ts
- **changes**: Register route plugins, configure CORS, rate limiting, and Swagger
- **path**: apps/backend/package.json
- **changes**: Add Fastify plugins and Zod dependencies

### New Files to Create

- **path**: apps/backend/src/routes/auth.ts
- **purpose**: Authentication endpoints (login, register, refresh, logout)
- **path**: apps/backend/src/routes/projects.ts
- **purpose**: Project CRUD operations and management
- **path**: apps/backend/src/routes/novels.ts
- **purpose**: Novel upload, processing, and text extraction endpoints
- **path**: apps/backend/src/routes/comics.ts
- **purpose**: Comic generation, status checking, and download endpoints
- **path**: apps/backend/src/routes/assets.ts
- **purpose**: File serving, upload, and asset management
- **path**: apps/backend/src/plugins/auth.ts
- **purpose**: JWT authentication plugin with Supabase integration
- **path**: apps/backend/src/plugins/validation.ts
- **purpose**: Zod validation plugin with error formatting
- **path**: apps/backend/src/plugins/rate-limit.ts
- **purpose**: Rate limiting configuration per route
- **path**: apps/backend/src/schemas/auth.ts
- **purpose**: Authentication request/response Zod schemas
- **path**: apps/backend/src/schemas/projects.ts
- **purpose**: Project-related Zod validation schemas
- **path**: apps/backend/src/schemas/novels.ts
- **purpose**: Novel upload and processing schemas
- **path**: apps/backend/src/schemas/comics.ts
- **purpose**: Comic generation and metadata schemas
- **path**: apps/backend/src/schemas/common.ts
- **purpose**: Shared validation schemas (pagination, errors, etc.)
- **path**: apps/backend/src/middleware/error-handler.ts
- **purpose**: Global error handling with proper HTTP status mapping
- **path**: apps/backend/src/middleware/request-logger.ts
- **purpose**: Request/response logging middleware
- **path**: apps/backend/src/types/api.ts
- **purpose**: TypeScript types generated from Zod schemas
- **path**: apps/backend/src/utils/response-helpers.ts
- **purpose**: Standardized API response formatting utilities

### External Dependencies


- **@fastify/cors** ^9.0.0

  - Cross-origin resource sharing configuration for frontend integration

- **@fastify/jwt** ^8.0.0

  - JWT token verification and authentication middleware

- **@fastify/swagger** ^8.0.0

  - OpenAPI documentation generation and API explorer

- **@fastify/rate-limit** ^9.0.0

  - API rate limiting to prevent abuse and ensure fair usage

- **zod** ^3.22.0

  - Runtime validation and TypeScript type inference for API schemas

- **@fastify/multipart** ^8.0.0

  - File upload handling for novel documents and images

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/routes/auth.test.ts`
  - Scenarios: JWT token validation success/failure, User registration and login flows, Token refresh mechanism
- **File**: `apps/backend/src/__tests__/routes/projects.test.ts`
  - Scenarios: CRUD operations for projects, Project ownership validation, Pagination and filtering
- **File**: `apps/backend/src/__tests__/schemas/validation.test.ts`
  - Scenarios: Valid request schemas pass validation, Invalid requests return proper error messages, Type coercion works correctly
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/api-routes.test.ts`
  - Scenarios: Complete user workflow from registration to comic creation, File upload and asset serving pipeline, ML service integration for comic processing
- **File**: `apps/backend/src/__tests__/integration/auth-flow.test.ts`
  - Scenarios: Supabase authentication integration, Protected route access control
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 1
- **Total**: 9

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Fastify plugins and dependencies in package.json
- **done**: False
- **task**: Create base Zod schemas for all domains (auth, projects, novels, comics)
- **done**: False
- **task**: Implement authentication plugin with Supabase JWT validation
- **done**: False
- **task**: Build core route handlers for each domain with proper validation
- **done**: False
- **task**: Configure rate limiting, CORS, and security middleware
- **done**: False
- **task**: Integrate OpenAPI/Swagger documentation generation
- **done**: False
- **task**: Implement error handling and response standardization
- **done**: False
- **task**: Write comprehensive unit and integration tests
- **done**: False
- **task**: Test ML service integration endpoints for async workflows
- **done**: False
- **task**: Document API endpoints and update technical documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task involves implementing the core API routes for Morpheus's backend services using Fastify 5. As a novel-to-comic transformation platform, we need RESTful endpoints for user management, novel upload/processing, comic generation workflows, project management, and asset serving. This is foundational infrastructure that enables the dashboard and storefront frontends to interact with backend services, manage the ML pipeline, and handle user data securely.

**Technical Approach:**
- Use Fastify 5's plugin architecture for modular route organization
- Implement OpenAPI/Swagger documentation with @fastify/swagger
- Apply JWT-based authentication with Supabase integration
- Use Zod for request/response validation and TypeScript type generation
- Implement rate limiting and CORS policies
- Follow RESTful conventions with proper HTTP status codes
- Use Fastify's built-in serialization for performance
- Implement middleware for logging, error handling, and request validation

**Dependencies:**
- External: @fastify/cors, @fastify/jwt, @fastify/swagger, @fastify/rate-limit, zod, @supabase/supabase-js
- Internal: Database schemas, authentication middleware, ML service integrations, file upload handlers

**Risks:**
- API versioning strategy: Implement /v1 prefix from start to avoid breaking changes
- Rate limiting bypass: Use distributed rate limiting with Redis for multi-instance deployments
- Validation performance: Cache Zod schemas and use Fastify's built-in serialization
- Authentication token leakage: Implement proper CORS, secure headers, and token rotation
- File upload vulnerabilities: Validate file types, implement size limits, scan for malware

**Complexity Notes:**
More complex than initially estimated due to need for comprehensive validation schemas, proper error handling patterns, and integration with multiple external services (Supabase, OpenAI, RunPod). The ML pipeline integration adds significant complexity for handling async operations and webhook endpoints.

**Key Files:**
- apps/backend/src/routes/: Route definitions organized by domain
- apps/backend/src/plugins/: Custom Fastify plugins for auth, validation
- apps/backend/src/schemas/: Zod validation schemas
- apps/backend/src/types/: TypeScript type definitions
- apps/backend/src/middleware/: Authentication and authorization middleware


### Design Decisions

[{'decision': 'Use Fastify plugin architecture with domain-based route organization', 'rationale': "Enables modular development, easy testing, and clear separation of concerns while leveraging Fastify's performance benefits", 'alternatives_considered': ['Express with custom middleware', 'Koa with router', 'NestJS decorators']}, {'decision': 'Implement Zod schemas for validation with automatic TypeScript type generation', 'rationale': 'Provides runtime validation, compile-time type safety, and reduces boilerplate while being framework agnostic', 'alternatives_considered': ['Joi validation', 'class-validator decorators', 'JSON Schema']}, {'decision': 'Use Supabase Auth integration with JWT verification middleware', 'rationale': 'Leverages existing Supabase infrastructure, provides secure token validation, and integrates with database RLS policies', 'alternatives_considered': ['Custom JWT implementation', 'Passport.js strategies', 'Auth0 integration']}]
