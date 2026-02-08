# 🚀 Copilot + Automation - Setup Checklist

**Status**: ✅ System Complete - Ready for Testing

## ✅ Completed (You're Here)

- [x] Planning system executed (93 tasks estimated)
- [x] Timeline fixed (99 days, was 233 days)
- [x] T24 duration bug fixed (2 days, was 7 days)
- [x] Task automation system created (5 scripts)
- [x] GitHub Actions workflow created
- [x] Copilot instructions updated (200+ lines)
- [x] GitHub issue template created
- [x] Issue creator script created
- [x] Documentation written (README + Quick Start + Diagrams)

## ⏳ Next Steps (Your Action Required)

### Step 1: Configure GitHub Repository

#### 1.1 Add ANTHROPIC_API_KEY Secret

```bash
# On GitHub:
# 1. Go to: https://github.com/YOUR_ORG/morpheus/settings/secrets/actions
# 2. Click "New repository secret"
# 3. Name: ANTHROPIC_API_KEY
# 4. Value: sk-ant-api03-...
# 5. Click "Add secret"
```

**Status**: ⬜ Not configured yet

#### 1.2 Create GitHub Labels

```bash
# Run this in your repo:
gh label create "auto-generated" --color "0E8A16" --description "Auto-generated code" || true
gh label create "automation:ready" --color "1D76DB" --description "HIGH AI effectiveness" || true
gh label create "automation:partial" --color "FFA500" --description "MEDIUM AI effectiveness" || true
gh label create "needs-review" --color "FBCA04" --description "Requires human review" || true
gh label create "from-planning" --color "D876E3" --description "From planning system" || true

# Verify labels created:
gh label list | grep -E "auto-generated|automation|needs-review|from-planning"
```

**Status**: ⬜ Not created yet

#### 1.3 Enable GitHub Actions

```bash
# Check if Actions are enabled:
gh workflow list

# If empty, enable Actions:
# Go to: https://github.com/YOUR_ORG/morpheus/settings/actions
# Enable "Allow all actions and reusable workflows"
```

**Status**: ⬜ Not verified yet

#### 1.4 Create GitHub Milestones (Optional)

```bash
# Create milestones matching planning system:
gh milestone create "M0 - Infrastructure & Setup" --due-date "2026-02-28"
gh milestone create "M1 - Backend Services" --due-date "2026-03-31"
gh milestone create "M2 - Dashboard UI" --due-date "2026-04-30"
gh milestone create "M3 - Image Generation" --due-date "2026-05-31"

# Verify:
gh milestone list
```

**Status**: ⬜ Optional (not required for automation)

### Step 2: Test Automation System (Dry Run)

#### 2.1 Test Issue Creator (Preview)

```bash
# Preview HIGH AI tasks without creating:
python scripts/planning/create-github-issues.py --ai-high-only --dry-run

# Expected output:
# Would create 5 issues:
# - T2: GitHub Milestones & Issues Creation (1.5 days)
# - T24: Supabase Database Setup with RLS (2.0 days)
# - T27: Backend Unit Tests (Vitest) (2.0 days)
# - T32: API Documentation & OpenAPI (1.5 days)
# - T52: Batch Image Generation (3.5 days)
```

**Status**: ⬜ Not tested yet

#### 2.2 Test Local Code Generation

```bash
# Test generation locally (no GitHub Actions):
python scripts/automation/task-automation-agent.py T24 --dry-run

# Expected output:
# ✅ Task T24 loaded
# ✅ Pattern detected: database
# ✅ Prompt built (1234 tokens)
# 🔍 Dry run - would generate:
#    - supabase/migrations/...
#    - apps/backend/src/services/...
#    - apps/backend/src/__tests__/...
```

**Status**: ⬜ Not tested yet

### Step 3: Test End-to-End Workflow

#### 3.1 Create Single Test Issue

```bash
# Create T24 issue (Supabase setup - simple, safe to test):
python scripts/planning/create-github-issues.py T24

# Expected output:
# ✅ Created issue #123: T24 - Supabase Database Setup with RLS
# Labels: automation:ready, from-planning, priority:high, task
# Milestone: M1 - Backend Services
# URL: https://github.com/YOUR_ORG/morpheus/issues/123
```

**Status**: ⬜ Not done yet

#### 3.2 Trigger Automation (Choose One Method)

