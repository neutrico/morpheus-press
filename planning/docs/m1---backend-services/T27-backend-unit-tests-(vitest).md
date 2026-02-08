---
area: backend
dependsOn:
- T25
effort: 5
iteration: I2
key: T27
milestone: M1 - Backend Services
priority: p0
title: Backend Unit Tests (Vitest)
type: Task
---

# Backend Unit Tests (Vitest)

## Acceptance Criteria

- [ ] **All core backend services achieve minimum 85% test coverage with comprehensive unit tests**
  - Verification: Run `npm run test:coverage` in backend package and verify coverage report meets threshold
- [ ] **AI service integrations are properly mocked with realistic test data and error scenarios**
  - Verification: Execute AI service tests in isolation with `npm run test -- ai` and verify no external API calls
- [ ] **Database operations use transaction rollback or in-memory patterns for test isolation**
  - Verification: Run database tests multiple times with `npm run test -- --reporter=verbose db` and verify no test pollution
- [ ] **Comic generation pipeline has end-to-end unit test coverage for all transformation stages**
  - Verification: Execute `npm run test -- comic` and verify novel parsing, character extraction, and scene generation are tested
- [ ] **Test suite runs in under 30 seconds locally and passes consistently in CI**
  - Verification: Time test execution with `time npm run test` and verify CI pipeline shows green status

## Technical Notes

### Approach

Implement comprehensive unit test suite using Vitest with co-located test files alongside source code. Create mock factories for AI service responses and use Fastify's inject method for endpoint testing. Establish database testing patterns using transactions or in-memory alternatives. Build reusable test fixtures for novel content, character data, and comic generation scenarios. Focus on testing business logic, data transformations, and error handling paths while mocking external dependencies.


### Files to Modify

- **path**: packages/backend/package.json
- **changes**: Add test scripts, vitest dependencies, and coverage configuration
- **path**: packages/backend/vitest.config.ts
- **changes**: Configure test environment, coverage thresholds, and mock patterns
- **path**: packages/backend/src/plugins/auth/index.ts
- **changes**: Add dependency injection support for better testability
- **path**: packages/backend/src/services/ai-service.ts
- **changes**: Refactor for dependency injection and mock-friendly interfaces

### New Files to Create

- **path**: packages/backend/test/fixtures/novel-samples.ts
- **purpose**: Sample novel content for testing parsing and character extraction
- **path**: packages/backend/test/fixtures/ai-responses.ts
- **purpose**: Mock AI service responses for consistent testing
- **path**: packages/backend/test/helpers/database.ts
- **purpose**: Database testing utilities and transaction management
- **path**: packages/backend/test/helpers/mock-factories.ts
- **purpose**: Factory functions for generating test data
- **path**: packages/backend/src/plugins/auth/__tests__/auth.test.ts
- **purpose**: Authentication and authorization unit tests
- **path**: packages/backend/src/services/__tests__/ai-service.test.ts
- **purpose**: AI service integration testing with mocks
- **path**: packages/backend/src/services/__tests__/comic-generator.test.ts
- **purpose**: Comic generation pipeline unit tests
- **path**: packages/backend/src/services/__tests__/file-storage.test.ts
- **purpose**: File upload and storage service tests
- **path**: packages/backend/src/plugins/database/__tests__/repository.test.ts
- **purpose**: Database repository pattern unit tests
- **path**: packages/backend/src/lib/__tests__/validators.test.ts
- **purpose**: Input validation and schema testing
- **path**: packages/backend/src/routes/__tests__/novels.test.ts
- **purpose**: Novel management API endpoint tests
- **path**: packages/backend/src/routes/__tests__/comics.test.ts
- **purpose**: Comic generation API endpoint tests
- **path**: packages/backend/src/routes/__tests__/users.test.ts
- **purpose**: User management API endpoint tests

### External Dependencies


- **@vitest/ui** ^1.0.0

  - Web UI for running and debugging tests during development

- **@faker-js/faker** ^8.0.0

  - Generate realistic test data for novels, characters, and user profiles

- **testcontainers** ^10.0.0

  - Optional: Spin up real PostgreSQL containers for integration-style tests

- **@types/supertest** ^6.0.0

  - TypeScript definitions if using supertest as fallback option

## Testing

### Unit Tests

- **File**: `packages/backend/src/plugins/auth/__tests__/auth.test.ts`
  - Scenarios: JWT token validation, User session management, Authentication middleware, Permission checking
