---
area: distribution
dependsOn: []
effort: 3
iteration: I6
key: T76
milestone: M6 - Commerce & Distribution
priority: p2
title: Reddit Integration
type: Task
---

# Reddit Integration

## Acceptance Criteria

- [ ] **Comics can be automatically shared to appropriate subreddits after publication**
  - Verification: Publish a test comic, verify it appears in configured subreddit queue and gets posted within scheduled timeframe
- [ ] **Rate limiting is properly handled with max 600 requests per 10 minutes**
  - Verification: Load test with 1000+ posts, verify exponential backoff triggers and no API errors occur
- [ ] **Admin dashboard allows configuration of Reddit credentials, subreddit lists, and posting schedules**
  - Verification: Navigate to /dashboard/distribution/reddit, verify all CRUD operations work for subreddits and scheduling
- [ ] **Content categorization correctly maps comic genres to relevant subreddits**
  - Verification: Test comics with genres 'sci-fi', 'comedy', 'horror' map to appropriate subreddit suggestions
- [ ] **Manual approval workflow prevents spam and policy violations**
  - Verification: Verify posts require admin approval before going live, and rejected posts don't get requeued

## Technical Notes

### Approach

Implement a Reddit distribution service that integrates with the existing comic completion pipeline. When a comic is published, trigger a job to analyze content and suggest appropriate subreddits based on genre/theme mapping. Queue posts with optimal timing (analyzing subreddit activity patterns) and include engagement tracking. Build dashboard components for configuring Reddit credentials, managing subreddit lists, reviewing pending posts, and viewing performance analytics.


### Files to Modify

- **path**: apps/api/src/services/comic-service.ts
- **changes**: Add hook to trigger Reddit distribution job after comic publication
- **path**: packages/shared/src/types/comic.ts
- **changes**: Add reddit_distribution_status field to Comic interface
- **path**: apps/api/src/config/redis.ts
- **changes**: Add Reddit job queue configuration
- **path**: apps/dashboard/src/routes/distribution.tsx
- **changes**: Add Reddit settings route and navigation

### New Files to Create

- **path**: apps/api/src/services/reddit-service.ts
- **purpose**: Core Reddit API integration, OAuth handling, posting logic
- **path**: apps/api/src/services/content-categorization-service.ts
- **purpose**: Map comic genres/themes to appropriate subreddit recommendations
- **path**: apps/api/src/jobs/reddit-publisher.ts
- **purpose**: Background job processor for scheduled Reddit posting
- **path**: apps/api/src/middleware/reddit-rate-limiter.ts
- **purpose**: Custom rate limiting middleware for Reddit API calls
- **path**: apps/dashboard/src/components/distribution/RedditSettings.tsx
- **purpose**: Admin UI for Reddit OAuth, subreddit management, posting schedules
- **path**: apps/dashboard/src/components/distribution/RedditQueue.tsx
- **purpose**: Admin UI for reviewing and approving pending Reddit posts
- **path**: apps/dashboard/src/components/distribution/RedditAnalytics.tsx
- **purpose**: Display Reddit posting performance metrics and engagement data
- **path**: packages/shared/src/types/distribution.ts
- **purpose**: TypeScript interfaces for Reddit configuration and posting data
- **path**: apps/api/src/routes/distribution/reddit.ts
- **purpose**: API endpoints for Reddit configuration and queue management
- **path**: apps/api/src/db/migrations/20240115_add_reddit_distribution.sql
- **purpose**: Database schema for Reddit credentials, subreddit lists, posting queue

### External Dependencies


- **snoowrap** ^1.23.0

  - Official Reddit API wrapper with OAuth 2.0 support and TypeScript definitions

- **bull** ^4.12.0

  - Redis-based job queue for managing scheduled Reddit posts and rate limiting

- **ioredis** ^5.3.0

  - Redis client for job queue storage and caching subreddit metadata

- **image-size** ^1.0.2

  - Extracting comic image dimensions for optimal Reddit display formatting

## Testing

### Unit Tests

- **File**: `apps/api/src/services/__tests__/reddit-service.test.ts`
  - Scenarios: OAuth authentication flow, Subreddit validation and posting, Rate limit handling with exponential backoff, Content categorization algorithm, Error handling for API failures
