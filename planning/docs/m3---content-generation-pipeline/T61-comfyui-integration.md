---
area: comic
dependsOn:
- T52
effort: 5
iteration: I5
key: T61
milestone: M3 - Content Generation Pipeline
priority: p0
title: ComfyUI Integration
type: Task
---

# ComfyUI Integration

## Acceptance Criteria

- [ ] **ComfyUI service successfully generates comic panels using predefined workflow templates**
  - Verification: POST /api/comic/generate-panel with character and scene prompts returns generated image URL within 30 seconds
- [ ] **WebSocket connection provides real-time progress updates during image generation**
  - Verification: Connect to WS endpoint and verify progress events (queued, processing, completed) are received during generation
- [ ] **Workflow templates support dynamic parameter injection for characters, styles, and prompts**
  - Verification: Generate same character with different poses using character template - verify consistency and pose variation
- [ ] **Queue system processes multiple comic generation requests without memory leaks**
  - Verification: Submit 10 concurrent panel generation requests, monitor GPU memory usage remains stable
- [ ] **Fallback mechanism activates when ComfyUI service is unavailable**
  - Verification: Stop ComfyUI server, attempt generation - verify graceful fallback to existing SD API with appropriate error logging

## Technical Notes

### Approach

Implement a ComfyUI service that manages workflow templates for comic generation tasks. Create a WebSocket-based communication layer for real-time progress tracking. Build workflow builders that inject dynamic parameters (prompts, styles, characters) into predefined templates. Integrate with the existing comic generation pipeline through a queue system that processes panels, characters, and backgrounds using appropriate ComfyUI workflows.


### Files to Modify

- **path**: apps/backend/src/services/comic-generation/comic-generator.ts
- **changes**: Add ComfyUI integration option, modify generatePanel method to use ComfyUI workflows
- **path**: apps/backend/src/services/image-processing/image-service.ts
- **changes**: Add ComfyUI result processing, integrate with existing post-processing pipeline
- **path**: apps/backend/src/routes/comic.ts
- **changes**: Add ComfyUI-specific endpoints for workflow management and progress tracking
- **path**: apps/backend/src/config/index.ts
- **changes**: Add ComfyUI configuration section with server URL, API keys, timeouts
- **path**: packages/shared/src/types/comic.ts
- **changes**: Add ComfyUI workflow types and generation request interfaces

### New Files to Create

- **path**: apps/backend/src/services/comfyui/client.ts
- **purpose**: Core ComfyUI API client with WebSocket and HTTP communication
- **path**: apps/backend/src/services/comfyui/workflow-builder.ts
- **purpose**: Dynamic workflow template builder with parameter injection
- **path**: apps/backend/src/services/comfyui/template-manager.ts
- **purpose**: Workflow template storage, versioning, and retrieval system
- **path**: apps/backend/src/services/comfyui/queue-manager.ts
- **purpose**: Queue management for batch processing and resource optimization
- **path**: apps/backend/src/services/comfyui/index.ts
- **purpose**: Main ComfyUI service orchestrator and public interface
- **path**: packages/shared/src/types/comfyui.ts
- **purpose**: TypeScript definitions for ComfyUI workflows, nodes, and API responses
- **path**: apps/backend/src/config/comfyui.ts
- **purpose**: ComfyUI-specific configuration management and validation
- **path**: apps/backend/src/services/comfyui/templates/character-sheet.json
- **purpose**: Character generation workflow template
- **path**: apps/backend/src/services/comfyui/templates/panel-generation.json
- **purpose**: Comic panel generation workflow template
- **path**: apps/backend/src/services/comfyui/templates/background.json
- **purpose**: Background generation workflow template
- **path**: apps/backend/src/middleware/comfyui-auth.ts
- **purpose**: ComfyUI API authentication and rate limiting middleware

### External Dependencies


- **ws** ^8.14.2

  - WebSocket client for ComfyUI API communication

- **form-data** ^4.0.0

  - Multipart form data for image uploads to ComfyUI

- **sharp** ^0.32.6

  - Image processing and format conversion

