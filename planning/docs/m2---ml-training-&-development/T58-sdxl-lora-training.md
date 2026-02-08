---
area: ml
dependsOn:
- T52
effort: 8
iteration: I4
key: T58
milestone: M2 - ML Training & Development
priority: p1
title: SDXL LoRA Training
type: Task
---

# SDXL LoRA Training

## Acceptance Criteria

- [ ] **LoRA training pipeline successfully processes datasets and generates model weights**
  - Verification: Upload test dataset via dashboard, trigger training job, verify .safetensors model file generated in Supabase storage
- [ ] **Real-time training progress monitoring displays loss curves and ETA updates**
  - Verification: Start training job and confirm WebSocket updates show loss metrics, current epoch, and estimated completion time in dashboard
- [ ] **Training job cost monitoring prevents GPU overruns with automatic termination**
  - Verification: Set $50 cost limit, start expensive training config, verify job auto-terminates when limit reached
- [ ] **Generated LoRA models integrate with existing SDXL inference pipeline**
  - Verification: Complete training job, load model weights in inference service, generate test images with LoRA applied
- [ ] **Training metadata and model versioning tracked in database**
  - Verification: Query training_jobs and model_versions tables, verify hyperparameters, timestamps, and artifact URLs stored correctly

## Technical Notes

### Approach

Build a comprehensive LoRA training pipeline that integrates with RunPod's GPU infrastructure through a dedicated training service. Implement dataset preprocessing, training job orchestration, and model artifact management as separate microservices. Create a dashboard interface for training configuration, progress monitoring, and model deployment. Use Redis for job queuing and WebSocket connections for real-time training progress updates.


### Files to Modify

- **path**: packages/database/src/schema.sql
- **changes**: Add training_jobs, model_versions, and training_datasets tables
- **path**: packages/ml-service/src/services/inference.ts
- **changes**: Add LoRA model loading and weight merging capabilities
- **path**: apps/dashboard/src/components/ModelLibrary.tsx
- **changes**: Display trained LoRA models with metadata and download options

### New Files to Create

- **path**: packages/ml-service/src/training/lora-trainer.ts
- **purpose**: Core LoRA training orchestration and job management
- **path**: packages/ml-service/src/training/dataset-processor.ts
- **purpose**: Dataset validation, preprocessing, and augmentation
- **path**: packages/ml-service/src/services/runpod-training.ts
- **purpose**: RunPod GPU cluster integration and job submission
- **path**: packages/ml-service/src/training/training-monitor.ts
- **purpose**: Real-time progress tracking and WebSocket updates
- **path**: apps/dashboard/src/pages/training/LoRATraining.tsx
- **purpose**: Training configuration UI with hyperparameter controls
- **path**: apps/dashboard/src/pages/training/TrainingProgress.tsx
- **purpose**: Real-time training monitoring dashboard
- **path**: packages/ml-service/src/training/cost-monitor.ts
- **purpose**: GPU cost tracking and automatic job termination
- **path**: packages/database/migrations/20241201_training_tables.sql
- **purpose**: Database schema for training jobs and model metadata
- **path**: packages/ml-service/src/training/model-validator.ts
- **purpose**: Automated quality assessment of trained models
- **path**: packages/shared/src/types/training.ts
- **purpose**: TypeScript interfaces for training job data structures

### External Dependencies


- **@runpod/sdk** ^1.2.0

  - RunPod API integration for GPU cluster management

- **ioredis** ^5.3.0

  - Redis client for training job queue management

- **@aws-sdk/client-s3** ^3.450.0

  - S3-compatible storage client for model artifacts

- **multer** ^1.4.5

  - File upload handling for training datasets

- **sharp** ^0.33.0

  - Image preprocessing and validation for training data

## Testing

### Unit Tests

- **File**: `packages/ml-service/src/__tests__/lora-trainer.test.ts`
  - Scenarios: Training job creation with valid parameters, Hyperparameter validation and sanitization, Training progress calculation, Error handling for invalid datasets, Cost calculation and monitoring