- **File**: `apps/api/src/jobs/__tests__/reddit-publisher.test.ts`
  - Scenarios: Job queue processing, Scheduled posting with optimal timing, Failed post retry logic
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/reddit-distribution.test.ts`
  - Scenarios: End-to-end comic publication to Reddit, Admin approval workflow, Analytics tracking integration
- **File**: `apps/dashboard/src/components/distribution/__tests__/RedditSettings.integration.test.tsx`
  - Scenarios: Reddit credential configuration flow, Subreddit management CRUD operations
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

- **task**: Setup Reddit OAuth application and obtain API credentials
- **done**: False
- **task**: Install and configure snoowrap, ioredis, bull dependencies
- **done**: False
- **task**: Implement core RedditService with authentication and posting methods
- **done**: False
- **task**: Create content categorization service for subreddit mapping
- **done**: False
- **task**: Build job queue system with Redis and Bull for scheduled posting
- **done**: False
- **task**: Implement rate limiting middleware with exponential backoff
- **done**: False
- **task**: Create database schema and migrations for Reddit distribution data
- **done**: False
- **task**: Build admin dashboard components for Reddit configuration
- **done**: False
- **task**: Integrate Reddit distribution trigger with comic publication flow
- **done**: False
- **task**: Add manual approval workflow and queue management UI
- **done**: False
- **task**: Implement analytics tracking for Reddit post performance
- **done**: False
- **task**: Write comprehensive tests for all components
- **done**: False
- **task**: Create documentation for Reddit integration setup and usage
- **done**: False
- **task**: Conduct security review of OAuth implementation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Reddit integration enables automated sharing of completed comics to relevant subreddits, driving organic discovery and user acquisition. This addresses the challenge of reaching niche audiences who are passionate about specific genres/topics that align with the comic content. Reddit's community-driven nature makes it ideal for showcasing AI-generated comics to engaged audiences who appreciate creativity and technology.

**Technical Approach:**
Use Reddit's OAuth 2.0 API via PRAW (Python Reddit API Wrapper) or Snoowrap (Node.js) to authenticate and post comics. Implement a queue-based system using Redis/Bull for scheduled posting to avoid rate limits. Create a content categorization service that maps comic genres/themes to appropriate subreddits. Build admin dashboard components for managing subreddit lists, posting schedules, and performance analytics.

**Dependencies:**
- External: snoowrap (Reddit API), ioredis (Redis client), bull (job queue), image-size (comic dimensions)
- Internal: comic-service (accessing completed comics), auth-service (storing Reddit credentials), analytics-service (tracking engagement)

**Risks:**
- Rate limiting (600 requests/10 minutes): implement exponential backoff and job queuing
- Subreddit moderation/spam detection: require manual approval workflow before auto-posting
- API changes/deprecation: abstract Reddit client behind service interface for easy swapping
- Content policy violations: implement content filtering and community guidelines checker

**Complexity Notes:**
More complex than initially estimated due to Reddit's strict anti-spam policies and varied subreddit rules. Requires sophisticated content matching algorithms and careful rate limiting. The social aspect adds complexity around timing optimization and community engagement tracking.

**Key Files:**
- apps/api/src/services/reddit-service.ts: core Reddit API integration
- apps/dashboard/src/components/distribution/RedditSettings.tsx: admin configuration UI
- packages/shared/src/types/distribution.ts: Reddit posting configuration types
- apps/api/src/jobs/reddit-publisher.ts: background job for scheduled posting


### Design Decisions

[{'decision': 'Use Node.js Snoowrap over direct API calls', 'rationale': 'Handles OAuth refresh, rate limiting, and provides TypeScript support that aligns with our stack', 'alternatives_considered': ['Direct fetch() to Reddit API', 'Python PRAW with microservice']}, {'decision': 'Queue-based publishing with Redis/Bull', 'rationale': 'Ensures posts are spread out to respect rate limits and allows retry logic for failed posts', 'alternatives_considered': ['Direct immediate posting', 'Cron-based scheduling']}, {'decision': 'Manual approval workflow for subreddit posts', 'rationale': 'Prevents spam flags and allows content optimization before posting to communities', 'alternatives_considered': ['Fully automated posting', 'AI-based content filtering only']}]
