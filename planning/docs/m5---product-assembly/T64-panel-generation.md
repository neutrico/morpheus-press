---
area: comic
dependsOn:
- T62
- T63
effort: 5
iteration: I5
key: T64
milestone: M5 - Product Assembly
priority: p0
title: Panel Generation
type: Feature
---

# Panel Generation

## Acceptance Criteria

- [ ] **Panel generation creates individual comic panels from scene data with proper layout, character placement, and speech bubbles**
  - Verification: POST /api/panels/generate with scene data returns panel with canvas data, character positions, and dialogue elements
- [ ] **Interactive panel editor allows real-time editing of panel elements with drag-and-drop repositioning**
  - Verification: Load PanelEditor component, drag character/bubble elements, verify position updates persist and render correctly
- [ ] **System supports multiple panel layout templates (1-panel, 2-panel horizontal, 3-panel grid) with automatic sizing**
  - Verification: Generate panels using different layout templates, verify dimensions follow template constraints and maintain aspect ratios
- [ ] **Batch panel generation processes full comic scenes with progress tracking and error handling**
  - Verification: POST /api/panels/batch-generate with multiple scenes, verify job queue processing, progress updates, and fallback handling
- [ ] **Canvas rendering performance handles 20+ panels without memory issues using virtualization**
  - Verification: Load comic with 25+ panels, verify smooth scrolling, memory usage <500MB, lazy loading of off-screen panels

## Technical Notes

### Approach

Implement a three-tier panel generation system: (1) Layout Engine calculates panel dimensions and positions based on narrative pacing and content analysis, (2) Asset Pipeline coordinates with RunPod Stable Diffusion to generate panel imagery with proper aspect ratios and compositions, (3) Composition Engine uses Fabric.js to combine generated images, speech bubbles, and effects into final panel canvases. The system supports both automated batch generation for full comics and interactive single-panel editing through a React-based visual editor with real-time preview capabilities.


### Files to Modify

- **path**: apps/dashboard/src/components/ComicEditor.tsx
- **changes**: Add PanelEditor integration and panel navigation
- **path**: apps/backend/src/services/ImageGenerationService.ts
- **changes**: Add panel-specific image generation with aspect ratio constraints
- **path**: packages/shared/src/types/Comic.ts
- **changes**: Add Panel[] property and panel relationship types

### New Files to Create

- **path**: apps/dashboard/src/components/PanelEditor.tsx
- **purpose**: Main React component for interactive panel editing with Fabric.js canvas
- **path**: apps/dashboard/src/services/panelGeneration.ts
- **purpose**: Client-side panel rendering, canvas management, and API integration
- **path**: apps/backend/src/services/PanelService.ts
- **purpose**: Server-side panel CRUD, batch processing, and job queue management
- **path**: packages/shared/src/types/Panel.ts
- **purpose**: TypeScript interfaces for panel data, layout templates, and canvas elements
- **path**: apps/backend/src/routes/panels.ts
- **purpose**: REST endpoints for panel operations (/generate, /batch-generate, CRUD)
- **path**: packages/shared/src/services/LayoutEngine.ts
- **purpose**: Panel layout algorithms, template definitions, and sizing calculations
- **path**: apps/dashboard/src/components/PanelTemplateSelector.tsx
- **purpose**: UI component for selecting and previewing panel layout templates
- **path**: apps/backend/src/jobs/PanelGenerationJob.ts
- **purpose**: Background job handler for batch panel generation with progress tracking
- **path**: apps/dashboard/src/hooks/usePanelEditor.ts
- **purpose**: React hook for panel editor state management and canvas operations
- **path**: packages/shared/src/utils/canvasUtils.ts
- **purpose**: Utility functions for canvas operations, image processing, and export

### External Dependencies


- **fabric** ^5.3.0

  - Canvas manipulation library for interactive panel editing and composition

- **sharp** ^0.32.0

  - High-performance image processing for panel image optimization and format conversion

- **pdf-lib** ^1.17.0

  - Generate PDF exports of completed comic panels for print/distribution

- **react-dnd** ^16.0.1

  - Drag and drop functionality for panel reordering and element positioning

- **bull** ^4.12.0

  - Job queue management for async panel generation workflows

## Testing

### Unit Tests

- **File**: `packages/shared/src/services/__tests__/LayoutEngine.test.ts`
  - Scenarios: Panel dimension calculations for different templates, Constraint validation for panel positioning, Aspect ratio maintenance, Edge cases with invalid dimensions
