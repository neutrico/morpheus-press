---
area: comic
dependsOn:
- T64
effort: 3
iteration: I5
key: T73
milestone: M5 - Product Assembly
priority: p2
title: Variant Generation
type: Feature
---

# Variant Generation

## Acceptance Criteria

- [ ] **Users can generate 2-5 variants of any comic panel with different artistic styles while maintaining consistent layout and character positioning**
  - Verification: Create panel, trigger variant generation with different style prompts, verify ControlNet preserves layout structure via visual comparison
- [ ] **Variant generation jobs are queued and processed asynchronously with real-time status updates to dashboard**
  - Verification: Generate variants for multiple panels simultaneously, verify Redis queue processing and WebSocket status updates in browser dev tools
- [ ] **Generated variants are stored hierarchically with parent-child relationships and accessible via API endpoints**
  - Verification: Query GET /api/variants/{panelId} and verify response includes variant tree structure with original panel as root
- [ ] **Variant explorer UI displays generated variants in comparison grid with selection and ranking capabilities**
  - Verification: Navigate to panel variant view, verify grid layout shows all variants, test selection state persistence and ranking controls
- [ ] **System implements cost controls limiting variants per panel (max 5) and provides generation cost estimates**
  - Verification: Attempt to generate >5 variants, verify rejection with 400 error, check cost estimation API returns RunPod pricing calculations

## Technical Notes

### Approach

Implement a hierarchical variant generation system that extends the existing Stable Diffusion pipeline with ControlNet integration for layout preservation. Create a queue-based architecture using Redis for managing variant generation jobs, with WebSocket real-time updates to the dashboard. Build a tree-structured storage system in Supabase to track variant relationships and implement intelligent preview generation to minimize storage costs. Develop a sophisticated variant explorer UI component that enables easy comparison and selection of generated variants.


### Files to Modify

- **path**: packages/shared/src/types/comic.types.ts
- **changes**: Add VariantNode, VariantGenerationRequest, VariantMetadata interfaces with hierarchical relationship fields
- **path**: apps/api/src/services/panel-generation.service.ts
- **changes**: Integrate variant generation hooks after initial panel creation, add variant cost tracking
- **path**: packages/ml-pipeline/src/stable-diffusion/base-generator.ts
- **changes**: Add ControlNet integration methods and prompt variation utilities

### New Files to Create

- **path**: apps/api/src/services/variant-generation.service.ts
- **purpose**: Core service managing variant generation logic, prompt strategies, and RunPod orchestration
- **path**: apps/api/src/controllers/variants.controller.ts
- **purpose**: REST endpoints for variant CRUD operations and generation triggering
- **path**: apps/api/src/queues/variant-generation.queue.ts
- **purpose**: Redis-based job queue for asynchronous variant processing
- **path**: packages/ml-pipeline/src/stable-diffusion/variant-generator.ts
- **purpose**: Specialized ML pipeline component for variant generation with ControlNet
- **path**: apps/dashboard/src/components/VariantExplorer.tsx
- **purpose**: React component for variant comparison, selection, and management interface
- **path**: apps/api/src/utils/semantic-hash.ts
- **purpose**: Utility for generating content hashes to prevent duplicate variant generation
- **path**: database/migrations/20240115_add_variant_tables.sql
- **purpose**: Database schema for variant relationships and metadata storage

### External Dependencies


- **@runpod/sdk-js** ^1.4.0

  - Extended integration for ControlNet-enabled variant generation endpoints

- **ioredis** ^5.3.0

  - Job queue management for batch variant processing and rate limiting

- **sharp** ^0.33.0

  - Image processing for preview generation, comparison grids, and format optimization

- **react-compare-slider** ^3.1.0

  - Interactive variant comparison UI component for side-by-side evaluation

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/variant-generation.test.ts`
  - Scenarios: Prompt variation strategy generation, Semantic hash collision detection, Cost calculation accuracy, Variant limit enforcement
- **File**: `apps/dashboard/src/components/__tests__/VariantExplorer.test.tsx`
  - Scenarios: Variant grid rendering with mock data, Selection state management, WebSocket connection handling, Loading states during generation
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/variant-workflow.test.ts`
  - Scenarios: End-to-end variant generation from API request to stored result, Redis queue job processing with RunPod integration, Variant relationship storage in Supabase, Cost limit enforcement across multiple requests
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

