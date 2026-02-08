---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T4
milestone: M0 - Infrastructure & Setup
priority: p0
title: Testing Infrastructure Setup
type: Task
---

# Testing Infrastructure Setup

## Acceptance Criteria

- [ ] **All packages have unit testing configured with Vitest and achieve >80% code coverage**
  - Verification: Run `pnpm test:unit` in root - all tests pass and coverage reports generated
- [ ] **API integration tests validate all endpoints with database isolation**
  - Verification: Run `pnpm test:integration` - Fastify routes tested against local Supabase with transaction rollback
- [ ] **E2E tests cover critical user flows across dashboard and storefront**
  - Verification: Run `pnpm test:e2e` - Playwright tests complete comic creation, payment, and admin workflows
- [ ] **ML service integrations are properly mocked with fallback to real API testing**
  - Verification: Tests run with MSW mocks by default, optional REAL_API=true flag for integration testing
- [ ] **Testing commands integrated into CI/CD with parallel execution**
  - Verification: GitHub Actions runs all test suites in parallel on PR creation with proper caching

## Technical Notes

### Approach

Establish a three-tier testing strategy: Vitest for fast unit tests across all packages, Supertest for Fastify API integration testing against local Supabase, and Playwright for full E2E workflows. Create shared test utilities for database seeding, auth mocking, and ML service stubbing. Use Turborepo to orchestrate parallel test execution and implement CI/CD integration with GitHub Actions for automated testing on PRs.


### Files to Modify

- **path**: package.json
- **changes**: Add test scripts and testing dependencies
- **path**: turbo.json
- **changes**: Configure test task orchestration and caching
- **path**: .github/workflows/ci.yml
- **changes**: Add testing steps with matrix strategy

### New Files to Create

- **path**: packages/shared/vitest.config.ts
- **purpose**: Base Vitest configuration for all packages
- **path**: packages/shared/test-utils/index.ts
- **purpose**: Shared testing utilities and helpers
- **path**: packages/database/test-utils/factories.ts
- **purpose**: Database test data factories
- **path**: packages/database/test-utils/setup.ts
- **purpose**: Test database setup and teardown
- **path**: packages/shared/test-utils/mocks/ai-services.ts
- **purpose**: Mock implementations for OpenAI/Anthropic
- **path**: packages/shared/test-utils/mocks/payment.ts
- **purpose**: Mock Stripe and payment processing
- **path**: playwright.config.ts
- **purpose**: Global Playwright configuration
- **path**: apps/dashboard/tests/setup.ts
- **purpose**: Dashboard-specific test setup
- **path**: apps/storefront/tests/setup.ts
- **purpose**: Storefront-specific test setup
- **path**: packages/api/src/__tests__/setup.ts
- **purpose**: API test setup with database isolation

### External Dependencies


- **vitest** ^2.0.0

  - Primary test runner with excellent TypeScript and monorepo support

- **@vitest/ui** ^2.0.0

  - Web-based test UI for debugging and development

- **playwright** ^1.40.0

  - Cross-browser E2E testing with visual regression capabilities

- **supertest** ^6.3.0

  - HTTP assertion testing for Fastify API endpoints

- **msw** ^2.0.0

  - Mock Service Worker for intercepting ML API calls in tests

- **@supabase/supabase-js** ^2.38.0

  - Test database client for integration testing

- **testcontainers** ^10.0.0

  - Docker container management for isolated test environments

## Testing

### Unit Tests

- **File**: `packages/api/src/__tests__/auth.test.ts`
  - Scenarios: JWT token validation, User session management, Permission checks
- **File**: `packages/comic-generator/src/__tests__/generator.test.ts`
  - Scenarios: Prompt processing, Image generation workflow, Error handling for API failures
- **File**: `packages/payment/src/__tests__/stripe.test.ts`
  - Scenarios: Payment intent creation, Webhook processing, Refund handling
### Integration Tests

