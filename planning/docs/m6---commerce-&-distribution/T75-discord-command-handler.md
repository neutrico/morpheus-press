---
area: distribution
dependsOn:
- T74
effort: 3
iteration: I6
key: T75
milestone: M6 - Commerce & Distribution
priority: p1
title: Discord Command Handler
type: Task
---

# Discord Command Handler

## Acceptance Criteria

- [ ] **Bot responds to /browse command with paginated comic listings showing title, price, and preview**
  - Verification: Execute /browse in Discord server, verify embed shows comics with navigation buttons
- [ ] **Users can purchase comics via /buy command with Stripe integration and receive download links**
  - Verification: Run /buy [comic-id], complete payment flow, verify comic delivery to DM
- [ ] **Bot handles Discord rate limits gracefully without crashing or losing user interactions**
  - Verification: Load test with 50 concurrent interactions, verify no 429 errors or timeouts
- [ ] **User authentication links Discord accounts to existing Morpheus accounts via /login command**
  - Verification: Execute /login, complete OAuth flow, verify user data synced in Supabase
- [ ] **Bot responds to all interactions within Discord's 3-second timeout requirement**
  - Verification: Monitor interaction response times, all must acknowledge within 3000ms

## Technical Notes

### Approach

Create a dedicated Discord bot service using discord.js with slash command handlers for comic browsing, purchasing, and user management. Implement webhook-based architecture where Discord interactions trigger Fastify backend endpoints that handle business logic and return formatted responses. Use Redis for caching comic data and user sessions to minimize database queries. Integrate with existing Supabase authentication by linking Discord users to Morpheus accounts, and leverage the current payment processing pipeline for comic purchases.


### Files to Modify

- **path**: packages/backend/src/routes/index.ts
- **changes**: Add Discord webhook route registration
- **path**: packages/backend/src/services/auth.service.ts
- **changes**: Add Discord OAuth integration methods
- **path**: packages/shared/src/types/user.ts
- **changes**: Add Discord user ID field to User interface
- **path**: docker-compose.yml
- **changes**: Add Redis service for Discord bot caching

### New Files to Create

- **path**: packages/discord-bot/src/index.ts
- **purpose**: Main Discord bot entry point and client initialization
- **path**: packages/discord-bot/src/commands/browse.ts
- **purpose**: Browse comics command handler with pagination
- **path**: packages/discord-bot/src/commands/buy.ts
- **purpose**: Purchase comic command handler
- **path**: packages/discord-bot/src/commands/login.ts
- **purpose**: User authentication command handler
- **path**: packages/discord-bot/src/services/discord-auth.service.ts
- **purpose**: Discord user authentication and account linking
- **path**: packages/discord-bot/src/services/comic-cache.service.ts
- **purpose**: Redis-based comic metadata caching
- **path**: packages/discord-bot/src/utils/embed-builder.ts
- **purpose**: Discord embed formatting utilities
- **path**: packages/discord-bot/src/types/commands.ts
- **purpose**: TypeScript interfaces for Discord commands
- **path**: packages/backend/src/routes/discord/webhooks.ts
- **purpose**: Discord interaction webhook handlers
- **path**: packages/backend/src/routes/discord/auth.ts
- **purpose**: Discord OAuth callback endpoints
- **path**: packages/backend/src/services/discord.service.ts
- **purpose**: Backend Discord integration service
- **path**: packages/shared/src/types/discord.ts
- **purpose**: Shared Discord-related type definitions
- **path**: packages/discord-bot/package.json
- **purpose**: Discord bot package configuration
- **path**: packages/discord-bot/Dockerfile
- **purpose**: Discord bot containerization

### External Dependencies


- **discord.js** ^14.14.1

  - Primary Discord API wrapper with TypeScript support

- **@discordjs/builders** ^1.7.0

  - Utility for building Discord API payloads and slash commands

- **@discordjs/rest** ^2.2.0

  - REST client for Discord API interactions and command registration

- **ioredis** ^5.3.2

  - Redis client for caching Discord interactions and user sessions

## Testing

### Unit Tests

