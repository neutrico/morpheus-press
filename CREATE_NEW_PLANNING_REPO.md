# 🚀 Creating Morpheus Press - Planning + Automation Repository

**Goal**: Extract planning system + automation to clean new repo → Initialize on GitHub → Generate issues → Start development with Copilot

**Location**: Inside devcontainer at `/workspaces/morpheus-press` (alongside main `/workspaces/morpheus` repo)

---

## ⚡ Quick Start (Automated Setup)

**Fastest way** - run the automated setup script:

```bash
# Run from /workspaces/morpheus
/workspaces/morpheus/scripts/setup-morpheus-press.sh
```

This will:
- ✅ Create `/workspaces/morpheus-press` directory
- ✅ Copy planning system (93 tasks, AI-aware estimates)
- ✅ Copy automation scripts (LLM orchestrator + generators)
- ✅ Copy GitHub integration (Actions + Copilot instructions)
- ✅ Copy documentation (guides + diagrams)
- ✅ Create config files (package.json, requirements.txt, .gitignore)
- ✅ Create README.md
- ✅ Initialize git

**Then continue with Step 3** (Create Python venv) below.

---

## 📖 Manual Setup (Step-by-Step)

If you prefer manual control, follow these steps:

---

## Step 1: Create New Repository Locally

```bash
# We're already in the devcontainer at /workspaces/morpheus
# Create new repo alongside it
cd /workspaces

# Create new repo
mkdir morpheus-press
cd morpheus-press

# Initialize git
git init
git branch -M main
```

## Step 2: Copy Planning & Automation Files

```bash
# Copy planning system (complete)
cp -r /workspaces/morpheus/planning .

# Copy automation scripts
mkdir -p scripts
cp -r /workspaces/morpheus/scripts/automation scripts/
cp /workspaces/morpheus/scripts/planning/create-github-issues.py scripts/

# Copy GitHub integration
mkdir -p .github/workflows .github/ISSUE_TEMPLATE
cp /workspaces/morpheus/.github/workflows/copilot-task-automation.yml .github/workflows/
cp /workspaces/morpheus/.github/copilot-instructions.md .github/
cp /workspaces/morpheus/.github/ISSUE_TEMPLATE/task-implementation.md .github/ISSUE_TEMPLATE/

# Copy documentation
mkdir -p docs/diagrams
cp /workspaces/morpheus/docs/COPILOT_AUTOMATION_INTEGRATION.md docs/
cp /workspaces/morpheus/docs/diagrams/AUTOMATION_WORKFLOW.md docs/diagrams/
cp /workspaces/morpheus/SETUP_CHECKLIST.md .

# Copy config files
cp /workspaces/morpheus/.gitignore .
```

## Step 3: Create Python Virtual Environment

```bash
# Create venv for Python scripts
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install anthropic pyyaml
pip freeze > requirements.txt
```

## Step 4: Create Minimal Package Files

### 4.1 Create `package.json`

```bash
cat > package.json << 'EOF'
{
  "name": "morpheus-press",
  "version": "1.0.0",
  "description": "AI-powered planning and automation system for Morpheus Press (novel-to-comic publishing platform)",
  "private": true,
  "scripts": {
    "plan": "python3 scripts/planning/run-pipeline.py",
    "plan:dry-run": "python3 scripts/planning/run-pipeline.py --dry-run",
    "automate": "python3 scripts/automation/task-automation-agent.py",
    "issues:create": "python3 scripts/create-github-issues.py",
    "issues:high-ai": "python3 scripts/create-github-issues.py --ai-high-only"
  },
  "keywords": ["planning", "automation", "ai", "copilot", "github-actions"],
  "author": "neutrico",
  "license": "MIT"
}
EOF
```

### 4.2 Create `requirements.txt`

```bash
cat > requirements.txt << 'EOF'
anthropic>=0.40.0
pyyaml>=6.0.1
python-dotenv>=1.0.0
EOF
```

### 4.3 Update `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env
.env.local

# Temporary
*.tmp
*.bak
EOF
```

## Step 5: Create New README.md

```bash
cat > README.md << 'EOF'
# Morpheus Press - Planning & Automation System

**AI-powered planning and task automation** for Morpheus Press - a novel-to-comic publishing platform.

## 🎯 What This Is

This repository contains:
- **Planning System**: AI-aware task estimation, dependency analysis, resource scheduling
- **Automation System**: LLM-powered code generation for repetitive tasks (database, testing, API routes)
- **GitHub Integration**: Automated workflow (create issue → auto-generate code → Copilot refines → merge)

