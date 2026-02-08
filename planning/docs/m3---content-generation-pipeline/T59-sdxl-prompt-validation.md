---
area: image-gen
dependsOn:
- T50
effort: 2
iteration: I4
key: T59
milestone: M3 - Content Generation Pipeline
priority: p0
title: SDXL Prompt Validation
type: Feature
---

# SDXL Prompt Validation

## Acceptance Criteria

- [ ] **SDXL prompts are validated against token limits (77 tokens for positive, 77 for negative prompts) and structural requirements**
  - Verification: Unit test with prompts exceeding limits returns specific error messages; API endpoint rejects invalid prompts with 400 status
- [ ] **Content moderation prevents NSFW/harmful prompts while allowing comic-appropriate fantasy/violence terms**
  - Verification: Integration test suite with 50+ test prompts (legitimate comic terms vs. actual NSFW content) achieves <5% false positive rate
- [ ] **Validation performance does not exceed 200ms for cached prompts and 2s for new prompts including moderation API calls**
  - Verification: Load test with 100 concurrent validation requests; Redis cache hit rate >80% in production metrics
- [ ] **Image generation pipeline integrates validation seamlessly with detailed error responses for invalid prompts**
  - Verification: E2E test: Submit invalid prompt through frontend, receive specific validation error; valid prompt proceeds to RunPod API
- [ ] **Validation service provides sync endpoint for real-time feedback and async processing for batch operations**
  - Verification: API documentation shows both /validate-prompt (sync) and /validate-batch (async) endpoints; manual testing confirms <500ms response for sync validation

## Technical Notes

### Approach

Create a PromptValidationService that accepts SDXL prompt objects and runs them through progressive validation layers: structural validation (required fields, types), constraint validation (token limits, aspect ratios), content validation (moderation API), and comic-context validation (genre-appropriate terms). The service returns detailed validation results with specific error messages and suggestions. Integrate this service into the existing image generation pipeline as a pre-processing step, with caching to optimize repeated validations.


### Files to Modify

- **path**: packages/image-gen/src/services/sdxl-service.ts
- **changes**: Add PromptValidationService integration before RunPod API calls; modify generateImage method to validate prompts first
- **path**: apps/backend/src/routes/image-gen.ts
- **changes**: Add /validate-prompt and /validate-batch endpoints; integrate validation middleware for existing generation endpoints
- **path**: packages/image-gen/src/types/sdxl.ts
- **changes**: Add ValidationResult, ValidationError, and PromptValidationOptions type definitions
- **path**: apps/backend/src/middleware/error-handler.ts
- **changes**: Add specific error handling for PromptValidationError with user-friendly messages

### New Files to Create

- **path**: packages/image-gen/src/validation/prompt-validation-service.ts
- **purpose**: Main validation service orchestrating all validation layers
- **path**: packages/image-gen/src/validation/content-moderator.ts
- **purpose**: OpenAI moderation API integration with comic-context awareness
- **path**: packages/image-gen/src/validation/constraint-validator.ts
- **purpose**: SDXL-specific validation (tokens, aspect ratios, model parameters)
- **path**: packages/image-gen/src/validation/comic-context-validator.ts
- **purpose**: Comic genre allowlist and context-aware filtering
- **path**: packages/shared/src/schemas/prompt-validation-schemas.ts
- **purpose**: Zod schemas for SDXL prompt structure validation
- **path**: packages/image-gen/src/validation/token-counter.ts
- **purpose**: CLIP tokenizer integration for accurate token counting
- **path**: packages/image-gen/src/validation/validation-cache.ts
- **purpose**: Redis caching layer for validation results
- **path**: packages/image-gen/src/validation/index.ts
- **purpose**: Barrel exports for validation services

### External Dependencies


- **zod** ^3.22.4

  - Type-safe schema validation with custom refinements for SDXL constraints

- **openai** ^4.28.0

  - Content moderation API to filter inappropriate prompts

- **ioredis** ^5.3.2

  - Redis client for caching validation results by prompt hash

- **gpt-3-encoder** ^1.1.4

  - Accurate token counting for prompt length validation

- **validator** ^13.11.0

  - Additional string validation utilities for prompt sanitization

## Testing

### Unit Tests

- **File**: `packages/image-gen/src/validation/__tests__/prompt-validation.test.ts`
  - Scenarios: Token limit validation for positive/negative prompts, Required field validation (prompt, model_version), Aspect ratio validation against SDXL supported ratios, Comic-specific term allowlist functionality, Cache hit/miss scenarios
