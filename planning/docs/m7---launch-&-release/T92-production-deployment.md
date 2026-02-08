---
area: release
dependsOn:
- T91
effort: 3
iteration: I7
key: T92
milestone: M7 - Launch & Release
priority: p0
title: Production Deployment
type: Task
---

# Production Deployment

## Acceptance Criteria

- [ ] **All services (storefront, dashboard, backend) are successfully deployed and accessible via HTTPS with proper SSL certificates**
  - Verification: curl -I https://app.morpheus.com returns 200, curl -I https://dashboard.morpheus.com returns 200, curl -I https://api.morpheus.com/health returns 200
- [ ] **Comic generation workflow completes end-to-end in production environment with proper job queue processing**
  - Verification: Submit novel through storefront, verify job creation in Redis, confirm comic generation via RunPod API, validate final output delivery
- [ ] **System handles concurrent load with auto-scaling enabled and response times under 2s for API calls**
  - Verification: Load test with 100 concurrent users, verify auto-scaling triggers, measure 95th percentile response times < 2000ms
- [ ] **Monitoring and alerting system captures critical metrics and sends notifications for failures**
  - Verification: Health checks report green status, error tracking captures exceptions, uptime monitoring shows >99.5% availability
- [ ] **Database migrations and environment configurations are properly applied across staging and production**
  - Verification: Run npm run db:migrate in production, verify all tables exist, confirm environment variables are correctly set

## Technical Notes

### Approach

Deploy Next.js applications to Vercel with environment-specific configurations and CDN optimization. 
Containerize the Fastify backend and deploy to a managed container platform (Railway/Render) with auto-scaling enabled.
Implement a job queue system using Redis and BullMQ to handle asynchronous comic generation tasks.
Set up comprehensive monitoring with health check endpoints, error tracking, and performance metrics.
Create a CI/CD pipeline that runs tests, builds containers, and deploys through staging to production environments.


### Files to Modify

- **path**: apps/backend/package.json
- **changes**: Add production dependencies, health check scripts, and container startup commands
- **path**: apps/backend/src/server.ts
- **changes**: Add graceful shutdown handling, health check endpoints, and production logging
- **path**: apps/dashboard/next.config.js
- **changes**: Configure CDN settings, environment variables, and performance optimizations
- **path**: apps/storefront/next.config.js
- **changes**: Add image optimization, CDN integration, and production build settings
- **path**: packages/database/src/index.ts
- **changes**: Implement connection pooling, read replica support, and production connection strings
- **path**: .github/workflows/test.yml
- **changes**: Extend to include deployment pipeline and environment promotion

### New Files to Create

- **path**: apps/backend/Dockerfile
- **purpose**: Containerize Fastify application with multi-stage build and security hardening
- **path**: apps/backend/src/health.ts
- **purpose**: Comprehensive health check endpoints for Kubernetes readiness and liveness probes
- **path**: apps/backend/src/queue/index.ts
- **purpose**: Redis-based job queue implementation using BullMQ for comic generation tasks
- **path**: docker-compose.prod.yml
- **purpose**: Production container orchestration with proper networking and volume mounts
- **path**: k8s/backend-deployment.yaml
- **purpose**: Kubernetes deployment manifest with auto-scaling, resource limits, and health checks
- **path**: k8s/ingress.yaml
- **purpose**: Nginx ingress controller configuration with SSL termination and load balancing
- **path**: terraform/main.tf
- **purpose**: Infrastructure as code for cloud resources, networking, and managed services
- **path**: terraform/monitoring.tf
- **purpose**: Monitoring stack deployment with Prometheus, Grafana, and alerting rules
- **path**: .env.production
- **purpose**: Production environment variables with database URLs, API keys, and service endpoints
- **path**: scripts/deploy.sh
- **purpose**: Deployment automation script with rollback capability and health verification
- **path**: scripts/migrate.sh
- **purpose**: Database migration script with backup and rollback procedures
- **path**: monitoring/alerts.yaml
- **purpose**: Alert manager configuration for critical system notifications

### External Dependencies


- **bullmq** ^5.0.0

  - Robust job queue system for handling comic generation tasks asynchronously

- **ioredis** ^5.3.0

  - Redis client for job queue and caching in production environment

- **@sentry/node** ^7.0.0

  - Error tracking and performance monitoring in production

- **pino** ^8.0.0

  - High-performance JSON logger for production logging and observability

- **helmet** ^7.0.0

  - Security headers and hardening for the Fastify backend in production

