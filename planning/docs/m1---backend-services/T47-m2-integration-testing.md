---
area: ingestion
dependsOn:
- T44
- T45
- T46
effort: 5
iteration: I3
key: T47
milestone: M1 - Backend Services
priority: p0
title: M2 Integration Testing
type: Task
---

# M2 Integration Testing

## Acceptance Criteria

- [ ] **Complete novel ingestion pipeline processes sample novels end-to-end with proper data flow validation**
  - Verification: Run `npm run test:integration -- --grep 'novel ingestion pipeline'` and verify all test scenarios pass
- [ ] **Integration tests achieve >90% code coverage for ingestion services and error handling paths**
  - Verification: Run `npm run test:coverage:integration` and verify coverage reports show >90% for ingestion modules
- [ ] **Mock external ML APIs (OpenAI/Anthropic/RunPod) respond correctly to all integration test scenarios**
  - Verification: Integration tests pass with MSW mocks active and log validation shows proper API call patterns
- [ ] **Database transactions and cleanup work correctly across all test scenarios with isolated test environments**
  - Verification: Run integration test suite 3 times consecutively without failures, verify test database isolation
- [ ] **Performance benchmarks meet requirements: <2s for novel upload, <30s for chapter processing**
  - Verification: Integration tests include timing assertions and performance regression detection

## Technical Notes

### Approach

Create a comprehensive integration testing suite that validates the complete novel ingestion and processing pipeline. Use Testcontainers for isolated PostgreSQL instances, MSW for mocking external ML APIs, and Vitest for the test runner. Implement test fixtures with sample novels and expected comic outputs, ensuring all error scenarios and edge cases are covered. Structure tests to run in parallel while maintaining data isolation, with proper setup/teardown for database state management.


### Files to Modify

- **path**: apps/backend/vitest.config.ts
- **changes**: Add integration test configuration with testcontainers setup and MSW integration
- **path**: packages/backend/src/services/ingestion/novel-processor.ts
- **changes**: Add test hooks and instrumentation for integration testing
- **path**: packages/backend/src/lib/database/client.ts
- **changes**: Add test database connection handling and transaction utilities

### New Files to Create

- **path**: packages/backend/src/__tests__/integration/novel-pipeline.test.ts
- **purpose**: End-to-end testing of complete novel processing workflow
- **path**: packages/backend/src/__tests__/integration/database-operations.test.ts
- **purpose**: Database transaction and consistency testing across services
- **path**: packages/backend/src/__tests__/fixtures/sample-novels.ts
- **purpose**: Test data fixtures with various novel formats and edge cases
- **path**: packages/backend/src/__tests__/helpers/test-database.ts
- **purpose**: Database setup/teardown utilities with testcontainers
- **path**: packages/backend/src/__tests__/helpers/api-mocks.ts
- **purpose**: MSW handlers for OpenAI, Anthropic, and RunPod API mocking
- **path**: packages/backend/src/__tests__/helpers/test-factories.ts
- **purpose**: Data factory functions for consistent test object generation
- **path**: packages/backend/src/__tests__/setup/integration-setup.ts
- **purpose**: Global test setup for integration test environment
- **path**: packages/shared/src/test-utils/performance-helpers.ts
- **purpose**: Shared performance testing utilities and assertions
- **path**: .github/workflows/integration-tests.yml
- **purpose**: CI/CD pipeline configuration for integration test execution

### External Dependencies


- **@testcontainers/postgresql** ^10.0.0

  - Isolated PostgreSQL instances for integration testing

- **msw** ^2.0.0

  - Mock external API calls to OpenAI, Anthropic, RunPod

- **@faker-js/faker** ^8.0.0

  - Generate realistic test data for novels and user scenarios

- **dotenv-cli** ^7.0.0

  - Environment variable management for test configurations

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/unit/ingestion-service.test.ts`
  - Scenarios: Novel file parsing and validation, Chapter extraction and segmentation, Database transaction rollback on errors, File upload size and format validation
- **File**: `packages/backend/src/__tests__/unit/llm-integration.test.ts`
  - Scenarios: OpenAI API response parsing, Rate limiting and retry logic, Token counting and chunking
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/novel-pipeline.test.ts`
  - Scenarios: Complete novel upload to comic generation flow, Multi-chapter processing with parallel execution, Error recovery and partial processing states, Authentication and authorization throughout pipeline
