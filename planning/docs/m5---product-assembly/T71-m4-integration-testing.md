---
area: comic
dependsOn:
- T67
- T68
- T69
effort: 5
iteration: I5
key: T71
milestone: M5 - Product Assembly
priority: p0
title: M4 Integration Testing
type: Task
---

# M4 Integration Testing

## Acceptance Criteria

- [ ] **Complete comic pipeline processes novel input to comic output end-to-end**
  - Verification: Run `npm run test:e2e -- --grep 'full pipeline'` - test uploads novel, generates 10-page comic with consistent characters
- [ ] **Pipeline completes within performance benchmarks (<2 minutes for 10-page comic)**
  - Verification: Performance test in tests/integration/performance.spec.ts reports execution time under 120 seconds
- [ ] **Integration tests achieve 90%+ reliability with mocked external services**
  - Verification: Run test suite 20 times - max 2 failures allowed, check CI metrics dashboard
- [ ] **Visual regression testing validates comic panel quality and layout consistency**
  - Verification: Playwright visual comparisons pass in tests/e2e/visual-regression.spec.ts with <5% pixel difference threshold
- [ ] **Test coverage for integration points reaches 85%+ across all pipeline services**
  - Verification: Run `npm run test:coverage` - integration test coverage report shows >85% for services in apps/backend/src/services/comic-pipeline/

## Technical Notes

### Approach

Implement a multi-layer integration testing strategy starting with isolated service-to-service tests using Vitest, progressing to full pipeline tests with Playwright. Mock external AI services for consistency while maintaining a subset of tests against real services for validation. Use visual regression testing for comic output quality and implement performance benchmarks to ensure the pipeline meets latency requirements. Create comprehensive test data factories that cover edge cases like complex novels, multiple characters, and various genre requirements.


### Files to Modify

- **path**: apps/backend/src/services/comic-pipeline/pipeline-orchestrator.ts
- **changes**: Add instrumentation for test hooks, error handling improvements, performance metrics collection
- **path**: apps/backend/src/services/novel-processor/index.ts
- **changes**: Add test mode flag for deterministic outputs, expose internal state for validation
- **path**: apps/backend/src/services/runpod-integration/client.ts
- **changes**: Add mock mode toggle, implement test-friendly error simulation
- **path**: playwright.config.ts
- **changes**: Add staging environment configuration, visual regression settings, parallel execution limits

### New Files to Create

- **path**: tests/integration/comic-pipeline.spec.ts
- **purpose**: Main integration test suite covering full pipeline with mocked external services
- **path**: tests/mocks/runpod-mock.ts
- **purpose**: MSW handlers for RunPod API responses, deterministic image generation mocks
- **path**: tests/mocks/llm-mock.ts
- **purpose**: Mock LLM responses for scene extraction and character analysis
- **path**: tests/fixtures/novels/test-novels.ts
- **purpose**: Test data factory for novels of varying complexity and characteristics
- **path**: tests/utils/comic-assertions.ts
- **purpose**: Custom Jest/Vitest matchers for comic output validation and fuzzy matching
- **path**: tests/utils/test-database.ts
- **purpose**: Database seeding, cleanup utilities for isolated test environments
- **path**: tests/e2e/comic-generation.spec.ts
- **purpose**: End-to-end Playwright tests covering user-facing comic generation flow
- **path**: tests/e2e/visual-regression.spec.ts
- **purpose**: Visual regression testing for comic output quality using Playwright screenshots
- **path**: tests/integration/performance.spec.ts
- **purpose**: Performance benchmarking tests for pipeline execution time and resource usage
- **path**: apps/backend/src/services/comic-pipeline/__tests__/pipeline-orchestrator.test.ts
- **purpose**: Unit tests for main pipeline orchestration logic
- **path**: apps/backend/src/services/comic-pipeline/__tests__/service-integration.test.ts
- **purpose**: Unit tests for service-to-service integration points
- **path**: tests/setup/test-environment.ts
- **purpose**: Test environment setup with Supabase branch, mock services initialization

### External Dependencies


- **@playwright/test** ^1.40.0

  - End-to-end testing of the complete comic generation pipeline across browser and API

- **msw** ^2.0.0

  - Mock Service Worker for intercepting and mocking RunPod and external AI service calls

- **sharp** ^0.33.0

  - Image processing for visual regression testing and comic output validation

- **pixelmatch** ^5.3.0

  - Pixel-level image comparison for visual regression testing of comic panels

- **@faker-js/faker** ^8.3.0

  - Generate realistic test data for novels, characters, and user scenarios

## Testing

### Unit Tests

- **File**: `apps/backend/src/services/comic-pipeline/__tests__/pipeline-orchestrator.test.ts`
  - Scenarios: Successful pipeline execution with mocked services, Service failure handling and retry logic, Input validation and sanitization, Character consistency across pipeline stages
- **File**: `apps/backend/src/services/comic-pipeline/__tests__/service-integration.test.ts`
  - Scenarios: Novel processor to scene extractor data flow, Scene extractor to image generator handoff, Image generator to comic assembler integration