- **task**: Set up database schema and migrations for variant storage with hierarchical relationships
- **done**: False
- **task**: Implement Redis queue system for variant generation jobs with proper error handling
- **done**: False
- **task**: Integrate ControlNet into existing Stable Diffusion pipeline for layout preservation
- **done**: False
- **task**: Build variant generation service with prompt variation strategies and cost controls
- **done**: False
- **task**: Create REST API endpoints for variant CRUD operations and generation triggering
- **done**: False
- **task**: Implement WebSocket real-time updates for variant generation status
- **done**: False
- **task**: Develop VariantExplorer React component with comparison grid and selection logic
- **done**: False
- **task**: Add semantic hashing system to prevent duplicate variant generation
- **done**: False
- **task**: Integrate variant generation into existing comic assembly pipeline
- **done**: False
- **task**: Implement storage cleanup policies and preview generation optimization
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Variant Generation enables creating multiple visual interpretations of the same comic scene/panel with different artistic styles, character designs, layouts, or visual treatments. This is crucial for allowing creators to explore different creative directions, A/B test visual approaches, and provide customers with customization options. In the novel-to-comic workflow, this comes after initial comic generation but before final assembly, allowing refinement of visual storytelling.

**Technical Approach:**
- Extend existing RunPod Stable Diffusion pipeline with variant generation capabilities
- Implement prompt variation strategies (style modifiers, composition changes, character appearance tweaks)
- Create a queue-based system for batch variant generation to manage computational costs
- Use ControlNet for maintaining consistent layouts while varying artistic elements
- Implement semantic hashing to avoid generating duplicate variants
- Store variants with hierarchical relationships (original -> variant tree) in Supabase
- Create real-time preview system using WebSocket connections for variant generation status

**Dependencies:**
- External: @runpod/sdk-js, ioredis (job queue), sharp (image processing), @supabase/realtime-js
- Internal: existing panel generation service, image storage service, comic assembly pipeline, dashboard variant comparison UI

**Risks:**
- Computational Cost Explosion: Multiple variants per panel could dramatically increase RunPod costs
  Mitigation: Implement variant limits, cost estimation, and user-configurable quality/speed tradeoffs
- Storage Bloat: Variants multiply storage requirements exponentially
  Mitigation: Implement smart cleanup policies, compressed preview generations, lazy full-resolution rendering
- UI Complexity: Comparing/selecting from many variants creates choice paralysis
  Mitigation: Intelligent variant ranking, progressive disclosure, and ML-powered similarity clustering

**Complexity Notes:**
Higher complexity than initially estimated due to the need for sophisticated variant relationship management, cost optimization strategies, and complex UI state management for variant comparison workflows. The technical challenge lies not in generation itself but in making variant exploration intuitive and cost-effective.

**Key Files:**
- apps/api/src/services/variant-generation.service.ts: Core variant generation logic
- packages/shared/src/types/comic.types.ts: Variant relationship type definitions
- apps/dashboard/src/components/VariantExplorer.tsx: Variant comparison interface
- apps/api/src/controllers/variants.controller.ts: Variant CRUD and generation endpoints
- packages/ml-pipeline/src/stable-diffusion/variant-generator.ts: ML pipeline integration


### Design Decisions

[{'decision': 'Tree-based variant storage with parent-child relationships', 'rationale': 'Enables tracking variant genealogy, selective regeneration, and hierarchical organization for complex variant exploration workflows', 'alternatives_considered': ['Flat variant arrays', 'Tag-based variant grouping', 'Session-based variant storage']}, {'decision': 'Queue-based batch processing with WebSocket status updates', 'rationale': 'Balances computational efficiency with user experience, prevents resource overwhelm while providing real-time feedback', 'alternatives_considered': ['Synchronous generation', 'Polling-based status', 'Email notification system']}, {'decision': 'ControlNet integration for layout consistency', 'rationale': 'Maintains panel composition and character positioning while allowing artistic variation, crucial for narrative coherence', 'alternatives_considered': ['Pure prompt variation', 'Image-to-image translation', 'Style transfer approaches']}]
