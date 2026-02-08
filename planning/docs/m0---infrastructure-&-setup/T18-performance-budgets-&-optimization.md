---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T18
milestone: M0 - Infrastructure & Setup
priority: p1
title: Performance Budgets & Optimization
type: Task
---

# Performance Budgets & Optimization

## Acceptance Criteria

- [ ] **Lighthouse CI fails builds when performance budgets are exceeded (LCP >2.5s, bundle size >500KB for critical routes)**
  - Verification: Run `npm run perf:check` - should fail with budget violations and pass when under thresholds
- [ ] **Real User Monitoring captures Core Web Vitals for all applications with <1% performance overhead**
  - Verification: Check Supabase `performance_metrics` table contains LCP, FID, CLS data with timestamps within 5min of page loads
- [ ] **Performance budgets are enforced per application with different thresholds (Dashboard: 800KB, Storefront: 500KB, API: <200ms)**
  - Verification: Verify `.lighthouserc.js` contains app-specific budgets and CI workflow runs separate checks per app
- [ ] **Automated performance alerts trigger when budgets exceeded in production**
  - Verification: Simulate performance regression - alert should fire within 5 minutes via configured webhook/email
- [ ] **Performance monitoring dashboard displays real-time metrics with 7-day historical trends**
  - Verification: Navigate to `/admin/performance` - should show current Core Web Vitals, API response times, and trend charts

## Technical Notes

### Approach

Establish performance budgets using Lighthouse CI for synthetic monitoring and web-vitals for RUM data collection. Configure tiered budgets (warning/error thresholds) per application in the monorepo. Integrate performance checks into Turborepo build pipeline and GitHub Actions. Create shared monitoring utilities package for consistent performance tracking across dashboard, storefront, and API layers. Set up automated alerts and reporting dashboard using Supabase for performance data storage.


### Files to Modify

- **path**: turbo.json
- **changes**: Add 'perf:check', 'perf:analyze', 'perf:monitor' tasks with dependencies
- **path**: apps/dashboard/next.config.js
- **changes**: Add bundle analyzer, performance configs, web-vitals integration
- **path**: apps/storefront/next.config.js
- **changes**: Add performance optimizations, image optimization, Core Web Vitals tracking
- **path**: package.json
- **changes**: Add performance-related scripts and dependencies (@lhci/cli, web-vitals, perfume.js)
- **path**: apps/backend/src/middleware/index.ts
- **changes**: Add response time tracking middleware with performance logging

### New Files to Create

- **path**: lighthouserc.js
- **purpose**: Lighthouse CI configuration with per-app performance budgets
- **path**: .github/workflows/performance.yml
- **purpose**: CI/CD performance gates and budget enforcement
- **path**: packages/monitoring/package.json
- **purpose**: Shared monitoring package with performance utilities
- **path**: packages/monitoring/src/performance-collector.ts
- **purpose**: Core Web Vitals and custom metrics collection service
- **path**: packages/monitoring/src/budget-validator.ts
- **purpose**: Performance budget validation and alerting logic
- **path**: packages/monitoring/src/types.ts
- **purpose**: TypeScript interfaces for performance metrics and budgets
- **path**: apps/dashboard/src/lib/performance.ts
- **purpose**: Dashboard-specific performance monitoring integration
- **path**: apps/storefront/src/lib/performance.ts
- **purpose**: Storefront-specific performance tracking and optimization
- **path**: apps/dashboard/src/pages/admin/performance.tsx
- **purpose**: Performance monitoring dashboard UI component
- **path**: scripts/performance-report.js
- **purpose**: Generate performance reports for stakeholders
- **path**: docs/performance-budgets.md
- **purpose**: Documentation for performance budget configuration and monitoring

### External Dependencies


- **@lhci/cli** ^0.12.0

  - Lighthouse CI for automated performance testing and budgets

- **web-vitals** ^3.5.0

  - Real user monitoring of Core Web Vitals metrics

- **@next/bundle-analyzer** ^14.0.0

  - Bundle size analysis and optimization for Next.js apps

- **perfume.js** ^8.4.0

  - Comprehensive performance monitoring library

- **@vercel/analytics** ^1.1.0

  - Web analytics and performance insights integration

## Testing

### Unit Tests