- **File**: `packages/ml-service/src/__tests__/runpod-training.test.ts`
  - Scenarios: RunPod API integration, Job submission and status polling, GPU instance management, Network error handling
### Integration Tests

- **File**: `packages/ml-service/src/__tests__/integration/lora-pipeline.test.ts`
  - Scenarios: End-to-end training pipeline with mock RunPod, Dataset upload to model deployment flow, Training job failure recovery, WebSocket progress updates
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

- **task**: Design database schema for training jobs and model versioning
- **done**: False
- **task**: Implement RunPod API integration for GPU provisioning
- **done**: False
- **task**: Create dataset preprocessing pipeline with validation
- **done**: False
- **task**: Build core LoRA training orchestration service
- **done**: False
- **task**: Implement real-time progress monitoring with WebSockets
- **done**: False
- **task**: Create training dashboard UI components
- **done**: False
- **task**: Add cost monitoring and automatic job termination
- **done**: False
- **task**: Integrate trained models with existing inference pipeline
- **done**: False
- **task**: Implement model quality validation and artifact cleanup
- **done**: False
- **task**: Write comprehensive tests and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
SDXL LoRA (Low-Rank Adaptation) training enables fine-tuning Stable Diffusion XL models with custom artistic styles, character consistency, and visual themes specific to comic book aesthetics. For Morpheus, this solves the critical problem of generating consistent character appearances and maintaining artistic coherence across comic panels. Instead of relying on generic SDXL outputs, LoRA training allows us to create specialized models that understand specific art styles, character designs, and visual narratives that align with the source novel's themes.

**Technical Approach:**
Implement LoRA training pipeline using RunPod's GPU infrastructure with Kohya-ss/sd-scripts framework. Create a training orchestration service in the backend that manages dataset preparation, training job submission, and model artifact storage. Use Supabase for storing training metadata, progress tracking, and model versioning. Integrate with existing ML pipeline through a dedicated LoRA training API that accepts training datasets, hyperparameters, and returns trained model weights.

**Dependencies:**
- External: kohya-ss/sd-scripts, diffusers>=0.21.0, transformers, torch>=2.0.0, accelerate, xformers
- Internal: ml-service (for RunPod integration), database schemas for training jobs, file storage service for datasets and model weights

**Risks:**
- GPU cost overruns: Implement training time limits and cost monitoring with automatic job termination
- Training instability: Use proven hyperparameter sets and gradient checkpointing to prevent divergence
- Storage bloat: Implement model pruning and automatic cleanup of failed training artifacts
- Quality inconsistency: Establish validation metrics and automated quality assessment before model deployment

**Complexity Notes:**
Higher complexity than initially estimated due to distributed training orchestration, dataset preprocessing pipelines, and integration with existing ML infrastructure. The need for training progress monitoring, automatic failure recovery, and model quality validation adds significant engineering overhead beyond basic LoRA implementation.

**Key Files:**
- packages/ml-service/src/training/lora-trainer.ts: Core training orchestration logic
- packages/ml-service/src/services/runpod-training.ts: RunPod GPU cluster integration
- packages/database/migrations/: Training jobs and model metadata schemas
- apps/dashboard/src/pages/training/: Training management UI components


### Design Decisions

[{'decision': 'Use Kohya-ss framework over custom LoRA implementation', 'rationale': 'Proven stability, extensive hyperparameter optimization, and active community support reduce development risk', 'alternatives_considered': ['Custom PyTorch LoRA implementation', 'HuggingFace PEFT library', 'Diffusers native LoRA training']}, {'decision': 'Implement asynchronous training job queue with Redis', 'rationale': 'Enables concurrent training jobs, proper resource management, and graceful failure handling', 'alternatives_considered': ['Synchronous training API', 'Database-based job queue', 'Celery task queue']}, {'decision': 'Store training datasets in Supabase Storage with metadata in PostgreSQL', 'rationale': 'Leverages existing infrastructure while providing efficient blob storage and relational metadata queries', 'alternatives_considered': ['AWS S3 with RDS', 'Local file system storage', 'Dedicated training data service']}]
