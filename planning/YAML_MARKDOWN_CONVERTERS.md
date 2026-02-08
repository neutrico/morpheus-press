# YAML ↔ Markdown Converters - Quick Guide

## Why Two Formats?

**Hybrid approach** - best of both worlds:

- **YAML** (`planning/issues/*.yaml`) - Source of truth for automation
  - Machine-parseable
  - Build system (validation, combining)
  - GitHub sync

- **Markdown** (`planning/docs/**/*.md`) - Human/agent-friendly editing
  - Readable formatting
  - GitHub renders beautifully
  - Works with Obsidian/Logseq
  - YAML frontmatter for metadata

## Quick Start

```bash
# 1. Generate Markdown from YAML
python scripts/yaml-to-markdown.py

# 2. Agents edit Markdown files
# (planning/docs/m1---backend-services/T23-backend-typescript-port.md)

# 3. Convert back to YAML
python scripts/markdown-to-yaml.py

# 4. Validate & build
python scripts/build-planning.py

# 5. Sync to GitHub
python scripts/sync-to-github.py
```

## Markdown Format

Each issue becomes a `.md` file with YAML frontmatter:

```markdown
---
key: T23
title: Backend TypeScript Port
type: Task
milestone: M1 - Backend Services
iteration: I2
priority: p0
effort: 8
area: backend
dependsOn: []
---

# Backend TypeScript Port

## Description

Port backend from Python to TypeScript with Fastify 5

**Context:** Current backend is Python, need TypeScript for monorepo

**Goal:** Unified TypeScript codebase

**Scope:** Core API routes, database abstraction, authentication

**Business Value:** Easier maintenance, better type safety

## Acceptance Criteria

- [ ] **Backend starts without errors**
  - Verification: Run `pnpm dev:backend` and check logs

- [ ] **All routes respond correctly**
  - Verification: curl `/health`, `/api/books`, `/api/users`

- [ ] **Tests pass**
  - Verification: `pnpm test:backend` shows 100% pass rate

## Technical Notes

### Approach

Use Fastify 5 plugin architecture for modularity. Separate concerns: routes →
services → providers.

### Files to Modify

- `apps/backend/src/server.ts` - Update Fastify initialization
- `apps/backend/package.json` - Add dependencies

### New Files to Create

- `apps/backend/src/types/fastify.d.ts`
- `apps/backend/src/routes/index.ts`

### External Dependencies

- **fastify** ^5.0.0
  - Fast and low overhead web framework
- **@supabase/supabase-js** ^2.38.0
  - Database client with RLS support

### Internal Dependencies

- DatabaseService (src/services/database.ts)
- LlmProviderFactory (src/providers/factory.ts)

## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/server.test.ts`
  - Scenarios: Server starts, Routes registered, Error handling

### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/api.test.ts`
  - Scenarios: Full API flow, Database queries, Auth middleware

### E2E Tests

- Scenario: Book upload → analysis → results
  - Step 1: POST /api/books with file
  - Step 2: Wait for processing
  - Step 3: GET /api/books/:id for results

## Documentation

### Updates Required

- Update README.md with new backend setup instructions
- Update API.md with new endpoints

### New Documentation

- Backend architecture diagram
- Service dependency map

## Risks

- **Risk**: TypeScript types for Supabase tables might be outdated
  - **Mitigation**: Regenerate types from latest schema

- **Risk**: Migration might break existing frontend
  - **Mitigation**: Keep API contract identical, test with current dashboard

## Estimates

- **Development**: 3d
- **Code Review**: 0.5d
- **Testing**: 1d
- **Documentation**: 0.5d
- **Total**: 5d

## Progress

- **Status**: not-started
- **Started**:
- **Completed**:

### Checklist

- [ ] Setup Fastify project structure
- [ ] Port authentication routes
- [ ] Port book management routes
- [ ] Port ML service routes
- [ ] Write tests
- [ ] Update documentation

## Agent Notes

### Research Findings

Investigated Fastify 5 vs Express:

- Fastify 3x faster than Express
- Native TypeScript support
- Plugin ecosystem mature
- Supabase v2 client supports RLS

Recommended approach: Fastify plugin architecture.

### Design Decisions

1. Use dependency injection via constructors
2. Keep routes thin, logic in services
3. Zod for request/response validation
4. Pino for structured logging

### Open Questions

- Should we migrate in stages or all at once?
- What's the rollback strategy if migration fails?
- Do we need feature flags for gradual rollout?
```

## Benefits

### For Agents (AI)

- ✅ Clear structure with headers (easy to parse sections)
- ✅ Empty sections are visible (shows what needs work)
- ✅ Can edit one issue without touching others (no merge conflicts)
- ✅ Standard Markdown format (LLMs trained on it)

### For Humans

- ✅ Readable in GitHub (renders beautifully)
- ✅ Can open in Obsidian/Logseq (knowledge graph)
- ✅ Can search across issues with grep/ripgrep
- ✅ Git diffs are small and clear

### For Tooling

- ✅ YAML source of truth preserved (automation still works)
- ✅ Build validation ensures consistency
- ✅ Round-trip conversion tested (YAML → MD → YAML)
- ✅ No data loss (all fields preserved)

## Directory Structure

```
planning/
├── issues/                          # YAML source of truth
│   ├── m0-infrastructure.yaml       (18 tasks)
│   ├── m1-backend.yaml              (19 tasks)
│   └── ...
└── docs/                            # Generated Markdown for editing
    ├── m0---infrastructure-&-setup/
    │   ├── T1-tech-stack-decision-documentation.md
    │   ├── T2-github-milestones-&-issues-creation.md
    │   └── ...
    ├── m1---backend-services/
    │   ├── T23-backend-typescript-port.md
    │   ├── T24-supabase-database-setup-with-rls.md
    │   └── ...
    └── ...