**This is NOT the main Morpheus application** - it's the planning/automation layer that generates development tasks and starter code.

## 🏗️ Structure

```
morpheus-press/
├── planning/
│   ├── docs/               # Task specifications (markdown)
│   ├── issues/             # Research findings (YAML)
│   ├── estimates/          # AI-aware effort estimates
│   ├── pi-visualization.ipynb  # Timeline & Gantt charts
│   └── roadmap.yaml        # Milestones & dependencies
├── scripts/
│   ├── automation/         # Code generators
│   │   ├── task-automation-agent.py  # Main LLM orchestrator
│   │   └── generators/     # CLI generators (DB, tests, API)
│   └── create-github-issues.py  # Bulk issue creator
├── .github/
│   ├── workflows/          # GitHub Actions automation
│   ├── copilot-instructions.md  # Instructions for Copilot Agent
│   └── ISSUE_TEMPLATE/     # Issue templates
└── docs/                   # Documentation & diagrams
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- GitHub CLI (`gh`)
- Anthropic API key (for code generation)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file
cat > .env << 'ENV'
ANTHROPIC_API_KEY=sk-ant-api03-...
ENV
```

### 3. Explore Planning Data

```bash
# View all tasks with AI effectiveness
cat planning/estimates/effort-map.yaml | head -50

# View task specifications
ls -la planning/docs/*/

# View timeline visualization
jupyter notebook planning/pi-visualization.ipynb
```

### 4. Test Automation (Local)

```bash
# List tasks suitable for automation
python3 scripts/automation/task-automation-agent.py --list

# Generate code for task (dry-run)
python3 scripts/automation/task-automation-agent.py T24 --dry-run

# Generate code for real
python3 scripts/automation/task-automation-agent.py T24
```

### 5. GitHub Integration Setup

See [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) for complete GitHub integration guide.

**Quick version:**

```bash
# 1. Create GitHub repo
gh repo create morpheus-press --public --source=. --remote=origin

# 2. Add secret
gh secret set ANTHROPIC_API_KEY

# 3. Create labels
gh label create "auto-generated" --color "0E8A16"
gh label create "automation:ready" --color "1D76DB"
gh label create "needs-review" --color "FBCA04"

# 4. Create GitHub issues from planning
python3 scripts/create-github-issues.py --ai-high-only

# 5. Trigger automation by commenting on issue
/automate
```

## 📊 Planning System

### AI-Aware Estimation

Tasks are estimated using **3-layer approach**:
1. **Research Agent** (Claude): Analyzes task complexity, AI suitability
2. **Planning Agent** (Claude): Generates acceptance criteria, dependencies
3. **Estimation Agent** (Claude): Calculates effort points & estimated days with AI acceleration

**Output**: [planning/estimates/effort-map.yaml](planning/estimates/effort-map.yaml)

### Timeline Visualization

Resource-aware scheduling with **2 developers** + **AI assistance**:

```bash
jupyter notebook planning/pi-visualization.ipynb
```

**Current timeline**: **99 days** for 93 tasks (M0-M4)

## 🤖 Automation System

### Code Generators

| Generator | Purpose | Usage |
|-----------|---------|-------|
| **task-automation-agent.py** | LLM orchestrator (Claude) | `python3 scripts/automation/task-automation-agent.py T24` |
| **setup-supabase.sh** | Database migrations + RLS | `./scripts/automation/generators/setup-supabase.sh T24` |
| **setup-tests.sh** | Test suites (unit/e2e) | `./scripts/automation/generators/setup-tests.sh T27 unit` |
| **api-generator.py** | Fastify CRUD routes | `python3 scripts/automation/generators/api-generator.py T25` |

### GitHub Actions Workflow

**Automatic code generation** when issue assigned to Copilot or comment `/automate`:

```
Issue Created → /automate → Workflow Runs → Code Generated → PR Created → Copilot Refines → Human Approves → Merge
```

**See**: [.github/workflows/copilot-task-automation.yml](.github/workflows/copilot-task-automation.yml)

### AI Effectiveness Tiers

Tasks are classified by **AI automation suitability**:

- **HIGH** (5 tasks, 10.5 days): Database, testing, API routes → **71% time savings**
- **MEDIUM** (30 tasks): Integration, debugging → **30% time savings**
- **LOW** (58 tasks): Architecture, algorithms → Manual implementation

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) | Step-by-step GitHub integration (30 min) |
| [docs/COPILOT_AUTOMATION_INTEGRATION.md](./docs/COPILOT_AUTOMATION_INTEGRATION.md) | End-to-end workflow guide |
| [docs/diagrams/AUTOMATION_WORKFLOW.md](./docs/diagrams/AUTOMATION_WORKFLOW.md) | Mermaid diagrams |
| [scripts/automation/README.md](./scripts/automation/README.md) | Complete automation docs (400+ lines) |
| [.github/copilot-instructions.md](./.github/copilot-instructions.md) | Instructions for Copilot Agent |

## 💰 Cost-Benefit Analysis

**5 HIGH AI tasks** (T2, T24, T27, T32, T52):

| Metric | Traditional | With Automation | Savings |
|--------|-------------|-----------------|---------|
| **Time** | 10.5 days | 3 days | **71%** |
| **Dev Cost** | $6,300 | $1,800 | **$4,500** |
| **LLM Cost** | $0 | $0.75 | -$0.75 |
| **Total Savings** | - | - | **$4,499** |
| **ROI** | - | - | **599,867%** |

## 🔧 Development Workflow

### Example: T24 (Supabase Database Setup)

```bash
# 1. Create issue on GitHub
python3 scripts/create-github-issues.py T24

# 2. On GitHub issue #X, comment:
/automate

# 3. GitHub Actions workflow:
#    ✅ Extracts task key (T24)
#    ✅ Checks AI effectiveness (HIGH)
#    ✅ Runs task-automation-agent.py
#    ✅ Generates migration files
#    ✅ Creates PR [AUTO-GENERATED]
#    ✅ Assigns to @copilot

# 4. Copilot Agent:
#    ✅ Reviews PR
#    ✅ Reads planning/docs/m1.../T24-*.md
#    ✅ Fixes TODO comments
#    ✅ Implements business logic
#    ✅ Runs tests
#    ✅ Pushes fixes

# 5. Human:
#    ✅ Reviews PR
#    ✅ Tests locally
#    ✅ Approves + merges
```

## 🎯 Use Cases

### Use Case 1: Generate All Issues

```bash
# Create all 93 issues from planning
python3 scripts/create-github-issues.py

# Or only HIGH AI tasks
python3 scripts/create-github-issues.py --ai-high-only

# Or by milestone
python3 scripts/create-github-issues.py --milestone M1
```

### Use Case 2: Automated Development

```bash
# For each HIGH AI task:
# 1. On GitHub issue, comment: /automate
# 2. Wait for PR
# 3. Review + approve
# 4. Merge

# Expected: 71% time savings on these tasks
```

### Use Case 3: Manual Generation

```bash
# Generate code locally without GitHub Actions
python3 scripts/automation/task-automation-agent.py T24

# Review generated files
git status

# Commit manually
git add .
git commit -m "feat: T24 - Supabase setup (auto-generated)"
git push
```

## 🐛 Troubleshooting

### Automation doesn't trigger

```bash
# Check workflow exists
ls -la .github/workflows/copilot-task-automation.yml

# Check Actions enabled
gh workflow list

# Check secret configured
gh secret list | grep ANTHROPIC_API_KEY
```

### Generated code doesn't compile

**Expected** - generated code has TODO comments for business logic.

**Fix**: Copilot Agent should implement TODOs based on specs in `planning/docs/`

### Can't find task spec

```bash
# Check task exists in planning system
grep -r "T24" planning/estimates/effort-map.yaml
grep -r "T24" planning/issues/

# Check docs exist
ls -la planning/docs/m*/T24-*.md
```

## 🤝 Contributing

This is a planning/automation system, not the main application.

**To add new tasks:**
1. Add to `planning/roadmap.yaml`
2. Run planning pipeline: `python3 scripts/planning/run-pipeline.py`
3. Create GitHub issues: `python3 scripts/create-github-issues.py`

**To improve automation:**
1. Edit generators in `scripts/automation/generators/`
2. Update LLM prompts in `task-automation-agent.py`
3. Test with `--dry-run` flag

## 📞 Support

**Questions?**
- Read: [docs/COPILOT_AUTOMATION_INTEGRATION.md](./docs/COPILOT_AUTOMATION_INTEGRATION.md)
- Check: [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)
- View diagrams: [docs/diagrams/AUTOMATION_WORKFLOW.md](./docs/diagrams/AUTOMATION_WORKFLOW.md)

