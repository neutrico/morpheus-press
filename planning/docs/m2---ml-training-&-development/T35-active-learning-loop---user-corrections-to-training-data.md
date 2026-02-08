---
area: ml
dependsOn:
- T34
effort: 3
iteration: I2
key: T35
milestone: M2 - ML Training & Development
priority: p2
title: Active Learning Loop - User Corrections to Training Data
type: Task
---

# Active Learning Loop - User Corrections to Training Data

## Acceptance Criteria

- [ ] **User corrections are captured and stored when editing comic scenes, characters, or panels**
  - Verification: Create comic → make corrections → verify feedback records in database with correct user_id, correction_type, and original/corrected data
- [ ] **Feedback processing worker transforms corrections into training-ready format within 30 seconds**
  - Verification: Monitor bull queue metrics and database timestamps between feedback creation and processed status
- [ ] **Training data versioning tracks dataset evolution with lineage from user feedback**
  - Verification: Generate training dataset → verify version increment and feedback_source references in training_datasets table
- [ ] **Data validation rejects low-quality feedback and flags suspicious corrections for review**
  - Verification: Submit invalid/malicious feedback → verify rejection with appropriate error codes and admin queue entries
- [ ] **Privacy controls allow users to opt-out and anonymize their feedback data**
  - Verification: Toggle privacy settings → verify feedback anonymization and opt-out status in user preferences

## Technical Notes

### Approach

Build a multi-tier feedback system: (1) Real-time collection APIs that capture user corrections during comic editing, (2) Validation layer using Zod schemas and business rules to ensure feedback quality, (3) Asynchronous processing workers that transform feedback into training-ready formats, (4) Integration with existing ML training pipelines to incorporate corrections into model fine-tuning. Implement data versioning to track training dataset evolution and A/B testing capabilities to validate improvements.


### Files to Modify

- **path**: apps/api/src/routes/comics.ts
- **changes**: Add feedback collection endpoints for scene/character corrections
- **path**: apps/api/src/middleware/auth.ts
- **changes**: Add user privacy preference validation for feedback collection
- **path**: apps/web/src/components/comic-editor/SceneEditor.tsx
- **changes**: Integrate feedback collection hooks on user corrections
- **path**: packages/database/migrations/002_comics.sql
- **changes**: Add feedback foreign key relationships to existing tables

### New Files to Create

- **path**: packages/database/schemas/feedback.sql
- **purpose**: Define feedback tables, indexes, and constraints for corrections storage
- **path**: apps/api/src/services/feedback-collector.ts
- **purpose**: Core service for capturing, validating, and storing user corrections
- **path**: apps/api/src/workers/training-data-processor.ts
- **purpose**: Bull queue worker for async processing of feedback into training format
- **path**: packages/ml-training/src/active-learning/feedback-processor.ts
- **purpose**: ML-specific logic for transforming feedback into model training data
- **path**: apps/api/src/routes/feedback.ts
- **purpose**: REST endpoints for feedback submission, status queries, and privacy controls
- **path**: packages/shared/src/types/feedback.ts
- **purpose**: TypeScript interfaces for feedback data structures across packages
- **path**: apps/api/src/services/data-quality-validator.ts
- **purpose**: Validation rules and quality scoring for feedback submissions
- **path**: packages/ml-training/src/dataset-versioning/training-dataset-manager.ts
- **purpose**: Version control and lineage tracking for training datasets
- **path**: apps/api/src/queues/feedback-processing.ts
- **purpose**: Bull queue configuration and job definitions for feedback processing
- **path**: packages/database/src/repositories/feedback-repository.ts
- **purpose**: Data access layer for feedback CRUD operations and queries

### External Dependencies


- **bull** ^4.12.0

  - Redis-based job queues for asynchronous feedback processing

- **ioredis** ^5.3.0

  - Redis client for Bull queue backend and caching

- **@bull-board/api** ^5.10.0

  - Queue monitoring dashboard for debugging training data processing

