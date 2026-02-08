---
area: distribution
dependsOn: []
effort: 5
iteration: I6
key: T74
milestone: M6 - Commerce & Distribution
priority: p1
title: Discord Bot
type: Task
---

# Discord Bot

## Acceptance Criteria

- [ ] **Discord bot responds to slash commands (/comics search, /comics subscribe, /buy, /link, /profile) with appropriate embeds and data**
  - Verification: Test each slash command in Discord server returns formatted embed with comic data from API
- [ ] **OAuth2 flow successfully links Discord users to Morpheus accounts in Supabase**
  - Verification: Complete /link command flow and verify user_discord_accounts table populated with correct discord_id and user_id mapping
- [ ] **Bot handles rate limits and API errors gracefully without crashing**
  - Verification: Simulate Discord API rate limit responses and verify bot queues requests and continues operating
- [ ] **Purchase flow through Discord validates payment and updates user subscriptions**
  - Verification: Execute /buy command, complete payment, verify subscription created in database and confirmation sent to Discord
- [ ] **Bot admin dashboard displays connection status, usage metrics, and configuration options**
  - Verification: Access apps/dashboard Discord integration page shows bot online status, command usage stats, and guild management

## Technical Notes

### Approach

Create a new Discord bot application in the Turborepo structure using discord.js v14 with TypeScript. Implement slash commands for comic browsing (/comics search, /comics subscribe), account management (/link, /profile), and purchasing (/buy). Use Discord OAuth2 to securely link Discord users to Morpheus accounts stored in Supabase. The bot communicates with the main Fastify API through internal service calls and handles Discord-specific data formatting. Deploy as a separate service with PM2 or Docker for process management and auto-restart capabilities.


### Files to Modify

- **path**: apps/api/src/routes/webhooks/index.ts
- **changes**: Add Discord webhook route registration
- **path**: packages/shared/types/user.ts
- **changes**: Add DiscordAccount interface and user relationship types
- **path**: apps/dashboard/src/components/layout/Sidebar.tsx
- **changes**: Add Discord integrations navigation item

### New Files to Create

- **path**: apps/discord-bot/package.json
- **purpose**: Discord bot dependencies and scripts
- **path**: apps/discord-bot/src/index.ts
- **purpose**: Bot entry point and client initialization
- **path**: apps/discord-bot/src/commands/comics.ts
- **purpose**: Comic search, browse, and subscription slash commands
- **path**: apps/discord-bot/src/commands/account.ts
- **purpose**: User account linking and profile management commands
- **path**: apps/discord-bot/src/commands/purchase.ts
- **purpose**: Comic purchase and payment flow commands
- **path**: apps/discord-bot/src/services/auth.ts
- **purpose**: Discord OAuth2 and account linking service
- **path**: apps/discord-bot/src/services/api-client.ts
- **purpose**: HTTP client for Morpheus API integration
- **path**: apps/discord-bot/src/utils/embeds.ts
- **purpose**: Discord embed formatting utilities for comics
- **path**: apps/discord-bot/src/utils/queue.ts
- **purpose**: Rate limiting and request queuing for Discord API
- **path**: apps/api/src/routes/webhooks/discord.ts
- **purpose**: Discord interaction webhook handlers
- **path**: apps/api/src/services/discord-integration.ts
- **purpose**: Discord API integration and webhook processing
- **path**: packages/shared/types/discord.ts
- **purpose**: Discord-specific type definitions and interfaces
- **path**: apps/dashboard/src/pages/integrations/discord.tsx
- **purpose**: Discord bot management and analytics dashboard
- **path**: packages/database/migrations/20240115000000_discord_accounts.sql
- **purpose**: Database schema for Discord user account linking
- **path**: apps/discord-bot/docker/Dockerfile
- **purpose**: Docker containerization for bot deployment
- **path**: apps/discord-bot/ecosystem.config.js
- **purpose**: PM2 process management configuration

### External Dependencies


- **discord.js** ^14.14.1

  - Primary Discord bot framework with excellent TypeScript support

- **@discordjs/builders** ^1.7.0

  - Builder utilities for slash commands and embeds

- **@discordjs/rest** ^2.2.0

  - REST API client for Discord interactions outside of gateway

- **p-queue** ^8.0.1

  - Queue system for managing Discord API rate limits

## Testing

### Unit Tests

- **File**: `apps/discord-bot/src/__tests__/commands/comics.test.ts`
  - Scenarios: Search command with valid query returns formatted results, Subscribe command with linked account creates subscription, Commands with unlinked account prompt OAuth flow, Invalid parameters return helpful error messages