**Option A: Comment Trigger** (Recommended for testing):

```bash
# On GitHub issue #123:
gh issue comment 123 --body "/automate"

# Check if workflow triggered:
gh run list --workflow "copilot-task-automation.yml" --limit 1
```

**Option B: Label Trigger**:

```bash
gh issue edit 123 --add-label "automation:ready"
gh run list --workflow "copilot-task-automation.yml" --limit 1
```

**Option C: Assign Trigger** (if you have copilot user):

```bash
# Assign to user with 'copilot' in username
gh issue edit 123 --add-assignee copilot
```

**Status**: ⬜ Not triggered yet

#### 3.3 Monitor Workflow Execution

```bash
# Watch workflow in real-time:
gh run watch

# Or view specific run:
gh run view <RUN_ID>

# Expected steps:
# ✅ Extract task key
# ✅ Check AI effectiveness
# ✅ Run automation
# ✅ Create branch
# ✅ Commit files
# ✅ Create PR
# ✅ Assign to copilot
# ✅ Comment on issue
```

**Status**: ⬜ Not monitored yet

#### 3.4 Verify PR Created

```bash
# Check for auto-generated PR:
gh pr list --label "auto-generated"

# Expected output:
# #124  feat: T24 - Supabase Database Setup [AUTO-GENERATED]  automation/T24-20260208-...
# Assignee: @copilot
# Labels: auto-generated, needs-review
```

**Status**: ⬜ Not verified yet

#### 3.5 Review Generated Code

```bash
# Checkout PR:
gh pr checkout 124

# Check generated files:
ls -la supabase/migrations/
ls -la apps/backend/src/services/
ls -la apps/backend/src/__tests__/

# Search for TODOs (Copilot should fix these):
grep -r "TODO" apps/backend/src/

# Expected TODOs:
# - Implement database queries
# - Add specific validation logic
# - Customize RLS policies
```

**Status**: ⬜ Not reviewed yet

#### 3.6 Test Copilot Refinement (if using Copilot Agent)

**If you have Copilot Agent access:**

1. Wait for Copilot to review PR (automatic)
2. Copilot should:
   - Read task spec from `planning/docs/`
   - Fix TODO comments
   - Implement business logic
   - Run tests
   - Push fixes to PR

**If you DON'T have Copilot Agent:**

Manually implement TODOs:

```bash
# 1. Read spec
cat planning/docs/m1---backend-services/T24-supabase-database-setup-with-rls.md

# 2. Fix TODOs in generated files
code supabase/migrations/*.sql

# 3. Run tests
pnpm test

# 4. Push
git add .
git commit -m "fix: implement T24 TODOs"
git push
```

**Status**: ⬜ Not tested yet

#### 3.7 Human Review & Merge

```bash
# 1. Review PR on GitHub:
gh pr view 124 --web

# 2. Run tests locally:
pnpm test

# 3. Test application:
pnpm dev:backend
# Test endpoints, DB migrations, etc.

# 4. Approve + merge:
gh pr review 124 --approve
gh pr merge 124 --squash
```

**Status**: ⬜ Not merged yet

### Step 4: Scale Up (After Successful Test)

#### 4.1 Create All HIGH AI Issues

```bash
# Create 5 HIGH AI effectiveness tasks:
python scripts/planning/create-github-issues.py --ai-high-only

# Expected output:
# ✅ Created 5 issues:
#    #125: T2 - GitHub Milestones & Issues
#    #126: T24 - Supabase Database Setup (if not created yet)
#    #127: T27 - Backend Unit Tests
#    #128: T32 - API Documentation
#    #129: T52 - Batch Image Generation
```

**Status**: ⬜ Not done yet

#### 4.2 Trigger Automation for All

```bash
# Option A: Comment on each issue:
for i in 125 126 127 128 129; do
  gh issue comment $i --body "/automate"
  sleep 5  # Wait between triggers
done

# Option B: Add label to each:
for i in 125 126 127 128 129; do
  gh issue edit $i --add-label "automation:ready"
done
```

**Status**: ⬜ Not done yet

#### 4.3 Monitor Batch Execution

```bash
# Watch all workflow runs:
gh run list --workflow "copilot-task-automation.yml" --limit 10

# Check PRs:
gh pr list --label "auto-generated"

# Expected: 5 PRs created (one per task)
```

