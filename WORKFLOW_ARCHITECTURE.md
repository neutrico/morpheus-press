# Morpheus-Press: Planning & Automation Repository

> Standalone repository for task planning, issue management, and automation workflows.

## 🎯 Purpose

This repository serves as the **control plane** for Morpheus development:

- 📋 **Planning** - Task specifications, effort estimates, milestones
- 🤖 **Automation** - Auto-generate starter code from planning docs
- 🏷️ **Issue Management** - Create and manage GitHub issues programmatically
- 🔄 **Workflow Coordination** - Trigger workflows in `neutrico/morpheus` repo

**Separation of Concerns:**
- `morpheus-press` = Planning + Automation (this repo)
- `neutrico/morpheus` = Application code + Tests + Deployment

---

## 📂 Repository Structure

```
morpheus-press/
├── planning/                  # Task specifications & estimates
│   ├── docs/                  # Detailed task documentation (markdown)
│   ├── issues/                # Issue definitions (YAML)
│   └── estimates/             # Effort estimates & AI effectiveness
│
├── scripts/                   # Automation scripts
│   ├── create-issues-api.py   # Create GitHub issues from planning/
│   ├── copilot_agent.py       # Assign Copilot agents to issues
│   ├── generate_tests_from_scenarios.py  # AI test generation
│   └── automation/            
│       └── task-automation-agent.py  # Auto-generate starter code
│
├── .github/
│   ├── agents/                # Copilot agent definitions
│   │   └── planning-agent.agent.md  # Test scenario planner
│   ├── workflows/             # GitHub Actions workflows
│   │   ├── copilot-task-automation.yml  # Auto-code-gen trigger
│   │   └── stale.yml          # Issue/PR cleanup
│   └── ISSUE_TEMPLATE/        # Issue templates
│
└── docs/                      # Documentation
    ├── COPILOT_WORKFLOW_INTEGRATION.md  # How Copilot + Actions work
    ├── GITHUB_ACTIONS_SETUP.md         # Setup guide
    └── COPILOT_AGENT_ASSIGNMENT.md     # Agent usage guide
```

---

## 🔄 Cross-Repo Workflow

### Phase 1: Planning (morpheus-press)

```yaml
1. Human creates task spec in planning/docs/
2. Run: python scripts/create-issues-api.py
3. GitHub issue created in morpheus-press
4. Planning Agent adds test_scenarios.yaml to issue
5. Human reviews test scenarios
```

**Output:** Issue with test scenarios in `morpheus-press` repo

---

### Phase 2: Auto-Generate Starter Code (morpheus-press → morpheus)

```yaml
Trigger: Issue assigned to @copilot OR comment "/automate"
Workflow: copilot-task-automation.yml (in morpheus-press)

Steps:
  1. Extract task key (T24, T25, etc.) from issue
  2. Check AI effectiveness in planning/estimates/effort-map.yaml
  3. If HIGH AI effectiveness:
     - Run: scripts/automation/task-automation-agent.py
     - Anthropic Claude generates boilerplate code
  4. Create branch in neutrico/morpheus repo: automation/T24-YYYYMMDD
  5. Commit generated code to morpheus repo
  6. Create PR in morpheus repo with [AUTO-GENERATED] tag
  7. Assign PR to @copilot in morpheus repo
```

**Output:** PR with starter code in `neutrico/morpheus` repo

---

### Phase 3: Implementation & Testing (morpheus)

```yaml
Workflow: copilot-branch-pipeline.yml (in neutrico/morpheus repo)
Trigger: Copilot pushes code to copilot/** branches in morpheus

Steps:
  1. Detect changes (backend/frontend/database)
  2. Download test_scenarios.yaml from morpheus-press issue
  3. Generate tests via OpenAI (scripts/generate_tests_from_scenarios.py)
  4. Commit tests to branch
  5. Run tests (Vitest) with coverage
  6. Run lint + type-check
  7. IF PASS:
       - Create PR in morpheus
       - Deploy preview to Vercel
       - Comment success on morpheus-press issue
  8. IF FAIL:
       - Comment errors on morpheus-press issue
       - Copilot reads error, fixes code, pushes again
       - Loop back to step 1 (iterative)
```

**Output:** PR with full implementation + tests in `neutrico/morpheus` repo

---

### Phase 4: Human Review & Merge (morpheus)

