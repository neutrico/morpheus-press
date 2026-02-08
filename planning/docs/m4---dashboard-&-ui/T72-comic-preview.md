---
area: comic
dependsOn:
- T64
effort: 3
iteration: I5
key: T72
milestone: M4 - Dashboard & UI
priority: p1
title: Comic Preview
type: Feature
---

# Comic Preview

## Acceptance Criteria

- [ ] **Comic preview renders with accurate panel layouts, character placements, and dialogue positioning matching user's novel chapter content**
  - Verification: Load test chapter, verify preview shows correct number of panels with character consistency and dialogue placement via visual regression tests
- [ ] **Real-time preview updates within 500ms when users modify generation parameters (style, layout, character designs)**
  - Verification: Performance test measuring time from parameter change to preview update using browser dev tools timeline
- [ ] **Preview system handles long novels (50+ chapters) without memory issues through virtualization**
  - Verification: Load test with 50 chapter novel, monitor memory usage stays under 500MB and scrolling remains smooth at 60fps
- [ ] **Mobile preview mode provides simplified but accurate representation with touch controls for zoom/pan**
  - Verification: Manual testing on mobile devices (iOS Safari, Android Chrome) confirming touch gestures work and performance is acceptable
- [ ] **Preview-to-final generation parity maintains 95% visual consistency**
  - Verification: A/B comparison test between preview and final generated comic pages using image similarity metrics

## Technical Notes

### Approach

Implement a dual-layer preview system: a fast client-side renderer for immediate feedback using cached assets, and a server-side preview generator for higher-fidelity mockups. The client component uses fabric.js canvas for interactive panel editing with drag-drop support. Real-time parameter changes trigger debounced API calls to generate updated preview data. Implement viewport virtualization to handle long comics efficiently, loading panels on-demand as users scroll.


### Files to Modify

- **path**: apps/dashboard/src/pages/comic/[id]/preview.tsx
- **changes**: Add preview page route with layout and navigation
- **path**: apps/dashboard/src/components/comic/ComicEditor.tsx
- **changes**: Integrate preview component and parameter controls
- **path**: apps/api/src/routes/comic/index.ts
- **changes**: Add preview endpoints to existing comic routes
- **path**: packages/database/src/schema/comic.sql
- **changes**: Add preview_settings and preview_cache tables

### New Files to Create

- **path**: apps/dashboard/src/components/comic/ComicPreview.tsx
- **purpose**: Main preview component with canvas rendering and controls
- **path**: apps/dashboard/src/components/comic/PreviewCanvas.tsx
- **purpose**: Canvas-specific rendering logic using fabric.js
- **path**: apps/dashboard/src/components/comic/PreviewControls.tsx
- **purpose**: Parameter controls for real-time preview updates
- **path**: apps/dashboard/src/hooks/useComicPreview.ts
- **purpose**: Preview state management and API integration
- **path**: apps/dashboard/src/hooks/useCanvasInteraction.ts
- **purpose**: Canvas interaction logic for zoom/pan/selection
- **path**: packages/comic-engine/src/preview/PreviewGenerator.ts
- **purpose**: Lightweight preview generation pipeline
- **path**: packages/comic-engine/src/preview/PanelLayoutEngine.ts
- **purpose**: Panel layout calculation for preview
- **path**: packages/comic-engine/src/preview/AssetCache.ts
- **purpose**: Caching system for character designs and backgrounds
- **path**: apps/api/src/routes/comic/preview.ts
- **purpose**: Preview generation and caching API endpoints
- **path**: apps/api/src/services/PreviewService.ts
- **purpose**: Server-side preview generation business logic
- **path**: packages/ui/src/components/Canvas/VirtualizedCanvas.tsx
- **purpose**: Virtualized canvas component for performance
- **path**: packages/ui/src/components/Canvas/CanvasControls.tsx
- **purpose**: Reusable zoom/pan/export controls
- **path**: apps/dashboard/src/utils/previewCache.ts
- **purpose**: Client-side preview caching utilities

### External Dependencies


- **fabric** ^5.3.0

  - Canvas manipulation and interactive editing capabilities

- **react-zoom-pan-pinch** ^3.1.0

  - Smooth zoom and pan controls for comic viewport

- **html2canvas** ^1.4.1

  - Export preview as image for sharing/saving

- **react-window** ^1.8.8

  - Virtualization for performance with long comics

- **use-debounce** ^9.0.4

  - Debounce preview updates to prevent excessive API calls

## Testing

### Unit Tests

- **File**: `apps/dashboard/src/components/comic/__tests__/ComicPreview.test.tsx`
  - Scenarios: Renders empty state correctly, Loads preview data from API, Handles parameter updates, Canvas interaction events, Error states and loading states
- **File**: `apps/dashboard/src/hooks/__tests__/useComicPreview.test.ts`
  - Scenarios: State management for preview data, Debounced API calls, WebSocket connection handling, Cache invalidation logic
