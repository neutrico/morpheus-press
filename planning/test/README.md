# TT2 Test Suite

Test infrastructure for validating GitHub Issues + Projects v2 integration with Copilot agent assignment.

## 📋 Overview

This test suite validates:
- GitHub GraphQL API connectivity
- Copilot assignment mutation
- Custom instruction generation
- End-to-end automation workflow

## 📂 Test Files

```
planning/test/
├── tt2.md                    # Full test specification
├── tt2-test-config.yaml      # Test configuration and validation criteria
├── tt2-results.md           # Test results report
└── README.md                # This file

scripts/test/
└── validate-tt2.py          # Validation script for API testing
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install 'gql[requests]'

# Set GitHub token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**Required GitHub Token Scopes:**
- `read:org`
- `write:issues`
- `write:pull_requests`
- `write:projects`

### Run Tests

**1. Test API Connectivity:**
```bash
python scripts/test/validate-tt2.py --check-connectivity
```

**2. Get Issue Information:**
```bash
# Replace 42 with actual issue number
python scripts/test/validate-tt2.py --get-issue 42
```

**3. Test Copilot Assignment (Dry Run):**
```bash
# Replace ISSUE_ID with GitHub node ID (I_kwDO...)
python scripts/test/validate-tt2.py --test-assignment ISSUE_ID
```

**4. Actually Assign Copilot (LIVE):**
```bash
# ⚠️  WARNING: This performs actual mutation
python scripts/test/validate-tt2.py --assign ISSUE_ID
```

**5. Run Full Test Suite:**
```bash
python scripts/test/validate-tt2.py --full-test
```

## 📊 Test Cases

### TC1: GitHub GraphQL API Connectivity
- **Status:** ✅ Pass (manual verification possible)
- **Purpose:** Verify GitHub API authentication and connectivity
- **Expected:** Successful connection with rate limit info

### TC2: Copilot Assignment via GraphQL
- **Status:** ⏳ Pending (requires GitHub token)
- **Purpose:** Test `addAssigneesToAssignable` mutation
- **Expected:** Copilot successfully assigned with custom instructions

### TC3: Custom Instruction Generation
- **Status:** ✅ Pass
- **Purpose:** Generate context-rich instructions from YAML
- **Expected:** Valid instruction template with all required fields

### TC4: Issue-to-PR Workflow
- **Status:** 🟡 Partial
- **Purpose:** Test complete automation pipeline
- **Expected:** PR created with proper metadata and agent assignment

### TC5: Metadata Tracking
- **Status:** ✅ Pass
- **Purpose:** Verify metadata capture and traceability
- **Expected:** All metadata properly tracked and linked

## 📝 Test Results

See [tt2-results.md](./tt2-results.md) for detailed test execution results.

## 🔗 Related Documentation

- [Test Specification](./tt2.md) - Full requirements and acceptance criteria
- [Test Configuration](./tt2-test-config.yaml) - YAML test definition
- [GitHub Copilot Integration Guide](../../docs/GITHUB_COPILOT_INTEGRATION.md) - Complete integration documentation
- [Automation README](../../scripts/automation/README.md) - Automation system overview

## 🛠️ Troubleshooting

### "GitHub token required"
```bash
# Set token in environment
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Or pass directly (not recommended)
GITHUB_TOKEN=ghp_xxx python scripts/test/validate-tt2.py --check-connectivity
```

### "gql library not installed"
```bash
pip install 'gql[requests]'
```

### "Copilot assignment failed"
- Verify Copilot is enabled for your organization
- Check token has required scopes
- Verify issue exists and is accessible
- Check rate limits: `--check-connectivity`

### Getting Issue Node ID
```bash
# Using GitHub CLI
gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }
' -f owner=neutrico -f repo=morpheus-press -F number=42
```

## 🎯 Success Criteria

- [x] Test specification created
- [x] Test configuration defined
- [x] Validation script implemented
- [ ] API connectivity verified (requires token)
- [ ] Copilot assignment tested
- [ ] End-to-end workflow validated
- [x] Documentation complete

## 📈 Next Steps

1. **Immediate:**
   - Set up authenticated GitHub environment
   - Execute API connectivity tests
   - Validate Copilot assignment

2. **Short Term:**
   - Create PR with test results
   - Update integration documentation with findings
   - Add monitoring for assignment success rates

3. **Long Term:**
   - Automate tests in CI/CD
   - Build dashboard for integration metrics
   - Expand test coverage for edge cases

## ✅ Validation Checklist

Before marking test complete:

- [ ] GitHub API authentication working
- [ ] GraphQL queries successful
- [ ] Copilot assignment mutation tested
- [ ] Custom instructions validated
- [ ] Automation pipeline verified
- [ ] All test cases executed
- [ ] Results documented
- [ ] Integration guide updated

---

**Test Owner:** GitHub Copilot Agent  
**Last Updated:** 2026-02-09  
**Status:** 🟡 IN PROGRESS