```yaml
Human reviews PR in neutrico/morpheus:
  - Check implementation quality
  - Verify tests pass
  - Test preview deployment
  - Approve and merge

Post-merge actions in morpheus:
  - Deploy to production (Vercel)
  - Close linked issue in morpheus-press
  - Update changelog
```

---

## 🤖 GitHub Actions Workflows

### In This Repo (morpheus-press)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `copilot-task-automation.yml` | Issue assigned / `/automate` comment | Auto-generate starter code in morpheus repo |
| `stale.yml` | Daily cron | Auto-close stale issues/PRs after 30+7 days |

### In neutrico/morpheus Repo

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `copilot-branch-pipeline.yml` | Push to `copilot/**` branches | Test generation + quality gates + PR creation |
| `test-coverage.yml` | PR opened/updated | Coverage tracking with Codecov |
| `security-scan.yml` | PR + weekly | npm audit, Snyk, CodeQL, secret detection |
| `lighthouse.yml` | PR opened/updated | Performance monitoring |
| `vercel-preview.yml` | PR opened/updated | Preview deployments |
| `pr-quality-gate.yml` | PR opened/updated | Auto-labeling, size checks, validation |
| `build-runpod-worker.yml` | Push to `runpod-worker/**` | Build ML worker Docker image |
| `deploy-storefront.yml` | Manual | Production deployment |

**Why separation?**
- `morpheus-press` workflows manage **planning and automation**
- `morpheus` workflows manage **code quality and deployment**
- Clear separation of concerns, easier to maintain

---

## 🚀 Quick Start Guide

### 1. Create New Task

```bash
# 1. Write task spec
vim planning/docs/m1---backend-services/T99-new-feature.md

# 2. Add to issues YAML
vim planning/issues/m1-backend-services.yaml

# 3. Create GitHub issue
python scripts/create-issues-api.py

# 4. Planning agent adds test scenarios (automatic)
# Check issue for test_scenarios.yaml comment

# 5. Trigger automation (if HIGH AI effectiveness)
gh issue comment 123 --body "/automate"

# 6. PR created in neutrico/morpheus with starter code
```

### 2. Monitor Progress

```bash
# Check all issues
gh issue list --repo neutrico/morpheus-press

# Check specific task
gh issue view 123

# Check PRs in main repo
gh pr list --repo neutrico/morpheus

# Check workflow runs
gh run list --repo neutrico/morpheus
```

### 3. Manual Implementation (LOW AI effectiveness tasks)

```bash
# 1. Read task spec
cat planning/docs/m1---backend-services/T99-new-feature.md

# 2. Implement manually in morpheus repo
cd /workspaces/morpheus
git checkout -b feature/T99-new-feature

# 3. Write code + tests
# 4. Push and create PR manually
```

---

## 📊 AI Effectiveness Levels

Defined in `planning/estimates/effort-map.yaml`:

- **HIGH** - Auto-generate starter code (70-80% complete)
  - Database setup (migrations, RLS, indexes)
  - CRUD API routes (Fastify + Zod)
  - Unit test scaffolding
  
- **MEDIUM** - Partial automation (30-50% complete)
  - Integration work with existing systems
  - Complex business logic (human review required)
  
- **LOW** - Manual implementation only
  - Architecture decisions
  - Novel algorithms
  - UX/UI design work

---

## 🔍 Key Files

### Planning

- `planning/estimates/effort-map.yaml` - All tasks with estimates and AI effectiveness
- `planning/docs/m*/T*-*.md` - Detailed task specifications
- `planning/issues/*.yaml` - Issue definitions for batch creation

### Automation

- `scripts/automation/task-automation-agent.py` - Main code generator (Anthropic Claude)
- `scripts/generate_tests_from_scenarios.py` - Test generator (OpenAI GPT-4o-mini)
- `scripts/create-issues-api.py` - Issue creator (GitHub GraphQL API)
- `scripts/copilot_agent.py` - Copilot agent assigner

### Configuration

- `.github/agents/planning-agent.agent.md` - Planning agent instructions
- `.github/workflows/copilot-task-automation.yml` - Auto-code-gen workflow
- `.github/labeler.yml` - Auto-labeling rules

---

## 💡 Best Practices

### For Planning

1. **Be specific** - Include exact acceptance criteria
2. **Define test scenarios** - Complete AAA pattern (Arrange, Act, Assert)
3. **Estimate complexity** - Helps prioritize tasks
4. **Mark AI effectiveness** - HIGH/MEDIUM/LOW determines automation level

