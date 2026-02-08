---
area: backend
dependsOn: []
effort: 1
iteration: I2
key: T33
milestone: M1 - Backend Services
priority: p1
title: Code Review & Standards Process
type: Task
---

# Code Review & Standards Process

## Acceptance Criteria

- [ ] **Pre-commit hooks prevent commits with linting errors, type errors, or formatting issues**
  - Verification: Attempt to commit code with ESLint errors - should fail with specific error messages
- [ ] **GitHub Actions PR workflow runs comprehensive checks (lint, type-check, security scan) and reports status**
  - Verification: Create PR with intentional code issues - workflow should fail with detailed reports
- [ ] **SonarCloud integration provides code quality metrics with <5% technical debt ratio**
  - Verification: Check SonarCloud dashboard shows project metrics and quality gate passes
- [ ] **Shared ESLint config enforces consistent standards across backend/frontend with custom rules**
  - Verification: Run 'npm run lint' in apps/backend and apps/frontend - both use shared config with zero errors
- [ ] **Conventional commits are enforced with automated semantic versioning**
  - Verification: Attempt commit with invalid format - should fail; valid commits trigger correct version bumps

## Technical Notes

### Approach

Create a shared ESLint configuration package that extends TypeScript-ESLint with custom rules for our Fastify/Next.js patterns. Set up pre-commit hooks using Husky and lint-staged to run incremental checks. Implement GitHub Actions workflows that run comprehensive linting, type checking, and security scans on PRs. Integrate SonarCloud for ongoing code quality metrics and technical debt tracking. Establish conventional commit standards with automated semantic versioning.


### Files to Modify

- **path**: turbo.json
- **changes**: Add lint, format, type-check tasks to pipeline configuration
- **path**: package.json
- **changes**: Add root-level scripts for lint:all, format:all, prepare (husky install)
- **path**: apps/backend/package.json
- **changes**: Add lint, format, type-check scripts and eslint-config dependency
- **path**: apps/frontend/package.json
- **changes**: Add lint, format, type-check scripts and eslint-config dependency
- **path**: .gitignore
- **changes**: Add SonarCloud and lint cache directories

### New Files to Create

- **path**: packages/eslint-config/package.json
- **purpose**: Shared ESLint configuration package definition
- **path**: packages/eslint-config/src/base.js
- **purpose**: Base ESLint configuration with TypeScript and common rules
- **path**: packages/eslint-config/src/backend.js
- **purpose**: Backend-specific rules for Fastify, Node.js patterns
- **path**: packages/eslint-config/src/frontend.js
- **purpose**: Frontend-specific rules for React, Next.js patterns
- **path**: packages/eslint-config/src/rules/fastify.js
- **purpose**: Custom ESLint rules for Fastify route patterns
- **path**: packages/eslint-config/src/rules/supabase.js
- **purpose**: Custom rules for Supabase query patterns
- **path**: .husky/pre-commit
- **purpose**: Git pre-commit hook running lint-staged
- **path**: .husky/commit-msg
- **purpose**: Conventional commit message validation
- **path**: .github/workflows/code-quality.yml
- **purpose**: Comprehensive PR checks (lint, type-check, security, quality)
- **path**: .github/workflows/release.yml
- **purpose**: Automated semantic release workflow
- **path**: sonar-project.properties
- **purpose**: SonarCloud project configuration
- **path**: .lintstagedrc.js
- **purpose**: Lint-staged configuration for pre-commit checks
- **path**: .commitlintrc.js
- **purpose**: Conventional commit validation rules
- **path**: apps/backend/.eslintrc.js
- **purpose**: Backend ESLint configuration extending shared config
- **path**: apps/frontend/.eslintrc.js
- **purpose**: Frontend ESLint configuration extending shared config
- **path**: .prettierrc.js
- **purpose**: Shared Prettier configuration
- **path**: .prettierignore
- **purpose**: Files to exclude from Prettier formatting

### External Dependencies


- **@typescript-eslint/eslint-plugin** ^6.0.0

  - TypeScript-specific linting rules for our TS-heavy codebase

- **eslint-plugin-security** ^1.7.0

  - Security vulnerability detection for our API endpoints

- **husky** ^8.0.0

  - Git hooks management for pre-commit linting

- **lint-staged** ^14.0.0

  - Run linters only on staged files for performance

- **prettier** ^3.0.0

  - Code formatting consistency across team

- **commitizen** ^4.3.0

  - Standardized commit message format

- **@sonarjs/eslint-plugin** ^0.23.0

  - Code smell detection and complexity analysis

## Testing

### Unit Tests

