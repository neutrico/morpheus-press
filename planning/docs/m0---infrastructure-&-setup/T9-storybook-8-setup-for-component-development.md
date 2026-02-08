---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T9
milestone: M0 - Infrastructure & Setup
priority: p1
title: Storybook 8 Setup for Component Development
type: Task
---

# Storybook 8 Setup for Component Development

## Acceptance Criteria

- [ ] **Storybook 8 workspace runs successfully in monorepo with components from Dashboard and Storefront packages**
  - Verification: Run `cd packages/storybook && npm run storybook` - opens on localhost:6006 with component stories visible
- [ ] **Tailwind CSS styling renders correctly in Storybook stories matching production apps**
  - Verification: Visual comparison between story components and production components shows identical styling
- [ ] **MSW integration provides working API mocks for Morpheus endpoints in stories**
  - Verification: Stories with API calls (novel upload, comic generation) work without real backend - check Network tab shows mocked responses
- [ ] **TypeScript compilation passes with proper type safety across monorepo packages**
  - Verification: Run `turbo build` includes storybook build without TypeScript errors
- [ ] **Chromatic visual regression testing pipeline configured and functional**
  - Verification: Git push triggers Chromatic build - check Chromatic dashboard shows visual diff detection

## Technical Notes

### Approach

Create a dedicated Storybook workspace that imports components from both Dashboard and Storefront packages. Configure Next.js framework adapter with proper TypeScript support and Tailwind CSS integration. Implement MSW for mocking Morpheus API endpoints (novel upload, comic generation) within stories. Setup automated visual testing pipeline with Chromatic and integrate with existing CI/CD workflows.


### Files to Modify

- **path**: turbo.json
- **changes**: Add storybook workspace with build/dev pipeline tasks
- **path**: package.json
- **changes**: Add storybook workspace to workspaces array
- **path**: apps/dashboard/package.json
- **changes**: Update exports field to expose components for Storybook consumption
- **path**: apps/storefront/package.json
- **changes**: Update exports field to expose components for Storybook consumption

### New Files to Create

- **path**: packages/storybook/package.json
- **purpose**: Storybook workspace package configuration with Next.js 16 compatible versions
- **path**: packages/storybook/.storybook/main.ts
- **purpose**: Core Storybook configuration with Next.js adapter and monorepo component resolution
- **path**: packages/storybook/.storybook/preview.ts
- **purpose**: Global decorators for Tailwind CSS, MSW, theme providers
- **path**: packages/storybook/.storybook/middleware.js
- **purpose**: MSW service worker setup for API mocking
- **path**: packages/storybook/src/mocks/handlers.ts
- **purpose**: MSW request handlers for Morpheus API endpoints
- **path**: packages/storybook/src/mocks/data.ts
- **purpose**: Mock data factories for novels, comics, user profiles
- **path**: packages/storybook/stories/dashboard/components.stories.ts
- **purpose**: Dashboard component stories with controls and docs
- **path**: packages/storybook/stories/storefront/components.stories.ts
- **purpose**: Storefront component stories with different variants
- **path**: packages/storybook/stories/shared/design-system.stories.ts
- **purpose**: Design tokens, colors, typography documentation stories
- **path**: packages/storybook/.chromatic.json
- **purpose**: Chromatic configuration for visual regression testing
- **path**: packages/storybook/tsconfig.json
- **purpose**: TypeScript configuration with path mapping to monorepo packages

### External Dependencies


- **@storybook/nextjs** ^8.0.0

  - Next.js 16 framework integration with webpack and routing support

- **@storybook/addon-essentials** ^8.0.0

  - Core addons bundle (docs, controls, actions, viewport)

- **chromatic** ^10.0.0

  - Visual regression testing and review workflows

- **msw** ^2.0.0

  - API mocking for realistic component stories

- **@storybook/addon-a11y** ^8.0.0

  - Accessibility testing for comic reader components

## Testing

### Unit Tests