### For Automation

1. **Review generated code** - Never merge without human review
2. **Check TODO comments** - Generated code has placeholders
3. **Verify business logic** - AI may miss domain nuances
4. **Run tests locally** - Before pushing to CI

### For Issue Management

1. **Link issues to PRs** - Use "Closes #123" in PR descriptions
2. **Comment updates** - Keep stakeholders informed
3. **Use labels** - area:backend, type:feature, priority:high, etc.
4. **Close stale issues** - Review issues marked as stale before auto-close

---

## 🔧 Setup Requirements

### Secrets (GitHub Repository Settings)

```bash
# morpheus-press secrets
ANTHROPIC_API_KEY=sk-ant-xxx   # For code generation (task-automation-agent.py)

# neutrico/morpheus secrets
OPENAI_API_KEY=sk-proj-xxx     # For test generation
VERCEL_TOKEN=xxx               # For preview deployments
VERCEL_ORG_ID=xxx
VERCEL_DASHBOARD_PROJECT_ID=xxx
VERCEL_STOREFRONT_PROJECT_ID=xxx
CODECOV_TOKEN=xxx              # Optional: coverage tracking
SNYK_TOKEN=xxx                 # Optional: security scanning
```

**Setup Guide:** See `docs/GITHUB_ACTIONS_SETUP.md`

---

## 📈 Performance Metrics

**Time Savings:**
- Manual implementation: 5-6 hours per task
- With automation: 45-60 minutes per task
- **Savings: 75%** (for HIGH AI effectiveness tasks)

**Cost Analysis:**
- OpenAI API (test generation): ~$0.02-0.05 per file
- Anthropic API (code generation): ~$0.20-0.30 per task
- **Total cost per task: ~$2-5**
- **ROI: $100-150 saved in developer time**

**Quality Improvements:**
- Test coverage: 80%+ enforced by CI
- Security vulnerabilities: Auto-detected weekly
- Performance: Lighthouse scores tracked per PR
- Code quality: Auto-linted and type-checked

---

## 🆘 Troubleshooting

### Issue: Automation workflow doesn't trigger

**Check:**
```bash
# 1. Verify task has HIGH AI effectiveness
grep "T99" planning/estimates/effort-map.yaml

# 2. Check workflow permissions
gh api repos/neutrico/morpheus-press/actions/permissions

# 3. Verify ANTHROPIC_API_KEY secret exists
gh secret list --repo neutrico/morpheus-press
```

### Issue: Test generation fails in morpheus

**Check:**
```bash
# 1. Verify OPENAI_API_KEY secret in morpheus repo
gh secret list --repo neutrico/morpheus

# 2. Check test scenarios in issue comment
gh issue view 123 --repo neutrico/morpheus-press

# 3. Verify YAML is valid
# Copy test_scenarios from issue and validate locally
python -c "import yaml; yaml.safe_load(open('test.yaml'))"
```

### Issue: Copilot doesn't fix failing tests

**Check:**
```bash
# 1. Verify feedback comment was posted
gh issue view 123 --repo neutrico/morpheus-press --comments

# 2. Check if Copilot is assigned
gh issue view 123 --json assignees

# 3. Manual fix if needed:
cd /workspaces/morpheus
git checkout copilot/123-branch
# Fix code
git commit -am "fix: address test failures"
git push  # Re-triggers workflow
```

---

## 🔗 Related Documentation

- [COPILOT_WORKFLOW_INTEGRATION.md](docs/COPILOT_WORKFLOW_INTEGRATION.md) - How Copilot interacts with GitHub Actions
- [GITHUB_ACTIONS_SETUP.md](docs/GITHUB_ACTIONS_SETUP.md) - Complete setup guide for all workflows
- [COPILOT_AGENT_ASSIGNMENT.md](scripts/COPILOT_AGENT_ASSIGNMENT.md) - How to assign Copilot agents

---

## 📞 Support

**Issues:** Create issue in `neutrico/morpheus-press` with `question` label
**Docs:** All documentation in `docs/` directory
**Logs:** Check GitHub Actions runs for debugging

---

**Last Updated:** February 9, 2026
**Repository:** https://github.com/neutrico/morpheus-press
**Main Repo:** https://github.com/neutrico/morpheus