- **File**: `packages/eslint-config/src/__tests__/rules.test.ts`
  - Scenarios: Custom Fastify route patterns detected correctly, Supabase query patterns enforced, ML service call patterns validated, TypeScript strict mode violations caught
- **File**: `packages/eslint-config/src/__tests__/config.test.ts`
  - Scenarios: Backend config extends base with Fastify rules, Frontend config extends base with React/Next.js rules, Shared config loads without conflicts
### Integration Tests

- **File**: `__tests__/integration/code-quality-pipeline.test.ts`
  - Scenarios: Full lint pipeline runs on sample backend code, Pre-commit hooks integrate with git workflow, GitHub Actions workflow completes successfully
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

- **task**: Create packages/eslint-config with base, backend, frontend configurations
- **done**: False
- **task**: Implement custom ESLint rules for Fastify and Supabase patterns
- **done**: False
- **task**: Set up Husky pre-commit hooks with lint-staged
- **done**: False
- **task**: Configure GitHub Actions workflows for PR checks and releases
- **done**: False
- **task**: Integrate SonarCloud for code quality metrics
- **done**: False
- **task**: Add Snyk security scanning to pipeline
- **done**: False
- **task**: Configure conventional commits with semantic-release
- **done**: False
- **task**: Update all package.json files with lint/format scripts
- **done**: False
- **task**: Test pre-commit hooks and GitHub Actions workflows
- **done**: False
- **task**: Document code standards and review process in README
- **done**: False

## Agent Notes

### Research Findings

**Context:**
A robust code review and standards process is critical for Morpheus as we scale the development team and ensure consistent, maintainable code quality across our multi-service architecture. This task establishes automated and manual review processes that catch bugs early, enforce TypeScript/JavaScript standards, maintain security practices, and ensure performance considerations for our ML-heavy workloads. Without proper standards, our complex monorepo with backend services, frontend apps, and ML integrations could quickly become unmaintainable.

**Technical Approach:**
Implement a multi-layered approach: (1) Pre-commit hooks with Husky + lint-staged for immediate feedback, (2) ESLint/Prettier configuration with custom rules for our stack, (3) GitHub Actions workflows for automated PR checks, (4) SonarCloud integration for code quality metrics, (5) Automated security scanning with Snyk, (6) Performance budgets for bundle analysis, (7) Custom ESLint rules for our specific patterns (Fastify routes, Supabase queries, ML service calls). Use conventional commits and semantic versioning across the monorepo.

**Dependencies:**
- External: eslint, prettier, husky, lint-staged, @typescript-eslint/*, commitizen, semantic-release, sonarcloud, snyk
- Internal: All existing services need linting configuration, CI/CD pipeline setup, documentation updates

**Risks:**
- Developer friction: too strict rules slow development - mitigation: gradual rollout with team feedback
- Performance overhead: extensive linting on large codebase - mitigation: incremental linting, caching strategies
- Configuration drift: different standards across packages - mitigation: shared config packages, automated synchronization
- False positives in ML code: AI-generated content might trigger unusual patterns - mitigation: custom rules for ML workflows

**Complexity Notes:**
More complex than initially estimated due to our diverse stack (Fastify + Next.js + ML services) requiring different linting strategies. The monorepo structure adds complexity for shared configurations. However, existing tooling maturity (ESLint 9+, TypeScript 5+) makes implementation more straightforward than building custom solutions.

**Key Files:**
- packages/eslint-config/: shared ESLint configurations
- .github/workflows/code-quality.yml: automated PR checks
- apps/backend/.eslintrc.js: Fastify-specific rules
- apps/frontend/.eslintrc.js: Next.js-specific rules
- turbo.json: add lint/format tasks to pipeline
- .husky/: git hooks configuration
- sonar-project.properties: code quality metrics


### Design Decisions

[{'decision': 'Shared ESLint configuration package with service-specific overrides', 'rationale': 'Ensures consistency across monorepo while allowing flexibility for different application types (Fastify vs Next.js vs ML services)', 'alternatives_considered': ['Single root ESLint config', 'Completely separate configs per service', 'External preset like Airbnb']}, {'decision': 'Husky + lint-staged for pre-commit hooks with escape hatch', 'rationale': 'Catches issues early without blocking emergency fixes, provides immediate developer feedback', 'alternatives_considered': ['Server-side only validation', 'IDE-only linting', 'Manual review process only']}, {'decision': 'SonarCloud integration for technical debt tracking', 'rationale': 'Provides metrics for code coverage, complexity, and security vulnerabilities with good GitHub integration', 'alternatives_considered': ['CodeClimate', 'Codacy', 'Self-hosted SonarQube']}]
