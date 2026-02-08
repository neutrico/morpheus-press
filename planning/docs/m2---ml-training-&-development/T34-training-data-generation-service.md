---
area: ml
dependsOn:
- T21
effort: 5
iteration: I2
key: T34
milestone: M2 - ML Training & Development
priority: p1
title: Training Data Generation Service
type: Task
---

# Training Data Generation Service

## Acceptance Criteria

- [ ] **Service generates high-quality synthetic training pairs (text + comic descriptions) with configurable templates and LLM prompts**
  - Verification: POST /api/v1/training-data/generate with template_id returns valid dataset with >90% schema compliance rate
- [ ] **Queue-based processing handles batch generation of 1000+ samples without memory overflow or timeouts**
  - Verification: BullMQ dashboard shows successful completion of batch job generating 1000 samples within 30 minutes
- [ ] **Dataset versioning and metadata tracking maintains full lineage from generation parameters to final output**
  - Verification: GET /api/v1/training-data/datasets/{id}/metadata returns complete generation config, timestamps, and quality metrics
- [ ] **Cost tracking accurately monitors API usage across OpenAI/Anthropic services with configurable budget limits**
  - Verification: Cost dashboard shows real-time spend tracking and auto-pauses generation when budget threshold exceeded
- [ ] **Streaming API efficiently delivers large datasets (>100MB) without server memory issues**
  - Verification: GET /api/v1/training-data/datasets/{id}/download streams 500MB dataset with <2GB server memory usage

## Technical Notes

### Approach

Implement a Fastify-based microservice that orchestrates training data generation through configurable pipelines. Use BullMQ for queue management with Redis, integrating with existing LLM services for text generation and Stable Diffusion for validation. Store datasets in Supabase with proper metadata and versioning, implementing streaming APIs for large dataset downloads. Include cost tracking, quality metrics, and automated validation workflows.


### Files to Modify

- **path**: apps/backend/src/index.ts
- **changes**: Register training data routes and BullMQ queue connections
- **path**: apps/backend/src/lib/database.ts
- **changes**: Add dataset storage helpers and versioning utilities
- **path**: packages/shared/src/types/index.ts
- **changes**: Export training data types for frontend consumption

### New Files to Create

- **path**: apps/backend/src/services/training-data-generator.ts
- **purpose**: Core orchestration service for data generation pipelines
- **path**: apps/backend/src/routes/training-data/index.ts
- **purpose**: API route registration and middleware setup
- **path**: apps/backend/src/routes/training-data/generate.ts
- **purpose**: POST endpoint for initiating dataset generation jobs
- **path**: apps/backend/src/routes/training-data/datasets.ts
- **purpose**: CRUD operations for dataset management and metadata
- **path**: apps/backend/src/routes/training-data/download.ts
- **purpose**: Streaming download endpoint for large datasets
- **path**: apps/backend/src/workers/data-generation.worker.ts
- **purpose**: BullMQ worker for background dataset generation processing
- **path**: packages/shared/src/schemas/training-data.ts
- **purpose**: Zod validation schemas for all training data structures
- **path**: apps/backend/src/lib/cost-tracker.ts
- **purpose**: API usage cost monitoring and budget enforcement
- **path**: apps/backend/src/lib/data-templates.ts
- **purpose**: Configurable templates for different dataset types
- **path**: apps/backend/src/lib/quality-validator.ts
- **purpose**: Multi-stage validation pipeline for generated data quality
- **path**: database/migrations/20241201_training_data_tables.sql
- **purpose**: Supabase schema for datasets, generations, and metadata

### External Dependencies


- **bullmq** ^5.0.0

  - Redis-based queue system for batch data generation jobs

- **@bull-board/fastify** ^5.0.0

  - Web UI for monitoring data generation job queues

- **@faker-js/faker** ^8.0.0

  - Generate synthetic metadata and augment training examples

- **csv-parser** ^3.0.0

  - Parse and process external dataset imports

