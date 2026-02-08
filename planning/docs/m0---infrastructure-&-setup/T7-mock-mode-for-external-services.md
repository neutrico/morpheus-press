---
area: setup
dependsOn: []
effort: 2
iteration: I1
key: T7
milestone: M0 - Infrastructure & Setup
priority: p1
title: Mock Mode for External Services
type: Task
---

# Mock Mode for External Services

## Acceptance Criteria

- [ ] **Mock mode is activated when NODE_ENV=development or MOCK_MODE=true, with all external service calls intercepted**
  - Verification: Run `npm run dev` with MOCK_MODE=true and verify logs show 'Mock service factory initialized' and no real API calls in network tab
- [ ] **Comic generation pipeline works end-to-end in mock mode with realistic delays (2-5s per step)**
  - Verification: POST /api/comics/generate in mock mode completes successfully within 15 seconds with valid comic structure
- [ ] **Error scenarios can be triggered via mock configuration flags (API_ERROR_RATE=0.3 causes 30% failure rate)**
  - Verification: Set API_ERROR_RATE=1.0 and verify comic generation returns appropriate error responses with 500 status codes
- [ ] **Mock data maintains consistency across related entities (characters, scenes, generated images)**
  - Verification: Generate multiple comics and verify character names/descriptions remain consistent within each comic's scenes
- [ ] **Real API integration tests pass in staging environment to prevent mock drift**
  - Verification: Run `npm run test:integration:staging` with real APIs and verify all external service tests pass

## Technical Notes

### Approach

Create a service factory pattern that instantiates either real or mock implementations based on environment configuration. Use MSW for REST API mocking (Supabase, payment APIs) and create mock classes implementing the same interfaces as real services for SDK-based integrations (OpenAI, RunPod). Build a mock data generator using Faker.js for realistic novel text, character descriptions, and comic metadata. Implement configurable delays and error injection to simulate real-world API behavior and failure scenarios.


### Files to Modify

- **path**: packages/backend/src/config/environment.ts
- **changes**: Add MOCK_MODE, API_ERROR_RATE, MOCK_DELAY_MS environment variables
- **path**: packages/backend/src/services/llm/index.ts
- **changes**: Update service initialization to use factory pattern
- **path**: packages/backend/src/services/image-generation/index.ts
- **changes**: Update service initialization to use factory pattern
- **path**: packages/backend/src/app.ts
- **changes**: Initialize mock service worker if in mock mode

### New Files to Create

- **path**: packages/backend/src/services/mock/factory.ts
- **purpose**: Service factory that returns mock or real implementations based on config
- **path**: packages/backend/src/services/mock/llm-mock.ts
- **purpose**: Mock implementation of LLM service with realistic text generation
- **path**: packages/backend/src/services/mock/image-mock.ts
- **purpose**: Mock implementation of image generation service with placeholder images
- **path**: packages/backend/src/services/mock/database-mock.ts
- **purpose**: Mock Supabase implementation with in-memory storage
- **path**: packages/backend/src/services/mock/payment-mock.ts
- **purpose**: Mock payment processor with simulated success/failure scenarios
- **path**: packages/backend/src/services/mock/data-generators.ts
- **purpose**: Faker.js-based generators for realistic mock data (novels, characters, etc.)
- **path**: packages/backend/src/services/mock/msw-handlers.ts
- **purpose**: MSW request handlers for external HTTP APIs
- **path**: packages/shared/types/mocks.ts
- **purpose**: TypeScript interfaces for mock configuration and responses
- **path**: packages/backend/src/middleware/mock-setup.ts
- **purpose**: Express middleware to initialize MSW in development mode

### External Dependencies


- **msw** ^2.0.0

  - Network-level HTTP API mocking for realistic testing

- **@faker-js/faker** ^8.0.0

  - Generate realistic mock data for novels, characters, and comic content

- **uuid** ^9.0.0

  - Generate consistent mock IDs for entities across requests

- **canvas** ^2.11.0

  - Generate mock comic panel images in Node.js environment

## Testing

### Unit Tests

- **File**: `packages/backend/src/services/mock/__tests__/mock-factory.test.ts`
  - Scenarios: Service factory returns mock implementations when MOCK_MODE=true, Service factory returns real implementations when MOCK_MODE=false, Mock configuration validation and error handling
