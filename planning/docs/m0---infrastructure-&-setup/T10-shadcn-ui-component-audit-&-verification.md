---
area: setup
dependsOn: []
effort: 2
iteration: I1
key: T10
milestone: M0 - Infrastructure & Setup
priority: p1
title: shadcn/ui Component Audit & Verification
type: Task
---

# shadcn/ui Component Audit & Verification

## Acceptance Criteria

- [ ] **All shadcn/ui components are centralized in @morpheus/ui workspace with consistent theming**
  - Verification: Run 'pnpm build' in packages/ui and verify all exports work, check components.json configs match
- [ ] **Component inventory spreadsheet tracks 100% of UI components used across Dashboard/Storefront**
  - Verification: Open packages/ui/COMPONENT_INVENTORY.md and verify all components listed with usage locations
- [ ] **Custom comic/novel themes render correctly in both light and dark modes**
  - Verification: Toggle theme in Dashboard and Storefront, verify reading-mode and editing-mode color schemes
- [ ] **All components pass accessibility audit with WCAG 2.1 AA compliance**
  - Verification: Run 'pnpm test:a11y' and verify axe-core tests pass with 0 violations
- [ ] **Storybook documentation covers all shared components with interactive examples**
  - Verification: Run 'pnpm storybook' and verify each component has stories with controls and documentation

## Technical Notes

### Approach

Set up a shared @morpheus/ui workspace containing audited shadcn/ui components with custom theming for novel/comic workflows. Create component inventory spreadsheet tracking usage across Dashboard/Storefront apps. Implement centralized Tailwind configuration with design tokens for reading modes, editing interfaces, and accessibility. Set up Vitest component testing and Storybook documentation. Verify all components work with TypeScript strict mode and establish linting rules for consistent component usage patterns.


### Files to Modify

- **path**: apps/dashboard/components.json
- **changes**: Update to use @morpheus/ui as component source, adjust aliases
- **path**: apps/storefront/components.json
- **changes**: Update to use @morpheus/ui as component source, adjust aliases
- **path**: packages/tailwind-config/index.ts
- **changes**: Add comic/novel design tokens, reading-mode variants
- **path**: apps/dashboard/tailwind.config.ts
- **changes**: Extend shared config with dashboard-specific overrides
- **path**: apps/storefront/tailwind.config.ts
- **changes**: Extend shared config with storefront-specific overrides
- **path**: turbo.json
- **changes**: Add build pipeline for @morpheus/ui workspace

### New Files to Create

- **path**: packages/ui/package.json
- **purpose**: Shared UI workspace configuration with shadcn/ui dependencies
- **path**: packages/ui/components.json
- **purpose**: Master shadcn/ui configuration for component generation
- **path**: packages/ui/src/components/index.ts
- **purpose**: Centralized component exports for the monorepo
- **path**: packages/ui/src/lib/utils.ts
- **purpose**: Shared utility functions (cn, theme helpers)
- **path**: packages/ui/src/styles/globals.css
- **purpose**: Global CSS variables and base styles
- **path**: packages/ui/COMPONENT_INVENTORY.md
- **purpose**: Comprehensive component usage tracking and documentation
- **path**: packages/ui/.storybook/main.ts
- **purpose**: Storybook configuration for component development
- **path**: packages/ui/src/stories/
- **purpose**: Directory containing all component stories
- **path**: packages/ui/src/themes/novel.ts
- **purpose**: Novel-specific theme configuration and tokens
- **path**: packages/ui/src/themes/comic.ts
- **purpose**: Comic-specific theme configuration and tokens
- **path**: packages/ui/vitest.config.ts
- **purpose**: Component testing configuration

### External Dependencies


- **shadcn-ui** ^0.8.0

  - Component library CLI for installation and updates

- **@radix-ui/react-*** ^1.0.0

  - Primitive components that shadcn/ui is built upon

- **class-variance-authority** ^0.7.0

  - Component variant management for shadcn/ui components

- **@storybook/react-vite** ^7.6.0

  - Component documentation and visual testing environment

- **tailwindcss-animate** ^1.0.7

  - Animation utilities for shadcn/ui components

## Testing

### Unit Tests

