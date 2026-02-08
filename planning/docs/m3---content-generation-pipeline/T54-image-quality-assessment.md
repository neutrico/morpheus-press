---
area: image-gen
dependsOn:
- T52
effort: 3
iteration: I4
key: T54
milestone: M3 - Content Generation Pipeline
priority: p0
title: Image Quality Assessment
type: Feature
---

# Image Quality Assessment

## Acceptance Criteria

- [ ] **Generated images receive quality scores (0-100) across technical, semantic, and comic-specific dimensions within 5 seconds**
  - Verification: POST /api/images/generate returns quality_score object with technical_score, semantic_score, comic_score, and overall_score fields
- [ ] **Images below configurable quality threshold (default 70) trigger automatic regeneration up to 3 attempts**
  - Verification: Monitor generation logs showing retry attempts and verify final image meets threshold or returns error after max retries
- [ ] **Quality assessment pipeline processes images asynchronously without blocking generation response**
  - Verification: Generation endpoint returns immediately with job_id, quality scores delivered via WebSocket within 5s
- [ ] **System stores quality metadata for analytics and provides quality trend dashboard**
  - Verification: Database contains image_quality_scores table with all metrics, admin dashboard shows quality trends over time
- [ ] **Manual quality override allows users to accept/reject images regardless of automatic scoring**
  - Verification: PUT /api/images/{id}/quality-override endpoint allows quality_approved boolean override with user feedback

## Technical Notes

### Approach

Implement a quality assessment service that processes generated images through multiple evaluation stages: technical metrics (sharpness, resolution, artifacts) using Sharp.js, followed by AI-powered semantic assessment via OpenAI Vision API. Quality scores are stored with configurable thresholds triggering automatic regeneration or user notification. The service integrates asynchronously with the existing RunPod Stable Diffusion pipeline, using Redis for job queuing and WebSocket connections for real-time quality updates to the frontend dashboard.


### Files to Modify

- **path**: apps/backend/src/routes/images/generate.ts
- **changes**: Add async quality assessment job creation, WebSocket integration for score delivery
- **path**: apps/backend/src/services/image-generation-service.ts
- **changes**: Integrate quality assessment callback, implement retry logic for failed quality checks
- **path**: apps/backend/src/lib/redis-client.ts
- **changes**: Add quality assessment job queue configuration and processors
- **path**: apps/frontend/src/components/ImagePanel.tsx
- **changes**: Display quality scores, manual override controls, loading states for assessment
- **path**: packages/database/src/schema.prisma
- **changes**: Add ImageQualityScore model with technical/semantic/comic score fields

### New Files to Create

- **path**: apps/backend/src/services/image-quality-service.ts
- **purpose**: Core quality assessment orchestration, score aggregation, threshold evaluation
- **path**: apps/backend/src/lib/image-processing.ts
- **purpose**: Technical quality metrics using Sharp.js - sharpness, noise, resolution analysis
- **path**: apps/backend/src/lib/openai-vision-client.ts
- **purpose**: OpenAI Vision API wrapper for semantic and comic-specific quality assessment
- **path**: packages/shared/src/types/image-quality.ts
- **purpose**: TypeScript interfaces for quality scores, assessment requests, and responses
- **path**: apps/backend/src/routes/images/quality.ts
- **purpose**: Quality override endpoints, manual assessment triggers, quality analytics
- **path**: apps/backend/src/jobs/quality-assessment.ts
- **purpose**: Background job processor for async quality assessment with Redis Bull
- **path**: packages/database/migrations/20241201_add_image_quality_scores.sql
- **purpose**: Database schema for quality scores, user overrides, and assessment metadata
- **path**: apps/frontend/src/components/QualityDashboard.tsx
- **purpose**: Admin dashboard for quality trends, threshold configuration, override management

### External Dependencies


- **sharp** ^0.32.0

  - High-performance image processing for technical quality metrics (sharpness, noise, resolution analysis)

- **canvas** ^2.11.0

  - Advanced image analysis capabilities for composition and visual balance assessment

- **openai** ^4.0.0

  - GPT-4 Vision API integration for semantic quality assessment of comic art style and composition