- **File**: `packages/backend/src/services/mock/__tests__/llm-mock.test.ts`
  - Scenarios: Mock LLM generates valid novel text with proper structure, Mock scene extraction returns consistent character data, Error injection works with configurable failure rates
- **File**: `packages/backend/src/services/mock/__tests__/image-mock.test.ts`
  - Scenarios: Mock image generation returns valid image URLs, Realistic delay simulation (2-4 seconds), Batch image generation maintains order
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/comic-generation-mock.test.ts`
  - Scenarios: End-to-end comic generation pipeline in mock mode, State persistence across multi-step generation process, Error recovery and partial completion scenarios
- **File**: `packages/backend/src/__tests__/integration/api-parity.test.ts`
  - Scenarios: Mock responses match real API response schemas, Mock and real service interfaces are identical
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

- **task**: Setup MSW and Faker.js dependencies, create mock service directory structure
- **done**: False
- **task**: Implement service factory pattern and environment configuration
- **done**: False
- **task**: Create mock LLM service with novel generation and scene extraction
- **done**: False
- **task**: Implement mock image generation service with placeholder images and delays
- **done**: False
- **task**: Build mock database service with in-memory state management
- **done**: False
- **task**: Create MSW handlers for external HTTP APIs (Supabase, payments)
- **done**: False
- **task**: Add error injection and configurable failure scenarios
- **done**: False
- **task**: Implement end-to-end comic generation pipeline testing
- **done**: False
- **task**: Add mock mode documentation and developer setup guide
- **done**: False
- **task**: Code review and integration testing with real APIs in staging
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Mock mode for external services is critical for local development and testing in Morpheus, which integrates with multiple costly/rate-limited external APIs (OpenAI/Anthropic LLMs, RunPod Stable Diffusion, Supabase, payment processors). Without mocking, developers face: slow feedback loops, API costs during development, rate limiting, network dependencies, and inability to test error scenarios. This enables offline development, faster CI/CD, predictable testing, and cost control.

**Technical Approach:**
Implement a hierarchical mocking system with environment-based configuration. Use MSW (Mock Service Worker) for HTTP API mocking, create mock implementations for SDK-based services, and build a unified service factory pattern that switches between real and mock implementations based on NODE_ENV and feature flags. Include realistic response delays, error simulation, and state persistence for complex workflows like comic generation pipelines.

**Dependencies:**
- External: msw ^2.0.0, faker-js ^8.0, uuid ^9.0, node-fetch-commonjs
- Internal: Environment config service, logging service, shared types/schemas

**Risks:**
- Mock drift: Real APIs change but mocks don't get updated. Mitigation: Regular integration tests against real APIs in staging
- Incomplete error coverage: Missing edge cases in mocks. Mitigation: Comprehensive error scenario mapping from API docs
- Performance assumptions: Mock responses too fast/slow vs reality. Mitigation: Configurable realistic delays based on API benchmarks
- State management complexity: Stateful mocks becoming too complex. Mitigation: Keep mocks stateless where possible, use simple in-memory stores

**Complexity Notes:**
Medium complexity. While individual service mocks are straightforward, coordinating stateful interactions (e.g., novel text → scene extraction → image generation → comic assembly) requires careful sequencing. The biggest challenge is maintaining realistic data relationships across the multi-step comic generation pipeline.

**Key Files:**
- packages/backend/src/services/mock/: Mock service implementations directory
- packages/backend/src/config/environment.ts: Add mock mode configuration
- packages/backend/src/services/factory.ts: Service factory for mock/real switching
- packages/backend/src/test/mocks/: Test-specific mock data and handlers
- packages/shared/types/mocks.ts: Mock configuration types


### Design Decisions

[{'decision': 'Use MSW for HTTP API mocking combined with factory pattern for SDK services', 'rationale': 'MSW provides realistic network-level mocking for REST APIs while factory pattern allows clean switching between mock/real implementations for SDK-based services like OpenAI', 'alternatives_considered': ['Nock for HTTP mocking', 'Manual fetch override', 'Docker containers with mock services']}, {'decision': 'Environment-based mock activation with granular service-level overrides', 'rationale': 'Allows flexible testing scenarios (mock AI but use real database) and gradual development workflow', 'alternatives_considered': ['All-or-nothing mock mode', 'Runtime mock toggling', 'Test-only mocking']}]
