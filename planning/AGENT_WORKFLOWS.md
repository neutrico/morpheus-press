# Agent Workflows for Issue Refinement

This document describes how research and planning agents should work with issues

in the modular planning structure.

## Two Ways to Edit Issues



### Option 1: Edit YAML directly (traditional)
```bash
# Edit issues/*.yaml files directly
vim planning/issues/m1-backend.yaml
```

### Option 2: Edit Markdown (RECOMMENDED for agents)
```bash
# 1. Generate Markdown from YAML
python scripts/yaml-to-markdown.py

# 2. Edit readable Markdown files with YAML frontmatter
vim planning/docs/m1---backend-services/T23-backend-typescript-port.md

# 3. Convert back to YAML
python scripts/markdown-to-yaml.py

# 4. Validate structure
python scripts/build-planning.py
```

**Why Markdown is better for agents:**
- ✅ More readable (proper headers, sections clearly visible)
- ✅ GitHub renders it beautifully (can review in browser)
- ✅ Works with Obsidian/Logseq (knowledge graphs, linking)
- ✅ Easier to see what's missing (empty sections are obvious)

- ✅ YAML frontmatter for structured metadata
- ✅ Small Git diffs (one file per task)


  
**Markdown format example:**
```markdown
---
key: T23
title: Backend TypeScript Port
type: Task
milestone: M1 - Backend Services
priority: p0
effort: 8

---

# Backend TypeScript Port

## Description
Port backend to TypeScript...

## Acceptance Criteria
- [ ] **Backend starts without errors**
  - Verification: Run `pnpm dev:backend`

## Technical Notes
### Approach
Use Fastify plugin architecture...

## Agent Notes
### Research Findings
Investigated Fastify 5 vs Express...
```

## Overview

Issues are stored in modular YAML files under `planning/issues/`, grouped by
milestone. Each issue should follow the structure defined in
`planning/ISSUE_TEMPLATE.yaml`.

## Directory Structure

```
planning/

├── ISSUE_TEMPLATE.yaml          # Template for issue structure
├── pi-metadata.yaml              # Project metadata

├── milestones.yaml               # Milestone definitions
├── labels.yaml                   # Labels and project fields
├── issues/                       # Issues grouped by milestone
│   ├── m0-infrastructure.yaml
│   ├── m1-backend.yaml
│   ├── m2-ml-training.yaml
│   ├── m3-content-generation.yaml
│   ├── m4-dashboard.yaml
│   ├── m5-product-assembly.yaml
│   ├── m6-commerce-distribution.yaml

│   └── m7-launch.yaml
└── pi.yaml.built                 # Generated combined file (DO NOT EDIT)
```

## Agent Responsibilities

### Research Agent

**Purpose:** Investigate technical approaches, gather requirements, identify
risks

**Tasks:**

1. Read current issue from milestone file (e.g.,
   `planning/issues/m1-backend.yaml`)
2. Research best practices for the task
3. Investigate technology options
4. Identify potential risks and blockers
5. Document findings in `agent_notes.research_findings`
6. Propose technical approach in `technical_notes.approach`
7. List external dependencies needed
8. Update issue YAML with research findings

**Example workflow:**

```bash
# 1. Read issue
cd planning/issues
cat m1-backend.yaml | grep -A 50 "key: T23"

# 2. Research (use web search, documentation, code examples)

# 3. Update issue with findings
# Edit m1-backend.yaml, add:
agent_notes:
  research_findings: |
    Investigated TypeScript backend patterns:
    - Fastify 5 is recommended for performance
    - Supabase client v2.x has RLS support
    - Average implementation time: 3-5 days
    
technical_notes:
  approach: |
    Use Fastify plugin architecture for modularity.
    Separate concerns: routes → services → database.
    
  external_dependencies:
    - name: "@supabase/supabase-js"
      version: "^2.38.0"
      reason: "Database client with RLS support"
```


### Planning Agent

**Purpose:** Break down tasks, define acceptance criteria, create implementation
plan

**Tasks:**

1. Read issue enhanced by research agent

2. Define detailed acceptance criteria
3. List files to modify/create
4. Define testing strategy
5. Estimate time and effort
6. Identify sub-tasks for checklist
7. Document design decisions
8. Update issue YAML with planning details

**Example workflow:**

```bash
# 1. Read enhanced issue
cat planning/issues/m1-backend.yaml | grep -A 100 "key: T23"

# 2. Add acceptance criteria
acceptance_criteria:
  - criterion: "Backend starts without errors"
    verification: "Run `pnpm dev:backend` and check logs"
  - criterion: "API responds to health check"
    verification: "curl http://localhost:3002/health returns 200"
  - criterion: "All routes are registered"
    verification: "Check Fastify route list in console"

# 3. Define implementation plan
technical_notes:
  files_to_modify:
    - path: apps/backend/src/server.ts
      changes: "Update Fastify initialization, register plugins"
    - path: apps/backend/package.json
      changes: "Add new dependencies"
  
  new_files:
    - path: apps/backend/src/types/fastify.d.ts
      purpose: "Fastify type augmentations"

# 4. Testing strategy
testing:
  unit_tests:
    - file: apps/backend/src/__tests__/server.test.ts
      coverage_target: 85%
      scenarios:
        - "Server starts successfully"
        - "Routes are registered"
        - "Error handling works"
```