**Issues with automation?**
- Check logs: `gh run list --workflow copilot-task-automation.yml`
- Test locally: `python3 scripts/automation/task-automation-agent.py T24 --dry-run`

## 📄 License

MIT

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: 2026-02-08  
**Maintainer**: @neutrico

**Related Repository**: [neutrico/morpheus](https://github.com/neutrico/morpheus) (main Morpheus Press application)
EOF
```

## Step 6: Create GitHub Repository

```bash
# Make sure you're in the new repo directory
cd /workspaces/morpheus-press

# Create GitHub repo
gh repo create neutrico/morpheus-press \
  --public \
  --description "AI-powered planning and automation system for Morpheus Press (novel-to-comic publishing)" \
  --source=. \
  --remote=origin

# Or if you want it private:
gh repo create neutrico/morpheus-press \
  --private \
  --description "AI-powered planning and automation system for Morpheus Press (novel-to-comic publishing)" \
  --source=. \
  --remote=origin
```

## Step 7: Initial Commit & Push

```bash
# Stage all files
git add .

# Commit
git commit -m "feat: initial commit - planning + automation system

- Planning system with AI-aware estimation (93 tasks, 99 days)
- Automation scripts (LLM orchestrator + CLI generators)
- GitHub Actions workflow for auto-code-generation
- Copilot Agent integration
- Complete documentation

Time savings: 71% on HIGH AI tasks
ROI: ~600,000%"

# Push to GitHub
git push -u origin main
```

## Step 8: Configure GitHub Repository

### 8.1 Add ANTHROPIC_API_KEY Secret

```bash
# Add secret (will prompt for value)
gh secret set ANTHROPIC_API_KEY

# Or set directly
gh secret set ANTHROPIC_API_KEY --body "sk-ant-api03-..."

# Verify
gh secret list
```

### 8.2 Create Labels

```bash
gh label create "auto-generated" --color "0E8A16" --description "Auto-generated code"
gh label create "automation:ready" --color "1D76DB" --description "HIGH AI effectiveness - automation ready"
gh label create "automation:partial" --color "FFA500" --description "MEDIUM AI effectiveness - partial automation"
gh label create "needs-review" --color "FBCA04" --description "Requires human review"
gh label create "from-planning" --color "D876E3" --description "Created from planning system"
gh label create "task" --color "D4C5F9" --description "Task from planning"
gh label create "priority:critical" --color "B60205" --description "Critical priority"
gh label create "priority:high" --color "D93F0B" --description "High priority"
gh label create "priority:medium" --color "FBCA04" --description "Medium priority"
gh label create "priority:low" --color "0E8A16" --description "Low priority"

# Verify
gh label list
```

### 8.3 Create Milestones

```bash
gh milestone create "M0 - Infrastructure & Setup" \
  --description "Project setup, CI/CD, devcontainer, Docker" \
  --due-date "2026-02-28"

gh milestone create "M1 - Backend Services" \
  --description "Supabase, API routes, services, testing" \
  --due-date "2026-03-31"

gh milestone create "M2 - Dashboard UI" \
  --description "Next.js dashboard, shadcn/ui components" \
  --due-date "2026-04-30"

gh milestone create "M3 - Image Generation" \
  --description "RunPod, Stable Diffusion, ComfyUI integration" \
  --due-date "2026-05-31"

gh milestone create "M4 - ML & Publishing" \
  --description "Propaganda detection, e-commerce, PDF generation" \
  --due-date "2026-06-30"

# Verify
gh milestone list
```

### 8.4 Enable GitHub Actions (if needed)

```bash
# Check workflow status
gh workflow list

# Enable workflow
gh workflow enable copilot-task-automation.yml
```

## Step 9: Generate GitHub Issues

### 9.1 Test with Single Issue (Dry Run)

```bash
# Preview what would be created
python3 scripts/create-github-issues.py T24 --dry-run
```

### 9.2 Create HIGH AI Tasks (Recommended Start)

```bash
# Create 5 HIGH AI effectiveness tasks
python3 scripts/create-github-issues.py --ai-high-only

# Expected output:
# ✅ Created issue #1: T2 - GitHub Milestones & Issues Creation
# ✅ Created issue #2: T24 - Supabase Database Setup with RLS
# ✅ Created issue #3: T27 - Backend Unit Tests (Vitest)
# ✅ Created issue #4: T32 - API Documentation & OpenAPI
# ✅ Created issue #5: T52 - Batch Image Generation
```

### 9.3 View Created Issues

```bash
# List all issues
gh issue list

# View specific issue
gh issue view 1

# View in browser
gh issue view 1 --web
```

## Step 10: Start Development with Copilot

### 10.1 Test Automation on T24

```bash
# Option A: Comment on issue
gh issue comment 2 --body "/automate"

# Option B: Add label (if not already added)
gh issue edit 2 --add-label "automation:ready"

# Option C: Assign to copilot (if you have copilot user)
# gh issue edit 2 --add-assignee copilot
```

### 10.2 Monitor Workflow

```bash
# Watch workflow in real-time
gh run watch

# View recent runs
gh run list --workflow copilot-task-automation.yml --limit 5

# View specific run
gh run view <RUN_ID>
```

### 10.3 Check for Generated PR

```bash
# List auto-generated PRs
gh pr list --label "auto-generated"

# View PR
gh pr view <PR_NUMBER>

# View in browser
gh pr view <PR_NUMBER> --web
```

### 10.4 Review & Merge

```bash
# Checkout PR
gh pr checkout <PR_NUMBER>

# Review generated files
ls -la apps/backend/src/
grep -r "TODO" apps/backend/src/

# Run tests (if applicable)
# pnpm test

# Approve
gh pr review <PR_NUMBER> --approve

# Merge
gh pr merge <PR_NUMBER> --squash
```

## Step 11: Scale Up Development

### 11.1 Create More Issues

```bash
# Create all M0 issues
python3 scripts/create-github-issues.py --milestone M0

# Create all M1 issues
python3 scripts/create-github-issues.py --milestone M1

# Create ALL issues (93 total)
python3 scripts/create-github-issues.py
```

### 11.2 Automate Multiple Tasks

```bash
# Trigger automation for multiple HIGH AI tasks
for issue_num in 1 2 3 4 5; do
  gh issue comment $issue_num --body "/automate"
  sleep 10  # Wait between triggers
done
```

### 11.3 Monitor Progress

```bash
# Dashboard view
gh issue list --json number,title,state,labels

# PRs
gh pr list

# Workflow runs
gh run list --limit 10
```

---

## 📊 Expected Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| **Setup** (Steps 1-8) | 30 min | Create repo, configure GitHub |
| **Issue Creation** (Step 9) | 5 min | Generate 5 HIGH AI issues |
| **First Automation** (Step 10) | 15 min | Test T24, review PR |
| **Scale Up** (Step 11) | 2-3 hours | Process remaining HIGH AI tasks |
| **Total** | **~4 hours** | Complete HIGH AI automation |

**Traditional development**: 10.5 days  
**Savings**: 71% (6.5 days saved)

---

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub repo created: `gh repo view neutrico/morpheus-press`
- [ ] Secret configured: `gh secret list | grep ANTHROPIC_API_KEY`
- [ ] Labels created: `gh label list | wc -l` (should be ~13)
- [ ] Milestones created: `gh milestone list | wc -l` (should be 5)
- [ ] Workflow exists: `gh workflow list`
- [ ] Issues created: `gh issue list | wc -l` (at least 5)
- [ ] Automation working: `gh run list --limit 1`
- [ ] PR generated: `gh pr list --label "auto-generated"`

---

## 🎓 Pro Tips

**1. Start Small**
- Test with T24 first (simple database setup)
- Don't create all 93 issues immediately

**2. Monitor Costs**
- Each task generation: ~$0.15
- 5 HIGH AI tasks: ~$0.75 total
- Set budget alerts in Anthropic dashboard

**3. Review Generated Code**
- Always check TODO comments
- Copilot Agent should implement them
- Don't merge without verification

**4. Iterate on Prompts**
- If generated code is poor, improve prompts in `task-automation-agent.py`
- Test with `--dry-run` flag

**5. Use Milestones**
- Group issues by milestone (M0, M1, etc.)
- Focus on one milestone at a time

---

## 🚀 Ready to Begin!

**Start here:**

```bash
# 1. Create repo locally
cd /workspaces && mkdir morpheus-press && cd morpheus-press

# 2. Run all copy commands from Step 2

# 3. Follow Steps 3-11

# 4. Start development!
```

**Questions?** Check [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)

**Status**: ✅ Ready for execution

---

**Good luck!** 🎉