- **File**: `packages/ui/src/__tests__/components.test.tsx`
  - Scenarios: Component rendering with default props, Theme variants (light/dark/reading-mode), Accessibility attributes and keyboard navigation, Custom prop combinations
- **File**: `packages/ui/src/__tests__/theme.test.ts`
  - Scenarios: Theme token resolution, CSS variable generation, Color scheme switching
### Integration Tests

- **File**: `apps/dashboard/src/__tests__/components/integration.test.tsx`
  - Scenarios: Components work within Dashboard layout, Theme switching affects all components
- **File**: `apps/storefront/src/__tests__/components/integration.test.tsx`
  - Scenarios: Components work within Storefront layout, Reading mode theme integration
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

- **task**: Create @morpheus/ui workspace and configure package.json
- **done**: False
- **task**: Audit existing shadcn/ui components in Dashboard and Storefront
- **done**: False
- **task**: Migrate components to centralized packages/ui workspace
- **done**: False
- **task**: Implement custom themes for novel/comic workflows
- **done**: False
- **task**: Create component inventory and usage documentation
- **done**: False
- **task**: Set up Vitest component testing with React Testing Library
- **done**: False
- **task**: Configure Storybook with theme switching controls
- **done**: False
- **task**: Run accessibility audit and fix violations
- **done**: False
- **task**: Update app configurations to use shared components
- **done**: False
- **task**: Create usage guidelines and contribution docs
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task involves auditing and verifying the shadcn/ui component library integration across the Morpheus platform's frontend applications (Dashboard and Storefront). shadcn/ui provides copy-paste React components built on Radix primitives and Tailwind CSS, offering consistent design system implementation. This audit ensures proper setup, identifies missing components needed for the novel-to-comic transformation workflows, verifies theming consistency, and establishes component usage patterns across the monorepo.

**Technical Approach:**
1. Audit existing shadcn/ui installation in both Next.js apps using the CLI tool
2. Create a centralized component inventory and usage matrix
3. Establish shared theming configuration across Dashboard/Storefront
4. Set up component testing patterns with Vitest for isolated component testing
5. Create component documentation and usage guidelines
6. Implement design tokens for comic/novel-specific theming (dark themes for reading, high contrast for editing)
7. Verify accessibility compliance across all components
8. Set up Storybook integration for component development and documentation

**Dependencies:**
- External: shadcn/ui CLI, @radix-ui/* primitives, tailwindcss, class-variance-authority
- Internal: Turborepo shared configs, design system tokens, TypeScript shared types

**Risks:**
- Version mismatches: Ensure consistent shadcn/ui versions across workspaces through pnpm workspace constraints
- Bundle size bloat: Audit for unused Radix primitives and implement tree-shaking
- Theme inconsistency: Risk of different color schemes between Dashboard and Storefront apps
- TypeScript conflicts: Potential type conflicts between Radix versions and custom extensions

**Complexity Notes:**
Medium complexity - while shadcn/ui components are straightforward to use, coordinating them across a monorepo with shared theming and ensuring proper TypeScript integration adds complexity. The novel-to-comic domain may require custom component extensions.

**Key Files:**
- packages/ui/: Shared component library workspace
- apps/dashboard/components.json: shadcn/ui config for dashboard
- apps/storefront/components.json: shadcn/ui config for storefront  
- packages/tailwind-config/: Shared Tailwind configuration
- apps/*/tailwind.config.ts: App-specific Tailwind extensions


### Design Decisions

[{'decision': 'Create shared @morpheus/ui package for shadcn/ui components', 'rationale': 'Ensures consistency across Dashboard and Storefront, reduces duplication, and provides single source of truth for component library', 'alternatives_considered': ['Duplicate components in each app', 'Use shadcn/ui CLI in each app separately']}, {'decision': 'Extend default shadcn/ui theme with comic/novel-specific design tokens', 'rationale': 'Novel reading and comic creation have specific UX needs (reading modes, panel editing themes) that require custom color schemes and spacing', 'alternatives_considered': ['Use default shadcn/ui themes only', 'Create completely custom component library']}, {'decision': 'Use Storybook for component documentation and testing', 'rationale': 'Provides visual component testing, documentation, and development environment for design system components', 'alternatives_considered': ['Custom documentation site', 'Component testing in Jest only']}]