- **zod** ^3.22.0

  - Runtime validation for feedback data schemas and type safety

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/feedback-collector.test.ts`
  - Scenarios: Valid scene correction capture, Character description feedback validation, Duplicate feedback deduplication, Privacy opt-out handling, Invalid feedback rejection
- **File**: `apps/api/src/__tests__/workers/training-data-processor.test.ts`
  - Scenarios: Feedback transformation to training format, Batch processing optimization, Error handling and retry logic, Data quality scoring
- **File**: `packages/ml-training/src/__tests__/active-learning/feedback-processor.test.ts`
  - Scenarios: Multi-modal feedback processing, Training dataset versioning, Bias detection algorithms, Stratified sampling validation
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/feedback-flow.test.ts`
  - Scenarios: End-to-end correction capture to training data, Queue processing with Redis integration, Database consistency across feedback tables, ML pipeline integration
- **File**: `packages/database/src/__tests__/feedback-schema.test.ts`
  - Scenarios: Feedback table relationships and constraints, Data retention policy enforcement, Index performance on large datasets
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

- **task**: Design and implement database schema for feedback storage
- **done**: False
- **task**: Create feedback collection service with validation layer
- **done**: False
- **task**: Implement Bull queue workers for async feedback processing
- **done**: False
- **task**: Build ML training pipeline integration for feedback incorporation
- **done**: False
- **task**: Add privacy controls and data anonymization features
- **done**: False
- **task**: Create REST API endpoints for feedback submission and management
- **done**: False
- **task**: Integrate feedback collection into comic editor UI components
- **done**: False
- **task**: Implement data versioning and lineage tracking system
- **done**: False
- **task**: Add monitoring and metrics for feedback processing pipeline
- **done**: False
- **task**: Write comprehensive tests and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Active learning loops are crucial for improving ML model quality by incorporating user corrections back into training data. For Morpheus, this means when users correct generated scene descriptions, character descriptions, or panel compositions, these corrections should be captured, validated, and fed back into the training pipeline to improve future generations. This creates a continuous improvement cycle that makes the platform smarter over time and reduces the need for manual corrections.

**Technical Approach:**
Implement a feedback collection system with PostgreSQL storage, asynchronous processing via queues, and integration with the existing ML training pipeline. Use a reward/penalty system for training data quality, implement data versioning for training datasets, and create validation mechanisms to ensure feedback quality. The system should track user corrections at multiple levels: text-to-scene conversion, scene-to-image generation, and panel layout optimization.

**Dependencies:**
- External: bull (Redis-based queues), zod (validation schemas), pg (PostgreSQL driver), openai SDK
- Internal: Supabase database schema, existing ML services, user authentication system, comic generation pipeline

**Risks:**
- Data quality degradation: Implement validation rules and expert review queues for high-impact corrections
- Training data bias: Use stratified sampling and bias detection algorithms to maintain dataset balance  
- Storage costs explosion: Implement data retention policies and compress/archive old feedback after model retraining
- User privacy concerns: Anonymize feedback data and provide opt-out mechanisms with clear consent flows

**Complexity Notes:**
More complex than initially expected due to the multi-modal nature (text + images), need for data lineage tracking, and integration with multiple ML models. The feedback loop affects both text generation (LLMs) and image generation (Stable Diffusion), requiring different training approaches for each modality.

**Key Files:**
- packages/database/schemas/feedback.sql: Create feedback tables and indexes
- apps/api/src/services/feedback-collector.ts: Core feedback collection service
- apps/api/src/workers/training-data-processor.ts: Background job for processing corrections
- packages/ml-training/src/active-learning/feedback-processor.ts: ML-specific feedback processing


### Design Decisions

[{'decision': 'Use PostgreSQL JSON columns for flexible feedback storage', 'rationale': 'Allows schema evolution as we discover new feedback types without migrations', 'alternatives_considered': ['Separate tables per feedback type', 'MongoDB for document storage']}, {'decision': 'Implement asynchronous processing with Redis/Bull queues', 'rationale': 'Prevents blocking user interactions while ensuring reliable processing', 'alternatives_considered': ['Synchronous processing', 'Database-only job queue', 'AWS SQS']}, {'decision': 'Create separate feedback pipelines for text and image corrections', 'rationale': 'Different ML models require different training data formats and validation', 'alternatives_considered': ['Single unified feedback pipeline', 'Model-agnostic feedback system']}]
