---
area: distribution
dependsOn: []
effort: 2
iteration: I6
key: T82
milestone: M6 - Commerce & Distribution
priority: p1
title: Analytics Tracking
type: Task
---

# Analytics Tracking

## Acceptance Criteria

- [ ] **Client-side analytics tracks user interactions (page views, clicks, form submissions) with privacy consent management**
  - Verification: Check browser developer tools for PostHog events, verify consent banner appears, test opt-out functionality
- [ ] **Server-side analytics captures critical business events (purchases, transformations, user registrations) with 100% accuracy**
  - Verification: Compare server-side event logs with database records for purchases and transformations over 24h period
- [ ] **Real-time analytics dashboard displays key metrics (revenue, conversion rates, transformation success rates) with <5 second data freshness**
  - Verification: Navigate to /admin/analytics, perform test purchase, verify metrics update within 5 seconds
- [ ] **GDPR/CCPA compliance implemented with data anonymization, consent management, and user data deletion**
  - Verification: Test consent banner, verify anonymized IP addresses in logs, test data deletion API endpoint
- [ ] **Analytics performance impact <100ms additional page load time and <1MB additional bundle size**
  - Verification: Run Lighthouse performance audit before/after, measure bundle size with webpack-bundle-analyzer

## Technical Notes

### Approach

Create a unified analytics layer that captures both user interactions and system events. Client-side tracking handles user behavior with privacy controls, while server-side events ensure accuracy for business metrics. Implement custom dashboards for transformation analytics (success rates, processing times, costs) alongside standard e-commerce metrics (conversion rates, revenue, user retention).


### Files to Modify

- **path**: apps/storefront/pages/_app.tsx
- **changes**: Add Analytics provider wrapper and consent management
- **path**: apps/dashboard/pages/_app.tsx
- **changes**: Add internal analytics tracking for admin actions
- **path**: apps/backend/src/routes/payments.ts
- **changes**: Add server-side purchase event tracking
- **path**: apps/backend/src/routes/transformations.ts
- **changes**: Add transformation analytics events
- **path**: apps/backend/src/middleware/auth.ts
- **changes**: Add user authentication events

### New Files to Create

- **path**: packages/shared/types/analytics.ts
- **purpose**: Shared TypeScript interfaces for analytics events and schema validation
- **path**: apps/backend/src/services/analytics.ts
- **purpose**: Server-side analytics service with event processing, validation, and external API integration
- **path**: apps/dashboard/lib/analytics.ts
- **purpose**: Client-side analytics utilities with privacy controls and PostHog integration
- **path**: apps/storefront/components/Analytics.tsx
- **purpose**: E-commerce specific tracking components and hooks
- **path**: apps/storefront/components/ConsentBanner.tsx
- **purpose**: GDPR/CCPA compliant consent management UI
- **path**: apps/dashboard/pages/admin/analytics.tsx
- **purpose**: Real-time analytics dashboard for business metrics
- **path**: apps/backend/src/routes/analytics.ts
- **purpose**: Analytics API endpoints for dashboard data and user preferences
- **path**: apps/backend/src/jobs/analytics-aggregation.ts
- **purpose**: Background job for aggregating analytics data and generating reports
- **path**: packages/shared/config/analytics.ts
- **purpose**: Analytics configuration constants and environment variables

### External Dependencies


- **posthog-js** ^1.96.0

  - Client-side analytics tracking with privacy features

- **posthog-node** ^3.6.0

  - Server-side event tracking for backend services

- **@vercel/analytics** ^1.1.0

  - Performance and Core Web Vitals tracking for Next.js apps

- **react-gtag** ^1.0.1

  - Google Analytics integration for marketing attribution

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/services/analytics.test.ts`
  - Scenarios: Event validation and sanitization, Batch event processing, Privacy compliance filtering, Event schema validation
- **File**: `apps/dashboard/lib/__tests__/analytics.test.ts`
  - Scenarios: Client-side event tracking, Consent management, Event batching and retry logic
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/analytics-flow.test.ts`
  - Scenarios: End-to-end purchase tracking (client -> server -> dashboard), Transformation analytics pipeline, Privacy consent flow integration
- **File**: `apps/storefront/__tests__/integration/ecommerce-tracking.test.ts`
  - Scenarios: Shopping cart events, Purchase completion tracking, User journey tracking
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

- **task**: Setup PostHog account and configure SDK integration
- **done**: False
- **task**: Create shared analytics types and event schema definitions
- **done**: False
- **task**: Implement server-side analytics service with event validation
- **done**: False
- **task**: Build client-side analytics utilities with privacy controls
- **done**: False
- **task**: Create GDPR-compliant consent management system
- **done**: False
- **task**: Integrate analytics tracking into storefront purchase flow
- **done**: False
- **task**: Add transformation pipeline analytics events
- **done**: False
- **task**: Build real-time analytics dashboard with key business metrics
- **done**: False
- **task**: Implement analytics data aggregation background jobs
- **done**: False
- **task**: Add comprehensive test coverage and performance monitoring
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Analytics tracking is crucial for a commerce platform to understand user behavior, conversion funnels, revenue attribution, and product performance. For Morpheus, this means tracking how users discover comics, engage with transformation features, complete purchases, and consume content. This data drives product decisions, marketing optimization, and revenue growth strategies.

**Technical Approach:**
Implement a multi-layered analytics architecture:
- Client-side tracking with privacy-first approach using PostHog or Mixpanel
- Server-side event tracking for critical business events (purchases, transformations)
- Custom analytics service for internal metrics (processing times, AI costs, success rates)
- Real-time dashboards for business metrics
- GDPR/CCPA compliant data collection with consent management

**Dependencies:**
- External: PostHog SDK, Google Analytics 4, Stripe webhooks for revenue tracking
- Internal: User authentication system, payment processing, transformation pipeline events, Supabase for event storage

**Risks:**
- Privacy compliance: Implement consent banners, data anonymization, and opt-out mechanisms
- Performance impact: Use lazy loading, event batching, and CDN delivery for tracking scripts
- Data accuracy: Ensure server-side validation of critical events to prevent client-side manipulation
- Cost escalation: Monitor API usage and implement sampling for high-volume events

**Complexity Notes:**
More complex than initially estimated due to privacy regulations and the need for both user behavior tracking and ML pipeline analytics. Requires coordination between frontend, backend, and ML services.

**Key Files:**
- apps/dashboard/lib/analytics.ts: Client-side tracking utilities
- apps/storefront/components/Analytics.tsx: E-commerce tracking wrapper
- apps/backend/src/services/analytics.ts: Server-side event processing
- packages/shared/types/analytics.ts: Event schema definitions


### Design Decisions

[{'decision': 'Use PostHog as primary analytics platform with custom backend events', 'rationale': 'PostHog offers privacy compliance, real-time analytics, and self-hosted options while supporting both product analytics and feature flags', 'alternatives_considered': ['Google Analytics + Mixpanel', 'Custom analytics with ClickHouse', 'Amplitude']}, {'decision': 'Implement event-driven architecture with Supabase real-time for internal dashboards', 'rationale': 'Leverages existing Supabase infrastructure and provides real-time updates for business-critical metrics', 'alternatives_considered': ['Redis Streams', 'Custom WebSocket service', 'Polling-based updates']}]
