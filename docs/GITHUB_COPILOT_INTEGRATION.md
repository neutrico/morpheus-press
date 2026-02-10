# GitHub Copilot Integration Guide

**Last Updated:** 2026-02-09  
**Status:** 🟢 Active  
**Version:** 1.0.0  

---

## 📋 Overview

This document describes the integration between GitHub Issues, Projects v2, and GitHub Copilot agents for automated task assignment and code generation in the Morpheus Press planning system.

### Key Capabilities

- 🤖 **Automated Agent Assignment**: Assign Copilot to issues via GraphQL API
- 📝 **Custom Instructions**: Generate context-rich prompts from YAML specifications
- 🔄 **Workflow Automation**: End-to-end issue → code → PR → review pipeline
- 📊 **Metadata Tracking**: Full traceability from planning to implementation

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Issues + Projects v2                   │
│                                                                   │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │  Issue   │──────│ Project  │──────│ Copilot  │              │
│  │  Tracker │      │  Board   │      │  Agent   │              │
│  └────┬─────┘      └────┬─────┘      └────┬─────┘              │
│       │                 │                   │                    │
└───────┼─────────────────┼───────────────────┼────────────────────┘
        │                 │                   │
        ▼                 ▼                   ▼
┌───────────────────────────────────────────────────────────────┐
│              Planning System (morpheus-press)                  │
│                                                                 │
│  ┌──────────────┐    ┌────────────────┐    ┌──────────────┐  │
│  │ planning/    │    │ scripts/       │    │ .github/     │  │
│  │ ├─ pi.yaml   │───▶│ automation/    │───▶│ workflows/   │  │
│  │ ├─ docs/     │    │ └─ generators/ │    │              │  │
│  │ └─ issues/   │    │                │    │              │  │
│  └──────────────┘    └────────────────┘    └──────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   Task Specs          Code Generation            Automation
   (Markdown)          (Python/TS)                (GitHub Actions)
