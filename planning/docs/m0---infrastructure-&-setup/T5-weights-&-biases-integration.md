---
area: ml
dependsOn: []
effort: 3
iteration: I1
key: T5
milestone: M0 - Infrastructure & Setup
priority: p1
title: Weights & Biases Integration
type: Task
---

# Weights & Biases Integration

## Acceptance Criteria

- [ ] **MLOps service successfully tracks LLM token usage, generation time, and costs for each comic generation request**
  - Verification: Check W&B dashboard shows metrics for token_count, generation_time_ms, estimated_cost per comic generation with proper experiment grouping
- [ ] **Stable Diffusion generation metrics are logged asynchronously without impacting comic generation performance**
  - Verification: Run load test generating 10 comics simultaneously - generation time should not increase >5% with W&B logging enabled vs disabled
- [ ] **User feedback scores are properly correlated with generation experiments in W&B Tables**
  - Verification: Generate test comic, submit feedback score, verify W&B Table entry links feedback to correct experiment run with comic metadata
- [ ] **A/B testing framework allows comparing different prompt templates with statistical significance tracking**
  - Verification: Create two prompt variants, generate 20 comics with each, verify W&B shows separate experiments with comparative metrics
- [ ] **Comic panel images and metadata are stored in W&B Tables without exposing sensitive user data**
  - Verification: Check W&B Tables contain comic_id, panel_count, generation_params but exclude user_id, email, or personal content

## Technical Notes

### Approach

Create a dedicated MLOps service that wraps the W&B SDK and integrates with our existing comic generation pipeline. Implement async logging queues to track LLM token usage, Stable Diffusion generation metrics, and user feedback without impacting performance. Use W&B's experiment tracking to A/B test different prompts and models, while leveraging W&B Tables to store comic metadata and generated artifacts for analysis.


### Files to Modify

- **path**: apps/backend/src/services/comic-generation.ts
- **changes**: Add MLOps service integration, metric collection points, experiment tracking calls
- **path**: apps/backend/src/routes/comics.ts
- **changes**: Inject experiment tracking for A/B testing, add feedback correlation endpoints
- **path**: apps/backend/package.json
- **changes**: Add wandb SDK dependency
- **path**: docker-compose.yml
- **changes**: Add WANDB_API_KEY and WANDB_PROJECT environment variables
- **path**: apps/backend/.env.example
- **changes**: Add W&B configuration variables with documentation

### New Files to Create

- **path**: apps/backend/src/services/mlops.ts
- **purpose**: Core W&B integration service with async logging queue and experiment management
- **path**: apps/backend/src/config/wandb.ts
- **purpose**: W&B configuration, environment validation, and SDK initialization
- **path**: packages/shared/src/types/mlops.ts
- **purpose**: TypeScript interfaces for ML metrics, experiment tracking, and W&B data structures
- **path**: apps/backend/src/utils/metric-calculator.ts
- **purpose**: Helper functions for calculating token costs, generation quality scores, and performance metrics
- **path**: apps/backend/src/middleware/experiment-tracking.ts
- **purpose**: Express middleware for automatic experiment context injection and A/B test assignment
- **path**: apps/backend/src/__tests__/fixtures/wandb-mock.ts
- **purpose**: Mock W&B responses for testing without external API dependency

### External Dependencies


- **wandb** ^0.16.0

  - Official Weights & Biases SDK for experiment tracking and ML monitoring

- **@types/node** ^20.0.0

  - TypeScript support for Node.js W&B integration

- **bull** ^4.12.0

  - Queue system for async ML metrics logging

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/mlops.test.ts`
  - Scenarios: MLOps service initialization with valid/invalid API keys, Async metric logging queue handles high volume, Metric sanitization removes sensitive data, Error handling when W&B API is unavailable, Experiment tracking creates proper run groups
- **File**: `apps/backend/src/__tests__/services/comic-generation.test.ts`
  - Scenarios: Comic generation with W&B logging enabled, Fallback behavior when MLOps service fails, Proper metric calculation for token usage
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/mlops-pipeline.test.ts`
  - Scenarios: End-to-end comic generation with W&B tracking, A/B test experiment creation and metric logging, User feedback correlation with experiment data, Batch metric upload and queue processing
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

- **task**: Install wandb SDK and configure environment variables
- **done**: False
- **task**: Create MLOps service with async logging queue and W&B SDK integration
- **done**: False
- **task**: Implement metric calculation utilities for LLM and Stable Diffusion tracking
- **done**: False
- **task**: Add experiment tracking middleware for A/B testing framework
- **done**: False
- **task**: Integrate MLOps service into comic generation pipeline with performance monitoring
- **done**: False
- **task**: Implement W&B Tables integration for comic metadata and user feedback correlation
- **done**: False
- **task**: Create comprehensive unit and integration test suite with W&B mocking
- **done**: False
- **task**: Set up W&B dashboard templates and automated alerts for key metrics
- **done**: False
- **task**: Performance test async logging under high load conditions
- **done**: False
- **task**: Documentation for MLOps service usage and W&B dashboard interpretation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Weights & Biases (W&B) integration is critical for monitoring and optimizing ML operations in Morpheus. Since we're using OpenAI/Anthropic LLMs and RunPod Stable Diffusion for novel-to-comic transformation, we need visibility into model performance, token usage, generation quality, and cost optimization. W&B provides experiment tracking, model versioning, and performance monitoring that will help us iterate on prompts, track comic generation quality metrics, and optimize our ML pipeline costs.

**Technical Approach:**
- Use official `wandb` SDK for Python/Node.js integration
- Create a dedicated MLOps service within the backend to centralize W&B operations
- Implement async logging to avoid blocking comic generation requests
- Track metrics: token usage, generation time, quality scores, user feedback
- Use W&B Tables for storing comic panel metadata and generated images
- Implement experiment tracking for A/B testing different prompts/models
- Set up automated model performance dashboards

**Dependencies:**
- External: wandb SDK, wandb Python API, environment variables for API keys
- Internal: ML service layer, comic generation pipeline, user feedback system
- Infrastructure: Environment variable management, logging infrastructure

**Risks:**
- API rate limits: implement exponential backoff and batching
- Data privacy: ensure no sensitive user content is logged inappropriately
- Performance overhead: async logging and sampling strategies needed
- Cost management: W&B storage costs can grow with image/artifact logging

**Complexity Notes:**
Medium complexity - the W&B SDK is well-documented, but integrating across our ML pipeline (LLM + Stable Diffusion) while maintaining performance requires careful architecture. The async nature of our comic generation process adds complexity to experiment tracking.

**Key Files:**
- apps/backend/src/services/mlops.ts: New W&B service wrapper
- apps/backend/src/services/comic-generation.ts: Add W&B logging calls
- apps/backend/src/config/wandb.ts: W&B configuration
- packages/shared/src/types/mlops.ts: Shared ML metrics types
- docker-compose.yml: Add W&B environment variables


### Design Decisions

[{'decision': 'Use W&B SDK with custom service wrapper pattern', 'rationale': 'Provides abstraction over W&B API, enables testing, and centralizes ML monitoring logic', 'alternatives_considered': ['Direct W&B SDK usage', 'Custom analytics solution', 'MLflow']}, {'decision': 'Async logging with queue-based approach', 'rationale': 'Prevents ML monitoring from blocking user-facing comic generation requests', 'alternatives_considered': ['Synchronous logging', 'Fire-and-forget approach']}, {'decision': 'Environment-based experiment organization', 'rationale': 'Separates dev/staging/production experiments while maintaining consistency', 'alternatives_considered': ['Manual project management', 'Git-branch based organization']}]
