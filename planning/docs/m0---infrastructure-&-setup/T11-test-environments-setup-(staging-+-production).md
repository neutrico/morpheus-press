---
area: setup
dependsOn: []
effort: 3
iteration: I1
key: T11
milestone: M0 - Infrastructure & Setup
priority: p0
title: Test Environments Setup (Staging + Production)
type: Task
---

# Test Environments Setup (Staging + Production)

## Acceptance Criteria

- [ ] **Staging environment successfully deploys and runs all services (API, web app, ML services) with isolated database**
  - Verification: Deploy to staging via CI/CD pipeline, verify health checks at staging.morpheus.app/health return 200, confirm separate Supabase project is used
- [ ] **Production environment deploys with zero-downtime and proper secret management**
  - Verification: Execute production deployment, verify no service interruption, confirm production secrets are isolated from staging via environment variable audit
- [ ] **Environment-specific ML service integration works with cost controls**
  - Verification: Run comic transformation in staging (uses mock/cheaper models), production (uses full RunPod endpoints), verify different API keys and rate limits
- [ ] **Automated CI/CD pipeline deploys to staging on main branch, production on release tags**
  - Verification: Create PR to main, verify staging auto-deploy. Create release tag, verify production deployment with manual approval gate
- [ ] **Environment configuration prevents cross-contamination of data and secrets**
  - Verification: Audit environment variables, verify staging cannot access production DB/APIs, test secret rotation affects only target environment

## Technical Notes

### Approach

Implement infrastructure-as-code approach using Docker Compose for local development, with separate Supabase projects for staging/production data isolation. Create environment-specific configuration management with secure secret handling and automated CI/CD pipelines. Establish tiered ML service integration (mock/staging/prod) to balance cost and testing fidelity. Set up comprehensive monitoring and logging with environment-appropriate alerting thresholds.


### Files to Modify

- **path**: apps/api/src/config/database.ts
- **changes**: Add environment-specific Supabase connection logic, connection pooling per environment
- **path**: apps/web/next.config.js
- **changes**: Add environment-specific build configurations, API endpoint URLs
- **path**: packages/shared/src/constants.ts
- **changes**: Add environment-specific constants (URLs, limits, feature flags)
- **path**: .github/workflows/ci.yml
- **changes**: Add staging deployment job triggered on main branch pushes

### New Files to Create

- **path**: packages/config/src/environments.ts
- **purpose**: Centralized environment configuration with type safety and validation
- **path**: docker-compose.staging.yml
- **purpose**: Staging-specific container orchestration with resource limits
- **path**: docker-compose.production.yml
- **purpose**: Production container configuration with performance optimizations
- **path**: .github/workflows/deploy-staging.yml
- **purpose**: Automated staging deployment pipeline with health checks
- **path**: .github/workflows/deploy-production.yml
- **purpose**: Production deployment with manual approval and rollback capability
- **path**: packages/ml-client/src/config.ts
- **purpose**: Environment-aware ML service endpoint and API key management
- **path**: scripts/setup-staging.sh
- **purpose**: Staging environment initialization and database seeding script
- **path**: scripts/deploy-production.sh
- **purpose**: Production deployment script with pre-flight checks and monitoring
- **path**: apps/api/src/middleware/environment.ts
- **purpose**: Request middleware to inject environment context and feature flags
- **path**: packages/config/src/secrets.ts
- **purpose**: Secure secret management with environment isolation
- **path**: docs/deployment.md
- **purpose**: Environment setup and deployment procedures documentation

### External Dependencies


- **dotenv-vault** ^1.25.0

  - Secure environment variable and secrets management across environments

- **zod** ^3.22.0

  - Runtime environment variable validation and type safety

- **@supabase/cli** ^1.110.0

  - Database migrations and Supabase project management

- **dockerode** ^4.0.0

  - Docker container management for local development environments

## Testing

### Unit Tests

