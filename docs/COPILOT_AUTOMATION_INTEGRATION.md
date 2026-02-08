# Copilot + Automation Integration - Quick Start

**End-to-end workflow**: Planning → GitHub Issue → Automation → Copilot → Merge

## 🎯 Overview

System składa się z 3 warstw:

1. **Planning System** (`planning/docs/`, `planning/issues/*.yaml`)
2. **Automation Layer** (GitHub Actions + CLI scripts)
3. **Copilot Agent** (reviews + refines generated code)

```
Planning Specs → GitHub Issue → Auto-Generate → Copilot Reviews → Human Approves → Merge
```

## 🚀 Complete Workflow

### Step 1: Create GitHub Issues from Planning

```bash
# Preview what issues would be created
python scripts/planning/create-github-issues.py --dry-run

# Create all issues
python scripts/planning/create-github-issues.py

# Create only HIGH AI effectiveness tasks
python scripts/planning/create-github-issues.py --ai-high-only

# Create single task
python scripts/planning/create-github-issues.py T24
```

**Result**: GitHub issues z pełną specyfikacją + automation hints

### Step 2: Trigger Automation

**Option A: Auto-trigger (GitHub Actions)**

```bash
# On GitHub:
1. Go to issue (e.g., #123)
2. Assign to @copilot
   → GitHub Actions automatically triggers
   → Creates PR with generated code
```

**Option B: Manual trigger (comment)**

```bash
# On GitHub issue:
/automate

# GitHub Actions will:
# 1. Extract task key (T24)
# 2. Check AI effectiveness
# 3. Run automation generator
# 4. Create PR branch
# 5. Assign PR to @copilot
```

**Option C: Local trigger (CLI)**

```bash
# Manual generation (local)
python scripts/automation/task-automation-agent.py T24

# Or use specific generator:
./scripts/automation/generators/setup-supabase.sh T24
./scripts/automation/generators/setup-tests.sh T27 unit
python scripts/automation/generators/api-generator.py T25
```

### Step 3: Copilot Reviews Auto-Generated Code

**Copilot automatically:**

1. Receives PR assignment
2. Reads task spec from `planning/docs/`
3. Reviews generated code
4. Fixes TODO comments
5. Refines implementation
6. Runs tests
7. Pushes fixes to PR branch

**Copilot workflow:**

```bash
# 1. Check for generated code
gh pr view <PR_NUMBER>

# 2. Read task spec (Copilot does this automatically)
cat planning/docs/m1---backend-services/T24-supabase-database-setup-with-rls.md

# 3. Search for TODOs
grep -r "TODO" apps/backend/src/

# 4. Implement TODOs
# (Copilot generates code based on specs)

# 5. Run tests
pnpm test

# 6. Push fixes
git push
```

### Step 4: Human Review & Approval

```bash
# 1. Review PR on GitHub
gh pr view <PR_NUMBER> --web

# 2. Check CI/CD status
# (tests, linting, type checking)

# 3. Test manually
pnpm dev:backend
# Test API endpoints, DB migrations, etc.

# 4. Approve & merge
gh pr review <PR_NUMBER> --approve
gh pr merge <PR_NUMBER>
```

## 📊 Examples

### Example 1: Database Setup (T24)

**1. Create issue:**

```bash
python scripts/planning/create-github-issues.py T24
```

**2. On GitHub:**

- Go to issue #X
- Assign to @copilot
- **OR** comment: `/automate`

**3. Automation runs:**

- Generates: `supabase/migrations/20260208_T24_setup.sql`
- Generates: `apps/backend/src/services/database.service.ts`
- Generates: `apps/backend/src/__tests__/database.test.ts`
- Creates PR: "feat: T24 - Supabase Database Setup [AUTO-GENERATED]"

**4. Copilot refines:**

- Reads spec from `planning/docs/m1---backend-services/T24-*.md`
- Fixes TODO comments
- Implements actual DB queries
- Updates tests
- Pushes to PR

**5. Human approves:**

- Review PR
- Test migrations: `supabase db reset`
- Test types: `pnpm type-check`
- Merge

**Time savings:**

- **Without automation**: ~2 days (16 hours)
- **With automation**: ~4 hours (generation 30min + Copilot review 2h + human
  1.5h)
- **Saved: 75%** 🚀

### Example 2: API Routes (T25)

**1. Create issue + trigger automation:**

```bash
python scripts/planning/create-github-issues.py T25
# Then on GitHub: comment /automate
```

**2. Automation generates:**

- `apps/backend/src/routes/api-routes.routes.ts` (CRUD + Zod)
- TODO comments for database queries
- Error handling boilerplate
- Structured logging

**3. Copilot implements:**

- Replaces TODO with actual database calls
- Adds authentication middleware
- Implements pagination
- Writes integration tests

**4. Human tests:**

