---
area: setup
dependsOn:
- T4
effort: 3
iteration: I1
key: T6
milestone: M0 - Infrastructure & Setup
priority: p0
title: CI/CD Workflows Setup
type: Task
---

# CI/CD Workflows Setup

## Acceptance Criteria

- [ ] **CI pipeline successfully runs tests and linting for all affected packages when code is pushed to any branch**
  - Verification: Push code changes and verify GitHub Actions runs Turborepo selective builds with test results in PR checks
- [ ] **Staging deployment automatically triggers on main branch merge and successfully deploys all services**
  - Verification: Merge PR to main and verify staging URLs are accessible with latest changes within 10 minutes
- [ ] **Production deployment requires manual approval and completes successfully with zero downtime**
  - Verification: Trigger production workflow, approve deployment, verify services remain accessible during deployment
- [ ] **ML API integration tests run with proper mocking and fallback handling during CI**
  - Verification: CI logs show ML tests passing with mock responses and timeout handling under 30 seconds per test
- [ ] **Visual regression tests validate comic generation output consistency**
  - Verification: Percy or similar tool shows no unexpected visual changes in comic generation pipeline

## Technical Notes

### Approach

Implement GitHub Actions workflows leveraging Turborepo's selective builds and remote caching. Create separate CI pipeline for testing/linting and CD pipelines for staging/production deployments. Use Docker containers for consistent test environments and implement proper secret management for ML API keys. Include visual regression testing for comic generation outputs and database migration validation.


### Files to Modify

- **path**: turbo.json
- **changes**: Add CI-specific pipeline configurations with selective builds and caching strategies
- **path**: package.json
- **changes**: Add CI scripts for testing, linting, and build validation across workspaces
- **path**: apps/backend/package.json
- **changes**: Add test:ci script with proper environment setup and ML API mocking
- **path**: apps/dashboard/package.json
- **changes**: Add build:ci and test:e2e scripts with Playwright configuration

### New Files to Create

- **path**: .github/workflows/ci.yml
- **purpose**: Main CI pipeline with matrix builds, testing, and linting for all packages
- **path**: .github/workflows/deploy-staging.yml
- **purpose**: Automated staging deployment triggered on main branch changes
- **path**: .github/workflows/deploy-prod.yml
- **purpose**: Production deployment with manual approval gates and rollback capability
- **path**: .github/workflows/visual-regression.yml
- **purpose**: Visual testing pipeline for comic generation output validation
- **path**: docker-compose.test.yml
- **purpose**: Testing environment with Supabase, Redis, and ML API mocks
- **path**: .github/scripts/setup-test-env.sh
- **purpose**: Environment setup script for CI runners with dependency installation
- **path**: packages/shared/src/config/ci.ts
- **purpose**: CI-specific configuration and environment variable management
- **path**: apps/backend/src/__tests__/setup/ml-mocks.ts
- **purpose**: Mock implementations for OpenAI/Anthropic APIs during testing
- **path**: .env.ci.example
- **purpose**: Template for CI environment variables with safe defaults

### External Dependencies


- **@vercel/ncc** ^0.38.0

  - Bundle GitHub Actions for faster execution

- **docker/build-push-action** v5

  - Build and push Docker images in CI pipeline

- **actions/cache** v3

  - Cache node_modules and Turborepo builds for faster CI

- **peaceiris/actions-gh-pages** v3

  - Deploy Storybook and documentation to GitHub Pages

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/workflows/ci.test.ts`
  - Scenarios: Turborepo selective build configuration, Environment variable validation, ML API mock responses
- **File**: `packages/shared/src/__tests__/config.test.ts`
  - Scenarios: CI environment detection, Secret management validation, Build configuration parsing
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/ml-pipeline.test.ts`
  - Scenarios: End-to-end comic generation with mocked APIs, Database migration validation, File upload and processing workflow
- **File**: `apps/dashboard/src/__tests__/e2e/deployment.spec.ts`
  - Scenarios: Staging deployment health checks, Authentication flow with test credentials, Cross-service communication validation
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

- **task**: Research and plan GitHub Actions workflow structure for monorepo
- **done**: False
- **task**: Configure Turborepo selective builds and remote caching for CI
- **done**: False
- **task**: Set up Docker test environment with service dependencies
- **done**: False
- **task**: Implement ML API mocking strategy with rate limit handling
- **done**: False
- **task**: Create CI workflow with matrix builds for parallel testing
- **done**: False
- **task**: Configure staging deployment pipeline with health checks
- **done**: False
- **task**: Set up production deployment with approval gates and monitoring
- **done**: False
- **task**: Implement visual regression testing for comic generation
- **done**: False
- **task**: Configure GitHub secrets and environment-specific variables
- **done**: False
- **task**: Test end-to-end CI/CD flow with feature branch and deployment
- **done**: False
- **task**: Document CI/CD processes and troubleshooting guide
- **done**: False

## Agent Notes

### Research Findings

**Context:**
CI/CD workflows are critical for the Morpheus project to ensure code quality, automated testing, and reliable deployments across a complex monorepo with multiple services (backend API, dashboard, storefront) and ML integrations. This solves the problem of manual testing/deployment overhead and provides fast feedback loops for developers working on novel-to-comic transformations.

**Technical Approach:**
GitHub Actions with matrix builds for the Turborepo monorepo structure. Implement parallel testing strategies for Vitest unit tests and Playwright E2E tests. Use Docker for consistent environments and implement staging/production deployment pipelines with proper secret management for OpenAI/Anthropic API keys and Supabase credentials. Include ML model validation steps and image generation testing.

**Dependencies:**
- External: GitHub Actions runners, Docker Hub/GHCR, Vercel/Railway for deployments
- Internal: Package.json scripts in each workspace, Turborepo build system, Supabase migrations, RunPod API integration tests

**Risks:**
- ML API rate limits during CI: implement test mocking and dedicated test API keys with lower quotas
- Monorepo build complexity: use Turborepo's remote caching and selective builds based on changed packages
- Secret management sprawl: centralize in GitHub secrets with environment-specific organization
- Long-running image generation tests: implement test timeouts and fallback mock responses

**Complexity Notes:**
More complex than typical due to ML service dependencies, multiple deployment targets (dashboard vs storefront), and need for visual regression testing for comic generation outputs. The monorepo structure adds coordination complexity but Turborepo helps significantly.

**Key Files:**
- .github/workflows/ci.yml: main CI pipeline with matrix strategy
- .github/workflows/deploy-staging.yml: staging deployment automation  
- .github/workflows/deploy-prod.yml: production deployment with manual approval
- turbo.json: build and test pipeline configuration
- docker-compose.test.yml: testing environment setup


### Design Decisions

[{'decision': 'GitHub Actions with Turborepo remote caching', 'rationale': 'Native GitHub integration, excellent monorepo support, cost-effective for open source, remote caching reduces build times', 'alternatives_considered': ['Jenkins (too much maintenance overhead)', 'GitLab CI (vendor lock-in concerns)', 'CircleCI (cost for private repos)']}, {'decision': 'Matrix builds for Node.js versions and test environments', 'rationale': 'Ensures compatibility across Node 18/20, parallel execution for faster feedback, separate staging/prod validation', 'alternatives_considered': ['Single Node version (risky for compatibility)', 'Sequential builds (too slow for monorepo)']}, {'decision': 'Separate workflows for CI vs CD with environment protection', 'rationale': 'Production deployments need manual approval, staging can be automatic, allows for different secret scopes', 'alternatives_considered': ['Single workflow with conditional steps (harder to manage)', 'Fully manual deployments (defeats automation purpose)']}]