- **File**: `packages/config/src/__tests__/environments.test.ts`
  - Scenarios: Environment variable loading for each env, Secret validation and masking, Configuration schema validation, Default value fallbacks
- **File**: `packages/ml-client/src/__tests__/config.test.ts`
  - Scenarios: Endpoint selection based on environment, API key configuration per environment, Model version mapping
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/environment.test.ts`
  - Scenarios: Database connection with staging config, ML service integration with staging endpoints, Authentication flow in staging environment, File upload/storage with staging buckets
- **File**: `apps/web/src/__tests__/e2e/environment.spec.ts`
  - Scenarios: Full comic transformation workflow in staging, User registration and auth in staging, Cross-service communication
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

- **task**: Setup separate Supabase projects for staging and production
- **done**: False
- **task**: Create environment configuration package with TypeScript types
- **done**: False
- **task**: Implement Docker Compose files for each environment
- **done**: False
- **task**: Configure GitHub Actions CI/CD pipelines with approval gates
- **done**: False
- **task**: Set up environment-specific ML service endpoints and API keys
- **done**: False
- **task**: Implement database migration strategy across environments
- **done**: False
- **task**: Create environment-specific monitoring and alerting
- **done**: False
- **task**: Test end-to-end deployment workflows
- **done**: False
- **task**: Document environment setup and deployment procedures
- **done**: False
- **task**: Security audit of secret management and environment isolation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Test environments are critical for the Morpheus platform to enable safe deployment pipelines, integration testing, and stakeholder preview without risking production data or user experience. Given the complexity of our stack (ML services, database migrations, multi-service architecture), we need isolated environments that mirror production for proper testing of novel-to-comic transformations, user workflows, and API integrations.

**Technical Approach:**
- Environment-specific configuration using dotenv-vault or similar for secrets management
- Separate Supabase projects for staging/production with database branching
- Docker containerization with environment-specific docker-compose files
- CI/CD pipeline integration with GitHub Actions for automated deployments
- Separate RunPod endpoints/API keys for staging ML workloads
- Environment-specific feature flags using tools like LaunchDarkly or custom implementation
- Monitoring with different log levels and alerting thresholds per environment

**Dependencies:**
- External: [@supabase/supabase-js, dotenv, docker, github-actions, playwright for e2e testing]
- Internal: [database schemas, API routes, ML service integrations, authentication flows]

**Risks:**
- Cost escalation: Multiple ML inference endpoints and database instances
- Data sync issues: Staging data becoming stale or inconsistent
- Configuration drift: Environments diverging over time
- Secret management: Accidentally using production secrets in staging
- ML model versioning: Different model versions across environments causing inconsistent results

**Complexity Notes:**
More complex than typical web apps due to ML pipeline dependencies, Supabase project management, and the need to mock/stage expensive AI services. The multi-tenancy nature of the comic transformation workflow adds complexity to test data management.

**Key Files:**
- packages/config/environments.ts: Environment configuration management
- docker-compose.staging.yml: Staging container orchestration
- .github/workflows/deploy-staging.yml: Staging deployment pipeline
- apps/api/src/config/database.ts: Environment-specific DB connections
- packages/ml-client/src/config.ts: ML service endpoint configuration


### Design Decisions

[{'decision': 'Use Supabase branching for database environments rather than single shared instance', 'rationale': 'Provides true isolation, enables safe schema migrations, and prevents test data pollution', 'alternatives_considered': ['Shared database with prefixed tables', 'Local PostgreSQL instances', 'Database-per-feature-branch']}, {'decision': 'Implement tiered ML service usage (mock → staging → production)', 'rationale': 'Reduces costs while maintaining realistic testing, with fallbacks for different testing scenarios', 'alternatives_considered': ['Full ML services in all environments', 'Mock-only for staging', 'Shared ML endpoints']}, {'decision': 'Environment-specific feature flags system', 'rationale': 'Enables testing new features in staging without production risk and gradual rollouts', 'alternatives_considered': ['No feature flags', 'Third-party service only', 'Database-driven flags only']}]
