---
area: comic
dependsOn:
- T64
effort: 3
iteration: I5
key: T70
milestone: M4 - Dashboard & UI
priority: p1
title: Quality Control Dashboard
type: Feature
---

# Quality Control Dashboard

## Acceptance Criteria

- [ ] **QC dashboard displays comics in kanban-style board with states: pending, in-review, approved, rejected**
  - Verification: Navigate to /quality-control, verify board shows 4 columns with comics sorted by status
- [ ] **Reviewers can annotate comic panels and submit approval/rejection with comments**
  - Verification: Click on comic card, add annotations using fabric.js tools, submit review form with status change
- [ ] **Real-time updates show status changes to all connected reviewers within 2 seconds**
  - Verification: Open dashboard in two browsers, change comic status in one, verify other updates automatically
- [ ] **Batch operations allow selecting and approving/rejecting multiple comics simultaneously**
  - Verification: Select 5+ comics using checkboxes, use batch action buttons, verify all selected items update status
- [ ] **Performance handles 100+ comics with lazy loading and maintains <3s initial load time**
  - Verification: Seed database with 100+ comics, measure initial page load with browser dev tools

## Technical Notes

### Approach

Create a dedicated QC section in the dashboard with a kanban-style board showing comics in different review states (pending, in-review, approved, rejected). Build reusable ReviewCard components that display comic panels with overlay annotation tools. Implement real-time status updates using Supabase subscriptions so multiple reviewers see live changes. Add batch operations for efficient processing and integrate approval workflows that trigger comic publication or regeneration requests.


### Files to Modify

- **path**: packages/database/schema.sql
- **changes**: Add qc_status, reviewer_id, review_comments, annotations columns to comics table
- **path**: apps/dashboard/src/app/(protected)/layout.tsx
- **changes**: Add Quality Control navigation item to admin sidebar
- **path**: packages/shared/types/index.ts
- **changes**: Export QC types and extend Comic interface with review fields

### New Files to Create

- **path**: apps/dashboard/src/app/(protected)/quality-control/page.tsx
- **purpose**: Main QC dashboard with kanban board layout
- **path**: apps/dashboard/src/components/qc/KanbanBoard.tsx
- **purpose**: Kanban board component with drag-and-drop functionality
- **path**: apps/dashboard/src/components/qc/ReviewCard.tsx
- **purpose**: Individual comic review card with thumbnail and quick actions
- **path**: apps/dashboard/src/components/qc/ReviewModal.tsx
- **purpose**: Full-screen comic review with annotation tools
- **path**: apps/dashboard/src/components/qc/AnnotationCanvas.tsx
- **purpose**: Fabric.js-based annotation overlay for comic panels
- **path**: apps/dashboard/src/components/qc/BatchActions.tsx
- **purpose**: Batch selection and operations component
- **path**: apps/backend/src/routes/qc/index.ts
- **purpose**: QC API routes for reviews, status updates, batch operations
- **path**: packages/database/migrations/20240315_add_qc_fields.sql
- **purpose**: Database migration for QC-related columns
- **path**: packages/shared/types/qc.ts
- **purpose**: TypeScript interfaces for QC status, reviews, annotations
- **path**: apps/dashboard/src/hooks/useQCSubscription.ts
- **purpose**: Custom hook for real-time QC status updates via Supabase
- **path**: apps/backend/src/services/qc-service.ts
- **purpose**: Business logic for QC operations and workflow management

### External Dependencies


- **fabric** ^5.3.0

  - Canvas-based image annotation for marking quality issues on comic panels

- **@tanstack/react-query** ^5.0.0

  - Efficient data fetching and caching for comic review queue management

- **react-hook-form** ^7.48.0

  - Form handling for review comments, ratings, and approval workflows

- **react-window** ^1.8.8

  - Virtualization for large lists of comics to maintain performance

## Testing

### Unit Tests

- **File**: `apps/dashboard/src/components/qc/__tests__/ReviewCard.test.tsx`
  - Scenarios: Renders comic panels correctly, Annotation tools functionality, Status change handling, Error states display
