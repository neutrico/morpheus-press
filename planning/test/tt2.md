# TT2: Backend Core API - Test Issue

**Task Key:** TT2 (TEST166)  
**Priority:** P1  
**Type:** Test/Validation  
**AI Effectiveness:** HIGH  
**Estimated Effort:** 2 days  

---

## 📋 Description

Test issue for validating GitHub Issues + Projects v2 integration with Copilot agent assignment workflow.

This task verifies:
1. ✅ GitHub GraphQL API integration for Copilot assignment
2. ✅ Custom instruction generation from YAML specifications
3. ✅ Issue-to-PR workflow automation
4. ✅ Agent metadata tracking and reporting

---

## 🎯 Objectives

### Primary Goals
- **Validate Copilot Assignment**: Test `addAssigneesToAssignable` GraphQL mutation
- **Test Custom Instructions**: Generate context-rich prompts from planning YAML
- **Verify Automation Pipeline**: End-to-end issue → automation → PR → review flow
- **Document Integration**: Capture findings for future task implementations

### Success Criteria
- [ ] Copilot agent successfully assigned to issue
- [ ] Custom instructions generated from task specification
- [ ] Test PR created with proper labels and metadata
- [ ] Documentation updated with integration findings
- [ ] Validation report generated

---

## 🔬 Research Findings

### GitHub GraphQL API Integration

**Copilot Assignment Mutation:**
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
      id
      ... on Issue {
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

**Custom Instruction Template:**
```markdown
# Task: {task_key} - {task_title}

## Context
{task_description}

## Technical Requirements
- Priority: {priority}
- Estimated Effort: {effort_points} points
- AI Effectiveness: {ai_effectiveness}

## Implementation Approach
{implementation_notes}

## Quality Standards
- Follow SOLID, DRY, KISS principles
- Write unit tests (Vitest)
- Add comprehensive error handling
- Use TypeScript strict mode

## Expected Files
{expected_file_list}
```

### Integration Patterns

**Pattern 1: Direct Assignment (Preferred)**
- Use GraphQL API with `addAssigneesToAssignable`
- Include custom instructions in `agentAssignment` parameter
- Provides best context and control

**Pattern 2: Comment-based Trigger**
- Comment `/automate` or assign `@copilot` in issue
- GitHub Actions workflow handles assignment
- Good for manual intervention

**Pattern 3: Label-based Automation**
- Add `automation:ready` label to trigger workflow
- Automated detection and assignment
- Best for batch processing

---

## 🛠️ Implementation Details

### Test Structure

```
planning/test/
├── tt2.md                    # This specification
├── tt2-test-config.yaml      # Test configuration
└── tt2-results.md           # Test results report
```

### Test Configuration (tt2-test-config.yaml)

```yaml
test_id: TT2
test_name: Backend Core API Test
type: integration_validation
priority: p1

test_cases:
  - id: TC1
    name: Copilot Assignment via GraphQL
    description: Test direct Copilot assignment with custom instructions
    expected_result: Agent assigned successfully
    
  - id: TC2
    name: Custom Instruction Generation
    description: Generate context-rich instructions from YAML
    expected_result: Valid instruction template generated
    
  - id: TC3
    name: Automation Pipeline
    description: Test end-to-end automation workflow
    expected_result: PR created with proper metadata

validation_criteria:
  - github_api_connectivity: true
  - graphql_mutation_success: true
  - instruction_template_valid: true
  - pr_creation_success: true
  - metadata_tracking: true
```

### Expected Outcomes

1. **Test Specification**: ✅ `planning/test/tt2.md` (this file)
2. **Test Configuration**: `planning/test/tt2-test-config.yaml`
3. **Test Results**: `planning/test/tt2-results.md`
4. **Integration Documentation**: Update `docs/COPILOT_INTEGRATION.md`

---

## 📊 Acceptance Criteria

### Functional Requirements
- [x] Test specification document created
- [ ] Test configuration YAML defined
- [ ] GraphQL API connection validated
- [ ] Copilot assignment mutation tested
- [ ] Custom instructions generated correctly
- [ ] Test results documented

### Technical Requirements
- [ ] Follow existing planning structure patterns
- [ ] Use consistent YAML schema
- [ ] Generate actionable test reports
- [ ] Document all findings and edge cases

### Quality Requirements
- [ ] Clear, reproducible test steps
- [ ] Comprehensive error handling in tests
- [ ] Well-documented test results
- [ ] Integration guide for future tasks

---

## 🔄 Testing Workflow

### Phase 1: Setup
1. Create test specification (this file)
2. Define test configuration YAML
3. Prepare test environment

### Phase 2: Execution
1. Test GitHub GraphQL API connectivity
2. Execute Copilot assignment mutation
3. Generate custom instructions
4. Verify automation pipeline

### Phase 3: Validation
1. Check Copilot assignment status
2. Validate instruction template quality
3. Review PR creation and metadata
4. Document findings

### Phase 4: Reporting
1. Generate test results report
2. Update integration documentation
3. Create recommendations for future tasks

---

## 📝 Notes

### Design Decisions

**Why GraphQL over REST?**
- Better type safety with schema validation
- Single request for complex operations
- More flexible for custom instructions
- Official GitHub recommendation for agent assignments

**Why YAML for Configuration?**
- Human-readable format
- Consistent with existing planning structure
- Easy to parse and validate
- Supports comments for documentation

### Known Limitations

1. **GitHub API Rate Limits**: GraphQL has separate rate limits
2. **Agent Availability**: Copilot assignment may have access restrictions
3. **Custom Instructions**: Length limits may apply
4. **Webhook Delays**: Assignment events may have propagation delays

### Future Enhancements

1. **Batch Assignment**: Support multiple issues at once
2. **Template Library**: Reusable instruction templates per task pattern
3. **Monitoring Dashboard**: Track assignment success rates
4. **Auto-retry Logic**: Handle transient API failures

---

## 🔗 Related Resources

### Documentation
- `.github/copilot-instructions.md` - Copilot behavior guidelines
- `scripts/automation/README.md` - Automation system overview
- `planning/AGENT_WORKFLOWS.md` - Agent workflow patterns

### Planning Files
- `planning/pi.yaml` - Full PI planning (93 tasks)
- `planning/issues/*.yaml` - Issue specifications per milestone
- `planning/estimates/effort-map.yaml` - AI effectiveness ratings

### GitHub Resources
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [Copilot Assignment API](https://docs.github.com/en/copilot)
- [GitHub Projects v2](https://docs.github.com/en/issues/planning-and-tracking-with-projects)

---

## ✅ Definition of Done

- [x] Test specification created and documented
- [ ] Test configuration YAML validated
- [ ] GraphQL API integration tested
- [ ] Copilot assignment workflow verified
- [ ] Test results documented
- [ ] Integration guide updated
- [ ] Findings presented to stakeholders

---

**Status**: 🟢 In Progress  
**Last Updated**: 2026-02-09  
**Test Owner**: GitHub Copilot Agent