- **sharp** ^0.32.0

  - Image processing and validation for generated visual data

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/training-data-generator.test.ts`
  - Scenarios: Template-based generation with valid schemas, LLM service integration with mocked responses, Data validation pipeline with edge cases, Cost calculation accuracy, Error handling for external service failures
- **File**: `apps/backend/src/__tests__/workers/data-generation.worker.test.ts`
  - Scenarios: Queue job processing success/failure, Batch processing with memory constraints, Progress tracking and status updates
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/training-data-flow.test.ts`
  - Scenarios: End-to-end dataset generation from API to storage, BullMQ job lifecycle with Redis integration, Supabase storage with versioning, LLM service integration with rate limiting
- **File**: `apps/backend/src/__tests__/integration/streaming-api.test.ts`
  - Scenarios: Large dataset streaming performance, Concurrent download handling
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

- **task**: Setup BullMQ infrastructure and Redis connection
- **done**: False
- **task**: Implement core TrainingDataGenerator service class
- **done**: False
- **task**: Create Zod schemas and validation pipeline
- **done**: False
- **task**: Build API endpoints for generation and dataset management
- **done**: False
- **task**: Implement BullMQ worker for background processing
- **done**: False
- **task**: Add streaming download functionality with memory optimization
- **done**: False
- **task**: Integrate cost tracking and budget enforcement
- **done**: False
- **task**: Create database migrations and Supabase integration
- **done**: False
- **task**: Build quality validation and bias detection metrics
- **done**: False
- **task**: Comprehensive testing and performance optimization
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Training Data Generation Service is critical for creating high-quality datasets to fine-tune ML models for novel-to-comic transformation. This service will generate synthetic training pairs of text descriptions and corresponding comic panel descriptions/styles, augment existing data, and create domain-specific datasets for character consistency, scene composition, and visual storytelling. Without quality training data, our comic generation models will produce inconsistent results and poor visual coherence.

**Technical Approach:**
Build a dedicated microservice using Fastify 5 that orchestrates data generation pipelines. Use OpenAI/Anthropic LLMs for text augmentation and synthetic scene generation, integrate with existing Stable Diffusion endpoints for image generation validation. Implement queue-based processing with BullMQ for batch operations, store generated datasets in Supabase with proper versioning and metadata tracking. Use Zod schemas for data validation and implement streaming responses for large dataset generation.

**Dependencies:**
- External: [@bull-board/fastify, bullmq, zod, @faker-js/faker, csv-parser, sharp, node-fetch]
- Internal: Existing LLM service abstraction, RunPod Stable Diffusion service, Supabase database schemas, shared validation schemas

**Risks:**
- Data Quality Degradation: Implement multi-stage validation and human-in-the-loop review processes
- Cost Explosion: Set strict API rate limits, implement cost tracking, and use cheaper models for bulk generation
- Storage Bloat: Implement data lifecycle policies, compression strategies, and archival systems
- Bias Amplification: Diversify data sources and implement bias detection metrics

**Complexity Notes:**
More complex than initially estimated due to need for sophisticated data validation pipelines and integration with multiple ML services. The challenge lies in maintaining data quality at scale while managing costs and ensuring reproducibility.

**Key Files:**
- apps/backend/src/services/training-data-generator.ts: Core service implementation
- apps/backend/src/routes/training-data/: API endpoints for dataset management
- packages/shared/src/schemas/training-data.ts: Validation schemas
- apps/backend/src/workers/data-generation.worker.ts: Background processing logic


### Design Decisions

[{'decision': 'Queue-based architecture with BullMQ for dataset generation', 'rationale': 'Training data generation is inherently batch-oriented and resource-intensive, requiring proper job management, retry logic, and progress tracking', 'alternatives_considered': ['Direct API processing', 'Serverless functions', 'Event-driven architecture']}, {'decision': 'Multi-tier data validation with LLM-assisted quality scoring', 'rationale': 'Ensures generated training data meets quality thresholds before expensive fine-tuning operations', 'alternatives_considered': ['Rule-based validation only', 'Human review only', 'No validation']}, {'decision': 'Versioned dataset storage with immutable snapshots', 'rationale': 'Enables reproducible training runs and A/B testing of different dataset versions', 'alternatives_considered': ['Mutable datasets', 'Git-based versioning', 'External dataset services']}]