- **File**: `apps/discord-bot/src/__tests__/services/auth.test.ts`
  - Scenarios: OAuth token exchange success, Account linking with existing user, Invalid OAuth state handling
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/discord-webhooks.test.ts`
  - Scenarios: Discord webhook interaction creates proper API response, Payment webhook from Discord purchase updates subscription, User linking flow end-to-end with Supabase
### Manual Testing


## Estimates

- **Development**: 5
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 1
- **Total**: 8.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Discord Developer Portal application and obtain bot token
- **done**: False
- **task**: Create Discord bot Turborepo package with TypeScript and discord.js
- **done**: False
- **task**: Implement slash command handlers for comics, account, and purchase flows
- **done**: False
- **task**: Build OAuth2 service for Discord account linking with Supabase integration
- **done**: False
- **task**: Create Discord webhook endpoints in Fastify API for interaction handling
- **done**: False
- **task**: Implement rate limiting and queue system for Discord API calls
- **done**: False
- **task**: Build Discord embed utilities for comic display and formatting
- **done**: False
- **task**: Create dashboard UI for Discord bot management and analytics
- **done**: False
- **task**: Setup Docker deployment and process management with PM2
- **done**: False
- **task**: Write comprehensive tests for commands, auth flow, and integrations
- **done**: False
- **task**: Document bot setup, deployment, and usage instructions
- **done**: False
- **task**: Conduct code review and security audit for OAuth and payment flows
- **done**: False

## Agent Notes

### Research Findings

**Context:**
A Discord bot serves as a distribution and community engagement channel for Morpheus-generated comics. Discord has massive communities of comic enthusiasts, web novel readers, and AI art fans. The bot enables users to discover new comics, subscribe to series updates, purchase comics directly through Discord, and share favorite panels with friends. This creates a viral marketing channel and reduces customer acquisition costs while building an engaged community around user-generated content.

**Technical Approach:**
Build a Discord bot using discord.js v14 with TypeScript, integrated with the existing Fastify backend through REST APIs and webhooks. The bot should support slash commands for comic discovery, subscription management, and purchasing. Implement OAuth2 flow to link Discord users with Morpheus accounts. Use Discord's embed system to showcase comic panels with rich metadata. Store Discord-specific data (guild configs, user preferences) in Supabase alongside existing user data. Implement rate limiting and queue systems to handle Discord API limits.

**Dependencies:**
- External: discord.js v14, @discordjs/builders, @discordjs/rest
- Internal: Existing auth service, payment service, comic metadata APIs, user management system
- Infrastructure: Discord Developer Portal app, webhook endpoints in Fastify backend

**Risks:**
- Discord API rate limits: Implement proper queuing with p-queue and exponential backoff
- Bot spam/abuse: Add user cooldowns, command rate limiting, and moderation features
- Payment fraud: Integrate existing payment validation, require account linking for purchases
- Scale issues: Discord bots can explode in usage quickly - design for horizontal scaling from day one

**Complexity Notes:**
Initially seems straightforward but Discord's ecosystem complexity is deceptive. Slash commands, permissions, guild management, and message embeds all have gotchas. The OAuth2 flow integration with existing Supabase auth adds significant complexity. Bot deployment and process management is also non-trivial compared to web services.

**Key Files:**
- apps/discord-bot/: New application in Turborepo structure
- packages/shared/types/discord.ts: Shared Discord-related types
- apps/api/src/routes/webhooks/discord.ts: Discord webhook handlers
- apps/api/src/services/discord-integration.ts: Discord API integration service
- apps/dashboard/src/pages/integrations/discord.tsx: Discord bot management UI


### Design Decisions

[{'decision': 'Separate Discord bot app in monorepo rather than embedding in main API', 'rationale': 'Discord bots have different scaling patterns, deployment needs, and development workflows. Separating allows independent scaling and reduces API service complexity.', 'alternatives_considered': ['Embed in main Fastify app', 'Serverless functions approach']}, {'decision': 'Use discord.js v14 with slash commands instead of message commands', 'rationale': 'Discord is deprecating message commands. Slash commands provide better UX with autocomplete and validation. v14 is the current stable release with best TypeScript support.', 'alternatives_considered': ['discord.py (Python)', 'older discord.js versions', 'raw Discord API']}, {'decision': 'OAuth2 account linking rather than separate Discord-only accounts', 'rationale': 'Users should have unified experience across platforms. Linking Discord to existing Morpheus accounts enables full feature access and consistent payment/subscription management.', 'alternatives_considered': ['Discord-only lightweight accounts', 'manual account claiming']}]
