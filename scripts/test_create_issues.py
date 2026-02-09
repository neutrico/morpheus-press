#!/usr/bin/env python3
"""
Test script for creating 5 test issues with full relationships.

This tests:
- Milestone assignment
- Label assignment
- Iteration assignment
- Parent/child relationships (addSubIssue)
- Blocking relationships (addBlockedBy)
- Projects v2 integration
"""

import json
import subprocess
import sys
import time
from pathlib import Path

# Import from create_issues_api (same directory)
sys.path.insert(0, str(Path(__file__).parent))

# Load the module by executing it
import importlib.util
spec = importlib.util.spec_from_file_location("create_issues_api", Path(__file__).parent / "create-issues-api.py")
create_issues_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create_issues_api)

# Import functions
run_graphql = create_issues_api.run_graphql
create_issue_rest = create_issues_api.create_issue_rest
get_issue_node_id = create_issues_api.get_issue_node_id
add_issue_to_project = create_issues_api.add_issue_to_project
set_issue_type = create_issues_api.set_issue_type
set_project_field = create_issues_api.set_project_field
set_project_iteration_field = create_issues_api.set_project_iteration_field
link_issue_dependency = create_issues_api.link_issue_dependency
set_parent_issue = create_issues_api.set_parent_issue

REPO_OWNER = create_issues_api.REPO_OWNER
REPO_NAME = create_issues_api.REPO_NAME
GITHUB_ISSUE_TYPE_FEATURE = create_issues_api.GITHUB_ISSUE_TYPE_FEATURE
FIELD_STATUS = create_issues_api.FIELD_STATUS
FIELD_ITERATION = create_issues_api.FIELD_ITERATION
STATUS_TODO_ID = create_issues_api.STATUS_TODO_ID
ITERATION_MAP = create_issues_api.ITERATION_MAP

# Test data: 5 issues with dependencies
# T1 -> T2 -> T3
#    \-> T4 -> T5
TEST_ISSUES = [
    {
        "key": "TT1",
        "title": "TT1: Infrastructure Setup",
        "milestone": 1,  # M0
        "iteration": "I1",
        "labels": ["automation:ready", "priority:high"],
        "dependencies": [],
        "parent": None,
    },
    {
        "key": "TT2",
        "title": "TT2: Backend Core API",
        "milestone": 2,  # M1
        "iteration": "I2",
        "labels": ["automation:ready"],
        "dependencies": ["TT1"],
        "parent": None,
    },
    {
        "key": "TT3",
        "title": "TT3: Dashboard UI",
        "milestone": 3,  # M2
        "iteration": "I3",
        "labels": ["automation:partial"],
        "dependencies": ["TT2"],
        "parent": "TT2",  # TT2 is parent of TT3
    },
    {
        "key": "TT4",
        "title": "TT4: ML Pipeline",
        "milestone": 2,  # M1
        "iteration": "I2",
        "labels": ["automation:ready"],
        "dependencies": ["TT1"],
        "parent": None,
    },
    {
        "key": "TT5",
        "title": "TT5: Image Generation",
        "milestone": 4,  # M3
        "iteration": "I4",
        "labels": ["automation:partial", "priority:critical"],
        "dependencies": ["TT4"],
        "parent": "TT4",  # TT4 is parent of TT5
    },
]


def create_test_issue(issue_data: dict, created_node_ids: dict) -> bool:
    """Create a single test issue with all metadata."""
    key = issue_data["key"]
    title = issue_data["title"]
    milestone = issue_data["milestone"]
    iteration_key = issue_data["iteration"]
    labels = issue_data["labels"] + ["from-planning", "test"]
    
    # Create issue body
    body = f"""## 📋 Description

Test issue for validating GitHub Issues + Projects v2 integration.

**AI Effectiveness**: high
**Estimated Effort**: 2 days

## 🤖 Automation Available

### Automation Status:
- [ ] ✅ Automation available for this task type
- [ ] Auto-generation triggered (comment `/automate`)
- [ ] PR created with generated code
- [ ] Code reviewed and refined

### Implementation Notes:
**Related Files:**
- Spec: `planning/test/{key.lower()}.md`
"""
    
    print(f"\n📝 Creating {key}...")
    print(f"   Title: {title}")
    print(f"   Milestone: M{milestone-1}")
    print(f"   Iteration: {iteration_key}")
    print(f"   Labels: {', '.join(labels)}")
    
    # 1. Create issue
    issue_number = create_issue_rest(title, body, labels, milestone)
    if not issue_number:
        print(f"   ❌ Failed to create issue")
        return False
    
    print(f"   ✅ Created issue #{issue_number}")
    
    # 2. Get node ID
    issue_node_id = get_issue_node_id(issue_number)
    if not issue_node_id:
        print(f"   ❌ Failed to get node ID")
        return False
    
    created_node_ids[key] = {"number": issue_number, "node_id": issue_node_id}
    
    # 3. Add to project
    print(f"   Adding to project...", end=" ", flush=True)
    project_item_id = add_issue_to_project(issue_node_id)
    if not project_item_id:
        print("❌")
        return False
    print("✅")
    
    # 4. Set issue type
    print(f"   Setting issue type to Feature...", end=" ", flush=True)
    if set_issue_type(issue_node_id, GITHUB_ISSUE_TYPE_FEATURE):
        print("✅")
    else:
        print("❌")
    
    # 5. Set status
    print(f"   Setting status to Todo...", end=" ", flush=True)
    if set_project_field(project_item_id, FIELD_STATUS, STATUS_TODO_ID):
        print("✅")
    else:
        print("❌")
    
    # 6. Set iteration
    if iteration_key in ITERATION_MAP:
        iteration_id = ITERATION_MAP[iteration_key]
        print(f"   Setting iteration to {iteration_key}...", end=" ", flush=True)
        if set_project_iteration_field(project_item_id, FIELD_ITERATION, iteration_id):
            print("✅")
        else:
            print("❌")
    
    time.sleep(0.5)  # Rate limit protection
    return True


