---
area: image-gen
dependsOn:
- T41
- T42
effort: 5
iteration: I4
key: T50
milestone: M3 - Content Generation Pipeline
priority: p0
title: Prompt Engineering Service
type: Feature
---

# Prompt Engineering Service

## Acceptance Criteria

- [ ] **Service generates consistent character prompts across multiple panels with same character descriptors**
  - Verification: POST /api/prompts/generate with same character_id returns prompts with identical character descriptions
- [ ] **Prompt templates correctly interpolate novel context and character data into Stable Diffusion format**
  - Verification: Generated prompts follow 'subject, style, background, lighting, quality modifiers' structure with < 77 tokens
- [ ] **Character consistency tracking persists visual descriptors with versioning**
  - Verification: Database query shows character_descriptors table maintains version history and retrieves latest by character_id
- [ ] **Service handles context window limits through intelligent chunking and summarization**
  - Verification: Novel chapters > 8000 tokens are automatically chunked and processed without LLM API errors
- [ ] **Caching reduces LLM API calls by >80% for repeated character/scene combinations**
  - Verification: Redis cache hit rate > 80% measured via /api/health/prompts endpoint after processing same novel twice

## Technical Notes

### Approach

Implement a service-oriented architecture with PromptEngineeringService as the core orchestrator. The service will use Handlebars templates for structured prompt generation, integrate with OpenAI/Anthropic for context analysis and enhancement, and maintain character consistency through a versioned descriptor system. A multi-tier caching strategy will optimize performance and costs. The service exposes REST endpoints for the image generation pipeline and includes comprehensive validation, testing, and monitoring capabilities.


### Files to Modify

- **path**: packages/database/src/schema/index.ts
- **changes**: Add character_descriptors and prompt_cache table imports
- **path**: apps/api/src/routes/index.ts
- **changes**: Register /api/prompts route handler
- **path**: apps/api/src/services/index.ts
- **changes**: Export PromptEngineeringService for dependency injection
- **path**: apps/api/src/middleware/validation.ts
- **changes**: Add prompt request validation middleware

### New Files to Create

- **path**: apps/api/src/services/prompt-engineering/PromptEngineeringService.ts
- **purpose**: Core service orchestrator for prompt generation and character consistency
- **path**: apps/api/src/services/prompt-engineering/PromptTemplateEngine.ts
- **purpose**: Handlebars template management and rendering
- **path**: apps/api/src/services/prompt-engineering/CharacterConsistencyTracker.ts
- **purpose**: Character descriptor persistence and versioning
- **path**: apps/api/src/services/prompt-engineering/ContextAnalyzer.ts
- **purpose**: Novel text analysis and chunking for LLM processing
- **path**: apps/api/src/services/prompt-engineering/PromptOptimizer.ts
- **purpose**: LLM integration for prompt enhancement and validation
- **path**: apps/api/src/services/prompt-engineering/PromptCache.ts
- **purpose**: Redis-based caching layer for templates and generated prompts
- **path**: apps/api/src/services/prompt-engineering/templates/character.hbs
- **purpose**: Character-focused prompt template
- **path**: apps/api/src/services/prompt-engineering/templates/scene.hbs
- **purpose**: Scene/background prompt template
- **path**: apps/api/src/services/prompt-engineering/templates/panel.hbs
- **purpose**: Comic panel layout prompt template
- **path**: apps/api/src/services/prompt-engineering/templates/style.hbs
- **purpose**: Art style and quality modifier template
- **path**: packages/shared/src/types/prompts.ts
- **purpose**: TypeScript interfaces and Zod schemas for prompt structures
- **path**: packages/shared/src/types/characters.ts
- **purpose**: Character descriptor and consistency tracking types
- **path**: apps/api/src/routes/prompts/index.ts
- **purpose**: REST API routes for prompt generation endpoints
- **path**: apps/api/src/routes/prompts/generate.ts
- **purpose**: POST /api/prompts/generate endpoint handler
- **path**: apps/api/src/routes/prompts/characters.ts
- **purpose**: Character descriptor CRUD endpoints
- **path**: packages/database/src/schema/prompts.sql
- **purpose**: Database tables for prompt cache and character descriptors
- **path**: apps/api/src/config/prompt-engineering.ts
- **purpose**: Service configuration including LLM API settings and cache TTL
- **path**: apps/api/src/services/prompt-engineering/utils/sanitization.ts
- **purpose**: Input sanitization and prompt injection prevention
- **path**: apps/api/src/services/prompt-engineering/utils/tokenizer.ts
- **purpose**: Token counting and context window management

### External Dependencies


- **openai** ^4.20.0

  - GPT-4 integration for intelligent prompt enhancement and narrative analysis

- **@anthropic-ai/sdk** ^0.9.0

  - Claude integration as fallback LLM and for specific prompt optimization tasks

- **handlebars** ^4.7.8

  - Template engine for structured, maintainable prompt generation with variable interpolation

- **ioredis** ^5.3.0

  - Redis client for high-performance caching of prompts and character descriptors

- **natural** ^6.0.0

  - NLP utilities for text analysis, sentiment detection, and entity extraction from novel content

