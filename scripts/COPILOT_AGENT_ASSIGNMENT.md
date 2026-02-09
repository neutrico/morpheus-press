# Copilot Agent Auto-Assignment

## Overview

Automated system to assign GitHub Copilot agent to the first ready-to-start task
with custom context-aware instructions.

## Features

✅ **Automatic Task Selection**

- Finds first task in milestone M0 or M1
- Ensures task has no blocking dependencies
- Prioritizes high AI effectiveness tasks
- Considers priority (p0 > p1 > p2) and effort (smaller first)

✅ **Custom Prompt Generation**

- Reads research findings from `planning/issues/*.yaml`
- Includes implementation approach and design decisions
- Adds technical requirements and quality standards
- Reminds about SOLID, DRY, KISS principles
- Specifies testing requirements (Vitest)

✅ **Full Integration**

- Seamlessly integrated into `create-issues-api.py` workflow
- Runs as Phase 3 after issue creation and relationships
- Uses official GitHub GraphQL API (`addAssigneesToAssignable`)
- Configurable base branch (defaults to `main`)

## Architecture

```
scripts/
├── copilot_agent.py             # Core Copilot agent functions
├── create-issues-api.py         # Main issue creation (uses copilot_agent)
├── test_create_issues.py        # Full E2E test (includes Copilot test)
└── test_copilot_agent.py        # Standalone Copilot assignment test
```

### Core Functions

#### `generate_copilot_instructions(task_key, task_data)`

Generates custom instructions from task metadata.

**Input:**

```python
task_data = {
    "task": "Supabase Database Setup",
    "description": "Set up database schema with RLS policies",
    "priority": "p0",
    "effort": 5,
    "ai_effectiveness": "high",
    "agent_notes": {
        "research_findings": "Supabase uses PostgreSQL with RLS...",
        "implementation_approach": "Create migrations with proper indexes...",
        "design_decisions": [
            {"decision": "Use RLS", "rationale": "Security by default"}
        ]
    }
}
```

**Output:**

```markdown
# T24: Supabase Database Setup

## Description

Set up database schema with RLS policies

## Research Findings

Supabase uses PostgreSQL with RLS...

## Implementation Approach

Create migrations with proper indexes...

## Key Design Decisions

- **Use RLS**: Security by default

## Technical Requirements

- Priority: p0
- Effort: 5 points
- AI Effectiveness: high

## Quality Standards

- Follow SOLID, DRY, KISS principles
- Write unit tests (Vitest)
- Add comprehensive error handling
- Use TypeScript strict mode

## Expected Files

- Refer to project structure in .github/copilot-instructions.md
- Follow existing patterns from similar files
```

#### `find_first_ready_task(all_tasks, created_issues, created_node_ids)`

Finds the first task that's ready to start.

**Selection Criteria:**

1. ✅ Task must be created (in `created_issues`)
2. ✅ No blocking dependencies (or all resolved)
3. ✅ Milestone M0 or Iteration I1 (preferred)
4. ✅ High AI effectiveness (preferred)
5. ✅ Sort by: priority → AI effectiveness → effort

**Returns:** `(task_key, issue_number, node_id)` or `None`

#### `assign_copilot_agent(issue_node_id, custom_instructions, base_ref="main")`

Assigns Copilot agent using GitHub GraphQL API.

**GraphQL Mutation:**

```graphql
mutation($assignableId: ID!, $agentAssignment: AgentAssignmentInput) {
  addAssigneesToAssignable(input: {
    assignableId: $assignableId
    assigneeIds: []
    agentAssignment: $agentAssignment
  }) {
    assignable {
      ... on Issue {
        id
        number
        title
      }
    }
  }
}
```

**AgentAssignmentInput:**

```json
{
  "baseRef": "main",
  "customInstructions": "Generated prompt...",
  "targetRepositoryId": "R_kgDORLroaw" // optional
}
```

## Usage

### 1. Full Workflow (create-issues-api.py)

Creates issues, sets relationships, assigns Copilot:

```bash
cd /workspaces/morpheus-press

# Create all issues and assign Copilot to first ready task
python3 scripts/create-issues-api.py --milestone="M0 - Infrastructure & Setup"

# Or with --dry-run to preview
python3 scripts/create-issues-api.py --milestone="M0 - Infrastructure & Setup" --dry-run
```

