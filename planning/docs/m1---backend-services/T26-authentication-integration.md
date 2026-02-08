---
area: backend
dependsOn:
- T24
effort: 3
iteration: I2
key: T26
milestone: M1 - Backend Services
priority: p0
title: Authentication Integration
type: Task
---

# Authentication Integration

## Acceptance Criteria

- [ ] **Users can register, login, and logout with email/password through Supabase Auth**
  - Verification: POST /auth/register, POST /auth/login, POST /auth/logout return appropriate status codes and valid JWT tokens
- [ ] **JWT tokens expire after 15 minutes and refresh tokens rotate properly**
  - Verification: Test token expiration at 15min mark and verify refresh endpoint returns new access/refresh token pair
- [ ] **Protected routes require valid JWT and return 401 for unauthorized requests**
  - Verification: Access protected endpoints without token returns 401, with valid token returns expected data
- [ ] **Role-based access control prevents unauthorized access to admin/premium features**
  - Verification: User role cannot access admin routes, premium features require premium role
- [ ] **Rate limiting prevents brute force attacks on authentication endpoints**
  - Verification: Exceed rate limit (5 attempts/minute) on /auth/login returns 429 status

## Technical Notes

### Approach

Create a Fastify plugin that integrates Supabase Auth with JWT token verification middleware. Implement user registration/login endpoints that leverage Supabase's built-in auth methods. Set up automatic JWT refresh handling and secure cookie-based session management. Create role-based middleware decorators for protecting routes based on user permissions. Establish user profile management with proper validation using Zod schemas.


### Files to Modify

- **path**: packages/backend/src/app.ts
- **changes**: Register auth plugin, add CORS configuration for auth endpoints
- **path**: packages/backend/package.json
- **changes**: Add dependencies: @supabase/supabase-js, @fastify/jwt, @fastify/cookie, @fastify/cors, bcrypt, zod
- **path**: packages/backend/.env.example
- **changes**: Add Supabase URL, anon key, service role key, JWT secret

### New Files to Create

- **path**: packages/backend/src/plugins/auth.ts
- **purpose**: Fastify plugin for Supabase Auth integration and JWT handling
- **path**: packages/backend/src/middleware/authenticate.ts
- **purpose**: JWT verification middleware with role-based access control
- **path**: packages/backend/src/middleware/rate-limit.ts
- **purpose**: Rate limiting middleware for auth endpoints
- **path**: packages/backend/src/routes/auth/register.ts
- **purpose**: User registration endpoint with validation
- **path**: packages/backend/src/routes/auth/login.ts
- **purpose**: User login endpoint with JWT token generation
- **path**: packages/backend/src/routes/auth/logout.ts
- **purpose**: User logout endpoint with token invalidation
- **path**: packages/backend/src/routes/auth/refresh.ts
- **purpose**: JWT refresh token endpoint
- **path**: packages/backend/src/routes/auth/profile.ts
- **purpose**: User profile management endpoints
- **path**: packages/backend/src/services/user.service.ts
- **purpose**: User management service interfacing with Supabase
- **path**: packages/backend/src/services/supabase.service.ts
- **purpose**: Supabase client configuration and utilities
- **path**: packages/backend/src/types/auth.ts
- **purpose**: TypeScript interfaces for authentication objects
- **path**: packages/backend/src/schemas/auth.schemas.ts
- **purpose**: Zod validation schemas for auth endpoints
- **path**: supabase/migrations/001_create_auth_tables.sql
- **purpose**: Database schema for user profiles and roles
- **path**: supabase/migrations/002_setup_rls_policies.sql
- **purpose**: Row Level Security policies for user data access

### External Dependencies


- **@supabase/supabase-js** ^2.39.0

  - Official Supabase client for authentication and database operations

- **@fastify/jwt** ^8.0.0

  - JWT token generation and verification for Fastify

- **@fastify/cookie** ^9.3.1

  - Secure cookie handling for refresh tokens

- **@fastify/cors** ^9.0.1

  - CORS configuration for frontend authentication requests

- **bcrypt** ^5.1.1

  - Password hashing for additional security layers