```

---

## 🔌 GitHub GraphQL API Integration

### Authentication

```bash
# Set GitHub personal access token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Required scopes:
# - read:org
# - write:issues
# - write:pull_requests
# - write:projects
```

### Copilot Assignment Mutation

**Operation:** `addAssigneesToAssignable`

```graphql
mutation AssignCopilot($issueId: ID!, $instructions: String!) {
  addAssigneesToAssignable(
    input: {
      assignableId: $issueId
      assigneeIds: ["copilot"]
      agentAssignment: {
        instructions: $instructions
      }
    }
  ) {
    assignable {
      ... on Issue {
        id
        number
        title
        assignees(first: 10) {
          nodes {
            login
          }
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "issueId": "I_kwDOAbcdEfgh1234567",
  "instructions": "# Task: T24 - Supabase Database Setup\n\n## Context\n..."
}
```

**Response:**
```json
{
  "data": {
    "addAssigneesToAssignable": {
      "assignable": {
        "id": "I_kwDOAbcdEfgh1234567",
        "number": 42,
        "title": "T24: Supabase Database Setup with RLS",
        "assignees": {
          "nodes": [
            { "login": "copilot" }
          ]
        }
      }
    }
  }
}
```

---

## 📝 Custom Instruction Generation

### Instruction Template Structure

```markdown
# Task: {task_key} - {task_title}

## Context
{task_description}

{research_findings}

## Technical Requirements
- Priority: {priority}
- Estimated Effort: {estimated_days} days
- AI Effectiveness: {ai_effectiveness}
- Type: {task_type}

## Implementation Approach
{implementation_notes}

{design_decisions}

## Quality Standards
- Follow SOLID, DRY, KISS principles
- Write unit tests (Vitest for backend, Playwright for E2E)
- Add comprehensive error handling
- Use TypeScript strict mode
- Follow patterns in .github/copilot-instructions.md

## Expected Files
{expected_file_list}

## Related Resources
- Spec: planning/docs/{milestone}/{task_key}.md
- Issues: planning/issues/{milestone}.yaml
- Architecture: .github/copilot-instructions.md

## Testing Requirements
{test_requirements}
```

### Example: T24 - Supabase Setup

```markdown
# Task: T24 - Supabase Database Setup with RLS

## Context
Set up Supabase PostgreSQL database schema with Row-Level Security (RLS) policies
for multi-tenant book management. Core tables: Book, Character, Scene, User.

Research findings indicate HIGH AI effectiveness for:
- SQL migration generation
- RLS policy templates
- Index optimization
- Trigger creation

## Technical Requirements
- Priority: P1
- Estimated Effort: 2.0 days
- AI Effectiveness: HIGH
- Type: database_setup

## Implementation Approach
1. Create migration: `supabase/migrations/YYYYMMDDHHMMSS_book_schema.sql`
2. Define tables with UUID primary keys
3. Implement RLS policies (user-based access control)
4. Add indexes for performance
5. Create triggers for `updated_at` timestamps
6. Grant permissions for anon/authenticated roles

Key design decisions:
- Use PascalCase for core tables (Book, Character)
- Use snake_case for feature tables (store_products)
- Enable RLS on all user-facing tables
- Use service role for admin operations

## Quality Standards
- Follow SOLID, DRY, KISS principles
- Write migration tests with Supabase CLI
- Add comprehensive comments in SQL
- Use PostgreSQL best practices
- Test RLS policies with different user roles

## Expected Files
- supabase/migrations/YYYYMMDDHHMMSS_T24_setup.sql
- apps/backend/src/services/database.service.ts (update)
- apps/backend/src/__tests__/database.test.ts
- docs/DATABASE_SCHEMA.md (update)

## Related Resources
- Spec: planning/docs/m1---backend-services/T24-supabase-database-setup-with-rls.md
- Architecture: .github/copilot-instructions.md (Database Patterns section)
- Supabase docs: https://supabase.com/docs/guides/database

## Testing Requirements
- Test migrations: `supabase db reset`
- Test RLS policies with different user roles
- Verify indexes exist: `\d+ table_name`
- Check trigger functionality
```

---

## 🤖 Automation Workflows

### Pattern 1: Direct Assignment (Recommended)

**Use Case:** Manual, controlled assignment for critical tasks

```python
# scripts/automation/assign-copilot.py
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def assign_copilot_to_issue(issue_id: str, instructions: str):
    """Assign GitHub Copilot to an issue with custom instructions."""
    
    transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
    )
    
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    mutation = gql("""
        mutation AssignCopilot($issueId: ID!, $instructions: String!) {
          addAssigneesToAssignable(
            input: {
              assignableId: $issueId
              assigneeIds: ["copilot"]
              agentAssignment: {
                instructions: $instructions
              }
            }
          ) {
            assignable {
              ... on Issue {
                id
                number
                assignees(first: 10) {
                  nodes {
                    login
                  }
                }
              }
            }
          }
        }
    """)
    
    result = client.execute(mutation, variable_values={
        "issueId": issue_id,
        "instructions": instructions
    })
    
    return result

# Usage
instructions = generate_instructions_from_yaml("T24")
assign_copilot_to_issue("I_kwDOAbcdEfgh1234567", instructions)
```

### Pattern 2: Comment-Based Trigger

**Use Case:** Ad-hoc automation via issue comments

**GitHub Actions Workflow:**
```yaml
# .github/workflows/copilot-assign.yml
name: Assign Copilot on Comment

on:
  issue_comment:
    types: [created]

jobs:
  assign:
    if: contains(github.event.comment.body, '/automate')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Extract Task Key
        id: task
        run: |
          TASK_KEY=$(echo "${{ github.event.issue.title }}" | grep -oP 'T\d+')
          echo "key=$TASK_KEY" >> $GITHUB_OUTPUT
      
      - name: Generate Instructions
        id: instructions
        run: |
          python scripts/automation/generate-instructions.py ${{ steps.task.outputs.key }}
      
      - name: Assign Copilot
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/automation/assign-copilot.py \
            --issue-id "${{ github.event.issue.node_id }}" \
            --instructions-file "/tmp/instructions.md"
```

### Pattern 3: Label-Based Automation

**Use Case:** Batch processing for multiple issues

**Workflow Trigger:**
```yaml
on:
  issues:
    types: [labeled]

jobs:
  automate:
    if: github.event.label.name == 'automation:ready'
    runs-on: ubuntu-latest
    steps:
      # ... similar to Pattern 2
```

---

## 📊 Integration with Planning System

### Task Metadata → Instructions

**Source:** `planning/pi.yaml` or `planning/issues/*.yaml`

```yaml
# Example: planning/issues/m1-backend.yaml
tasks:
  - key: T24
    title: Supabase Database Setup with RLS
    description: |
      Set up PostgreSQL schema with RLS policies for multi-tenant access.
    priority: p1
    estimated_days: 2.0
    ai_effectiveness: high
    milestone: M1
    area: backend
    type: database_setup
    
    implementation_notes: |
      - Create migrations in supabase/migrations/
      - Use PascalCase for core tables
      - Enable RLS on all tables
      - Add indexes for foreign keys
    
    agent_notes:
      research_findings: |
        HIGH AI effectiveness for SQL generation, RLS policies,
        and index optimization. LLM can generate production-ready
        migrations with proper naming conventions.
```

**Generated Instructions:**
```python
def generate_instructions(task_yaml: dict) -> str:
    """Generate Copilot instructions from task YAML."""
    
    template = f"""
# Task: {task_yaml['key']} - {task_yaml['title']}

## Context
{task_yaml['description']}

{task_yaml.get('agent_notes', {}).get('research_findings', '')}

## Technical Requirements
- Priority: {task_yaml['priority'].upper()}
- Estimated Effort: {task_yaml['estimated_days']} days
- AI Effectiveness: {task_yaml['ai_effectiveness'].upper()}
- Milestone: {task_yaml['milestone']}
- Area: {task_yaml['area']}

## Implementation Approach
{task_yaml.get('implementation_notes', 'See detailed spec in planning/docs/')}

## Quality Standards
- Follow SOLID, DRY, KISS principles
- Write tests (Vitest for backend)
- Add comprehensive error handling
- Follow .github/copilot-instructions.md

## Expected Files
{_generate_expected_files(task_yaml)}

## Related Resources
- Spec: planning/docs/{task_yaml['milestone'].lower()}/{task_yaml['key']}.md
- Architecture: .github/copilot-instructions.md
"""
    return template.strip()
```

---

## 🎯 Best Practices

### DO ✅

1. **Comprehensive Context**: Include all relevant information in instructions
2. **Clear Acceptance Criteria**: Define what "done" means
3. **Link to Resources**: Reference docs, specs, and examples
4. **Specify Patterns**: Point to existing code patterns to follow
5. **Error Handling**: Request comprehensive error handling
6. **Testing Requirements**: Specify test coverage expectations

### DON'T ❌

1. **Vague Instructions**: Avoid "implement feature X" without context
2. **Missing Constraints**: Always specify technical requirements
3. **Ignore Quality**: Don't skip code quality standards
4. **Forget Testing**: Always include test requirements
5. **Overload Instructions**: Keep under 4KB (GitHub limit)

### Example: Good vs. Bad Instructions

**❌ Bad (Vague):**
```markdown
# Task: Add database support

Implement database functionality.
```

**✅ Good (Specific):**
```markdown
# Task: T24 - Supabase Database Setup with RLS

## Context
Set up PostgreSQL schema for multi-tenant book management.
Core tables: Book, Character, Scene, User.

## Technical Requirements
- Use Supabase PostgreSQL (local Docker setup)
- Enable Row-Level Security on all tables
- Follow naming: PascalCase for core, snake_case for features

## Implementation
1. Create migration: supabase/migrations/YYYYMMDDHHMMSS_T24_setup.sql
2. Define schema with UUID primary keys
3. Implement RLS policies for user-based access
4. Add indexes on foreign keys
5. Create updated_at triggers

## Quality
- Follow .github/copilot-instructions.md patterns
- Write migration tests
- Document schema in docs/DATABASE_SCHEMA.md

## Testing
- Test: `supabase db reset`
- Verify RLS with different user roles
- Check indexes: `\d+ table_name`
```

---

## 📈 Monitoring and Metrics

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Assignment Success Rate | > 95% | GraphQL mutation success |
| Instruction Quality | High | Human review score |
| Time to First Response | < 1 hour | Copilot reply timestamp |
| Code Generation Success | > 80% | Tests pass on first try |
| Manual Intervention | < 20% | Requires human fixes |

### Monitoring Script

```python
# scripts/automation/monitor-assignments.py
def monitor_copilot_assignments():
    """Monitor Copilot assignment success rates."""
    
    metrics = {
        "total_assignments": 0,
        "successful_assignments": 0,
        "failed_assignments": 0,
        "average_response_time": 0,
        "code_quality_score": 0
    }
    
    # Query GitHub GraphQL for assignment history
    # Calculate metrics
    # Generate report
    
    return metrics
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Copilot not available" | Org permissions | Verify Copilot enabled for org |
| "Assignment failed" | Invalid issue ID | Use GitHub node ID, not number |
| "Instructions too long" | > 4KB limit | Compress or link to full docs |
| "No response from Copilot" | API rate limit | Implement exponential backoff |
| "Generated code fails tests" | Insufficient context | Improve instruction quality |

### Debug GraphQL Queries

```bash
# Test GraphQL connectivity
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -X POST \
     -d '{"query":"query { viewer { login } }"}' \
     https://api.github.com/graphql

# Get issue node ID
gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) {
        id
        title
      }
    }
  }
' -f owner=neutrico -f repo=morpheus-press -F number=42
```

---

## 🚀 Future Enhancements

### Short Term (1-2 months)
- [ ] Implement batch assignment for multiple issues
- [ ] Add template library for common task types
- [ ] Create monitoring dashboard
- [ ] Auto-retry logic for transient failures

### Medium Term (3-6 months)
- [ ] ML-based instruction optimization
- [ ] Feedback loop from code reviews
- [ ] Integration with project boards
- [ ] Automated test case generation

### Long Term (6+ months)
- [ ] Self-improving instruction templates
- [ ] Predictive task automation
- [ ] Cross-repository pattern learning
- [ ] Full autonomous development pipeline

---

## 📚 References

### Internal Documentation
- [Copilot Instructions](../.github/copilot-instructions.md)
- [Automation README](../scripts/automation/README.md)
- [Agent Workflows](../planning/AGENT_WORKFLOWS.md)
- [Test Results](../planning/test/tt2-results.md)

### GitHub Documentation
- [GraphQL API v4](https://docs.github.com/en/graphql)
- [Copilot for Business](https://docs.github.com/en/copilot)
- [Projects v2 API](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions](https://docs.github.com/en/actions)

### External Resources
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## ✅ Validation Checklist

Before using this integration:

- [ ] GitHub Copilot enabled for organization
- [ ] Personal access token with required scopes
- [ ] Planning YAML files properly structured
- [ ] Task specifications in `planning/docs/`
- [ ] Test environment configured
- [ ] Monitoring scripts in place
- [ ] Error handling implemented
- [ ] Documentation reviewed and up-to-date

---

**Document Owner:** GitHub Copilot Agent  
**Last Reviewed:** 2026-02-09  
**Next Review:** 2026-03-09  
**Status:** 🟢 Active
