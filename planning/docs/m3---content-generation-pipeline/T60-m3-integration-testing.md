---
area: image-gen
dependsOn:
- T54
- T57
- T59
effort: 5
iteration: I4
key: T60
milestone: M3 - Content Generation Pipeline
priority: p0
title: M3 Integration Testing
type: Task
---

# M3 Integration Testing

## Acceptance Criteria

- [ ] **End-to-end novel-to-comic pipeline completes successfully with all services integrated**
  - Verification: Run `npm run test:e2e` - all Playwright tests pass, comic panels are generated and stored in Supabase
- [ ] **Generated comic images match visual quality standards with <5% pixel difference from baseline**
  - Verification: Visual regression tests pass with `npm run test:visual-regression` showing pixelmatch scores
- [ ] **Pipeline handles failures gracefully with proper error recovery and logging**
  - Verification: Integration tests simulate RunPod failures, database timeouts - system recovers without data corruption
- [ ] **Test suite runs in <10 minutes with reliable, non-flaky results**
  - Verification: CI pipeline completes integration tests within time limit with <1% failure rate over 10 runs
- [ ] **All service-to-service communications are properly mocked and tested**
  - Verification: Vitest integration tests cover LLM→RunPod→Supabase flow with MSW mocks, 90%+ coverage

## Technical Notes

### Approach

Build a comprehensive integration testing suite that validates the entire novel-to-comic pipeline using Docker-orchestrated services. Create test fixtures with known novel inputs and expected comic outputs, then use Playwright to drive the full user workflow while Vitest validates service-level integrations. Implement visual regression testing to ensure generated images meet quality standards, and use Supabase branching for isolated test environments.


### Files to Modify

- **path**: packages/image-gen/src/services/image-generation.ts
- **changes**: Add test mode flags, deterministic seed support for consistent testing
- **path**: packages/supabase/src/client.ts
- **changes**: Add test database configuration, cleanup utilities for test data
- **path**: apps/backend/src/services/content-pipeline.ts
- **changes**: Add integration test hooks, mock service injection points

### New Files to Create

- **path**: tests/integration/content-pipeline.spec.ts
- **purpose**: Main integration test suite for end-to-end pipeline validation
- **path**: tests/fixtures/novels/test-novel-short.txt
- **purpose**: Minimal novel for fast integration testing
- **path**: tests/fixtures/novels/test-novel-complex.txt
- **purpose**: Complex multi-chapter novel for comprehensive testing
- **path**: tests/fixtures/expected-outputs/
- **purpose**: Baseline comic panels and metadata for regression testing
- **path**: packages/testing/src/visual-regression.ts
- **purpose**: Image comparison utilities using pixelmatch and sharp
- **path**: packages/testing/src/test-utils.ts
- **purpose**: Shared testing utilities, mock factories, test data generators
- **path**: docker-compose.test.yml
- **purpose**: Orchestrate test environment with mock RunPod, local Supabase
- **path**: tests/setup/test-environment.ts
- **purpose**: Test environment initialization, database seeding, cleanup
- **path**: tests/mocks/runpod-mock-server.ts
- **purpose**: MSW-based RunPod API mocking with realistic response delays
- **path**: tests/e2e/comic-generation-workflow.spec.ts
- **purpose**: Playwright-driven end-to-end user workflow testing
- **path**: .github/workflows/integration-tests.yml
- **purpose**: CI/CD pipeline configuration for integration testing

### External Dependencies


- **@playwright/test** ^1.40.0

  - End-to-end testing of the complete user workflow through the web interface

- **pixelmatch** ^5.3.0

  - Pixel-level image comparison for visual regression testing of generated comic panels

- **sharp** ^0.32.0

  - Image processing and normalization for consistent test comparisons

- **msw** ^2.0.0

  - Mock external API calls to OpenAI/Anthropic during integration tests

- **docker** ^24.0.0

  - Orchestrate test environment with mock RunPod services and isolated databases

- **testcontainers** ^10.2.0

  - Programmatically manage Docker containers for Stable Diffusion API mocking

## Testing

### Unit Tests

- **File**: `packages/image-gen/src/__tests__/image-validator.test.ts`
  - Scenarios: Valid comic panel validation, Corrupted image handling, Unsupported format rejection
- **File**: `packages/testing/src/__tests__/visual-regression.test.ts`
  - Scenarios: Pixel-perfect image comparison, Acceptable difference thresholds, Baseline image management
