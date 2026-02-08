---
area: comic
dependsOn: []
effort: 5
iteration: I5
key: T63
milestone: M5 - Product Assembly
priority: p0
title: Comic Layout & Composition
type: Feature
---

# Comic Layout & Composition

## Acceptance Criteria

- [ ] **System automatically generates comic panel layouts from novel text with at least 3 different layout templates (splash, grid, dynamic)**
  - Verification: POST /api/comics/{id}/generate-layout returns layout JSON with panels array, coordinates, and template type
- [ ] **Interactive layout editor allows drag-and-drop panel repositioning with real-time canvas updates**
  - Verification: Manual test: drag panels in LayoutEditor component, verify position updates persist in database
- [ ] **Layout engine handles speech bubble positioning without overlap and maintains reading flow (left-to-right, top-to-bottom)**
  - Verification: Unit test verifies bubble collision detection returns false for generated layouts, manual test confirms reading order
- [ ] **System renders high-resolution comic pages (300 DPI) within 10 seconds for pages with up to 8 panels**
  - Verification: Integration test measures rendering time with performance.now(), load test with various panel counts
- [ ] **Generated layouts are responsive and maintain aspect ratios across different output formats (web, print, mobile)**
  - Verification: Visual regression tests compare layout outputs at 16:9, 4:3, and mobile aspect ratios

## Technical Notes

### Approach

Build a hybrid layout system combining algorithmic panel arrangement with interactive editing. The layout engine analyzes scene content to suggest optimal panel sizes and arrangements, then renders using Fabric.js canvas for real-time manipulation. Implement a template library with common comic layouts (splash pages, action sequences, dialogue scenes) that can be automatically selected based on content analysis. Store layout metadata in Supabase with versioning support for iterative editing.


### Files to Modify

- **path**: apps/api/src/routes/comics.ts
- **changes**: Add POST /:id/layout endpoint for layout generation and PUT /:id/layout for updates
- **path**: apps/dashboard/src/pages/ComicEditor.tsx
- **changes**: Integrate LayoutEditor component, add layout tab to editor interface
- **path**: packages/shared/src/types/comic.ts
- **changes**: Add ComicLayout interface and PanelConfiguration types
- **path**: apps/api/src/services/comic-generation.ts
- **changes**: Integrate layout engine into comic generation pipeline

### New Files to Create

- **path**: apps/api/src/services/layout-engine.ts
- **purpose**: Core layout algorithm implementation with template system
- **path**: apps/api/src/services/canvas-renderer.ts
- **purpose**: Server-side canvas rendering for PDF generation using node-canvas
- **path**: apps/api/src/models/comic-layout.ts
- **purpose**: Supabase schema and queries for layout persistence
- **path**: apps/dashboard/src/components/comic/LayoutEditor.tsx
- **purpose**: Interactive Fabric.js-based layout editing interface
- **path**: apps/dashboard/src/components/comic/PanelToolbar.tsx
- **purpose**: Panel manipulation tools (resize, delete, style)
- **path**: apps/dashboard/src/components/comic/LayoutTemplates.tsx
- **purpose**: Template gallery and selection interface
- **path**: apps/api/src/utils/layout-algorithms.ts
- **purpose**: Panel arrangement algorithms (grid, dynamic, artistic)
- **path**: apps/api/src/utils/speech-bubble-positioning.ts
- **purpose**: Collision detection and optimal positioning for speech bubbles
- **path**: packages/shared/src/types/layout.ts
- **purpose**: Shared TypeScript interfaces for layout data structures
- **path**: apps/dashboard/src/hooks/useLayoutEditor.ts
- **purpose**: Custom hook for managing layout editor state and canvas operations
- **path**: apps/api/src/services/pdf-export.ts
- **purpose**: PDF generation service integrating layouts with pdf-lib

### External Dependencies


- **fabric** ^5.3.0

  - Canvas manipulation and interactive editing capabilities

- **pdf-lib** ^1.17.1

  - High-quality PDF generation for final comic output

- **sharp** ^0.33.0

  - Image processing and optimization for panel composition

- **@types/fabric** ^5.3.0

  - TypeScript definitions for Fabric.js

## Testing

### Unit Tests

