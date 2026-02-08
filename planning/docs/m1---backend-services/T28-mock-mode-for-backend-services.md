---
area: backend
dependsOn:
- T25
effort: 2
iteration: I2
key: T28
milestone: M1 - Backend Services
priority: p1
title: Mock Mode for Backend Services
type: Task
---

# Mock Mode for Backend Services

## Acceptance Criteria

- [ ] **Mock mode can be enabled/disabled via environment variables and configuration**
  - Verification: Set MOCK_MODE=true and verify all external services return mock responses via integration tests
- [ ] **All external services (OpenAI, Anthropic, RunPod, Supabase) have realistic mock implementations**
  - Verification: Run npm test -- --grep 'mock services' and verify 100% of external API calls return deterministic responses
- [ ] **Mock responses include configurable delays and error scenarios**
  - Verification: Set MOCK_DELAY=2000 and MOCK_ERROR_RATE=0.1, verify responses take ~2s and 10% fail appropriately
- [ ] **Development dashboard allows runtime switching of mock scenarios**
  - Verification: Access /dev/mocks endpoint, switch to 'error' scenario, verify subsequent API calls return error responses
- [ ] **Mock data maintains narrative coherence for comic generation workflows**
  - Verification: Generate complete comic using mocks, verify story elements (characters, themes) remain consistent across panels

## Technical Notes

### Approach

Create a service abstraction layer with interfaces for all external dependencies (LLM, image generation, database). Implement mock versions of each service that return realistic, deterministic responses from JSON fixtures. Use a service factory pattern controlled by environment variables to instantiate either real or mock services. Include configurable delays and error injection to simulate real-world conditions. Provide a development endpoint to switch mock scenarios at runtime.


### Files to Modify

- **path**: packages/backend/src/config/index.ts
- **changes**: Add mock mode configuration options and validation
- **path**: packages/backend/src/services/llm/base-llm-service.ts
- **changes**: Extract interface for dependency injection
- **path**: packages/backend/src/services/image/stable-diffusion-service.ts
- **changes**: Extract interface for mock implementation
- **path**: packages/backend/src/middleware/service-injection.ts
- **changes**: Add service factory integration for request context

### New Files to Create

- **path**: packages/backend/src/services/mocks/mock-llm-service.ts
- **purpose**: Mock implementation for OpenAI/Anthropic LLM services
- **path**: packages/backend/src/services/mocks/mock-image-service.ts
- **purpose**: Mock implementation for RunPod Stable Diffusion API
- **path**: packages/backend/src/services/mocks/mock-database-service.ts
- **purpose**: Mock implementation for Supabase database operations
- **path**: packages/backend/src/factories/service-factory.ts
- **purpose**: Factory for instantiating real vs mock services based on config
- **path**: packages/backend/src/fixtures/llm-responses.json
- **purpose**: Realistic LLM response data for story analysis and generation
- **path**: packages/backend/src/fixtures/image-metadata.json
- **purpose**: Mock image generation responses with URLs and metadata
- **path**: packages/backend/src/fixtures/comic-scenarios.json
- **purpose**: Pre-defined comic generation scenarios for testing
- **path**: packages/backend/src/config/mock-config.ts
- **purpose**: Mock mode configuration schema and defaults
- **path**: packages/backend/src/routes/dev/mock-dashboard.ts
- **purpose**: Development endpoint for controlling mock behavior
- **path**: packages/backend/src/utils/mock-delay.ts
- **purpose**: Utility for adding realistic delays to mock responses
- **path**: packages/backend/src/types/mock-types.ts
- **purpose**: TypeScript interfaces for mock service contracts

### External Dependencies


- **msw** ^2.0.0

  - Intercept and mock HTTP requests at the network level

- **@faker-js/faker** ^8.0.0

  - Generate realistic test data for user profiles, content, etc.

- **nock** ^13.0.0

  - HTTP server mocking for API integration tests

## Testing

### Unit Tests