```

## Conversion Details

### yaml-to-markdown.py

**What it does:**

- Reads YAML from `planning/issues/*.yaml`
- Generates Markdown files in `planning/docs/milestone/`
- Preserves all fields (no data loss)
- Creates directory per milestone

**Features:**

- Formats acceptance criteria as checkboxes
- Formats technical notes with sub-sections
- Formats testing with test types
- YAML frontmatter for metadata

**Usage:**

```bash
python scripts/yaml-to-markdown.py [--issues-dir planning/issues] [--output-dir planning/docs]
```

### markdown-to-yaml.py

**What it does:**

- Reads Markdown from `planning/docs/**/*.md`
- Parses YAML frontmatter
- Parses Markdown sections
- Updates YAML files in `planning/issues/`

**Features:**

- Parses acceptance criteria checkboxes
- Extracts technical notes sub-sections
- Preserves task count metadata
- Maps milestones to correct files

**Usage:**

```bash
python scripts/markdown-to-yaml.py [--input-dir planning/docs] [--output-dir planning/issues]
```

## Validation

After editing Markdown and converting back:

```bash
# 1. Convert Markdown → YAML
python scripts/markdown-to-yaml.py

# 2. Validate structure
python scripts/build-planning.py
# Should show:
# ✅ Build successful!
#    Output: /workspaces/morpheus/planning/pi.yaml.built
#    Milestones: 8
#    Issues: 93
#    Labels: 18

# 3. Review changes
git diff planning/issues/

# 4. If valid, commit
git add planning/issues/
git commit -m "refine(planning): Updated issues from Markdown"
```

## Common Patterns

### Adding Research Findings

```markdown
## Agent Notes

### Research Findings

**LLM Provider Selection:**

- Investigated OpenAI GPT-4o vs Anthropic Claude 3.5 Haiku
- Claude Haiku: $0.25/MTok input, $1.25/MTok output
- GPT-4o-mini: $0.15/MTok input, $0.60/MTok output
- Recommendation: Use GPT-4o-mini for cost optimization

**Technical Approach:**

- Fastify plugin architecture for modularity
- Dependency injection via constructors
- Zod for validation
```

### Adding Implementation Plan

```markdown
## Technical Notes

### Approach

1. Create Fastify instance with plugins
2. Register routes as plugins
3. Setup error handlers
4. Add request/response logging

### Files to Modify

- `apps/backend/src/server.ts` - Main server setup
- `apps/backend/src/routes/books.ts` - Book routes
- `apps/backend/package.json` - Add dependencies

### New Files to Create

- `apps/backend/src/types/fastify.d.ts` - Type augmentations
- `apps/backend/src/plugins/supabase.ts` - Supabase plugin
```

### Adding Testing Strategy

```markdown
## Testing

### Unit Tests

- **File**: `apps/backend/src/__tests__/server.test.ts`
  - Scenarios: Server initialization, Plugin registration, Error handling

### Integration Tests

- **File**: `apps/backend/src/__tests__/integration/books.test.ts`
  - Scenarios: Create book, List books, Update book, Delete book

### E2E Tests

- Scenario: Full book upload flow
  - Step 1: Upload book file
  - Step 2: Verify book created in DB
  - Step 3: Verify analysis started
```

## Troubleshooting

### Error: "Unknown milestone"

**Problem:**

```
⚠️  Warning: Unknown milestone 'M3 - Content Generation', skipping
```

**Solution:** Check milestone name in frontmatter matches `milestones.yaml`:

```bash
grep "^- name:" planning/milestones.yaml
```

Update Markdown frontmatter to match exact name.

### Error: "No valid YAML frontmatter found"

**Problem:**

```
❌ Error parsing T23-backend-typescript-port.md: No valid YAML frontmatter found
```

**Solution:** Ensure frontmatter has `---` delimiters:

```markdown
---
key: T23
title: Backend TypeScript Port
---

# Content here
```

### Validation fails after conversion

**Problem:**

```bash
python scripts/build-planning.py
# Error: Issue T23 references non-existent dependency T99
```

**Solution:** Check `dependsOn` in frontmatter - ensure all referenced tasks
exist:

```yaml
---
dependsOn: [T21, T22]  # Must be valid task keys
---
```

## Next Steps

1. **Generate Markdown**: `python scripts/yaml-to-markdown.py`
2. **Edit issues**: Open `planning/docs/**/*.md` in your editor
3. **Convert back**: `python scripts/markdown-to-yaml.py`
4. **Validate**: `python scripts/build-planning.py`
5. **Review**: `git diff planning/issues/`
6. **Commit**: `git add planning/ && git commit`

## See Also

- [planning/README.md](planning/README.md) - Main planning documentation
- [planning/AGENT_WORKFLOWS.md](planning/AGENT_WORKFLOWS.md) - Agent guide
- [planning/ISSUE_TEMPLATE.yaml](planning/ISSUE_TEMPLATE.yaml) - Issue structure
- [docs/TASK_FORMAT_COMPARISON.md](docs/TASK_FORMAT_COMPARISON.md) - Format
  comparison