- **File**: `packages/backend/src/__tests__/integration/database-operations.test.ts`
  - Scenarios: Transaction consistency across multiple services, Concurrent user processing isolation, Data migration and schema validation
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

- **task**: Setup testcontainers configuration and Docker test environment
- **done**: False
- **task**: Create MSW mock handlers for all external ML APIs with realistic responses
- **done**: False
- **task**: Build comprehensive test fixtures with sample novels and expected outputs
- **done**: False
- **task**: Implement database helpers with proper seeding and cleanup strategies
- **done**: False
- **task**: Write core integration tests for novel ingestion pipeline
- **done**: False
- **task**: Add database transaction and consistency validation tests
- **done**: False
- **task**: Implement performance benchmarking and regression detection
- **done**: False
- **task**: Setup CI/CD pipeline with parallel test execution and reporting
- **done**: False
- **task**: Create comprehensive test documentation and debugging guides
- **done**: False
- **task**: Conduct thorough code review and integration with existing test suite
- **done**: False

## Agent Notes

### Research Findings

**Context:**
M2 Integration Testing refers to comprehensive end-to-end testing for Milestone 2 features, likely focusing on the complete novel-to-comic transformation pipeline. This task ensures that all components (ingestion, LLM processing, image generation, storage) work together seamlessly. Given the p0 priority and "ingestion" area, this specifically tests the data flow from novel input through the entire transformation process, validating that the backend services can handle real-world scenarios with proper error handling, data consistency, and performance requirements.

**Technical Approach:**
- Use Vitest for unit/integration tests with test containers for isolated database testing
- Implement Playwright for full E2E workflows simulating real user journeys
- Create test fixtures with sample novels, expected outputs, and mock ML responses
- Build integration test harnesses using Fastify's testing utilities
- Implement database seeding/cleanup strategies with Supabase test environments
- Use MSW (Mock Service Worker) for mocking external API calls (OpenAI/Anthropic/RunPod)
- Create comprehensive test data factories for consistent test scenarios

**Dependencies:**
- External: @testcontainers/postgresql, msw, @faker-js/faker, dotenv-cli
- Internal: All M1 backend services, database schema, authentication middleware, ingestion pipeline, LLM integration services

**Risks:**
- Flaky tests due to external API dependencies: Use comprehensive mocking strategies
- Test data management complexity: Implement proper seeding/teardown with isolated test DBs
- Performance bottlenecks in CI: Parallelize tests and use selective test running
- Mock drift from real APIs: Regular validation of mocks against actual API responses

**Complexity Notes:**
This is more complex than typical integration testing due to the multi-service architecture involving ML APIs, file processing, and real-time data transformations. The async nature of comic generation and potential webhook integrations add coordination complexity.

**Key Files:**
- packages/backend/src/__tests__/integration/: Test suite structure
- packages/backend/src/__tests__/fixtures/: Sample novels and expected outputs
- packages/backend/src/__tests__/helpers/: Test utilities and database helpers
- apps/backend/vitest.config.ts: Vitest configuration for integration tests
- packages/shared/src/test-utils/: Shared testing utilities across packages


### Design Decisions

[{'decision': 'Use Testcontainers for database isolation', 'rationale': 'Ensures clean test environment without affecting development DB, enables parallel test execution', 'alternatives_considered': ['Shared test database', 'In-memory database', 'Database transactions rollback']}, {'decision': 'MSW for external API mocking', 'rationale': 'Provides realistic HTTP mocking at network level, works across different test environments', 'alternatives_considered': ['Jest mocks', 'Nock', 'Manual mock implementations']}, {'decision': 'Separate integration test environment', 'rationale': 'Isolates integration tests from unit tests, allows different configuration and longer timeouts', 'alternatives_considered': ['Mixed test approach', 'Only E2E tests', 'Only unit tests']}]