- **File**: `apps/backend/src/services/__tests__/PanelService.test.ts`
  - Scenarios: Panel CRUD operations, Batch generation job creation, Error handling for invalid scene data, Image generation API integration
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/panel-generation.test.ts`
  - Scenarios: Full panel generation pipeline from scene to canvas, RunPod Stable Diffusion integration with fallback, Panel data persistence in Supabase
- **File**: `apps/dashboard/src/__tests__/integration/PanelEditor.test.ts`
  - Scenarios: Panel editor component with fabric.js canvas, Real-time updates and persistence, Drag-and-drop functionality
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2.5
- **Documentation**: 1
- **Total**: 13

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Fabric.js dependencies and Canvas API integration
- **done**: False
- **task**: Implement LayoutEngine with panel templates and sizing algorithms
- **done**: False
- **task**: Create Panel data models and TypeScript interfaces
- **done**: False
- **task**: Build PanelService with CRUD operations and RunPod integration
- **done**: False
- **task**: Develop PanelEditor React component with drag-and-drop functionality
- **done**: False
- **task**: Implement batch generation with job queue and progress tracking
- **done**: False
- **task**: Add panel virtualization for performance optimization
- **done**: False
- **task**: Create comprehensive test suite with Canvas testing utilities
- **done**: False
- **task**: Integrate panel editor into main comic creation workflow
- **done**: False
- **task**: Performance testing and cross-browser compatibility validation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Panel Generation is the core visual output of the Morpheus platform - transforming structured narrative content (scenes, dialogue, descriptions) into individual comic book panels with appropriate layouts, compositions, and visual elements. This is essential for the M5 Product Assembly milestone as it creates the final visual comic product from the processed novel content. Without proper panel generation, users cannot see their transformed comics, making this a critical p0 feature.

**Technical Approach:**
- Use Canvas API or Fabric.js for client-side panel composition and layout
- Implement panel templates system with predefined layouts (single panel, 2-panel horizontal, 3-panel grid, etc.)
- Create panel sizing algorithms based on narrative importance and pacing
- Integrate with Stable Diffusion API (RunPod) for background/character image generation
- Use React-based panel editor component for real-time preview
- Implement server-side panel data persistence in Supabase
- Create FastAPI endpoints for panel CRUD operations and batch generation

**Dependencies:**
- External: fabric.js, canvas, sharp (image processing), pdf-lib (export), react-dnd (drag/drop)
- Internal: Scene analysis service, Character tracking, Image generation pipeline, Comic layout engine

**Risks:**
- Canvas performance: Large comics with many panels could cause browser memory issues
  Mitigation: Implement virtual scrolling and lazy loading for panel rendering
- Image generation latency: Stable Diffusion calls may timeout for complex panels  
  Mitigation: Implement async job queue with progress tracking and fallback images
- Layout complexity: Dynamic panel sizing could create inconsistent visual flow
  Mitigation: Create constraint-based layout system with predefined templates
- Cross-browser compatibility: Canvas rendering differs between browsers
  Mitigation: Use Fabric.js abstraction layer and extensive cross-browser testing

**Complexity Notes:**
This is significantly more complex than initially estimated. Panel generation involves multiple AI services coordination, complex visual layout algorithms, real-time rendering performance, and sophisticated user interaction patterns. The visual quality requirements and performance constraints make this a high-complexity feature requiring careful architecture planning.

**Key Files:**
- apps/dashboard/src/components/PanelEditor.tsx: Main panel editing interface
- apps/dashboard/src/services/panelGeneration.ts: Client-side panel logic  
- apps/backend/src/services/PanelService.ts: Server-side panel operations
- packages/shared/src/types/Panel.ts: Panel data structures
- apps/backend/src/routes/panels.ts: Panel API endpoints
- packages/shared/src/services/LayoutEngine.ts: Panel layout algorithms


### Design Decisions

[{'decision': 'Use Fabric.js for canvas-based panel composition', 'rationale': 'Provides high-level canvas abstraction with built-in drag/drop, object manipulation, and serialization capabilities essential for interactive panel editing', 'alternatives_considered': ['Raw Canvas API (too low-level)', 'Konva.js (React-specific but less mature)', 'SVG-based approach (performance limitations)']}, {'decision': 'Implement template-based panel layouts with constraint solver', 'rationale': 'Balances creative flexibility with visual consistency, allows non-designers to create professional layouts while enabling customization', 'alternatives_considered': ['Fully manual layout (too complex for users)', 'Fixed grid system (too restrictive)', 'AI-generated layouts (too unpredictable)']}, {'decision': 'Use job queue for async panel generation with WebSocket progress updates', 'rationale': 'Panel generation involves multiple AI API calls that can take 30+ seconds, requiring non-blocking UX with real-time progress feedback', 'alternatives_considered': ['Synchronous generation (poor UX)', 'Polling-based progress (inefficient)', 'Client-side generation (limited by browser resources)']}]