- **File**: `packages/discord-bot/src/__tests__/commands/browse.test.ts`
  - Scenarios: Browse command with valid pagination, Browse command with no comics available, Browse command with invalid page number
- **File**: `packages/discord-bot/src/__tests__/commands/buy.test.ts`
  - Scenarios: Successful purchase flow, Payment failure handling, Invalid comic ID error
- **File**: `packages/discord-bot/src/__tests__/services/discord-auth.test.ts`
  - Scenarios: Discord user linking to existing account, New user registration via Discord, Invalid authentication token handling
### Integration Tests

- **File**: `packages/backend/src/__tests__/integration/discord-webhooks.test.ts`
  - Scenarios: Discord interaction webhook processing, Payment completion webhook flow, Authentication callback integration
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 0.5
- **Total**: 8.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Set up Discord bot package structure and dependencies
- **done**: False
- **task**: Implement Discord bot client initialization and slash command registration
- **done**: False
- **task**: Create browse command with paginated comic listings and embeds
- **done**: False
- **task**: Implement user authentication flow linking Discord to Morpheus accounts
- **done**: False
- **task**: Build purchase command with Stripe integration and comic delivery
- **done**: False
- **task**: Set up Redis caching service for comic metadata
- **done**: False
- **task**: Create Discord webhook handlers in Fastify backend
- **done**: False
- **task**: Implement error handling and rate limiting protection
- **done**: False
- **task**: Write comprehensive test suite and documentation
- **done**: False
- **task**: Deploy bot and conduct end-to-end testing
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Discord Command Handler is essential for M6 Commerce & Distribution as it enables direct comic sales and distribution through Discord servers. This creates an additional revenue channel beyond the web storefront, allowing users to discover, preview, and purchase comics directly within Discord communities. It supports the business goal of expanding distribution channels and reaching users where they already engage with content.

**Technical Approach:**
- Use discord.js v14 as the primary Discord API wrapper
- Implement slash command architecture with proper command registration
- Create modular command handlers with TypeScript interfaces for type safety
- Integrate with existing Supabase backend for user authentication and comic data
- Use webhook-based event handling for scalable bot interactions
- Implement Redis caching for frequently accessed comic metadata
- Follow Discord's interaction response patterns (3-second acknowledgment rule)
- Use Discord embeds for rich comic previews with image attachments

**Dependencies:**
- External: discord.js, @discordjs/builders, @discordjs/rest
- Internal: Supabase client, authentication service, comic catalog API, payment processing service
- Infrastructure: Redis for caching, webhook endpoints in Fastify backend

**Risks:**
- Rate limiting: Discord API has strict rate limits that could impact user experience
- Token security: Bot tokens must be securely managed and rotated
- Interaction timeouts: Discord requires responses within 3 seconds, complex operations need deferring
- Permission complexity: Discord server permissions can be complex and vary by server
- Scaling challenges: Single bot instance may not handle high concurrent usage

**Complexity Notes:**
Higher complexity than initially estimated due to Discord's interaction model requiring careful state management and the need to integrate with multiple existing services (auth, payments, catalog). The asynchronous nature of Discord interactions adds complexity to error handling and user feedback.

**Key Files:**
- packages/discord-bot/: New package for Discord bot functionality
- packages/backend/src/routes/discord/: Discord webhook handlers
- packages/shared/src/types/discord.ts: Shared Discord types
- packages/backend/src/services/discord.ts: Discord service integration


### Design Decisions

[{'decision': 'Use slash commands instead of message-based commands', 'rationale': "Slash commands provide better UX with auto-completion, validation, and are Discord's recommended modern approach", 'alternatives_considered': ['Message-based prefix commands', 'Context menu commands only']}, {'decision': 'Separate Discord bot as independent service with webhook integration', 'rationale': 'Allows independent scaling and deployment while maintaining loose coupling with main backend', 'alternatives_considered': ['Embedded bot within Fastify backend', 'Serverless Discord functions']}, {'decision': 'Implement command cooldowns and user session management', 'rationale': 'Prevents abuse and manages Discord API rate limits while providing smooth user experience', 'alternatives_considered': ['No rate limiting', 'Global rate limiting only']}]