- **@fastify/rate-limit** ^9.0.0

  - Rate limiting to protect against abuse and ensure fair resource usage

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/health.test.ts`
  - Scenarios: Health endpoint returns proper status, Database connection check, Redis connectivity validation
- **File**: `apps/backend/src/__tests__/queue.test.ts`
  - Scenarios: Job creation and processing, Queue failure handling, Job retry logic
### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/deployment.test.ts`
  - Scenarios: Full comic generation pipeline, Environment variable loading, Database connection pooling, External API connectivity
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 2
- **Testing**: 3
- **Documentation**: 1
- **Total**: 14

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Set up container registry and build multi-stage Dockerfiles
- **done**: False
- **task**: Configure Vercel deployments for Next.js apps with environment-specific settings
- **done**: False
- **task**: Deploy Fastify backend to managed container platform with auto-scaling
- **done**: False
- **task**: Implement Redis job queue system with BullMQ for asynchronous processing
- **done**: False
- **task**: Set up Supabase production database with connection pooling and read replicas
- **done**: False
- **task**: Configure CDN integration for static assets and image delivery
- **done**: False
- **task**: Implement comprehensive monitoring with health checks and error tracking
- **done**: False
- **task**: Create CI/CD pipeline with automated testing and deployment
- **done**: False
- **task**: Perform load testing and validate auto-scaling behavior
- **done**: False
- **task**: Configure security measures including rate limiting, HTTPS, and secret management
- **done**: False
- **task**: Create runbooks and deployment documentation
- **done**: False
- **task**: Conduct production readiness review and go-live checklist
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Production deployment is the final critical step to launch Morpheus to real users. This involves setting up robust, scalable infrastructure that can handle real traffic, ensure high availability, implement proper monitoring, and maintain security standards. The platform needs to serve both the customer-facing storefront and creator dashboard while processing computationally intensive novel-to-comic transformations. This is essential for generating revenue and validating the product-market fit.

**Technical Approach:**
- Container orchestration with Docker + Kubernetes or managed services (Vercel for Next.js apps, Railway/Render for Fastify backend)
- Multi-environment setup (staging, production) with environment-specific configurations
- CDN integration for static assets and image delivery (Cloudflare/AWS CloudFront)
- Load balancing and auto-scaling for the Fastify backend
- Database connection pooling and read replicas for Supabase
- CI/CD pipeline with automated testing, building, and deployment
- Infrastructure as Code (Terraform/Pulumi) for reproducible deployments
- Comprehensive monitoring with health checks, metrics, and alerting
- Security hardening: HTTPS, rate limiting, DDoS protection, secret management

**Dependencies:**
- External: Docker, Kubernetes/managed platform, monitoring tools (DataDog/New Relic), CDN provider
- Internal: All application services must be production-ready, database migrations, environment configuration management

**Risks:**
- Downtime during initial deployment: Use blue-green or rolling deployments
- Database migration failures: Implement rollback procedures and test migrations thoroughly
- Resource exhaustion under load: Implement auto-scaling and load testing
- Secret leakage: Use proper secret management (Vault, K8s secrets, platform-managed)
- RunPod API rate limits/failures: Implement circuit breakers and fallback mechanisms
- Cost overruns: Set up billing alerts and resource quotas

**Complexity Notes:**
This is significantly more complex than initially appears. Beyond basic deployment, it requires orchestrating multiple services (frontend, backend, database, ML APIs), handling asynchronous job processing, managing secrets across environments, implementing proper observability, and ensuring the system can handle the computational load of image generation at scale.

**Key Files:**
- apps/backend/Dockerfile: Containerize Fastify application
- apps/dashboard/next.config.js: Production optimizations and environment variables
- apps/storefront/next.config.js: CDN configuration and performance tuning
- packages/database/migrations/: Production database schema
- .github/workflows/deploy.yml: CI/CD pipeline configuration
- docker-compose.prod.yml: Production service orchestration
- k8s/: Kubernetes manifests for deployment, services, ingress
- terraform/: Infrastructure as code definitions


### Design Decisions

[{'decision': 'Hybrid deployment: Vercel for Next.js frontends, managed container service for Fastify backend', 'rationale': 'Leverages platform strengths - Vercel excels at Next.js deployment with global CDN, while managed containers provide flexibility for the backend without K8s complexity', 'alternatives_considered': ['Full Kubernetes cluster', 'All-in-one platform like Railway', 'AWS ECS with ALB']}, {'decision': 'Implement asynchronous job processing with Redis/BullMQ for comic generation', 'rationale': 'Comic generation is CPU/time intensive and should not block HTTP requests. Queue system allows for better resource management and user experience', 'alternatives_considered': ['Synchronous processing with long timeouts', 'Serverless functions', 'Background jobs in database']}, {'decision': 'Use Supabase managed PostgreSQL with connection pooling', 'rationale': 'Supabase provides production-grade managed database with built-in connection pooling, backups, and monitoring without operational overhead', 'alternatives_considered': ['Self-managed PostgreSQL on VPS', 'AWS RDS', 'PlanetScale MySQL']}]