- **File**: `packages/backend/src/__tests__/services/mocks/mock-llm-service.test.ts`
  - Scenarios: Returns deterministic story analysis responses, Simulates API errors and timeouts, Respects configured delays, Maintains character consistency across requests
- **File**: `packages/backend/src/__tests__/services/mocks/mock-image-service.test.ts`
  - Scenarios: Returns mock image URLs with metadata, Simulates generation failures, Handles different art styles consistently
- **File**: `packages/backend/src/__tests__/factories/service-factory.test.ts`
  - Scenarios: Returns mock services when MOCK_MODE=true, Returns real services when MOCK_MODE=false, Throws error for invalid configuration
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/mock-comic-generation.test.ts`
  - Scenarios: Complete comic generation flow using mocks, Error handling during mock service failures, Performance with configured delays
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

- **task**: Create service interfaces and extract from existing implementations
- **done**: False
- **task**: Implement mock service classes with realistic response data
- **done**: False
- **task**: Build service factory with environment-based switching
- **done**: False
- **task**: Create JSON fixtures with coherent comic generation data
- **done**: False
- **task**: Add mock configuration management and validation
- **done**: False
- **task**: Implement development dashboard for runtime control
- **done**: False
- **task**: Add configurable delays and error injection mechanisms
- **done**: False
- **task**: Integrate mock services into existing API endpoints
- **done**: False
- **task**: Write comprehensive test suite covering all scenarios
- **done**: False
- **task**: Create documentation and development setup guide
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Mock Mode is essential for development and testing environments where external services (OpenAI/Anthropic LLMs, RunPod Stable Diffusion, Supabase) are expensive, unreliable, or unavailable. This solves several critical problems: eliminates API costs during development, enables offline development, provides deterministic responses for testing, prevents hitting rate limits, and allows simulation of error scenarios. For Morpheus, this is crucial given the high cost of AI services and the need for predictable comic generation workflows during development.

**Technical Approach:**
Implement a configuration-driven mock system using environment variables and dependency injection. Create mock implementations for each external service that return realistic, deterministic data. Use factories to switch between real and mock services based on NODE_ENV or MOCK_MODE flags. Store mock data as JSON fixtures organized by service and scenario (success, error, timeout). Implement a mock server for webhook testing and provide a development dashboard to control mock responses.

**Dependencies:**
- External: msw (Mock Service Worker), nock (HTTP mocking), faker-js (realistic test data)
- Internal: Service abstraction layer, configuration management, logging system

**Risks:**
- Mock drift: Mock responses diverging from real API responses over time. Mitigation: Regular sync with actual API documentation and response validation
- Incomplete error simulation: Missing edge cases in mock responses. Mitigation: Comprehensive error scenario mapping
- Performance differences: Mocks being too fast compared to real services, hiding timing issues. Mitigation: Configurable delays in mock responses

**Complexity Notes:**
Initially seems straightforward but becomes complex when considering all the edge cases, error scenarios, and maintaining parity with real services. The challenge lies in creating realistic mock data for complex AI responses (story analysis, image generation) that maintains narrative coherence.

**Key Files:**
- packages/backend/src/services/mocks/: Mock service implementations
- packages/backend/src/config/mock-config.ts: Mock mode configuration
- packages/backend/src/factories/service-factory.ts: Service instantiation logic
- packages/backend/src/fixtures/: Mock response data


### Design Decisions

[{'decision': 'Use dependency injection with service factories to switch between real and mock implementations', 'rationale': 'Allows clean separation of mock logic from business logic, makes testing easier, and enables runtime switching of implementations', 'alternatives_considered': ['Direct mocking with nock/msw', 'Compile-time switching with webpack', 'Proxy pattern wrapper']}, {'decision': 'Store mock data as structured JSON fixtures with scenario-based organization', 'rationale': 'Provides version control for mock data, allows easy editing by non-developers, and enables scenario-based testing', 'alternatives_considered': ['Generated mock data with faker', 'In-memory hardcoded responses', 'Database-stored mock data']}]
