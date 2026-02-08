---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T16
milestone: M0 - Infrastructure & Setup
priority: p0
title: Deployment Strategy & Procedures
type: Task
---

# Deployment Strategy & Procedures

## Acceptance Criteria

- [ ] **All services deploy successfully to their respective platforms (Railway for backend, Vercel for frontend, Supabase for database)**
  - Verification: Run `npm run deploy:all` and verify all deployment URLs return 200 status with health checks passing
- [ ] **Only changed packages trigger deployments based on Turborepo change detection**
  - Verification: Make isolated changes to single package and verify only that service deploys, check GitHub Actions logs for deployment skips
- [ ] **Database migrations run automatically before backend deployments without data loss**
  - Verification: Deploy schema changes and verify migration logs show successful execution with rollback capability intact
- [ ] **Production deployments include automated rollback on health check failures**
  - Verification: Simulate deployment failure and verify automatic rollback to previous version within 5 minutes
- [ ] **Environment variables and secrets are properly managed across all deployment targets**
  - Verification: Check deployment logs contain no exposed secrets and services can access required environment variables

## Technical Notes

### Approach

Implement a multi-platform deployment strategy using GitHub Actions for orchestration. Backend Fastify services deploy to Railway with Docker containers, Next.js applications deploy to Vercel with optimized builds, and database migrations run via Supabase CLI. Use Turborepo's change detection to deploy only modified packages, with comprehensive health checks and automated rollback procedures for production deployments.


### Files to Modify

- **path**: turbo.json
- **changes**: Add deploy pipeline tasks and change detection filters for each service
- **path**: package.json
- **changes**: Add deployment scripts for all platforms and environments
- **path**: apps/backend/package.json
- **changes**: Add Railway-specific deployment configuration and health check endpoints
- **path**: apps/frontend/package.json
- **changes**: Add Vercel deployment configuration and build optimization

### New Files to Create

- **path**: .github/workflows/deploy.yml
- **purpose**: Main CI/CD pipeline orchestrating multi-platform deployments
- **path**: .github/workflows/deploy-staging.yml
- **purpose**: Staging environment deployment pipeline
- **path**: .github/workflows/deploy-production.yml
- **purpose**: Production deployment with additional safety checks
- **path**: docker-compose.yml
- **purpose**: Local development environment matching production containers
- **path**: apps/backend/Dockerfile
- **purpose**: Backend service containerization for Railway deployment
- **path**: apps/worker/Dockerfile
- **purpose**: ML worker service containerization
- **path**: deploy/scripts/health-check.sh
- **purpose**: Universal health check script for all services
- **path**: deploy/scripts/rollback.sh
- **purpose**: Automated rollback procedures for failed deployments
- **path**: deploy/scripts/migrate.sh
- **purpose**: Database migration execution with validation
- **path**: deploy/config/railway.json
- **purpose**: Railway platform configuration for backend services
- **path**: deploy/config/vercel.json
- **purpose**: Vercel platform configuration for frontend applications
- **path**: deploy/utils/deployment-utils.ts
- **purpose**: Shared utilities for deployment validation and monitoring
- **path**: deploy/environments/.env.staging
- **purpose**: Staging environment configuration template
- **path**: deploy/environments/.env.production
- **purpose**: Production environment configuration template

### External Dependencies


- **@vercel/cli** ^32.0.0

  - Deploy Next.js dashboard and storefront to Vercel platform

- **@railway/cli** ^3.0.0

  - Deploy Fastify backend services to Railway platform

- **supabase** ^1.120.0

  - Manage database migrations and environment synchronization

- **docker** ^24.0.0

  - Container runtime for consistent deployment environments

- **@docker/actions** ^3.0.0

  - GitHub Actions integration for container builds and pushes

- **dotenv-cli** ^7.3.0

  - Environment variable management in deployment scripts

## Testing

### Unit Tests

- **File**: `deploy/__tests__/deployment-utils.test.ts`
  - Scenarios: Health check validation, Environment variable parsing, Migration status checking, Rollback trigger conditions
- **File**: `packages/database/__tests__/migrations.test.ts`
  - Scenarios: Migration execution order, Rollback procedures, Schema validation
### Integration Tests