```bash
pnpm dev:backend
# Test endpoints with curl/Postman
curl http://localhost:3002/api/items
```

### Example 3: Unit Tests (T27)

**1. Trigger:**

```bash
# Local generation
./scripts/automation/generators/setup-tests.sh T27 unit
```

**2. Generated:**

- `apps/backend/src/__tests__/T27-backend-unit-tests.test.ts`
- Test fixtures
- Happy path + error handling structure
- TODO: Actual assertions

**3. Copilot implements:**

- Writes actual test assertions
- Adds edge cases
- Mocks external dependencies
- Ensures 80%+ coverage

## 🔧 Configuration

### GitHub Secrets Required

Add to repository secrets:

```bash
# .github/workflows/copilot-task-automation.yml needs:
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=<auto-provided>
```

### GitHub Labels Required

Create these labels:

```bash
gh label create "auto-generated" --color "0E8A16" --description "Auto-generated code"
gh label create "automation:ready" --color "1D76DB" --description "HIGH AI effectiveness - automation ready"
gh label create "automation:partial" --color "FFA500" --description "MEDIUM AI effectiveness"
gh label create "needs-review" --color "FBCA04" --description "Requires human review"
gh label create "from-planning" --color "D876E3" --description "Created from planning system"
```

### Optional: GitHub Milestones

```bash
# Create milestones matching planning system
gh milestone create "M0 - Infrastructure & Setup"
gh milestone create "M1 - Backend Services"
# etc.
```

## 📈 Monitoring

### Check Automation Status

```bash
# List auto-generated PRs
gh pr list --label "auto-generated"

# Check workflow runs
gh run list --workflow "copilot-task-automation.yml"

# View specific run logs
gh run view <RUN_ID>
```

### Metrics

Track automation effectiveness:

```bash
# Count automated tasks
gh pr list --label "auto-generated" --state all --json number | jq length

# Time saved (estimated)
# Each HIGH AI task: ~1.5 days saved
# Each MEDIUM AI task: ~0.5 days saved
```

## 🐛 Troubleshooting

### Automation doesn't trigger

**Check:**

1. Issue has task key in title/body (e.g., "T24")
2. ANTHROPIC_API_KEY secret is set
3. Workflow file exists: `.github/workflows/copilot-task-automation.yml`
4. GitHub Actions are enabled for repo

**Fix:**

```bash
# Test locally
python scripts/automation/task-automation-agent.py T24 --dry-run

# Check GitHub Actions status
gh workflow list
gh workflow enable copilot-task-automation.yml
```

### Generated code doesn't compile

**Cause:** LLM generated placeholder code

**Fix:**

1. Copilot Agent should fix (that's its job!)
2. If not: manually implement TODO comments
3. Search for `TODO` in generated files
4. Implement based on `planning/docs/` specs

### Tests fail after generation

**Expected** - generated tests have TODO comments

**Workflow:**

1. Auto-generator creates test structure
2. Copilot implements actual tests
3. Human verifies coverage

## 📚 Resources

- **Main README**:
  [scripts/automation/README.md](../scripts/automation/README.md)
- **Workflow File**:
  [.github/workflows/copilot-task-automation.yml](../.github/workflows/copilot-task-automation.yml)
- **Copilot Instructions**:
  [.github/copilot-instructions.md](../.github/copilot-instructions.md)
- **Planning Docs**: [planning/docs/](../planning/docs/)
- **AI Effectiveness**:
  [planning/estimates/effort-map.yaml](../planning/estimates/effort-map.yaml)

## 🎓 Best Practices

### DO ✅

- ✅ Assign HIGH AI tasks to @copilot immediately
- ✅ Let automation run before manual work
- ✅ Review auto-generated code thoroughly
- ✅ Use `/automate` comment for manual trigger
- ✅ Test locally before merging
- ✅ Report automation failures (improve system)

### DON'T ❌

- ❌ Skip reviewing auto-generated code
- ❌ Merge without running tests
- ❌ Assume business logic is correct
- ❌ Use automation for LOW AI tasks
- ❌ Modify workflow without testing

## 🔄 CI/CD Integration

Workflow integrates with:

- ✅ GitHub Actions (auto-trigger)
- ✅ Copilot Agent (assignment-based)
- ✅ PR checks (tests, linting)
- ✅ Issue tracking (auto-close on merge)

## 📞 Support

**Issues?**

1. Check automation logs: `gh run view <RUN_ID>`
2. Test locally:
   `python scripts/automation/task-automation-agent.py T24 --dry-run`
3. Read planning spec: `cat planning/docs/.../T24-*.md`
4. Review Copilot instructions: `.github/copilot-instructions.md`

---

**Status**: ✅ Production Ready

**Version**: 1.0.0

**Last Updated**: 2026-02-08

**Maintainer**: @neutrico