**Output:**

```
🚀 Creating issues...
   ✅ Created issue #164 (T24: Supabase Database Setup)
   ✅ Created issue #165 (T25: Backend API Skeleton)
   ...

✅ Complete: 5/5 issues created

🔗 Setting blocking relationships...
   #165 (T25) blocked by #164 (T24)... ✅
   ...

✅ Set 4 blocking relationships

🤖 Assigning Copilot agent to first ready task...
   Found ready task: #164 (T24)
   Generated instructions (1234 characters)
   Assigning Copilot to #164 (T24)... ✅

   📝 Custom instructions generated (1234 characters)
   🔗 View: https://github.com/neutrico/morpheus-press/issues/164

🔗 View issues: https://github.com/neutrico/morpheus-press/issues
🔗 View project: https://github.com/orgs/neutrico/projects/5
```

### 2. Standalone Test (test_copilot_agent.py)

Test Copilot assignment on existing issue:

```bash
# Test on issue #159 (from previous test run)
python3 scripts/test_copilot_agent.py 159
```

**Output:**

```
🧪 TEST: Assign Copilot agent to issue #159
================================================================================

📝 Step 1: Getting issue details...
✅ Found issue #159: TT1: Infrastructure Setup
   State: OPEN
   Node ID: I_kwDORLroa87pUX0B

📝 Step 2: Generating custom instructions...
✅ Generated instructions (856 characters)

────────────────────────────────────────────────────────────────────────────────
# TEST159: Test Task #159

## Description
This is a test task to verify Copilot agent assignment works correctly.

## Research Findings
Test research findings - GitHub Copilot can be assigned via GraphQL API...
────────────────────────────────────────────────────────────────────────────────

📝 Step 3: Assigning Copilot agent...
   Calling GitHub API... ✅

================================================================================
✅ TEST PASSED: Copilot successfully assigned to issue #159
================================================================================

🔗 View issue: https://github.com/neutrico/morpheus-press/issues/159
```

### 3. E2E Test (test_create_issues.py)

Full test including Copilot assignment:

```bash
python3 scripts/test_create_issues.py
```

**Output includes Phase 4:**

```
...

🤖 Phase 4: Testing Copilot agent assignment...
   Found ready task: #159 (TT1)
   Generated instructions (856 chars)
   Assigning Copilot agent... ✅

   🎉 Copilot successfully assigned to issue #159
   🔗 View: https://github.com/neutrico/morpheus-press/issues/159

================================================================================
✅ TEST PASSED: All issues created with correct relationships!
================================================================================
```

## API Reference

### GitHub GraphQL Schema

```graphql
type Mutation {
  addAssigneesToAssignable(input: AddAssigneesToAssignableInput!): AddAssigneesToAssignablePayload
}

input AddAssigneesToAssignableInput {
  assignableId: ID!           # Issue/PR node ID
  assigneeIds: [ID!]!         # User/bot IDs (can be empty with agentAssignment)
  agentAssignment: AgentAssignmentInput
}

input AgentAssignmentInput {
  targetRepositoryId: ID      # Target repo (optional, defaults to issue's repo)
  baseRef: String             # Branch (optional, defaults to default branch)
  customInstructions: String  # Custom prompt
  customAgent: String         # Agent selection (optional)
}
```

**Node IDs:**