- **File**: `apps/backend/src/routes/qc/__tests__/qc-routes.test.ts`
  - Scenarios: GET /qc/comics returns paginated results, POST /qc/review creates review with validation, PATCH /qc/batch-update handles multiple comics, Authorization checks for reviewer role
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/qc-workflow.test.ts`
  - Scenarios: Comic submission to approval pipeline, Real-time subscription updates, Batch operations with database consistency
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 8

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Create database migration for QC fields and run migration
- **done**: False
- **task**: Implement TypeScript types and interfaces for QC system
- **done**: False
- **task**: Build QC backend API routes with authentication and validation
- **done**: False
- **task**: Create KanbanBoard component with drag-and-drop using react-beautiful-dnd
- **done**: False
- **task**: Implement ReviewCard component with comic thumbnail and quick actions
- **done**: False
- **task**: Build ReviewModal with fabric.js annotation canvas integration
- **done**: False
- **task**: Add real-time subscription hooks using Supabase realtime
- **done**: False
- **task**: Implement batch operations with optimistic updates
- **done**: False
- **task**: Add performance optimizations: virtualization and lazy loading
- **done**: False
- **task**: Write comprehensive tests and documentation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
A Quality Control Dashboard is essential for the novel-to-comic transformation pipeline to ensure generated comics meet quality standards before publication. This addresses the critical need to catch AI-generated content issues (poor image quality, inconsistent character designs, narrative flow problems, text readability) and provides human reviewers with tools to approve, reject, or request revisions. Without this, low-quality comics could reach users, damaging the platform's reputation and user experience.

**Technical Approach:**
Build a dedicated QC dashboard within the existing Next.js admin interface using React Server Components for performance. Implement a queue-based review system with real-time updates via Supabase realtime subscriptions. Use a card-based layout for comic review with side-by-side comparison views, annotation tools, and batch operations. Integrate with the existing comic generation pipeline by adding QC status fields to the comics table and creating approval workflows.

**Dependencies:**
- External: @tanstack/react-query for state management, react-hook-form for review forms, fabric.js for image annotation, react-virtualized for large lists
- Internal: existing auth system, comic generation services, notification system, user management, Supabase client

**Risks:**
- Bottleneck in review process: implement parallel review workflows and priority queues
- Large image loading performance: add progressive loading, thumbnails, and CDN optimization
- Reviewer fatigue from poor UX: design intuitive interfaces with keyboard shortcuts and batch operations
- Inconsistent quality standards: create detailed review guidelines and training materials

**Complexity Notes:**
More complex than initially expected due to need for real-time collaboration features, image annotation capabilities, and integration with existing comic generation workflow. The challenge lies in building an efficient review interface that handles large volumes of visual content while maintaining good performance.

**Key Files:**
- apps/dashboard/src/app/(protected)/quality-control/page.tsx: main QC dashboard
- apps/dashboard/src/components/qc/ReviewCard.tsx: individual comic review component
- packages/database/migrations/: add QC status and reviewer fields to comics table
- apps/backend/src/routes/qc/: QC API endpoints for reviews and approvals
- packages/shared/types/qc.ts: QC-related TypeScript types


### Design Decisions

[{'decision': 'Queue-based review system with real-time updates', 'rationale': 'Enables multiple reviewers to work efficiently without conflicts, with immediate visibility into review progress', 'alternatives_considered': ['Simple list-based approach', 'Assignment-based system', 'AI-first with human override']}, {'decision': 'In-browser image annotation using Fabric.js', 'rationale': 'Allows reviewers to mark specific issues directly on comic panels without external tools', 'alternatives_considered': ['Comment-only system', 'External annotation tools', 'Simple approve/reject workflow']}, {'decision': 'Integration with existing Supabase realtime for live updates', 'rationale': 'Leverages existing infrastructure for real-time collaboration and status updates', 'alternatives_considered': ['WebSocket implementation', 'Polling-based updates', 'Server-sent events']}]
