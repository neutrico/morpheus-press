#!/usr/bin/env python3
"""
GitHub Issues Creator with full GitHub Projects v2 API support.
Creates issues with proper milestone, project assignment, custom fields, and relationships.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Import Copilot agent functions
from copilot_agent import (
    assign_copilot_agent,
    find_first_ready_task,
    generate_copilot_instructions,
)

# Configuration
WORKSPACE_ROOT = Path("/workspaces/morpheus-press")
EFFORT_MAP_PATH = WORKSPACE_ROOT / "planning/estimates/effort-map.yaml"
ISSUES_DIR = WORKSPACE_ROOT / "planning/issues"
DOCS_DIR = WORKSPACE_ROOT / "planning/docs"

REPO_OWNER = "neutrico"
REPO_NAME = "morpheus-press"
PROJECT_NUMBER = 5  # Morpheus Press - Planning & Automation
PROJECT_ID = "PVT_kwDOACzkfM4BOras"

# GitHub Projects v2 Field IDs
FIELD_STATUS = "PVTSSF_lADOACzkfM4BOraszg9TxGA"
FIELD_MILESTONE = "PVTF_lADOACzkfM4BOraszg9TxGM"
FIELD_PARENT_ISSUE = "PVTF_lADOACzkfM4BOraszg9TxGc"
FIELD_BLOCKED_BY = "PVTF_lADOACzkfM4BOraszg9TzuM"  # Custom text field
FIELD_ITERATION = "PVTIF_lADOACzkfM4BOraszg9T_B8"  # Iteration field

STATUS_TODO_ID = "f75ad846"
STATUS_IN_PROGRESS_ID = "47fc9ee4"
STATUS_DONE_ID = "98236657"

# GitHub Native Issue Types (ONLY these are used)
GITHUB_ISSUE_TYPE_TASK = "IT_kwDOACzkfM4ABHiZ"
GITHUB_ISSUE_TYPE_BUG = "IT_kwDOACzkfM4ABHic"
GITHUB_ISSUE_TYPE_FEATURE = "IT_kwDOACzkfM4ABHie"

# Milestone mapping (created in previous step)
MILESTONE_MAP = {
    "M0 - Infrastructure & Setup": 1,
    "M1 - Backend Services": 2,
    "M2 - Dashboard UI": 3,
    "M3 - Content Generation Pipeline": 4,  # Fixed: was "M3 - Image Generation"
    "M4 - ML & Publishing": 5,
}

# Iteration mapping (I1-I7 -> iteration IDs)
ITERATION_MAP = {
    "I1": "aa0d8cf1",  # I1 - Infrastructure
    "I2": "8ff7fbce",  # I2 - Backend Core
    "I3": "7e358c77",  # I3 - ML Foundation
    "I4": "c49f86bc",  # I4 - Generation Pipeline
    "I5": "7467ed8f",  # I5 - Dashboard & Assembly
    "I6": "946f740b",  # I6 - Commerce & Distribution
    "I7": "088db25a",  # I7 - Launch & Release
}

# Cache for created issues (task_key -> issue_number)
created_issues_cache: Dict[str, int] = {}

# Cache for issue node IDs (task_key -> node_id) - needed for parent/sub-issue relationships
created_issues_node_ids: Dict[str, str] = {}

# Parent mapping (child_key -> parent_key) - for demo purposes
# In production, this should be derived from YAML structure or inferred from Feature/Task relationships
PARENT_MAPPING = {
    # M1 Backend tasks could be children of T25 (API Routes) if it existed
    # For now, keep them standalone
    # "T24": "T25",  # Database → API Routes
    # "T27": "T25",  # Tests → API Routes  
    # "T32": "T25",  # Docs → API Routes
}


def run_gh_api(
    endpoint: str, method: str = "GET", data: Optional[Dict] = None
) -> Dict:
    """Run GitHub REST API command."""
    cmd = ["gh", "api", endpoint, "-X", method]
    if data:
        cmd.extend(["-f", f"input={json.dumps(data)}"])
        for key, value in data.items():
            if isinstance(value, (str, int)):
                cmd.extend(["-f", f"{key}={value}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ API Error: {result.stderr}")
        return {}
    return json.loads(result.stdout) if result.stdout else {}


def run_graphql(query: str, variables: Optional[Dict] = None) -> Dict:
    """Run GitHub GraphQL API query."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    if variables:
        # Use -F for JSON variables (non-string types)
        for key, value in variables.items():
            if isinstance(value, bool):
                # Boolean values need lowercase true/false in JSON
                cmd.extend(["-F", f"{key}={json.dumps(value)}"])
            elif isinstance(value, (dict, list)):
                cmd.extend(["-F", f"{key}={json.dumps(value)}"])
            else:
                cmd.extend(["-F", f"{key}={json.dumps(value)}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ GraphQL Error: {result.stderr}")
        return {}
    return json.loads(result.stdout) if result.stdout else {}


def load_effort_map() -> Dict:
    """Load effort-map.yaml with task definitions."""
    with open(EFFORT_MAP_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def topological_sort_tasks(tasks: List[tuple]) -> List[tuple]:
    """
    Sort tasks by dependencies (topological sort).
    Tasks without dependencies come first, then tasks that depend on them.
    
    Args:
        tasks: List of (task_key, task_data) tuples
    
    Returns:
        Sorted list of (task_key, task_data) tuples
    """
    # Build dependency graph
    task_map = {task_key: task_data for task_key, task_data in tasks}
    
    # Calculate in-degree (number of dependencies)
    in_degree = {}
    for task_key, task_data in tasks:
        dependencies = task_data.get("dependencies", [])
        # Only count dependencies that are in our filtered task list
        valid_deps = [dep for dep in dependencies if dep in task_map]
        in_degree[task_key] = len(valid_deps)
    
    # Start with tasks that have no dependencies
    sorted_tasks = []
    queue = [task_key for task_key in in_degree if in_degree[task_key] == 0]
    
    # Process tasks in order
    while queue:
        # Sort queue for deterministic order
        queue.sort()
        task_key = queue.pop(0)
        sorted_tasks.append((task_key, task_map[task_key]))
        
        # Find tasks that depend on this one and decrement their in-degree
        for other_key, other_data in tasks:
            if other_key in [t[0] for t in sorted_tasks]:
                continue
            dependencies = other_data.get("dependencies", [])
            if task_key in dependencies:
                in_degree[other_key] -= 1
                if in_degree[other_key] == 0:
                    queue.append(other_key)
    
    # Add any remaining tasks (circular dependencies or orphans)
    remaining = [t for t in tasks if t[0] not in [s[0] for s in sorted_tasks]]
    sorted_tasks.extend(remaining)
    
    return sorted_tasks


def get_milestone_number(milestone_key: str) -> Optional[int]:
    """Get milestone number from milestone name (e.g., 'M0 - Infrastructure & Setup' -> 1)."""
    if not milestone_key:
        return None
    
    # Direct lookup - milestone_key is already the full title
    return MILESTONE_MAP.get(milestone_key)


def get_issue_node_id(issue_number: int) -> Optional[str]:
    """Get GraphQL node ID for an issue."""
    result = run_gh_api(f"/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}")
    return result.get("node_id")


def create_issue_rest(
    title: str,
    body: str,
    labels: List[str],
    milestone: Optional[int] = None,
) -> Optional[int]:
    """Create issue using REST API (returns issue number)."""
    # Build JSON payload
    payload = {
        "title": title,
        "body": body,
        "labels": labels,
    }
    if milestone:
        payload["milestone"] = milestone
    
    # Use --input with JSON via stdin
    cmd = [
        "gh", "api",
        f"/repos/{REPO_OWNER}/{REPO_NAME}/issues",
        "-X", "POST",
        "--input", "-",  # Read from stdin
    ]
    
    result = subprocess.run(
        cmd,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        print(f"   ❌ Failed to create issue: {result.stderr}")
        return None
    
    issue_data = json.loads(result.stdout)
    return issue_data.get("number")


def add_issue_to_project(issue_node_id: str) -> Optional[str]:
    """Add issue to GitHub Project (returns project item ID)."""
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {
        projectId: $projectId
        contentId: $contentId
      }) {
        item {
          id
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={"projectId": PROJECT_ID, "contentId": issue_node_id},
    )
    
    try:
        return result["data"]["addProjectV2ItemById"]["item"]["id"]
    except (KeyError, TypeError):
        return None


def set_project_field(
    project_item_id: str, field_id: str, value: str
) -> bool:
    """Set a single-select field value on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: {
          singleSelectOptionId: $value
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "projectId": PROJECT_ID,
            "itemId": project_item_id,
            "fieldId": field_id,
            "value": value,
        },
    )
    
    return "data" in result and "updateProjectV2ItemFieldValue" in result["data"]


def set_project_text_field(
    project_item_id: str, field_id: str, text_value: str
) -> bool:
    """Set a text field value on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: {
          text: $value
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "projectId": PROJECT_ID,
            "itemId": project_item_id,
            "fieldId": field_id,
            "value": text_value,
        },
    )
    
    return "data" in result and "updateProjectV2ItemFieldValue" in result["data"]


def set_project_iteration_field(
    project_item_id: str, field_id: str, iteration_id: str
) -> bool:
    """Set an iteration field value on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: {
          iterationId: $value
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "projectId": PROJECT_ID,
            "itemId": project_item_id,
            "fieldId": field_id,
            "value": iteration_id,
        },
    )
    
    return "data" in result and "updateProjectV2ItemFieldValue" in result["data"]


def set_issue_type(issue_node_id: str, issue_type_id: str) -> bool:
    """Set GitHub native Issue Type on an issue."""
    mutation = """
    mutation($issueId: ID!, $issueTypeId: ID!) {
      updateIssue(input: {
        id: $issueId
        issueTypeId: $issueTypeId
      }) {
        issue {
          id
          issueType {
            id
            name
          }
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "issueId": issue_node_id,
            "issueTypeId": issue_type_id,
        },
    )
    
    return "data" in result and "updateIssue" in result["data"]


def set_parent_issue(parent_node_id: str, sub_issue_node_id: str) -> bool:
    """
    Set parent/sub-issue relationship using official GitHub GraphQL API.
    This creates a parent → child link visible in the GitHub UI.
    
    Args:
        parent_node_id: Node ID of the parent issue
        sub_issue_node_id: Node ID of the child/sub-issue
    
    Returns:
        True if successful, False otherwise
    """
    mutation = """
    mutation($issueId: ID!, $subIssueId: ID!, $replaceParent: Boolean) {
      addSubIssue(input: {
        issueId: $issueId
        subIssueId: $subIssueId
        replaceParent: $replaceParent
      }) {
        issue {
          id
          number
          title
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "issueId": parent_node_id,
            "subIssueId": sub_issue_node_id,
            "replaceParent": True,
        },
    )
    
    return "data" in result and "addSubIssue" in result["data"]


def link_issue_dependency(blocked_issue_node_id: str, blocking_issue_node_id: str) -> bool:
    """
    Mark issue as blocked by another issue using official GitHub GraphQL API.
    This creates a "blocked by" relationship visible in the GitHub UI Relationships section.
    
    Args:
        blocked_issue_node_id: Node ID of the issue that is blocked
        blocking_issue_node_id: Node ID of the issue that is blocking
    
    Returns:
        True if successful, False otherwise
    """
    mutation = """
    mutation($issueId: ID!, $blockingIssueId: ID!) {
      addBlockedBy(input: {
        issueId: $issueId
        blockingIssueId: $blockingIssueId
      }) {
        issue {
          id
          number
          title
        }
      }
    }
    """
    
    result = run_graphql(
        mutation,
        variables={
            "issueId": blocked_issue_node_id,
            "blockingIssueId": blocking_issue_node_id,
        },
    )
    
    return "data" in result and "addBlockedBy" in result["data"]


def create_github_issue(
    task_key: str,
    task_data: Dict,
    milestone_key: str,
    spec_file: Optional[Path] = None,
) -> Optional[int]:
    """Create a GitHub issue with full project integration."""
    
    # Build issue title
    title = f"{task_key}: {task_data['task']}"
    
    # Build issue body
    # NOTE: Milestone and Dependencies are set via GitHub parameters (milestone field + relationships),
    # so we don't duplicate them in the body text.
    body_parts = []
    
    # Task description with metadata
    body_parts.append(f"## 📋 Description\n")
    body_parts.append(f"{task_data.get('description', task_data['task'])}\n")
    body_parts.append(f"**AI Effectiveness**: {task_data.get('ai_effectiveness', 'unknown')}")
    body_parts.append(f"**Estimated Effort**: {task_data.get('estimated_days', '?')} days")
    
    if spec_file and spec_file.exists():
        body_parts.append(f"\n**Detailed Spec**: `{spec_file.relative_to(WORKSPACE_ROOT)}`")
    
    # Add automation section
    body_parts.append("\n## 🤖 Automation Available\n")
    body_parts.append("### Automation Status:\n")
    body_parts.append("- [ ] ✅ Automation available for this task type")
    body_parts.append("- [ ] Auto-generation triggered (comment `/automate`)")
    body_parts.append("- [ ] PR created with generated code")
    body_parts.append("- [ ] Code reviewed and refined")
    
    body_parts.append("\n### Implementation Notes:\n")
    body_parts.append("**Related Files:**")
    if spec_file:
        body_parts.append(f"- Spec: `{spec_file.relative_to(WORKSPACE_ROOT)}`")
    
    # Research findings from issues/*.yaml
    issue_file = ISSUES_DIR / f"{task_key.lower()}.yaml"
    if issue_file.exists():
        body_parts.append(f"- Research: `{issue_file.relative_to(WORKSPACE_ROOT)}` (search for {task_key})")
    
    body_parts.append(f"- Estimate: `planning/estimates/effort-map.yaml` ({task_key})")
    
    body = "\n".join(body_parts)
    
    # Build labels (removed "task" label - use Issue Type field instead)
    labels = ["from-planning"]
    ai_effectiveness = task_data.get("ai_effectiveness", "").lower()
    if ai_effectiveness == "high":
        labels.append("automation:ready")
    elif ai_effectiveness == "medium":
        labels.append("automation:partial")
    
    priority = task_data.get("priority", "").lower()
    if priority in ["critical", "high"]:
        labels.append(f"priority:{priority}")
    
    # Get milestone number
    milestone_num = get_milestone_number(milestone_key)
    
    # Create issue via REST API
    print(f"   Creating {task_key}...", end=" ", flush=True)
    issue_number = create_issue_rest(title, body, labels, milestone_num)
    
    if not issue_number:
        print("❌ Failed")
        return None
    
    print(f"✅ Issue #{issue_number}")
    
    # Get issue node ID for GraphQL
    issue_node_id = get_issue_node_id(issue_number)
    if not issue_node_id:
        print("   ⚠️ Could not get node ID, skipping project assignment")
        return issue_number
    
    # Add to project
    print(f"   Adding to project...", end=" ", flush=True)
    project_item_id = add_issue_to_project(issue_node_id)
    if not project_item_id:
        print("❌ Failed")
        return issue_number
    
    print("✅")
    
    # Set GitHub Issue Type to "Feature" (native GitHub feature)
    print(f"   Setting issue type to Feature...", end=" ", flush=True)
    if set_issue_type(issue_node_id, GITHUB_ISSUE_TYPE_FEATURE):
        print("✅")
    else:
        print("❌")
    
    # Set status to "Todo"
    print(f"   Setting status to Todo...", end=" ", flush=True)
    if set_project_field(project_item_id, FIELD_STATUS, STATUS_TODO_ID):
        print("✅")
    else:
        print("❌")
    
    # Set Iteration (I1-I7) if specified
    iteration_key = task_data.get("iteration", "")
    if iteration_key and iteration_key in ITERATION_MAP:
        iteration_id = ITERATION_MAP[iteration_key]
        iteration_name = {
            "I1": "I1 - Infrastructure",
            "I2": "I2 - Backend Core", 
            "I3": "I3 - ML Foundation",
            "I4": "I4 - Generation Pipeline",
            "I5": "I5 - Dashboard & Assembly",
            "I6": "I6 - Commerce & Distribution",
            "I7": "I7 - Launch & Release",
        }.get(iteration_key, iteration_key)
        print(f"   Setting iteration to {iteration_name}...", end=" ", flush=True)
        if set_project_iteration_field(project_item_id, FIELD_ITERATION, iteration_id):
            print("✅")
        else:
            print("❌")
    
    # Set "Blocked By" field if dependencies exist in cache
    dependencies = task_data.get("dependencies", [])
    if dependencies and project_item_id:
        # Build blocked by text (e.g., "#36 (T24)")
        blocked_by_items = []
        missing_deps = []
        for dep in dependencies:
            if dep in created_issues_cache:
                issue_num = created_issues_cache[dep]
                blocked_by_items.append(f"#{issue_num}")
            else:
                missing_deps.append(dep)
        
        if blocked_by_items:
            blocked_by_text = ", ".join(blocked_by_items)
            print(f"   Setting blocked by: {blocked_by_text}...", end=" ", flush=True)
            if set_project_text_field(project_item_id, FIELD_BLOCKED_BY, blocked_by_text):
                print("✅")
            else:
                print("❌")
        
        if missing_deps:
            print(f"   ⚠️  Missing dependencies (not yet created): {', '.join(missing_deps)}")
    
    # Cache issue number and node ID for future references
    created_issues_cache[task_key] = issue_number
    created_issues_node_ids[task_key] = issue_node_id
    
    # Set parent issue if defined in PARENT_MAPPING
    parent_key = PARENT_MAPPING.get(task_key)
    if parent_key and parent_key in created_issues_node_ids:
        parent_node_id = created_issues_node_ids[parent_key]
        parent_issue_num = created_issues_cache[parent_key]
        print(f"   Setting parent to #{parent_issue_num} ({parent_key})...", end=" ", flush=True)
        if set_parent_issue(issue_node_id, parent_node_id):
            print("✅")
        else:
            print("❌")
    elif parent_key and parent_key not in created_issues_node_ids:
        print(f"   ⚠️  Parent {parent_key} not yet created, skipping parent link")
    
    # Small delay to avoid rate limits
    time.sleep(0.5)
    
    return issue_number


def find_spec_file(task_key: str, milestone: str) -> Optional[Path]:
    """Find detailed spec file for a task."""
    milestone_dir = milestone.lower().replace(" ", "-").split("-")[0]  # M0, M1, etc.
    
    # Try multiple patterns
    patterns = [
        f"{milestone_dir}*/{task_key.lower()}-*.md",
        f"*/{task_key.lower()}-*.md",
    ]
    
    for pattern in patterns:
        matches = list(DOCS_DIR.glob(pattern))
        if matches:
            return matches[0]
    
    return None


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create GitHub issues from planning data")
    parser.add_argument("--ai-high-only", action="store_true", help="Only HIGH AI effectiveness tasks")
    parser.add_argument("--milestone", type=str, help="Filter by milestone (e.g., M0)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    parser.add_argument("--update-relationships", action="store_true", help="Update relationships for existing issues")
    parser.add_argument("task_keys", nargs="*", help="Specific task keys (e.g., T24 T25)")
    
    args = parser.parse_args()
    
    # If updating relationships only
    if args.update_relationships:
        print("\n🔗 Updating relationships for existing issues...")
        print("⚠️  Note: GitHub API doesn't support 'blocked by' relationships yet.")
        print("    You'll need to set these manually in the UI for now.")
        print("\n✅ Tip: Dependencies are shown in issue body with links.")
        return
    
    # Load task data
    effort_map = load_effort_map()
    tasks = effort_map.get("estimates", {})  # Changed from "tasks" to "estimates"
    
    # Extract AI effectiveness from reasoning field (contains "AI Impact: HIGH/MEDIUM/LOW")
    def extract_ai_effectiveness(task_data: Dict) -> str:
        """Extract AI effectiveness from reasoning field."""
        reasoning = task_data.get("reasoning", "")
        if "AI Impact: HIGH" in reasoning or "AI effectiveness: HIGH" in reasoning:
            return "high"
        elif "AI Impact: MEDIUM" in reasoning:
            return "medium"
        elif "AI Impact: LOW" in reasoning:
            return "low"
        return "unknown"
    
    # Load dependencies from planning/issues/*.yaml
    dependencies_map = {}
    for issue_file in (WORKSPACE_ROOT / "planning/issues").glob("*.yaml"):
        with open(issue_file, "r", encoding="utf-8") as f:
            milestone_data = yaml.safe_load(f)
            for issue in milestone_data.get("issues", []):
                task_key = issue.get("key")
                if task_key:
                    dependencies_map[task_key] = issue.get("dependsOn", [])
    
    # Filter tasks
    filtered_tasks = []
    for task_key, task_data in tasks.items():
        # Extract AI effectiveness from reasoning
        ai_effectiveness = extract_ai_effectiveness(task_data)
        
        # Skip if specific keys requested and not in list
        if args.task_keys and task_key not in args.task_keys:
            continue
        
        # Skip if milestone filter and doesn't match
        if args.milestone and not task_data.get("milestone", "").startswith(args.milestone):
            continue
        
        # Skip if HIGH AI only and not HIGH
        if args.ai_high_only and ai_effectiveness.lower() != "high":
            continue
        
        # Merge AI data and dependencies into task_data
        task_data["ai_effectiveness"] = ai_effectiveness
        task_data["task"] = task_data.get("title", "")  # Map title -> task
        task_data["dependencies"] = dependencies_map.get(task_key, [])
        
        filtered_tasks.append((task_key, task_data))
    
    # Sort by dependencies (topological sort) - tasks without deps first
    print(f"📊 Sorting {len(filtered_tasks)} tasks by dependencies...")
    filtered_tasks = topological_sort_tasks(filtered_tasks)
    
    print(f"\n📊 Found {len(filtered_tasks)} issue(s) to create\n")
    
    if args.dry_run:
        print("🔍 DRY RUN - would create:\n")
        for task_key, task_data in filtered_tasks:
            milestone = task_data.get("milestone", "")
            ai_eff = task_data.get("ai_effectiveness", "unknown")
            print(f"  • {task_key}: {task_data['task']} ({milestone}, {ai_eff})")
        return
    
    # Confirm
    if len(filtered_tasks) > 5:
        confirm = input(f"Create {len(filtered_tasks)} GitHub issue(s)? (y/n): ")
        if confirm.lower() != "y":
            print("❌ Cancelled")
            return
    
    # Create issues
    print("\n🚀 Creating issues...\n")
    success_count = 0
    
    for task_key, task_data in filtered_tasks:
        milestone = task_data.get("milestone", "")
        spec_file = find_spec_file(task_key, milestone)
        
        issue_number = create_github_issue(task_key, task_data, milestone, spec_file)
        if issue_number:
            success_count += 1
    
    print(f"\n✅ Complete: {success_count}/{len(filtered_tasks)} issues created")
    
    # Phase 2: Set blocking relationships using persisted queries
    print("\n🔗 Setting blocking relationships...\n")
    relationships_count = 0
    
    for task_key, task_data in filtered_tasks:
        dependencies = task_data.get("dependencies", [])
        if not dependencies:
            continue
        
        # Get this issue's node ID
        blocked_issue_node_id = created_issues_node_ids.get(task_key)
        if not blocked_issue_node_id:
            continue
        
        blocked_issue_num = created_issues_cache.get(task_key)
        
        # Set blocking relationship for each dependency
        for dep_key in dependencies:
            blocking_issue_node_id = created_issues_node_ids.get(dep_key)
            blocking_issue_num = created_issues_cache.get(dep_key)
            
            if blocking_issue_node_id and blocking_issue_num:
                print(f"   #{blocked_issue_num} ({task_key}) blocked by #{blocking_issue_num} ({dep_key})...", end=" ", flush=True)
                if link_issue_dependency(blocked_issue_node_id, blocking_issue_node_id):
                    print("✅")
                    relationships_count += 1
                else:
                    print("❌")
                time.sleep(0.3)  # Rate limit protection
    
    print(f"\n✅ Set {relationships_count} blocking relationships")
    
    # Phase 3: Assign Copilot agent to first ready task
    print("\n🤖 Assigning Copilot agent to first ready task...\n")
    
    ready_task = find_first_ready_task(
        filtered_tasks,
        created_issues_cache,
        created_issues_node_ids,
    )
    
    if ready_task:
        task_key, issue_num, node_id = ready_task
        task_data = next((data for key, data in filtered_tasks if key == task_key), None)
        
        if task_data:
            # Generate custom instructions
            custom_instructions = generate_copilot_instructions(task_key, task_data)
            
            # Assign Copilot
            print(f"   Assigning Copilot to #{issue_num} ({task_key})...", end=" ", flush=True)
            if assign_copilot_agent(node_id, custom_instructions, base_ref="main"):
                print("✅")
                print(f"\n   📝 Custom instructions sent ({len(custom_instructions)} characters)")
                print(f"   🔗 View: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/{issue_num}")
                print(f"   ⚠️  NOTE: Copilot for Issues is in beta - bot may not appear as assignee yet")
            else:
                print("❌")
                print("   ℹ️  Copilot API integration ready, waiting for beta graduation")
    else:
        print("   ⚠️  No ready tasks found for Copilot assignment")
        print("   💡 All tasks have dependencies or are not yet created")
    
    print(f"\n🔗 View issues: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")
    print(f"🔗 View project: https://github.com/orgs/{REPO_OWNER}/projects/{PROJECT_NUMBER}")



if __name__ == "__main__":
    main()