- **File**: `apps/api/src/__tests__/services/layout-engine.test.ts`
  - Scenarios: Panel arrangement algorithms, Speech bubble collision detection, Template selection logic, Layout validation, Error handling for invalid scene data
- **File**: `apps/dashboard/src/__tests__/components/LayoutEditor.test.tsx`
  - Scenarios: Canvas initialization, Panel drag and drop, Template switching, Save/load functionality
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/comic-layout.test.ts`
  - Scenarios: Full layout generation from text to rendered page, Database persistence of layout changes, Integration with image generation service, PDF export with layouts
- **File**: `apps/dashboard/src/__tests__/integration/layout-editor.test.tsx`
  - Scenarios: Real-time collaboration on layout editing, Undo/redo functionality, Template library integration
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

- **task**: Set up Fabric.js and canvas infrastructure in dashboard
- **done**: False
- **task**: Implement core layout algorithms and template system
- **done**: False
- **task**: Create Supabase schema for layout persistence
- **done**: False
- **task**: Build interactive LayoutEditor component with drag-drop
- **done**: False
- **task**: Implement speech bubble collision detection and positioning
- **done**: False
- **task**: Integrate layout engine with existing image generation pipeline
- **done**: False
- **task**: Add server-side rendering for PDF export
- **done**: False
- **task**: Create layout template library with 5+ templates
- **done**: False
- **task**: Implement real-time collaboration features for layout editing
- **done**: False
- **task**: Performance optimization and memory management
- **done**: False
- **task**: Comprehensive testing and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task handles the automated creation of comic panel layouts and visual composition from novel text. It's the bridge between narrative content and visual storytelling, determining how scenes are arranged into panels, speech bubbles are positioned, and visual elements are composed. This is critical for Morpheus as it transforms linear text into the spatial, visual medium of comics. Without proper layout composition, generated comic pages would lack professional polish and readability.

**Technical Approach:**
Implement a rule-based layout engine with ML enhancement using canvas-based rendering. Use Fabric.js or Konva.js for interactive canvas manipulation, combined with layout algorithms that consider panel hierarchy, reading flow, and visual balance. Integrate with the existing image generation pipeline to compose final pages. Store layout templates and rules in PostgreSQL, with real-time preview capabilities for the dashboard.

**Dependencies:**
- External: fabric.js/konva.js (canvas manipulation), pdf-lib (PDF generation), sharp (image processing), layout algorithms library
- Internal: Image generation service, scene analysis from text processing, character positioning system, speech bubble generation

**Risks:**
- Performance degradation: Complex layouts with many panels could slow rendering - mitigate with canvas virtualization and progressive loading
- Layout quality inconsistency: Automated layouts may lack artistic coherence - implement template-based systems with manual override capabilities  
- Memory consumption: High-resolution comic pages consume significant memory - implement streaming and chunked processing
- Cross-device compatibility: Canvas rendering differs across browsers - extensive testing and fallback strategies needed

**Complexity Notes:**
This is significantly more complex than initially estimated. Comic layout involves sophisticated spatial reasoning, aesthetic considerations, and integration with multiple ML services. The combination of automated layout generation with user customization options adds substantial complexity to the UI/UX layer.

**Key Files:**
- apps/api/src/services/layout-engine.ts: Core layout algorithm implementation
- apps/dashboard/src/components/comic/LayoutEditor.tsx: Interactive layout editing interface
- apps/api/src/models/comic-layout.ts: Database schema for layout data
- packages/shared/src/types/layout.ts: Shared layout type definitions


### Design Decisions

[{'decision': 'Use rule-based layout engine with template system rather than pure ML generation', 'rationale': 'Provides predictable, customizable results while maintaining artistic quality. ML layout generation is still experimental and hard to control.', 'alternatives_considered': ['Pure ML layout generation', 'Manual layout only', 'Grid-based rigid layouts']}, {'decision': 'Implement canvas-based editor with Fabric.js for real-time layout manipulation', 'rationale': 'Provides professional-grade editing capabilities with good performance. Fabric.js has extensive comic/graphic design community support.', 'alternatives_considered': ['SVG-based editor', 'CSS Grid layouts', 'Custom WebGL solution']}]
