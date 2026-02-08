# Morpheus Press - Planning & Automation System

**AI-powered planning and task automation** for Morpheus Press - a novel-to-comic publishing platform.

## 🎯 What This Is

This repository contains:
- **Planning System**: AI-aware task estimation (93 tasks, 99 days timeline)
- **Automation System**: LLM-powered code generation (71% time savings on HIGH AI tasks)
- **GitHub Integration**: Auto-generate code → Copilot refines → merge

**This is NOT the main application** - it's the planning/automation layer.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Test Automation

```bash
# List automatable tasks
python3 scripts/automation/task-automation-agent.py --list

# Generate code (dry-run)
python3 scripts/automation/task-automation-agent.py T24 --dry-run
```

### 3. GitHub Integration

See [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) for complete setup.

**Quick version:**

```bash
# 1. Add secret
gh secret set ANTHROPIC_API_KEY

# 2. Create labels
gh label create "auto-generated" --color "0E8A16"
gh label create "automation:ready" --color "1D76DB"

# 3. Create issues
python3 scripts/create-github-issues.py --ai-high-only

# 4. Trigger automation
# On GitHub issue, comment: /automate
```

## 📊 System Overview

**93 tasks** across 5 milestones (M0-M4)  
**99 days timeline** with 2 developers + AI  
**5 HIGH AI tasks** (71% time savings)  
**$0.75 LLM cost** for automation  
**$4,500 dev cost saved**  

## 📚 Documentation

- [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) - 30min setup guide
- [docs/COPILOT_AUTOMATION_INTEGRATION.md](./docs/COPILOT_AUTOMATION_INTEGRATION.md) - Workflow examples
- [docs/diagrams/AUTOMATION_WORKFLOW.md](./docs/diagrams/AUTOMATION_WORKFLOW.md) - Mermaid diagrams
- [scripts/automation/README.md](./scripts/automation/README.md) - Complete automation docs

## 🤖 Automation Workflow

```
Create Issue → Comment /automate → Code Generated → Copilot Refines → Human Approves → Merge
```

**5 HIGH AI tasks ready**: T2, T24, T27, T32, T52

## 📄 License

MIT

**Related**: [neutrico/morpheus](https://github.com/neutrico/morpheus) (main application)