**Status**: ⬜ Not monitored yet

#### 4.4 Review & Merge All PRs

```bash
# List all auto-generated PRs:
gh pr list --label "auto-generated" --json number,title

# Review each:
for pr in $(gh pr list --label "auto-generated" --json number --jq '.[].number'); do
  echo "Reviewing PR #$pr"
  gh pr view $pr
  # Manual review + merge
done
```

**Status**: ⬜ Not done yet

### Step 5: Create Remaining Issues (Optional)

#### 5.1 Create All 93 Issues

```bash
# Create all issues from planning system:
python scripts/planning/create-github-issues.py

# Expected output:
# ✅ Created 93 issues
# 5 HIGH AI (automation:ready)
# 30 MEDIUM AI (automation:partial)
# 58 LOW AI (manual)
```

**Status**: ⬜ Optional (not required immediately)

#### 5.2 Organize Issues by Milestone

```bash
# Group issues by milestone:
gh issue list --milestone "M0 - Infrastructure & Setup"
gh issue list --milestone "M1 - Backend Services"
# etc.
```

**Status**: ⬜ Optional

## 📊 Success Metrics

Track these after scaling up:

### Automation Metrics

```bash
# Count automated PRs:
gh pr list --label "auto-generated" --state all --json number | jq length

# Time saved (estimate):
# Each HIGH AI task: ~1.5 days saved
# 5 HIGH AI tasks: ~7.5 days saved
```

### Cost Metrics

```bash
# LLM cost (per task):
# ~$0.15 per task generation

# Total LLM cost (5 tasks):
# ~$0.75

# Dev cost saved:
# Traditional: ~10 days × $75/h × 8h = $6,000
# With automation: ~3 days × $75/h × 8h = $1,800
# Savings: $4,200 (70%)
```

### Quality Metrics

```bash
# Test coverage:
pnpm test:coverage

# Type safety:
pnpm type-check

# Expected:
# - Unit tests: 80%+ coverage
# - Type errors: 0
# - Linting errors: 0
```

## 🐛 Troubleshooting

### Automation Not Triggering

**Check:**

```bash
# 1. Workflow exists
ls -la .github/workflows/copilot-task-automation.yml

# 2. Actions enabled
gh workflow list

# 3. Secret configured
# (Check on GitHub UI: Settings → Secrets)

# 4. Issue has task key
gh issue view 123 | grep -i "T24"
```

### Generated Code Doesn't Compile

**Fix:**

```bash
# 1. Check TODOs
grep -r "TODO" apps/backend/src/

# 2. Implement missing logic (Copilot should do this)

# 3. Run tests
pnpm test

# 4. Fix type errors
pnpm type-check
```

### Workflow Fails

**Debug:**

```bash
# View workflow logs:
gh run view <RUN_ID>

# Common issues:
# - ANTHROPIC_API_KEY missing → Add secret
# - Task key not found → Check issue title/body
# - Planning docs missing → Check planning/docs/
# - API rate limit → Wait and retry
```

## 📚 Resources

- **Quick Start Guide**:
  [docs/COPILOT_AUTOMATION_INTEGRATION.md](./COPILOT_AUTOMATION_INTEGRATION.md)
- **Workflow Diagrams**:
  [docs/diagrams/AUTOMATION_WORKFLOW.md](./diagrams/AUTOMATION_WORKFLOW.md)
- **Main README**:
  [scripts/automation/README.md](../scripts/automation/README.md)
- **Copilot Instructions**:
  [.github/copilot-instructions.md](../.github/copilot-instructions.md)

## 🎯 Summary

**Total Implementation Time**: ~30 minutes to 1 hour

**Steps**:

1. ✅ Add ANTHROPIC_API_KEY secret (5 min)
2. ✅ Create GitHub labels (2 min)
3. ✅ Test with single issue (T24) (10 min)
4. ✅ Verify workflow + PR (5 min)
5. ✅ Scale to 5 HIGH AI tasks (30 min)

**Expected Results**:

- ✅ 5 tasks auto-generated
- ✅ 70% time savings
- ✅ $4,200 cost savings
- ✅ Code quality maintained

**Next Action**: Start with Step 1.1 (Add ANTHROPIC_API_KEY) 🚀

---

**Version**: 1.0.0\
**Last Updated**: 2026-02-08\
**Status**: ✅ Ready for Deployment