- **File**: `packages/backend/src/services/__tests__/ai-service.test.ts`
  - Scenarios: OpenAI API integration mocking, Anthropic API responses, Rate limiting behavior, Error handling and retries
- **File**: `packages/backend/src/services/__tests__/comic-generator.test.ts`
  - Scenarios: Novel text parsing, Character extraction, Scene generation, Image generation coordination
- **File**: `packages/backend/src/plugins/database/__tests__/repository.test.ts`
  - Scenarios: CRUD operations, Transaction handling, Query optimization, Connection pooling
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/api-endpoints.test.ts`
  - Scenarios: Complete novel upload and processing flow, User authentication and authorization flow, Comic generation end-to-end pipeline
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 1
- **Documentation**: 0.5
- **Total**: 6.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Vitest configuration and test infrastructure
- **done**: False
- **task**: Create test fixtures and mock factories for AI services
- **done**: False
- **task**: Implement database testing patterns with transaction rollback
- **done**: False
- **task**: Write unit tests for authentication and authorization
- **done**: False
- **task**: Create comprehensive tests for AI service integrations
- **done**: False
- **task**: Build comic generation pipeline test coverage
- **done**: False
- **task**: Implement API endpoint tests using Fastify inject method
- **done**: False
- **task**: Add file storage and upload testing
- **done**: False
- **task**: Configure CI/CD pipeline integration
- **done**: False
- **task**: Verify coverage thresholds and optimize test performance
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Backend unit tests are critical for the Morpheus platform's reliability, especially given the complex AI/ML integrations and data transformations involved in novel-to-comic conversion. This task establishes comprehensive test coverage for business logic, API endpoints, data models, and external service integrations (OpenAI/Anthropic, RunPod). Unit tests provide rapid feedback during development, prevent regressions, and enable confident refactoring as the platform scales.

**Technical Approach:**
- Use Vitest as the primary test runner (already in tech stack) with TypeScript support
- Implement test organization following Fastify 5 plugin structure
- Mock external services (LLMs, image generation APIs) using vi.mock()
- Use supertest-like testing for HTTP endpoints via Fastify's inject method
- Implement repository pattern testing with in-memory databases or transaction rollback
- Follow AAA pattern (Arrange, Act, Assert) with descriptive test names
- Create test fixtures for novel parsing, character extraction, and scene generation
- Use dependency injection for better testability of services

**Dependencies:**
- External: @vitest/ui, @faker-js/faker, supertest, testcontainers (optional)
- Internal: Database schemas, authentication middleware, AI service wrappers, comic generation pipeline

**Risks:**
- Flaky tests: External API mocks may not reflect real behavior changes
- Slow tests: Database operations and file I/O could slow CI/CD pipeline
- Mock drift: Mocked AI responses may diverge from actual API behavior
- Test maintenance: Complex business logic changes requiring extensive test updates

**Complexity Notes:**
Higher complexity than initially expected due to:
- Complex AI/ML integration points requiring sophisticated mocking strategies
- Novel parsing and comic generation pipelines with multiple data transformation stages
- Supabase-specific testing patterns and database transaction handling
- File upload/storage testing for images and generated comics

**Key Files:**
- packages/backend/src/**/*.test.ts: Unit test files alongside source
- packages/backend/test/: Shared test utilities, fixtures, and helpers
- packages/backend/vitest.config.ts: Vitest configuration
- packages/backend/src/plugins/: Plugin-specific test files
- packages/backend/src/services/: Service layer unit tests
- packages/backend/src/lib/: Utility and helper function tests


### Design Decisions

[{'decision': 'Co-locate unit tests alongside source files using .test.ts suffix', 'rationale': 'Improves discoverability and maintainability, follows modern testing practices, easier refactoring', 'alternatives_considered': ['Separate /test directory', '/tests folder structure', '__tests__ folders']}, {'decision': "Use Fastify's built-in inject() method instead of supertest", 'rationale': 'Native Fastify testing approach, better TypeScript support, no additional HTTP server startup', 'alternatives_considered': ['supertest library', 'Manual HTTP requests', 'Custom test helpers']}, {'decision': 'Mock external AI services at the service layer boundary', 'rationale': 'Allows testing business logic without API calls, predictable test data, faster execution', 'alternatives_considered': ['Integration tests with real APIs', 'Record/replay approach', 'Stub entire service classes']}]