- **File**: `packages/image-gen/src/validation/__tests__/content-moderation.test.ts`
  - Scenarios: OpenAI moderation API integration, Comic context filtering (violence/fantasy terms), Moderation API failure handling, Custom moderation rules for comic art
### Integration Tests

- **File**: `packages/image-gen/src/__tests__/integration/validation-pipeline.test.ts`
  - Scenarios: Full validation pipeline with Redis caching, Integration with existing image generation service, Batch validation processing, Error propagation through pipeline
### E2E Tests

- **File**: `apps/backend/src/__tests__/e2e/image-gen-validation.test.ts`
  - Scenarios: Frontend prompt submission through validation to RunPod, Invalid prompt rejection with user-friendly error messages, Valid prompt processing end-to-end
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

- **task**: Setup validation service structure and dependencies (zod, openai, ioredis)
- **done**: False
- **task**: Implement Zod schemas for SDXL prompt structure validation
- **done**: False
- **task**: Create token counting service using CLIP tokenizer
- **done**: False
- **task**: Implement constraint validator for SDXL limits (tokens, aspect ratios)
- **done**: False
- **task**: Build content moderator with OpenAI API integration and comic allowlist
- **done**: False
- **task**: Create Redis caching layer for validation results
- **done**: False
- **task**: Implement main PromptValidationService orchestrator
- **done**: False
- **task**: Integrate validation into existing SDXL service and API routes
- **done**: False
- **task**: Add comprehensive test suite (unit, integration, e2e)
- **done**: False
- **task**: Update API documentation and error handling
- **done**: False
- **task**: Performance testing and cache optimization
- **done**: False
- **task**: Code review and deployment preparation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
SDXL (Stable Diffusion XL) prompt validation is critical for the content generation pipeline to ensure high-quality comic panel generation. Invalid prompts can cause RunPod API failures, wasted compute resources, poor image quality, or NSFW content generation. This task ensures prompts are properly formatted, within token limits, contain appropriate descriptors for comic art style, and are filtered for content policy compliance before expensive GPU inference.

**Technical Approach:**
Implement a multi-layered validation system using Zod schemas for structure validation, custom validators for SDXL-specific constraints, and OpenAI moderation API for content filtering. Create a validation service that integrates with the existing image generation pipeline, providing both sync validation (for immediate feedback) and async batch validation (for processing queues). Use a caching layer (Redis) to avoid re-validating identical prompts.

**Dependencies:**
- External: zod (validation schemas), openai (moderation API), ioredis (caching), validator.js (string validation)
- Internal: Image generation service, content moderation service, prompt engineering utilities, error handling middleware

**Risks:**
- Over-aggressive filtering: Could block legitimate comic art prompts; mitigation: implement allowlist for comic-specific terms
- Performance bottleneck: Validation could slow down generation pipeline; mitigation: implement async validation with queuing
- False positives in moderation: AI moderation may flag comic violence/fantasy; mitigation: custom moderation rules for comic context
- Token counting accuracy: Different tokenizers between validation and SDXL; mitigation: use CLIP tokenizer for accurate counting

**Complexity Notes:**
Initially seems straightforward but complexity increases due to SDXL's specific requirements (negative prompts, style modifiers, aspect ratios), comic genre considerations (fantasy violence, supernatural elements), and the need for context-aware validation that understands comic art terminology vs. potentially harmful content.

**Key Files:**
- packages/image-gen/src/validation/: New validation service directory
- packages/image-gen/src/services/sdxl-service.ts: Integrate validation before API calls
- packages/shared/src/schemas/prompt-schemas.ts: Zod schemas for prompt validation
- apps/backend/src/routes/image-gen.ts: Add validation endpoint for frontend


### Design Decisions

[{'decision': 'Use Zod for schema validation with custom refinements', 'rationale': 'Type-safe validation that integrates well with TypeScript codebase, allows custom validation logic, and provides detailed error messages for debugging', 'alternatives_considered': ['Joi validation', 'Manual validation functions', 'JSON Schema with ajv']}, {'decision': 'Implement tiered validation (fast local checks, then AI moderation)', 'rationale': 'Optimize for performance by catching obvious issues locally before expensive API calls, while still ensuring content safety', 'alternatives_considered': ['AI-only moderation', 'Rule-based only', 'User reporting system']}, {'decision': 'Cache validation results by prompt hash', 'rationale': 'Avoid redundant validation of identical prompts, especially important for batch processing and user iterations', 'alternatives_considered': ['No caching', 'Database-based caching', 'In-memory only caching']}]