- **image-ssim** ^0.2.0

  - Structural similarity metrics for comparing generated images against reference quality standards

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/image-quality-service.test.ts`
  - Scenarios: Technical quality metrics calculation, OpenAI Vision API integration with mocked responses, Quality threshold evaluation logic, Score aggregation and weighting, Error handling for API failures
- **File**: `apps/backend/src/__tests__/lib/image-processing.test.ts`
  - Scenarios: Sharpness detection algorithms, Noise level analysis, Resolution validation, Artifact detection
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/image-quality-pipeline.test.ts`
  - Scenarios: End-to-end quality assessment with real image files, Integration with Redis job queue, WebSocket quality score delivery, Database quality score persistence, Automatic regeneration trigger flow
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 8.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup database migration for image quality scores table
- **done**: False
- **task**: Implement technical quality metrics with Sharp.js (sharpness, noise, resolution)
- **done**: False
- **task**: Create OpenAI Vision API client for semantic quality assessment
- **done**: False
- **task**: Build core ImageQualityService with score aggregation and threshold logic
- **done**: False
- **task**: Integrate async quality assessment job processing with Redis Bull
- **done**: False
- **task**: Modify image generation pipeline to trigger quality assessment
- **done**: False
- **task**: Add WebSocket delivery for real-time quality score updates
- **done**: False
- **task**: Implement manual quality override API endpoints
- **done**: False
- **task**: Create frontend components for quality display and override controls
- **done**: False
- **task**: Build admin quality dashboard with analytics and threshold configuration
- **done**: False
- **task**: Add comprehensive error handling and retry logic for API failures
- **done**: False
- **task**: Performance optimization and caching for repeated assessments
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Image Quality Assessment (IQA) is critical for Morpheus's content generation pipeline to ensure generated comic panels meet publication standards. This addresses two key problems: 1) Stable Diffusion models can produce inconsistent quality outputs requiring filtering, and 2) Users need confidence that generated images are suitable for their comic projects. This prevents poor-quality images from reaching the final comic, reducing manual review time and improving user satisfaction.

**Technical Approach:**
Implement a multi-tier assessment system combining:
- Technical metrics (resolution, sharpness, noise levels) using image processing libraries
- AI-powered quality scoring via OpenAI Vision API for semantic quality assessment
- Domain-specific comic art validation (character consistency, panel composition)
- Configurable quality thresholds per generation request
- Real-time scoring during image generation with automatic retry logic
- Quality metadata storage for analytics and model improvement

**Dependencies:**
- External: sharp (image processing), @tensorflow/tfjs-node (optional ML models), openai (GPT-4 Vision), canvas (image analysis)
- Internal: image-generation service, database schemas for quality scores, job queue system, notification service

**Risks:**
- Performance bottleneck: IQA could significantly slow generation pipeline - mitigate with async processing and caching
- Subjective quality metrics: Comic art quality is subjective - mitigate with configurable scoring weights and user feedback loops  
- API costs: Vision API calls for every image - mitigate with local models for basic checks, Vision API for final validation
- False positives/negatives: Over-filtering good images or passing poor ones - mitigate with A/B testing and manual override options

**Complexity Notes:**
More complex than initially estimated due to the subjective nature of comic art quality. Requires balancing multiple quality dimensions (technical, artistic, narrative consistency) and building feedback mechanisms for continuous improvement. The integration with existing generation pipeline adds complexity around error handling and retry logic.

**Key Files:**
- apps/backend/src/services/image-quality-service.ts: Core IQA implementation
- apps/backend/src/lib/image-processing.ts: Technical quality metrics
- packages/shared/src/types/image-quality.ts: Quality score interfaces
- apps/backend/src/routes/images/generate.ts: Integration with generation endpoint
- packages/database/migrations/: Quality scores table schema


### Design Decisions

[{'decision': 'Hybrid local + cloud quality assessment', 'rationale': 'Balance between speed/cost (local technical metrics) and accuracy (cloud AI for semantic quality)', 'alternatives_considered': ['Purely local assessment', 'Purely cloud-based assessment', 'Third-party IQA services']}, {'decision': 'Configurable quality thresholds per user/project', 'rationale': 'Different comic styles and user requirements need different quality standards', 'alternatives_considered': ['Global quality thresholds', 'Model-based adaptive thresholds']}, {'decision': 'Async quality assessment with webhook notifications', 'rationale': 'Prevents blocking the generation pipeline while allowing real-time user updates', 'alternatives_considered': ['Synchronous assessment', 'Polling-based status checks']}]