### Integration Tests

- **File**: `tests/integration/content-pipeline.spec.ts`
  - Scenarios: Complete novel-to-comic transformation, Multi-panel comic generation, Asset storage and retrieval, Error recovery and retry logic
- **File**: `tests/integration/service-communication.spec.ts`
  - Scenarios: LLM scene description generation, RunPod Stable Diffusion API calls, Supabase asset upload/download, Pipeline orchestration timing
### E2E Tests

- **File**: `tests/e2e/comic-generation-workflow.spec.ts`
  - Scenarios: User uploads novel, receives completed comic, Progress tracking throughout pipeline, Error handling in UI
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

- **task**: Set up Docker test environment with mock services
- **done**: False
- **task**: Create test fixtures (sample novels, expected outputs)
- **done**: False
- **task**: Implement visual regression testing utilities with pixelmatch
- **done**: False
- **task**: Build MSW mocks for RunPod and external API dependencies
- **done**: False
- **task**: Write Vitest integration tests for service-to-service communication
- **done**: False
- **task**: Implement Playwright E2E tests for user workflows
- **done**: False
- **task**: Add test mode configurations to existing services
- **done**: False
- **task**: Create CI/CD pipeline for automated integration testing
- **done**: False
- **task**: Optimize test execution time and reliability
- **done**: False
- **task**: Document testing procedures and maintenance guidelines
- **done**: False

## Agent Notes

### Research Findings

**Context:**
M3 Integration Testing focuses on validating the entire Content Generation Pipeline end-to-end, particularly the image generation components. This is critical because the pipeline involves complex integrations between LLMs (for scene description), RunPod Stable Diffusion (for image generation), and Supabase (for asset storage). Without comprehensive integration tests, we risk deploying a system where individual components work but fail when orchestrated together, leading to poor user experience and potential data corruption.

**Technical Approach:**
- Use Playwright for full E2E testing of the novel-to-comic transformation workflow
- Implement Vitest integration tests for service-to-service communication (API → ML services → Database)
- Create mock RunPod environments using Docker containers for consistent testing
- Use Supabase local development setup with test data fixtures
- Implement visual regression testing for generated comic panels using pixelmatch
- Create test harnesses that can validate image generation quality and consistency

**Dependencies:**
- External: @playwright/test, @supabase/supabase-js, pixelmatch, sharp, docker, msw (Mock Service Worker)
- Internal: image-generation service, content-pipeline orchestrator, novel-parser service, supabase client wrapper

**Risks:**
- Flaky tests due to ML model non-determinism: Use seed values and mock responses for consistent results
- RunPod API rate limits during testing: Implement request queuing and circuit breaker patterns
- Large test asset storage costs: Use compressed test images and cleanup strategies
- Long test execution times: Parallel test execution and selective test running based on changed files

**Complexity Notes:**
This is significantly more complex than typical integration testing due to:
1. ML service dependencies that are inherently non-deterministic
2. Large binary assets (images) that need validation beyond simple API responses
3. Multi-service orchestration with async processing pipelines
4. Visual quality assessment that goes beyond functional correctness

**Key Files:**
- tests/integration/content-pipeline.spec.ts: Main integration test suite
- tests/fixtures/: Test novels, expected comic outputs, mock API responses
- packages/image-gen/src/test-utils.ts: Image generation testing utilities
- docker-compose.test.yml: Test environment orchestration
- packages/testing/src/visual-regression.ts: Image comparison utilities


### Design Decisions

[{'decision': 'Use Docker-based RunPod mocking instead of live API calls', 'rationale': 'Ensures test determinism, reduces costs, and eliminates external service dependencies that could cause CI failures', 'alternatives_considered': ['Live API with test account', 'Simple HTTP mocking', 'RunPod sandbox environment']}, {'decision': 'Implement visual regression testing for generated images', 'rationale': 'Functional tests alone cannot validate that generated comic panels meet quality standards or detect visual regressions in ML models', 'alternatives_considered': ['Hash-based image comparison', 'Manual visual inspection', 'Metadata-only validation']}, {'decision': 'Create separate integration test database with Supabase branching', 'rationale': 'Allows testing real database interactions without polluting development data or requiring complex cleanup logic', 'alternatives_considered': ['In-memory database', 'Shared test database', 'Transaction rollback strategy']}]