- **File**: `packages/monitoring/src/__tests__/performance-collector.test.ts`
  - Scenarios: Web vitals data collection and validation, API response time tracking, Error handling for invalid metrics, Performance budget threshold checking
- **File**: `packages/monitoring/src/__tests__/budget-validator.test.ts`
  - Scenarios: Bundle size budget validation, Core Web Vitals threshold checking, Custom metric budget evaluation
### Integration Tests

- **File**: `apps/dashboard/src/__tests__/integration/performance.test.ts`
  - Scenarios: Performance metrics are collected during page navigation, Bundle size stays within configured budgets
- **File**: `apps/storefront/src/__tests__/integration/performance.test.ts`
  - Scenarios: Core Web Vitals tracking on product pages, Image optimization performance validation
### Manual Testing


## Estimates

- **Development**: 4.5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 1
- **Total**: 8

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Create packages/monitoring structure and install dependencies
- **done**: False
- **task**: Implement performance collector and budget validator utilities
- **done**: False
- **task**: Configure Lighthouse CI with per-app budgets and thresholds
- **done**: False
- **task**: Integrate web-vitals tracking in dashboard and storefront apps
- **done**: False
- **task**: Add performance middleware to backend API with response time tracking
- **done**: False
- **task**: Set up Supabase performance_metrics table and logging
- **done**: False
- **task**: Create GitHub Actions workflow for CI/CD performance gates
- **done**: False
- **task**: Build performance monitoring dashboard UI
- **done**: False
- **task**: Configure automated alerts and notification system
- **done**: False
- **task**: Write comprehensive documentation and create performance reports
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Performance budgets define measurable thresholds for web performance metrics (load times, bundle sizes, Core Web Vitals) that the Morpheus platform must not exceed. This is critical for M0 because:
- Comic generation involves heavy image processing that can impact UX
- Dashboard needs to remain responsive during long-running ML operations  
- Storefront must load quickly for user engagement and SEO
- Early establishment prevents performance debt accumulation
- Sets foundation for monitoring and alerting systems

**Technical Approach:**
Implement multi-layered performance budgets covering:
1. Bundle size limits per application/route
2. Core Web Vitals thresholds (LCP <2.5s, FID <100ms, CLS <0.1)
3. API response time budgets (<200ms for critical paths)
4. Image optimization and delivery budgets
5. Real User Monitoring (RUM) integration
6. CI/CD performance gates using Lighthouse CI
7. Runtime performance monitoring with error budgets

**Dependencies:**
- External: @lhci/cli, web-vitals, @vercel/analytics, bundle-analyzer, perfume.js
- Internal: Requires integration with existing Turborepo build system, Supabase logging, Next.js analytics

**Risks:**
- Budget thresholds too strict: Start conservative, iterate based on real usage
- CI/CD pipeline slowdown: Use parallel execution and caching strategies
- False positives in monitoring: Implement proper error boundaries and sampling
- Performance vs feature velocity tension: Establish clear escalation processes

**Complexity Notes:**
Higher complexity than initial estimate due to:
- Multi-application monorepo requiring different budgets per app
- ML workload performance patterns being unpredictable
- Need for both synthetic and RUM monitoring
- Integration with existing Fastify/Next.js performance tooling

**Key Files:**
- turbo.json: Add performance check tasks
- apps/dashboard/next.config.js: Bundle analyzer and performance config
- apps/storefront/next.config.js: Similar performance optimizations
- packages/monitoring: New package for shared performance utilities
- .github/workflows/performance.yml: CI performance gates
- lighthouserc.js: Lighthouse CI configuration


### Design Decisions

[{'decision': 'Use Lighthouse CI with custom performance budgets per application', 'rationale': 'Provides consistent synthetic monitoring across all environments with configurable thresholds', 'alternatives_considered': ['WebPageTest API', 'Custom performance testing', 'Vercel Analytics only']}, {'decision': 'Implement tiered budget system (strict/warning/error levels)', 'rationale': 'Allows gradual performance improvements without blocking development', 'alternatives_considered': ['Binary pass/fail budgets', 'Manual performance reviews']}, {'decision': 'Separate budgets for dashboard vs storefront applications', 'rationale': 'Different user expectations and performance characteristics require tailored thresholds', 'alternatives_considered': ['Single unified budget', 'Route-level budgets only']}]
