# Morpheus Planning Structure

Modular YAML-based planning for PI-2026-Q1 (Program Increment Q1 2026).

## Quick Start

```bash
# 1. Generate Markdown for agent editing (optional but recommended)
python scripts/yaml-to-markdown.py

# 2. Agents edit Markdown files in planning/docs/

# 3. Convert back to YAML
python scripts/markdown-to-yaml.py

# 4. Build combined YAML from modules
python scripts/build-planning.py

# 5. Dry-run sync to GitHub (see what would happen)
python scripts/sync-to-github.py --dry-run

# 6. Actual sync to GitHub
python scripts/sync-to-github.py
```

## Structure

```
planning/
├── README.md                     # This file
├── AGENT_WORKFLOWS.md            # Guide for research/planning agents
├── ISSUE_TEMPLATE.yaml           # Template for issue structure
├── pi-metadata.yaml              # Project metadata
├── milestones.yaml               # 8 milestones (M0-M7)
├── labels.yaml                   # Labels and project fields
├── pi.yaml                       # DEPRECATED: Use modular files instead
├── pi.yaml.built                 # Generated combined file (auto-generated)
├── issues/                       # 93 tasks across 8 milestones (YAML source of truth)
│   ├── m0-infrastructure.yaml    # 18 tasks - Dev setup, CI/CD, monitoring
│   ├── m1-backend.yaml           # 19 tasks - API, database, auth
│   ├── m2-ml-training.yaml       # 13 tasks - Model training, datasets
│   ├── m3-content-generation.yaml # 12 tasks - SDXL, ComfyUI, prompts
│   ├── m4-dashboard.yaml         # 2 tasks  - Web UI, preview
│   ├── m5-product-assembly.yaml  # 9 tasks  - Comic layout, PDF export
│   ├── m6-commerce-distribution.yaml # 17 tasks - E-commerce, social channels
│   └── m7-launch.yaml            # 3 tasks  - Final testing, deployment
└── docs/                         # Generated Markdown (for agent editing)
    ├── m0---infrastructure-&-setup/
    │   ├── T1-tech-stack-decision-documentation.md
    │   ├── T2-github-milestones-&-issues-creation.md
    │   └── ...
    ├── m1---backend-services/
    │   ├── T23-backend-typescript-port.md
    │   └── ...
    └── ...
```

## Agent Workflow

See **[AGENT_WORKFLOWS.md](./AGENT_WORKFLOWS.md)** for complete guide on how
research and planning agents should refine issues.

**Quick summary:**

1. **Generate Markdown**: `python scripts/yaml-to-markdown.py`
2. **Research agent** investigates and documents technical approach in `.md`
   files
3. **Planning agent** defines acceptance criteria and implementation plan
4. **Convert back to YAML**: `python scripts/markdown-to-yaml.py`
5. **Validate**: `python scripts/build-planning.py`
6. **Sync to GitHub**: `python scripts/sync-to-github.py`

## YAML ↔ Markdown Conversion

**Why two formats?**

- **YAML** (`issues/*.yaml`) - Source of truth, automation-friendly, build
  system
- **Markdown** (`docs/**/*.md`) - Human/agent-friendly editing, GitHub renders
  beautifully

**Workflow:**

```bash
# Generate Markdown from YAML (one-time or when syncing from upstream)
python scripts/yaml-to-markdown.py

# Agents edit Markdown files (easier to read/write)
# Example: planning/docs/m1---backend-services/T23-backend-typescript-port.md

# Convert Markdown back to YAML (before committing)
python scripts/markdown-to-yaml.py

# Validate (ensures all references are valid)
python scripts/build-planning.py
```

**Markdown format** (with YAML frontmatter):

```markdown
---
key: T23
title: Backend TypeScript Port
type: Task
milestone: M1 - Backend Services
priority: p0
effort: 8
area: backend
---

# Backend TypeScript Port

## Description

Port backend from Python to TypeScript with Fastify 5

## Acceptance Criteria

- [ ] **Backend starts without errors**
  - Verification: Run `pnpm dev:backend`

## Technical Notes

### Approach

Use Fastify plugin architecture for modularity

### Files to Modify

- `apps/backend/src/server.ts` - Update initialization
```

## Building & Syncing

```bash
# 1. Build combined YAML (validates structure)
python scripts/build-planning.py

# 2. Sync to GitHub (creates issues, milestones, project links)
python scripts/sync-to-github.py --dry-run  # Preview first
python scripts/sync-to-github.py             # Actual sync
```

## Issue Template

All issues follow `ISSUE_TEMPLATE.yaml` structure with:

- Metadata (key, title, type, milestone, priority, effort)
- Description (context, goal, scope, business value)
- Acceptance criteria (verifiable conditions)
- Technical notes (approach, files to modify, dependencies)
- Testing strategy (unit, integration, e2e)
- Estimates (dev, review, test, docs time)
- Agent notes (research findings, design decisions)

## Statistics

- **93 tasks** across **8 milestones** and **7 iterations**
- Duration: Feb 10 - May 20, 2026 (14 weeks)
- Capacity: 30 points per iteration

See [planning/README.md](./README.md) for complete documentation.