- **File**: `packages/api/src/__tests__/integration/comics.test.ts`
  - Scenarios: Create comic end-to-end, User authentication flow, Payment processing integration
- **File**: `packages/api/src/__tests__/integration/database.test.ts`
  - Scenarios: Database migrations, Seed data consistency, Transaction isolation
### E2E Tests

- **File**: `apps/dashboard/tests/admin-workflows.spec.ts`
  - Scenarios: User management interface, Analytics dashboard, System configuration
- **File**: `apps/storefront/tests/customer-journey.spec.ts`
  - Scenarios: Comic creation flow, Payment and checkout, Profile management
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

- **task**: Install and configure testing dependencies across monorepo
- **done**: False
- **task**: Create shared Vitest configuration and test utilities
- **done**: False
- **task**: Setup database test utilities with factories and isolation
- **done**: False
- **task**: Implement MSW mocks for external AI and payment services
- **done**: False
- **task**: Configure Playwright for E2E testing with proper selectors
- **done**: False
- **task**: Create unit tests for core packages (auth, comic-generator, payment)
- **done**: False
- **task**: Implement API integration tests with Supertest
- **done**: False
- **task**: Build E2E test suites for critical user workflows
- **done**: False
- **task**: Configure Turborepo task orchestration for parallel testing
- **done**: False
- **task**: Setup GitHub Actions CI/CD with testing pipeline
- **done**: False
- **task**: Documentation and team training on testing practices
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Testing infrastructure is foundational for a complex multi-service platform like Morpheus. With ML workflows, async comic generation, payment processing, and user management across multiple frontends, we need comprehensive testing to catch regressions early, ensure API reliability, and validate complex user workflows. This prevents costly bugs in production and enables confident deployment of new features.

**Technical Approach:**
- Unit Testing: Vitest for all packages with shared config, fast execution, and TypeScript support
- Integration Testing: Supertest for Fastify API testing with test database isolation  
- E2E Testing: Playwright for cross-browser testing of Next.js apps with visual regression detection
- Database Testing: Supabase local instance with migrations + seed data for consistent test state
- ML Testing: Mock OpenAI/Anthropic responses, test RunPod integration with fake endpoints
- Monorepo Testing: Turborepo task orchestration for parallel test execution across workspaces

**Dependencies:**
- External: vitest, @vitest/ui, playwright, supertest, msw, testcontainers
- Internal: Shared test utilities, database factories, auth mocks, API clients

**Risks:**
- Test database pollution: Use transactions + rollback or fresh DB per test suite
- Flaky E2E tests: Implement proper waits, stable selectors, retry logic
- ML API costs in tests: Mock external services, use rate limiting for real API tests
- Slow test suite: Parallel execution, selective testing, proper test isolation

**Complexity Notes:**
More complex than typical due to ML workflows, multi-frontend coordination, and database state management. Need sophisticated mocking for external AI services and payment flows.

**Key Files:**
- packages/shared/vitest.config.ts: Base Vitest configuration
- packages/api/tests/: API integration tests with Supertest
- apps/dashboard/tests/: Playwright E2E tests for admin workflows  
- apps/storefront/tests/: Customer journey E2E tests
- packages/database/test-utils/: DB factories and test helpers


### Design Decisions

[{'decision': 'Use Vitest over Jest for all JavaScript/TypeScript testing', 'rationale': 'Native ESM support, faster execution, better TypeScript integration, Vite ecosystem alignment', 'alternatives_considered': ['Jest with ts-jest', 'Node.js native test runner']}, {'decision': 'Implement test database isolation with Supabase local instance', 'rationale': 'Matches production environment exactly, supports RLS policies, easier than mocking complex queries', 'alternatives_considered': ['SQLite for tests', 'Docker PostgreSQL', 'Full database mocking']}, {'decision': 'Mock ML services by default, with opt-in real API testing', 'rationale': 'Prevents API costs, ensures test determinism, faster execution while still allowing integration validation', 'alternatives_considered': ['Always use real APIs', 'Record/replay HTTP interactions']}]