## Testing

### Unit Tests

- **File**: `apps/api/src/services/prompt-engineering/__tests__/PromptEngineeringService.test.ts`
  - Scenarios: Template interpolation with valid data, Character consistency tracking, Prompt validation and sanitization, Cache hit/miss scenarios, LLM API error handling
- **File**: `apps/api/src/services/prompt-engineering/__tests__/PromptTemplateEngine.test.ts`
  - Scenarios: Handlebars template rendering, Template not found errors, Invalid template data handling
- **File**: `packages/shared/src/types/__tests__/prompts.test.ts`
  - Scenarios: Zod schema validation success/failure, Type guard functions
### Integration Tests

- **File**: `apps/api/src/services/prompt-engineering/__tests__/integration/prompt-pipeline.test.ts`
  - Scenarios: End-to-end novel text to optimized prompt generation, Character persistence across multiple API calls, Redis cache integration, LLM API integration with rate limiting
- **File**: `apps/api/src/routes/__tests__/integration/prompts.test.ts`
  - Scenarios: REST API endpoints with authentication, Error handling and validation
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2
- **Documentation**: 1
- **Total**: 12.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup database schema and Redis configuration for caching
- **done**: False
- **task**: Implement core PromptEngineeringService with dependency injection
- **done**: False
- **task**: Create Handlebars template system with character/scene/style templates
- **done**: False
- **task**: Build CharacterConsistencyTracker with versioned descriptor persistence
- **done**: False
- **task**: Integrate LLM APIs (OpenAI/Anthropic) with error handling and rate limiting
- **done**: False
- **task**: Implement multi-tier caching strategy with Redis
- **done**: False
- **task**: Create REST API endpoints with validation middleware
- **done**: False
- **task**: Add comprehensive unit and integration test suites
- **done**: False
- **task**: Implement monitoring, logging, and health check endpoints
- **done**: False
- **task**: Create API documentation and service integration guides
- **done**: False

## Agent Notes

### Research Findings

**Context:**
The Prompt Engineering Service is critical for the comic generation pipeline, responsible for transforming novel text into optimized prompts for Stable Diffusion image generation. This service needs to analyze narrative context, extract visual elements, maintain character consistency across panels, and generate prompts that produce coherent comic artwork. Without sophisticated prompt engineering, the generated images will lack narrative coherence, visual consistency, and comic-appropriate styling.

**Technical Approach:**
- Create a dedicated `PromptEngineeringService` class with template-based prompt construction
- Implement prompt templates for different comic elements (characters, scenes, panels, styles)
- Use LLM integration (OpenAI/Anthropic) for intelligent prompt enhancement and context analysis
- Build character consistency tracking with visual descriptor persistence
- Create prompt validation and optimization pipeline with A/B testing capabilities
- Implement caching layer for prompt templates and character descriptors using Redis
- Use Zod schemas for prompt structure validation and type safety

**Dependencies:**
- External: openai ^4.0.0, @anthropic-ai/sdk, zod ^3.22.0, ioredis ^5.3.0, handlebars ^4.7.8
- Internal: Database service (character persistence), Novel parsing service, Image generation queue, Analytics service

**Risks:**
- Prompt drift: Character descriptions changing between panels - mitigate with strict descriptor versioning
- Context window limits: Large novels exceeding LLM context - implement chunking and summarization
- Prompt injection: User input contaminating prompts - strict sanitization and validation
- Cost escalation: Excessive LLM API calls - implement aggressive caching and batch processing
- Style inconsistency: Prompts generating different art styles - maintain strict style guide templates

**Complexity Notes:**
This is significantly more complex than initially apparent. The service must handle narrative analysis, visual consistency across potentially hundreds of panels, character relationship tracking, and dynamic style adaptation. The context-aware prompt generation requires sophisticated NLP and may need custom fine-tuning of smaller models for cost efficiency.

**Key Files:**
- apps/api/src/services/prompt-engineering/: Main service directory
- apps/api/src/services/prompt-engineering/templates/: Handlebars prompt templates
- packages/shared/src/types/prompts.ts: TypeScript interfaces for prompt structures
- apps/api/src/routes/prompts/: REST endpoints for prompt generation
- packages/database/src/schema/prompts.sql: Prompt cache and character descriptor tables


### Design Decisions

[{'decision': 'Use template-based prompt construction with Handlebars', 'rationale': 'Provides structured, maintainable prompt generation with variable interpolation while allowing non-technical team members to modify templates', 'alternatives_considered': ['String concatenation', 'Custom DSL', 'Pure LLM generation']}, {'decision': 'Implement character descriptor versioning with database persistence', 'rationale': 'Ensures visual consistency across comic panels by maintaining canonical character descriptions that evolve predictably', 'alternatives_considered': ['In-memory storage', 'File-based descriptors', 'LLM-only consistency']}, {'decision': 'Multi-tier caching strategy (Redis + in-memory)', 'rationale': 'Reduces LLM API costs and improves response times for frequently used prompts while handling high-frequency requests', 'alternatives_considered': ['Database-only caching', 'No caching', 'File system cache']}]
