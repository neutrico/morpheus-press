# Contributing to Morpheus Press

Thank you for your interest in contributing to Morpheus Press! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Issue Management](#issue-management)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## 🚀 Getting Started

### Prerequisites

- Node.js 20+ and pnpm
- Docker and Docker Compose
- VSCode with DevContainer extension (recommended)
- GitHub CLI (`gh`)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/neutrico/morpheus-press.git
   cd morpheus-press
   ```

2. Open in DevContainer (recommended) or install dependencies:
   ```bash
   pnpm install
   ```

3. Start development environment:
   ```bash
   pnpm dev
   ```

## 💼 Development Workflow

### 1. Find or Create an Issue

- Browse [existing issues](https://github.com/neutrico/morpheus-press/issues)
- Check the [project board](https://github.com/orgs/neutrico/projects/1) for available tasks
- If creating a new issue, use the appropriate template:
  - **Bug Report**: For bugs or unexpected behavior
  - **Feature Request**: For new features or enhancements
  - **Development Task**: For technical implementation work

### 2. Assign Yourself

- Comment on the issue to indicate you're working on it
- Ask for assignment if you don't have write access

### 3. Create a Branch

```bash
git checkout -b feature/T24-your-feature-name
# or
git checkout -b fix/issue-123-bug-description
```

Branch naming conventions:
- `feature/T[XX]-description` - For new features
- `fix/issue-[number]-description` - For bug fixes
- `chore/description` - For maintenance tasks
- `docs/description` - For documentation updates

### 4. Make Your Changes

Follow our [coding standards](#coding-standards) and ensure:
- Code follows existing patterns in the codebase
- Tests are added/updated for your changes
- Documentation is updated if needed
- No security vulnerabilities introduced

### 5. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add dialogue extraction service"
git commit -m "fix: resolve image generation timeout"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for character service"
```

Commit types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `style:` - Code style changes (formatting, etc.)

### 6. Push and Create PR

```bash
git push origin your-branch-name
```

Then create a Pull Request using the [PR template](.github/PULL_REQUEST_TEMPLATE.md).

## 🎯 Issue Management

### Issue Lifecycle

1. **Triage** (`status:triage`) - New issue, needs review
2. **Ready** (`status:ready`) - Approved and ready for implementation
3. **In Progress** (`status:in-progress`) - Currently being worked on
4. **Blocked** (`status:blocked`) - Blocked by dependencies or issues
5. **Done** (`status:done`) - Completed and closed

### Labels

Issues are labeled by:

**Area:**
- `area: setup` - Infrastructure and setup
- `area: backend` - Backend API and services
- `area: ml` - Machine learning
- `area: image-gen` - Image generation
- `area: comic` - Comic assembly
- And more...

**Priority:**
- `priority:p0` - Critical (blocks development)
- `priority:p1` - High (major feature)
- `priority:p2` - Medium (minor feature)
- `priority:p3` - Low (enhancement)

**Type:**
- `Task` - Development task
- `Feature` - New feature
- `Bug` - Bug report

### Milestones

The project is organized into milestones:

- **M0 - Infrastructure & Setup**: Dev environment, CI/CD, testing
- **M1 - Backend Services**: API, database, authentication
- **M2 - ML Training & Development**: ML models and training
- **M3 - Content Generation Pipeline**: Image generation
- **M4 - Dashboard & UI**: Web interface
- **M5 - Product Assembly**: Comic layout and export
- **M6 - Commerce & Distribution**: E-commerce and distribution
- **M7 - Launch & Release**: Final integration and deployment

## 🔄 Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   pnpm test                    # Run all tests
   pnpm test:backend            # Backend tests only
   pnpm type-check              # TypeScript type checking
   pnpm build                   # Production build
   ```

2. **Code Review Checklist**
   - [ ] Code follows project style guidelines
   - [ ] Tests are comprehensive and passing
   - [ ] Documentation updated (if needed)
   - [ ] No security vulnerabilities
   - [ ] Performance impact considered

3. **Link Related Issues**
   - Use "Closes #123" or "Fixes #123" in PR description
   - Reference related issues with "#123"

### PR Review

- PRs require at least one approval before merging
- Address all review comments
- Keep PRs focused and reasonably sized
- Rebase on main if conflicts arise

### Merge Strategy

- **Squash and merge** for most PRs (keeps history clean)
- **Merge commit** for release PRs or multiple logical commits
- Delete branch after merging

## 📝 Coding Standards

### General Principles

- **SOLID Principles**: Follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY**: Don't Repeat Yourself - Extract reusable logic
- **KISS**: Keep It Simple, Stupid - Simplest solution that works
- **Separation of Concerns**: UI ≠ business logic ≠ data fetching

### TypeScript

- Use strict TypeScript configuration
- Prefer `interface` over `type` for object shapes
- Use `const` for immutable values
- Avoid `any` - use `unknown` and type guards instead

### React

- Use functional components with hooks
- Memoize expensive computations with `useMemo`
- Memoize callbacks with `useCallback`
- Use `React.memo()` for expensive components
- Avoid inline functions/objects in JSX props

### Backend (Fastify)

- Services are singletons with constructor DI
- Routes are async functions registered via `app.register()`
- Use Zod schemas for request/response validation
- Always add error handlers (try/catch)
- Use structured logging with `fastify.log`

### Testing

- Write tests FIRST for new features (TDD)
- Test happy path, edge cases, and error conditions
- Mock external dependencies
- Aim for high coverage on business logic

## 🧪 Testing Guidelines

### Test Structure

```typescript
describe('ServiceName', () => {
  describe('methodName', () => {
    it('should handle happy path', async () => {
      // Arrange
      const input = {...};
      
      // Act
      const result = await service.method(input);
      
      // Assert
      expect(result).toBe(expected);
    });
    
    it('should handle error case', async () => {
      // Test error handling
    });
  });
});
```

### Test Commands

```bash
# All tests
pnpm test

# Backend tests only
pnpm test:backend

# Watch mode
pnpm test:watch

# E2E tests
cd apps/dashboard && pnpm test:e2e
```

### Test Coverage

- Aim for >80% coverage on business logic
- 100% coverage on critical paths (auth, payments, data integrity)
- Don't test framework code or trivial getters/setters

## 🤖 Automation

### Task Automation

For tasks with **HIGH AI effectiveness**, you can trigger automated code generation:

1. Comment `/automate` on the issue
2. Wait for the automation workflow to create a PR
3. Review the generated code and fix TODO comments
4. Test and refine

See [Task Automation README](../scripts/automation/README.md) for details.

## 📚 Additional Resources

- [Project Management Guide](PROJECT_MANAGEMENT.md)
- [Architecture Documentation](../docs/)
- [API Documentation](../apps/backend/README.md)
- [Database Schema](../supabase/migrations/)

## 💬 Getting Help

- **GitHub Discussions**: Ask questions and discuss ideas
- **Issues**: Report bugs or request features
- **Project Board**: View current work and roadmap

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