- **File**: `packages/comic-engine/src/preview/__tests__/PreviewGenerator.test.ts`
  - Scenarios: Panel layout generation, Character positioning, Dialogue bubble placement, Asset caching and retrieval
### Integration Tests

- **File**: `apps/dashboard/src/__tests__/integration/comic-preview-flow.test.tsx`
  - Scenarios: Complete preview generation flow from chapter upload to rendered preview, Real-time parameter updates through WebSocket, Preview export functionality
- **File**: `apps/api/src/__tests__/integration/preview-api.test.ts`
  - Scenarios: Preview generation API endpoints, Asset caching and retrieval, Concurrent preview requests
### E2E Tests

- **File**: `apps/e2e/tests/comic-preview.spec.ts`
  - Scenarios: User uploads chapter and sees preview, User modifies parameters and sees real-time updates, User navigates through multi-chapter preview, Mobile responsive preview interaction
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

- **task**: Set up database schema for preview caching and settings
- **done**: False
- **task**: Implement server-side preview generation pipeline
- **done**: False
- **task**: Create fabric.js-based canvas preview component
- **done**: False
- **task**: Build real-time parameter update system with WebSockets
- **done**: False
- **task**: Implement viewport virtualization for long comics
- **done**: False
- **task**: Add mobile-optimized preview mode with touch controls
- **done**: False
- **task**: Integrate preview with existing comic editor interface
- **done**: False
- **task**: Implement caching system for preview assets
- **done**: False
- **task**: Add export functionality (PNG/PDF) from preview
- **done**: False
- **task**: Performance optimization and memory management
- **done**: False
- **task**: Comprehensive testing across all components
- **done**: False
- **task**: Documentation and API specification
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Comic Preview allows users to see how their novel chapters will look as comic pages before finalizing the transformation. This is crucial for user confidence and iteration - users need to validate panel layouts, character consistency, dialogue placement, and overall visual flow before committing to expensive generation operations. It reduces wasted generations and improves user satisfaction by making the process more transparent and controllable.

**Technical Approach:**
Build a real-time preview system using React components with canvas/SVG rendering for comic layouts. Implement a lightweight preview generation pipeline that creates low-res mockups using cached character designs and simplified panel structures. Use WebSockets for real-time updates as users modify settings. Leverage Supabase real-time subscriptions for collaborative editing scenarios. Create a responsive preview component that scales from mobile to desktop with zoom/pan capabilities.

**Dependencies:**
- External: fabric.js for canvas manipulation, react-zoom-pan-pinch for viewport control, html2canvas for export functionality, framer-motion for smooth transitions
- Internal: Comic generation service APIs, Character design cache service, Panel layout algorithms, Scene parsing utilities, User preferences service

**Risks:**
- Performance degradation: Large novels could create memory issues with too many preview panels - implement virtualization and lazy loading
- Character consistency: Preview might not match final output due to different generation parameters - maintain strict parity between preview and production pipelines
- Real-time sync complexity: Multiple users editing same comic could cause race conditions - implement operational transforms or conflict resolution
- Mobile performance: Canvas operations are CPU intensive on mobile devices - provide simplified mobile preview mode

**Complexity Notes:**
More complex than initially expected due to need for real-time rendering pipeline that mirrors production quality. The preview system essentially requires building a lightweight version of the entire comic generation stack. Canvas performance optimization and responsive design across devices adds significant complexity.

**Key Files:**
- apps/dashboard/src/components/comic/ComicPreview.tsx: Main preview component
- apps/dashboard/src/hooks/useComicPreview.ts: Preview state management
- packages/comic-engine/src/preview/: Lightweight preview generation pipeline
- apps/api/src/routes/comic/preview.ts: Preview API endpoints
- packages/ui/src/components/Canvas/: Shared canvas utilities


### Design Decisions

[{'decision': 'Canvas-based rendering with fabric.js for interactive preview', 'rationale': 'Provides pixel-perfect control over comic layouts, supports drag-drop editing, and can export high-quality previews. Better performance than DOM-based approaches for complex layouts.', 'alternatives_considered': ['SVG-based rendering', 'HTML/CSS grid layouts', 'WebGL with three.js']}, {'decision': 'Separate preview pipeline from production comic generation', 'rationale': 'Allows optimizations for speed over quality in previews, prevents preview operations from affecting production generation queue, enables different caching strategies.', 'alternatives_considered': ['Reuse production pipeline with quality flags', 'Client-side only preview generation']}, {'decision': 'WebSocket-based real-time updates with Supabase realtime', 'rationale': 'Provides instant feedback as users adjust parameters, supports collaborative editing scenarios, integrates well with existing Supabase infrastructure.', 'alternatives_considered': ['HTTP polling', 'Server-sent events', 'Custom WebSocket implementation']}]