- **File**: `deploy/__tests__/integration/full-deployment.test.ts`
  - Scenarios: End-to-end deployment pipeline, Multi-service coordination, Cross-platform deployment verification
- **File**: `deploy/__tests__/integration/rollback.test.ts`
  - Scenarios: Automatic rollback on failure, Manual rollback procedures
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 1
- **Total**: 8

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Set up GitHub Actions workflows for CI/CD pipeline
- **done**: False
- **task**: Create Dockerfile configurations for all containerized services
- **done**: False
- **task**: Configure Railway deployment for backend Fastify services
- **done**: False
- **task**: Configure Vercel deployment for Next.js frontend applications
- **done**: False
- **task**: Implement database migration automation with Supabase CLI
- **done**: False
- **task**: Set up Turborepo change detection and selective deployment
- **done**: False
- **task**: Create health check endpoints and monitoring scripts
- **done**: False
- **task**: Implement automated rollback procedures for production
- **done**: False
- **task**: Configure environment variable management and secrets
- **done**: False
- **task**: Test full deployment pipeline across all environments
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Deployment strategy is critical for Morpheus as it's a multi-service platform with backend APIs, frontend applications, database migrations, and ML model integrations. This task establishes reliable, automated deployment procedures for development, staging, and production environments. Without proper deployment strategy, the team risks manual errors, inconsistent environments, downtime during releases, and difficulty scaling the platform.

**Technical Approach:**
- **Container-first deployment** using Docker for consistent environments across services
- **Platform-as-a-Service** deployment via Railway/Render for backend, Vercel for Next.js frontends
- **Database migrations** integrated into deployment pipeline with Supabase CLI
- **Multi-environment strategy** (dev/staging/prod) with environment-specific configurations
- **CI/CD pipeline** using GitHub Actions triggered by Turborepo change detection
- **Health checks and rollback procedures** for zero-downtime deployments
- **Environment variable management** using platform-native secret management
- **ML model deployment** strategy for RunPod integration and model versioning

**Dependencies:**
- External: Docker, GitHub Actions, Vercel CLI, Railway CLI, Supabase CLI, @vercel/turborepo
- Internal: All workspace packages, environment configuration, database schemas, API routes

**Risks:**
- **Environment drift**: Different behavior between local/staging/prod - mitigate with containerization and strict environment parity
- **Database migration failures**: Schema changes breaking production - mitigate with migration testing and rollback procedures
- **ML model availability**: RunPod downtime affecting image generation - mitigate with fallback strategies and health checks
- **Secrets exposure**: API keys leaked in deployment logs - mitigate with proper secret management and log filtering
- **Monorepo complexity**: Deploying unchanged services unnecessarily - mitigate with Turborepo's change detection

**Complexity Notes:**
More complex than initially estimated due to ML integration requirements and monorepo coordination. The need to deploy multiple services with different requirements (Fastify backend, Next.js apps, ML workers) while maintaining data consistency adds significant complexity. However, modern PaaS platforms reduce infrastructure management overhead.

**Key Files:**
- .github/workflows/deploy.yml: Main CI/CD pipeline
- docker-compose.yml: Local development environment
- apps/*/Dockerfile: Service-specific container configurations  
- packages/database/migrations/: Database schema changes
- deploy/: Deployment scripts and configurations
- turbo.json: Build and deployment task definitions


### Design Decisions

[{'decision': 'Use platform-specific deployment (Vercel for Next.js, Railway for Fastify) rather than single platform', 'rationale': 'Optimizes each service for its ideal platform - Vercel excels at Next.js with edge functions, Railway provides better backend service management', 'alternatives_considered': ['Single platform (Vercel/Railway for everything)', 'Self-managed Kubernetes cluster', 'AWS ECS/Fargate']}, {'decision': 'Implement blue-green deployment strategy for backend services', 'rationale': 'Ensures zero-downtime deployments for API services that handle payment processing and user data', 'alternatives_considered': ['Rolling deployments', 'Canary deployments', 'Direct replacement']}, {'decision': 'Use Supabase CLI for database migration management', 'rationale': 'Native integration with Supabase provides atomic migrations, rollback capabilities, and environment synchronization', 'alternatives_considered': ['Custom migration scripts', 'Prisma migrations', 'Manual SQL execution']}]