- **Repository**: `R_kgDORLroaw` (neutrico/morpheus-press)
- **Issue**: Get via `get_issue_node_id(issue_number)`
- **Project**: `PVT_kwDOACzkfM4BOras` (Project #5)

## Requirements

### Prerequisites

1. **GitHub CLI (`gh`)** with authentication:
   ```bash
   gh auth status
   # Should show: Logged in to github.com as <username>
   ```

2. **Permissions:**
   - `repo:write` - Create and modify issues
   - `project:write` - Update project fields
   - `copilot:write` - Assign Copilot agent (beta feature)

3. **Copilot Agent Beta Access:**
   - GitHub Copilot for Issues is in beta
   - May require waitlist approval
   - Check: https://github.com/features/copilot

### Python Dependencies

```bash
pip3 install pyyaml
```

## Troubleshooting

### Issue: `addAssigneesToAssignable` returns error

**Error:**

```json
{
  "errors": [
    {
      "message": "Resource not accessible by integration",
      "type": "FORBIDDEN"
    }
  ]
}
```

**Solutions:**

1. Check Copilot beta access: https://github.com/features/copilot
2. Verify GitHub CLI permissions: `gh auth status`
3. Re-authenticate with full scopes:
   `gh auth login --scopes repo,project,copilot`
4. Check repository settings: Settings → Features → Copilot

### Issue: No ready tasks found

**Message:**

```
⚠️  No ready tasks found for Copilot assignment
💡 All tasks have dependencies or are not yet created
```

**Solutions:**

- Ensure at least one task has no `dependencies: []`
- Check `planning/estimates/effort-map.yaml` for dependency graph
- Manually create a standalone task for testing

### Issue: Custom instructions too long

**Error:**

```
Variable customInstructions of type String exceeds maximum length
```

**Solutions:**

- Instructions are truncated to ~2000 chars automatically
- If still failing, reduce research findings length in YAML
- Consider summarizing design decisions

## Testing Strategy

### Unit Tests (copilot_agent.py)

```python
def test_generate_copilot_instructions():
    """Test prompt generation."""
    task_data = {
        "task": "Test Task",
        "ai_effectiveness": "high",
        "priority": "p1",
        "effort": 3,
    }
    
    instructions = generate_copilot_instructions("T1", task_data)
    
    assert "# T1: Test Task" in instructions
    assert "SOLID, DRY, KISS" in instructions
    assert "Vitest" in instructions

def test_find_first_ready_task():
    """Test task selection logic."""
    tasks = [
        ("T1", {"dependencies": [], "milestone": "M0"}),
        ("T2", {"dependencies": ["T1"], "milestone": "M1"}),
    ]
    
    result = find_first_ready_task(tasks, {"T1": 1, "T2": 2}, {"T1": "id1", "T2": "id2"})
    
    assert result[0] == "T1"  # T1 has no dependencies
```

### Integration Tests (test_copilot_agent.py)

Tests against live GitHub API:

- ✅ Get issue node ID
- ✅ Generate custom instructions
- ✅ Assign Copilot via GraphQL
- ✅ Verify assignment visible in UI

### E2E Tests (test_create_issues.py)

Full workflow test:

- ✅ Create 5 test issues
- ✅ Set parent/child relationships
- ✅ Set blocking dependencies
- ✅ Assign Copilot to first ready task
- ✅ Verify all operations succeeded

## Implementation Notes

### Why Empty `assigneeIds`?

When using `agentAssignment`, GitHub automatically handles the Copilot bot
assignment:

```python
# No explicit Copilot bot ID needed
addAssigneesToAssignable(input: {
  assignableId: $issueId
  assigneeIds: []              # Empty - GitHub handles this
  agentAssignment: {
    customInstructions: "..."  # GitHub assigns Copilot automatically
  }
})
```

### Prompt Length Limits

GitHub GraphQL has input limits:

- **Tested limit**: ~2000 characters for `customInstructions`
- **Safe limit**: 1500 characters
- **Auto-truncation**: `generate_copilot_instructions()` truncates research
  findings to 500 chars

### Rate Limiting

GitHub API rate limits:

- **GraphQL**: 5000 points/hour
- **Points per mutation**: ~1 point
- **Sleep delays**: 0.3s between operations in scripts

## Future Enhancements

### Priority 1 (Next Sprint)

- [ ] Read `agent_notes` directly from `planning/issues/*.yaml` files
- [ ] Support multiple Copilot assignments (parallel task execution)
- [ ] Add webhook integration for auto-assignment on issue creation

### Priority 2 (Future)

- [ ] Generate prompts from OpenAPI specs for API tasks
- [ ] Include relevant code snippets in prompts
- [ ] Track Copilot completion metrics (success rate, time to completion)
- [ ] Auto-escalate if Copilot gets stuck (assign human after N hours)

### Priority 3 (Nice to Have)

- [ ] Custom agent selection (`customAgent` field)
- [ ] Multi-repository support (`targetRepositoryId`)
- [ ] A/B testing different prompt formats

## References

- **GitHub GraphQL Schema**: https://docs.github.com/en/graphql
- **Copilot for Issues**: https://github.com/features/copilot
- **GitHub CLI**: https://cli.github.com/manual/

## License

Part of Morpheus Press project - see root LICENSE file.