### Integration Tests

- **File**: `tests/integration/comic-pipeline.spec.ts`
  - Scenarios: Full pipeline with simple 3-character novel, Complex multi-character novel with scene transitions, Error recovery from RunPod API failures, Pipeline performance benchmarking, Database state consistency after pipeline completion
- **File**: `tests/integration/service-mocks.spec.ts`
  - Scenarios: Mock RunPod responses for consistent image generation, Mock LLM responses for deterministic scene extraction, Failure simulation and graceful degradation
### E2E Tests

- **File**: `tests/e2e/comic-generation.spec.ts`
  - Scenarios: User uploads novel and receives completed comic, Comic download and PDF validation, Progress tracking throughout pipeline stages
- **File**: `tests/e2e/visual-regression.spec.ts`
  - Scenarios: Comic panel layout consistency, Character appearance consistency across panels, Typography and speech bubble rendering
### Manual Testing


## Estimates

- **Development**: 6
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 1
- **Total**: 10

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup test environment with Supabase branch and mock services
- **done**: False
- **task**: Create test data factories and novel fixtures for various scenarios
- **done**: False
- **task**: Implement RunPod and LLM mock services with MSW
- **done**: False
- **task**: Build custom assertion utilities for comic output validation
- **done**: False
- **task**: Develop integration test suite covering service-to-service interactions
- **done**: False
- **task**: Create end-to-end Playwright tests for full user workflow
- **done**: False
- **task**: Implement visual regression testing with screenshot comparisons
- **done**: False
- **task**: Add performance benchmarking and monitoring instrumentation
- **done**: False
- **task**: Setup CI/CD pipeline integration with test reporting
- **done**: False
- **task**: Document testing procedures and troubleshooting guide
- **done**: False

## Agent Notes

### Research Findings

**Context:**
M4 Integration Testing refers to comprehensive end-to-end testing of the core comic generation pipeline after M4 (Comic Generation) milestone. This is critical because the comic generation involves complex interactions between multiple services: novel processing, scene extraction, character consistency, image generation via RunPod/Stable Diffusion, and comic panel assembly. Integration testing ensures these components work together seamlessly before the M5 product assembly phase. Without this, we risk shipping a product where individual components work but fail when orchestrated together.

**Technical Approach:**
- Use Playwright for end-to-end testing that spans the full pipeline from novel upload to comic output
- Implement test data factories for consistent novel inputs and expected comic outputs
- Create mock RunPod endpoints for reliable, fast image generation testing
- Use Vitest for integration testing of backend services (novel processor → scene extractor → image generator → comic assembler)
- Implement visual regression testing for comic panel layouts and quality
- Set up staging environment with Supabase branch for isolated testing
- Create performance benchmarks for the full pipeline (target: <2 minutes for 10-page comic)

**Dependencies:**
- External: @playwright/test, msw (Mock Service Worker), sharp (image comparison), pdf-parse (comic output validation)
- Internal: Novel processing service, Scene extraction service, Character consistency engine, RunPod integration, Comic assembly service, Supabase schemas

**Risks:**
- Flaky tests due to AI/ML non-deterministic outputs: Use seed values and mock responses for consistency
- Test data management complexity: Implement proper test database seeding/cleanup
- Long test execution times: Parallelize tests and use mocked external services
- Environment drift between test/prod: Use Docker containers for consistent environments

**Complexity Notes:**
This is significantly more complex than typical integration testing due to the AI/ML pipeline nature. The non-deterministic outputs from LLMs and image generation make traditional assertion patterns difficult. Requires sophisticated mocking strategies and potentially fuzzy matching for outputs.

**Key Files:**
- tests/integration/comic-pipeline.spec.ts: Main pipeline test suite
- tests/mocks/runpod-mock.ts: Mock RunPod API responses
- tests/fixtures/novels/: Test novel inputs of varying complexity
- tests/utils/comic-assertions.ts: Custom matchers for comic output validation
- apps/backend/src/services/comic-pipeline/: Integration points to test
- playwright.config.ts: E2E test configuration with staging environment


### Design Decisions

[{'decision': 'Use hybrid approach: mocked external services for speed, real services for critical path validation', 'rationale': 'Balances test reliability/speed with realistic validation of actual service integrations', 'alternatives_considered': ['Full mocking (too disconnected from reality)', 'Full real services (too slow/unreliable)']}, {'decision': 'Implement visual regression testing for comic outputs using perceptual hashing', 'rationale': 'Comic quality is inherently visual; traditional text assertions insufficient for validating layout and image quality', 'alternatives_considered': ['Text-only validation', 'Manual QA only', 'Pixel-perfect comparison']}, {'decision': 'Create dedicated test database branch in Supabase for integration tests', 'rationale': 'Ensures test isolation while maintaining realistic data relationships and constraints', 'alternatives_considered': ['In-memory database', 'Shared test database', 'Production database subset']}]