- **File**: `packages/storybook/src/__tests__/story-utils.test.ts`
  - Scenarios: Story generation utilities, Mock data factories, Component wrapper helpers
### Integration Tests

- **File**: `packages/storybook/src/__tests__/integration/component-loading.test.ts`
  - Scenarios: Components load from Dashboard package, Components load from Storefront package, Shared design tokens resolve correctly, MSW handlers intercept API calls
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 1
- **Total**: 7.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Create Storybook workspace package.json with Next.js 16 compatible dependencies
- **done**: False
- **task**: Configure Storybook main.ts with Next.js adapter and monorepo webpack resolve
- **done**: False
- **task**: Setup Tailwind CSS integration in preview.ts with shared design tokens
- **done**: False
- **task**: Implement MSW integration with Morpheus API endpoint mocks
- **done**: False
- **task**: Configure TypeScript with proper path mapping to Dashboard/Storefront packages
- **done**: False
- **task**: Create initial component stories for key Dashboard and Storefront components
- **done**: False
- **task**: Setup Chromatic account and configure visual regression testing pipeline
- **done**: False
- **task**: Integrate Storybook build/dev tasks into Turbo pipeline
- **done**: False
- **task**: Add accessibility addon and configure a11y testing standards
- **done**: False
- **task**: Create documentation stories for design system tokens and guidelines
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Storybook 8 setup is crucial for the Morpheus project to enable isolated component development, visual testing, and design system documentation across multiple frontend apps (Dashboard + Storefront). Given the comic transformation UI complexity, components need thorough visual testing and documentation. Storybook serves as a living style guide for the design system while enabling faster development cycles through component isolation.

**Technical Approach:**
- Setup Storybook 8 as a separate workspace in the Turborepo monorepo
- Configure to consume components from both Dashboard and Storefront packages
- Integrate with Tailwind CSS for consistent styling
- Setup MSW (Mock Service Worker) for API mocking in stories
- Configure Chromatic for visual regression testing
- Use TypeScript throughout with proper type safety
- Implement automatic story generation for common component patterns
- Setup addon ecosystem: docs, controls, viewport, a11y

**Dependencies:**
- External: @storybook/nextjs, @storybook/addon-essentials, chromatic, msw-storybook-addon, storybook-addon-designs
- Internal: shared UI components from dashboard/storefront packages, design tokens, Tailwind config

**Risks:**
- Build performance: Storybook builds can be slow with large component libraries - use webpack optimization and selective story loading
- Version conflicts: Next.js 16 + Storybook compatibility issues - pin compatible versions and use webpack aliases
- Monorepo complexity: Component resolution across workspaces - configure proper tsconfig paths and webpack resolve
- Maintenance overhead: Stories becoming stale - implement story coverage reports and CI checks

**Complexity Notes:**
Moderate complexity due to monorepo setup and Next.js 16 integration. The multi-app component sharing adds complexity but provides significant value for design consistency across Dashboard/Storefront.

**Key Files:**
- packages/storybook/.storybook/main.ts: Core Storybook configuration
- packages/storybook/.storybook/preview.ts: Global decorators and parameters
- packages/storybook/package.json: Storybook dependencies and scripts
- turbo.json: Add storybook build/dev tasks
- packages/storybook/stories/: Component stories organization


### Design Decisions

[{'decision': 'Use @storybook/nextjs framework adapter', 'rationale': 'Provides best integration with Next.js 16, handles webpack config, image optimization, and routing automatically', 'alternatives_considered': ['@storybook/react-webpack5', 'Custom webpack config', '@storybook/vite']}, {'decision': 'Separate Storybook workspace in monorepo', 'rationale': 'Allows consuming components from multiple apps, centralizes design system documentation, independent deployment', 'alternatives_considered': ['Storybook in each app', 'Single shared stories folder', 'External repository']}, {'decision': 'MSW integration for API mocking', 'rationale': 'Enables realistic component testing with mocked ML/transformation APIs, consistent with likely testing strategy', 'alternatives_considered': ['Static mock data', 'Custom fetch mocking', 'No API integration']}]