- **zod** ^3.22.4

  - Runtime validation for authentication payloads

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/plugins/auth.test.ts`
  - Scenarios: JWT token generation and validation, User role verification, Token refresh logic, Error handling for invalid tokens
- **File**: `packages/backend/src/__tests__/middleware/authenticate.test.ts`
  - Scenarios: Valid token allows access, Expired token returns 401, Missing token returns 401, Role-based access validation
- **File**: `packages/backend/src/__tests__/services/user.service.test.ts`
  - Scenarios: User profile creation/updates, Password validation, Role assignment logic
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/auth.test.ts`
  - Scenarios: Complete registration flow with Supabase, Login flow with JWT generation, Token refresh workflow, Protected route access with middleware, Rate limiting enforcement
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

- **task**: Setup Supabase project and obtain API keys
- **done**: False
- **task**: Install required dependencies and configure environment variables
- **done**: False
- **task**: Create database migrations for user profiles and roles
- **done**: False
- **task**: Implement Supabase service and auth plugin
- **done**: False
- **task**: Create JWT middleware with role-based access control
- **done**: False
- **task**: Implement authentication route handlers (register/login/logout/refresh)
- **done**: False
- **task**: Add rate limiting middleware to auth endpoints
- **done**: False
- **task**: Create user profile management endpoints
- **done**: False
- **task**: Write comprehensive unit and integration tests
- **done**: False
- **task**: Update API documentation and create usage examples
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Authentication is the foundational security layer for Morpheus, enabling user registration, login, and secure access control across the platform. This directly supports user management for the comic creation pipeline, subscription handling, and API access control. Since Morpheus uses Supabase as the database, leveraging Supabase Auth provides a comprehensive, production-ready authentication system with minimal custom implementation.

**Technical Approach:**
Implement Supabase Auth as the primary authentication provider, integrated with Fastify 5 backend. Use JWT-based authentication with refresh token rotation. Implement role-based access control (RBAC) with roles like 'user', 'premium', 'admin'. Create authentication middleware for route protection, session management utilities, and user profile management endpoints. Follow OAuth 2.0 patterns for third-party integrations (Google, GitHub).

**Dependencies:**
- External: @supabase/supabase-js, @fastify/jwt, @fastify/cookie, @fastify/cors, bcrypt, zod (validation)
- Internal: Database schemas (users, profiles, roles), error handling service, logging service, rate limiting middleware

**Risks:**
- Session management complexity: Use Supabase's built-in session handling with proper refresh token rotation
- JWT security vulnerabilities: Implement short-lived access tokens (15min) with secure refresh mechanism
- Rate limiting bypass: Implement strict rate limiting on auth endpoints to prevent brute force
- Data consistency across services: Use Supabase RLS (Row Level Security) for consistent access control

**Complexity Notes:**
Medium complexity - Supabase Auth significantly reduces implementation overhead compared to custom auth. Main complexity lies in proper middleware integration with Fastify 5's new plugin system and ensuring seamless frontend integration.

**Key Files:**
- packages/backend/src/plugins/auth.ts: Fastify auth plugin
- packages/backend/src/middleware/authenticate.ts: JWT verification middleware
- packages/backend/src/routes/auth/: Authentication route handlers
- packages/backend/src/services/user.service.ts: User management logic
- packages/backend/src/types/auth.ts: Authentication type definitions
- supabase/migrations/: User tables and RLS policies


### Design Decisions

[{'decision': 'Use Supabase Auth as primary authentication provider', 'rationale': 'Leverages existing Supabase infrastructure, provides enterprise-grade security, handles complex auth flows, and reduces maintenance overhead', 'alternatives_considered': ['Custom JWT implementation', 'Auth0', 'Firebase Auth']}, {'decision': 'Implement middleware-based route protection in Fastify', 'rationale': "Provides clean separation of concerns, reusable across routes, and integrates well with Fastify's plugin architecture", 'alternatives_considered': ['Decorator-based auth', 'Route-level auth checks', 'Gateway-level auth']}, {'decision': 'Use Row Level Security (RLS) for database-level access control', 'rationale': 'Ensures data security at the database layer, prevents data leaks even if application logic fails, and scales automatically', 'alternatives_considered': ['Application-level access control', 'View-based security', 'Manual query filtering']}]
