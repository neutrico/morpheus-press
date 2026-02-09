# TT1: Infrastructure Setup Test

**Task Key**: TT1  
**Priority**: p1 (Critical - Validation Test)  
**Estimated Effort**: 2 days  
**AI Effectiveness**: HIGH  

## 📋 Description

Test issue for validating the GitHub Issues + Projects v2 integration with Copilot agent assignment system.

This test verifies that:
1. Issues can be created and tracked in the planning system
2. Copilot agents can be assigned via GitHub GraphQL API
3. The automation workflow triggers correctly
4. Generated code follows SOLID, DRY, KISS principles

## 🎯 Objectives

### Primary Goal
Validate end-to-end workflow for Copilot agent assignment using GitHub's GraphQL API with custom instructions.

### Success Criteria
- [ ] Test issue (TT1) successfully created in GitHub
- [ ] Copilot agent can be assigned via GraphQL mutation
- [ ] Agent receives context-rich custom instructions
- [ ] Workflow automation triggers correctly
- [ ] Test validation script confirms all systems operational

## 🔍 Research Findings

### GitHub Copilot Assignment
- **API**: GitHub GraphQL API v4
- **Mutation**: `addAssigneesToAssignable` with `agentAssignment` parameter
- **Custom Instructions**: Passed via `customPrompt` field
- **Context**: Generated from YAML task specifications

### Key Design Decisions
1. **Use GraphQL over REST**: Better type safety and flexibility for complex operations
2. **Generate custom prompts from YAML**: Provides context-rich instructions for better AI performance
3. **Validate infrastructure before assignment**: Ensure all systems are ready

## 🏗️ Technical Requirements

### Infrastructure Components
1. **GitHub Actions Workflow**: `.github/workflows/copilot-task-automation.yml`
2. **Planning System**: YAML-based task specifications
3. **Automation Scripts**: Python-based code generators
4. **Issue Templates**: Standardized issue creation

### Validation Points
- GitHub Actions workflow syntax
- Label configuration
- Secret availability (ANTHROPIC_API_KEY)
- Python dependencies
- Planning system integrity

## 📝 Implementation Approach

### Phase 1: Test Specification (This File)
Create comprehensive test documentation at `planning/test/tt1.md` including:
- Test objectives and success criteria
- Infrastructure requirements
- Validation checklist
- Expected outcomes

### Phase 2: Validation Script
Create `scripts/test/validate-infrastructure.py` to check:
- GitHub Actions workflow is valid
- Required labels exist
- Secrets are configured (check availability, not values)
- Planning system is intact
- Automation scripts are executable

### Phase 3: Test Execution
1. Run validation script
2. Verify all checks pass
3. Document results in `planning/test/tt1-results.md`
4. Report findings

## 🧪 Test Cases

### Test Case 1: Workflow Validation
**Given**: GitHub Actions workflow file exists  
**When**: Workflow syntax is validated  
**Then**: No errors or warnings detected

### Test Case 2: Label Configuration
**Given**: Required labels defined in planning system  
**When**: Labels are checked in repository  
**Then**: All automation labels exist with correct colors

### Test Case 3: Planning System Integrity
**Given**: Planning YAML files exist  
**When**: Schema validation runs  
**Then**: All files pass validation without errors

### Test Case 4: Automation Script Availability
**Given**: Automation scripts exist in `scripts/automation/`  
**When**: Scripts are checked for executability  
**Then**: All scripts have correct permissions and dependencies

## 📊 Quality Standards

Following SOLID, DRY, KISS principles:

### Code Quality
- ✅ **Single Responsibility**: Each validation check in separate function
- ✅ **DRY**: Reusable validation utilities
- ✅ **KISS**: Simple, clear test logic
- ✅ **Error Handling**: Comprehensive try/catch with descriptive messages
- ✅ **Logging**: Structured output for debugging

### Testing
- Unit tests for validation functions (if time permits)
- Integration test for complete workflow
- Manual verification of GitHub UI integration

## 📦 Expected Deliverables

1. **Test Specification**: `planning/test/tt1.md` (this file)
2. **Validation Script**: `scripts/test/validate-infrastructure.py`
3. **Test Results**: `planning/test/tt1-results.md`
4. **Documentation**: Updates to SETUP_CHECKLIST.md if needed

## 🔗 Related Files

- Spec: `planning/test/tt1.md` (this file)
- Workflow: `.github/workflows/copilot-task-automation.yml`
- Copilot Instructions: `.github/copilot-instructions.md`
- Setup Guide: `SETUP_CHECKLIST.md`
- Planning System: `planning/pi.yaml`, `planning/estimates/effort-map.yaml`

## 🚀 Execution Plan

### Step 1: Create Test Infrastructure
- [x] Create test directory: `planning/test/`
- [x] Write test specification: `planning/test/tt1.md`
- [ ] Create validation script: `scripts/test/validate-infrastructure.py`

### Step 2: Implement Validation
- [ ] Check GitHub Actions workflow syntax
- [ ] Verify label configuration
- [ ] Validate planning system integrity
- [ ] Check automation script dependencies

### Step 3: Execute & Report
- [ ] Run validation script
- [ ] Document test results
- [ ] Update setup checklist if issues found
- [ ] Report success/failure

## 📈 Success Metrics

- **All validation checks pass**: 100% infrastructure ready
- **Clear documentation**: Test results and recommendations documented
- **Minimal changes**: Only add necessary test infrastructure
- **Reproducible**: Other developers can run validation independently

## 🔐 Security Considerations

- Do NOT expose secret values in validation output
- Only check for presence of secrets, not their contents
- Ensure test scripts have appropriate permissions
- Validate workflow permissions are minimal and necessary

## 📚 References

- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub Copilot Agent Assignment](https://github.blog/changelog/2024-11-copilot-agent-assignment/)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- Project Copilot Instructions: `.github/copilot-instructions.md`

---

**Created**: 2026-02-09  
**Status**: In Progress  
**Assignee**: @copilot  
**Labels**: automation:ready, test, infrastructure