- **ioredis** ^5.3.2

  - Redis client for job queue and workflow caching

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/comfyui/workflow-builder.test.ts`
  - Scenarios: Template parameter injection, Workflow validation, Invalid parameter handling
- **File**: `apps/backend/src/__tests__/services/comfyui/client.test.ts`
  - Scenarios: WebSocket connection management, API request/response handling, Error recovery mechanisms
- **File**: `apps/backend/src/__tests__/services/comfyui/queue-manager.test.ts`
  - Scenarios: Queue prioritization, Batch processing, Resource cleanup
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/comfyui-comic-pipeline.test.ts`
  - Scenarios: End-to-end panel generation workflow, Character consistency across panels, Queue integration with comic generation service
- **File**: `apps/backend/src/__tests__/integration/comfyui-websocket.test.ts`
  - Scenarios: Real-time progress tracking, Connection recovery on failures
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

- **task**: Set up ComfyUI development environment and API exploration
- **done**: False
- **task**: Create core ComfyUI client with WebSocket and HTTP API integration
- **done**: False
- **task**: Implement workflow template system with parameter injection
- **done**: False
- **task**: Build queue manager for batch processing and resource management
- **done**: False
- **task**: Create initial workflow templates for characters, panels, and backgrounds
- **done**: False
- **task**: Integrate ComfyUI service with existing comic generation pipeline
- **done**: False
- **task**: Implement WebSocket progress tracking and error handling
- **done**: False
- **task**: Add fallback mechanism to existing Stable Diffusion API
- **done**: False
- **task**: Create comprehensive test suite with mocked ComfyUI responses
- **done**: False
- **task**: Write API documentation and workflow template guides
- **done**: False
- **task**: Performance testing and GPU memory optimization
- **done**: False
- **task**: Code review and security audit
- **done**: False

## Agent Notes

### Research Findings

**Context:**
ComfyUI integration replaces the current RunPod Stable Diffusion setup with ComfyUI, a node-based UI for Stable Diffusion that offers more flexible workflow composition and better control over the image generation pipeline. This is crucial for comic generation as it allows for consistent character generation, style transfer, panel layout control, and advanced prompt engineering through visual workflows. ComfyUI provides better reproducibility and fine-grained control over the generation process compared to basic Stable Diffusion APIs.

**Technical Approach:**
- Create a ComfyUI workflow service that communicates via WebSocket API
- Design workflow templates for different comic generation tasks (character sheets, panels, backgrounds)
- Implement a queue system for batch processing comic pages
- Create workflow builders for dynamic prompt injection and parameter adjustment
- Use ComfyUI's API mode for headless operation in production
- Implement workflow versioning and template management

**Dependencies:**
- External: [@comfyui/api-client, ws, axios, form-data, sharp]
- Internal: existing image processing service, job queue system, comic generation pipeline

**Risks:**
- ComfyUI API stability: Monitor API changes and maintain fallback workflows
- Workflow complexity: Start with simple templates and gradually add complexity
- Resource management: Implement proper GPU memory cleanup and queue throttling
- Workflow persistence: Store workflow definitions in database for consistency

**Complexity Notes:**
More complex than initial estimate due to workflow management requirements and the need to create reusable templates for different comic generation scenarios. The visual nature of ComfyUI workflows requires careful abstraction.

**Key Files:**
- apps/backend/src/services/comfyui/: New service directory
- apps/backend/src/services/comic-generation/: Integration with existing pipeline
- packages/shared/src/types/comfyui.ts: Type definitions
- apps/backend/src/config/comfyui.ts: Configuration management


### Design Decisions

[{'decision': 'Use ComfyUI API mode with WebSocket communication', 'rationale': 'Provides real-time progress updates and better resource management than HTTP polling', 'alternatives_considered': ['HTTP-only API', 'Direct Python integration', 'Docker container per job']}, {'decision': 'Implement workflow template system with parameter injection', 'rationale': 'Allows reusable workflows while maintaining flexibility for different comic styles and requirements', 'alternatives_considered': ['Hardcoded workflows', 'Dynamic workflow generation', 'User-defined workflows']}, {'decision': 'Queue-based processing with job prioritization', 'rationale': 'Handles multiple comic generation requests efficiently and allows for different priority levels', 'alternatives_considered': ['Direct API calls', 'Batch processing only', 'Real-time generation']}]