## Workflow Steps

### Step 1: Select Issue to Refine
  

```bash
# List all issues in a milestone
cat planning/issues/m1-backend.yaml

# Find unrefined issues (minimal details)
grep -B 2 "description:" planning/issues/m1-backend.yaml
```

### Step 2: Research Phase

Research agent adds:

- `description` (context, goal, scope, business value)
- `agent_notes.research_findings`
- `technical_notes.approach`
- `technical_notes.external_dependencies`
- `risks` (with mitigations)

### Step 3: Planning Phase


Planning agent adds:


- `acceptance_criteria` (detailed, verifiable)
- `technical_notes.files_to_modify`
- `technical_notes.new_files`
- `testing` (unit, integration, e2e, manual)
- `documentation` (what needs updating)
- `estimates` (dev, review, testing, docs)
- `progress.checklist` (implementation steps)

### Step 4: Validation

```bash
# Build combined YAML
python scripts/build-planning.py

# Check for errors
echo $?  # Should be 0

# Review changes
git diff planning/issues/
```

### Step 5: Commit Changes

```bash
git add planning/issues/
git commit -m "refine(planning): enhance T23 - Backend TypeScript Port"
git push origin main
```

## Issue States

Track refinement progress using `progress.status`:


 
- `not-started` - Initial state, needs research
- `researched` - Research complete, needs planning

- `planned` - Planning complete, ready for development
- `in-progress` - Development started
- `in-review` - Code review in progress

- `blocked` - Blocked by external dependency
 
- `done` - Completed and merged


## Best Practices

### For Research Agent

1. **Be Thorough:** Research multiple approaches, compare pros/cons
2. **Cite Sources:** Link to documentation, articles, examples
3. **Identify Risks:** Call out potential issues early
4. **Consider Alternatives:** Document options considered and why chosen
   approach is best
5. **Check Dependencies:** Ensure all required libraries/tools are identified

### For Planning Agent

1. **Be Specific:** Acceptance criteria should be unambiguous and testable
2. **List All Files:** Don't miss configuration files, tests, docs
3. **Define Tests:** Cover happy path, errors, edge cases
4. **Realistic Estimates:** Account for learning curve, review cycles
5. **Break Down Complex Tasks:** Large tasks should have 5-10 checklist items

### For Both

1. **Follow Template:** Use `ISSUE_TEMPLATE.yaml` as reference
2. **Validate YAML:** Ensure proper indentation and structure

3. **Cross-Reference:** Check dependencies between tasks
4. **Update Timestamps:** Set `progress.started_at` when beginning work
5. **Document Decisions:** Record "why" not just "what"

## Example: Fully Refined Issue

See `planning/ISSUE_TEMPLATE.yaml` for complete example with all sections
filled.


Key sections a refined issue MUST have:

- ✅ description (4 subsections: Context, Goal, Scope, Business Value)
- ✅ acceptance_criteria (3-5 criteria with verification)
- ✅ technical_notes.approach
- ✅ technical_notes.files_to_modify OR new_files
- ✅ testing (at least unit_tests defined)
- ✅ estimates (all 4 fields)
- ✅ progress.checklist (5-10 items)
- ✅ agent_notes.research_findings
- ✅ agent_notes.design_decisions

## Building and Syncing

After refining issues:

```bash
# 1. Build combined YAML
python scripts/build-planning.py
# Output: planning/pi.yaml.built

# 2. Validate structure
# (build script runs validation automatically)

# 3. Dry-run sync to GitHub
python scripts/sync-to-github.py --dry-run

# 4. Actual sync (when ready)
python scripts/sync-to-github.py
```

## Common Issues & Solutions

**Problem:** YAML validation fails

- **Solution:** Check indentation (use 2 spaces), ensure all lists use `-`
  format

**Problem:** Duplicate task keys

- **Solution:** Each `key: TX` must be unique across all milestone files

**Problem:** Missing dependencies

- **Solution:** Run `grep dependsOn planning/issues/*.yaml` to find all
  dependencies

**Problem:** Agent confused about structure

- **Solution:** Always reference `ISSUE_TEMPLATE.yaml` for canonical structure

## Tools for Agents

```bash
# Find issues by status
grep -r "status: not-started" planning/issues/

# Find unrefined issues (missing description)
grep -L "description:" planning/issues/*.yaml

# Count issues per milestone
for f in planning/issues/*.yaml; do 
  echo "$f: $(grep -c "^  - key:" $f) issues"
done

# Validate all YAML files
find planning -name "*.yaml" -exec yamllint {} \;
```

## Questions?

If structure is unclear:

1. Check `ISSUE_TEMPLATE.yaml`
2. Look at existing refined issues
3. Ask in Slack #morpheus-planning
4. Review this document

---

**Remember:** Detailed planning saves implementation time. A well-refined issue
should allow a developer to start coding immediately without research.