def set_relationships(test_issues: list, created_node_ids: dict) -> None:
    """Set blocking and parent/child relationships after all issues are created."""
    print("\n🔗 Setting relationships...")
    
    for issue_data in test_issues:
        key = issue_data["key"]
        
        if key not in created_node_ids:
            continue
        
        issue_node_id = created_node_ids[key]["node_id"]
        issue_number = created_node_ids[key]["number"]
        
        # Set blocking relationships
        dependencies = issue_data.get("dependencies", [])
        for dep_key in dependencies:
            if dep_key not in created_node_ids:
                print(f"   ⚠️  Dependency {dep_key} not found for {key}")
                continue
            
            blocking_node_id = created_node_ids[dep_key]["node_id"]
            blocking_number = created_node_ids[dep_key]["number"]
            
            print(f"   #{issue_number} ({key}) blocked by #{blocking_number} ({dep_key})...", end=" ", flush=True)
            if link_issue_dependency(issue_node_id, blocking_node_id):
                print("✅")
            else:
                print("❌")
            time.sleep(0.3)
        
        # Set parent relationship
        parent_key = issue_data.get("parent")
        if parent_key and parent_key in created_node_ids:
            parent_node_id = created_node_ids[parent_key]["node_id"]
            parent_number = created_node_ids[parent_key]["number"]
            
            print(f"   #{issue_number} ({key}) is child of #{parent_number} ({parent_key})...", end=" ", flush=True)
            if set_parent_issue(parent_node_id, issue_node_id):
                print("✅")
            else:
                print("❌")
            time.sleep(0.3)


def verify_relationships(created_node_ids: dict) -> bool:
    """Verify all relationships were set correctly."""
    print("\n✅ Verifying relationships...")
    
    # Build GraphQL query to check all issues
    issue_numbers = [data["number"] for data in created_node_ids.values()]
    
    query = f"""
    {{
      repository(owner: "{REPO_OWNER}", name: "{REPO_NAME}") {{
        {" ".join([f'i{num}: issue(number: {num}) {{ number title parent {{ number }} blockedBy(first: 10) {{ totalCount nodes {{ number }} }} }}'
                   for num in issue_numbers])}
      }}
    }}
    """
    
    result = run_graphql(query)
    
    if "data" not in result:
        print("   ❌ Failed to fetch relationships")
        return False
    
    all_correct = True
    
    for key, data in created_node_ids.items():
        issue_num = data["number"]
        issue_data = result["data"]["repository"][f"i{issue_num}"]
        
        # Find expected data
        test_issue = next(i for i in TEST_ISSUES if i["key"] == key)
        
        # Check parent
        expected_parent = test_issue.get("parent")
        actual_parent = issue_data.get("parent", {}).get("number") if issue_data.get("parent") else None
        
        if expected_parent:
            expected_parent_num = created_node_ids[expected_parent]["number"]
            if actual_parent != expected_parent_num:
                print(f"   ❌ {key} parent mismatch: expected #{expected_parent_num}, got {actual_parent}")
                all_correct = False
            else:
                print(f"   ✅ {key} parent correct: #{actual_parent}")
        
        # Check blocking
        expected_deps = test_issue.get("dependencies", [])
        actual_blocking_count = issue_data["blockedBy"]["totalCount"]
        
        if len(expected_deps) != actual_blocking_count:
            print(f"   ❌ {key} blocking count mismatch: expected {len(expected_deps)}, got {actual_blocking_count}")
            all_correct = False
        else:
            if expected_deps:
                print(f"   ✅ {key} blocked by {actual_blocking_count} issue(s)")
    
    return all_correct


def main():
    """Main test execution."""
    print("=" * 80)
    print("🧪 TEST: Create 5 issues with full relationships")
    print("=" * 80)
    
    created_node_ids = {}
    
    # Phase 1: Create all issues
    print("\n📝 Phase 1: Creating issues...")
    for issue_data in TEST_ISSUES:
        if not create_test_issue(issue_data, created_node_ids):
            print(f"\n❌ Test failed: Could not create {issue_data['key']}")
            return 1
    
    # Phase 2: Set relationships
    set_relationships(TEST_ISSUES, created_node_ids)
    
    # Phase 3: Verify
    if verify_relationships(created_node_ids):
        print("\n" + "=" * 80)
        print("✅ TEST PASSED: All issues created with correct relationships!")
        print("=" * 80)
        print(f"\n🔗 View issues: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")
        print(f"🔗 View project: https://github.com/orgs/{REPO_OWNER}/projects/5")
        return 0
    else:
        print("\n" + "=" * 80)
        print("❌ TEST FAILED: Relationship verification failed")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
