#!/usr/bin/env python3
"""
Quick test for Copilot agent assignment on an existing issue.

Usage:
  python3 scripts/test_copilot_agent.py <issue_number>

Example:
  python3 scripts/test_copilot_agent.py 159
"""

import json
import subprocess
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from copilot_agent import (
    assign_copilot_agent,
    generate_copilot_instructions,
)


def get_issue_node_id(issue_number: int) -> str:
    """Get node ID for an existing issue."""
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
          number
          title
          state
        }
      }
    }
    """
    
    cmd = [
        "gh", "api", "graphql",
        "-f", f"query={query}",
        "-F", "owner=neutrico",
        "-F", "repo=morpheus-press",
        "-F", f"number={issue_number}",
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error getting issue: {result.stderr}")
        return None
    
    data = json.loads(result.stdout)
    
    if "data" in data and "repository" in data["data"]:
        issue = data["data"]["repository"]["issue"]
        if issue:
            print(f"✅ Found issue #{issue['number']}: {issue['title']}")
            print(f"   State: {issue['state']}")
            print(f"   Node ID: {issue['id']}")
            return issue["id"]
    
    return None


def main():
    """Test Copilot agent assignment on an existing issue."""
    if len(sys.argv) < 2:
        print("Usage: python3 test_copilot_agent.py <issue_number>")
        print("Example: python3 test_copilot_agent.py 159")
        return 1
    
    try:
        issue_number = int(sys.argv[1])
    except ValueError:
        print(f"❌ Invalid issue number: {sys.argv[1]}")
        return 1
    
    print("=" * 80)
    print(f"🧪 TEST: Assign Copilot agent to issue #{issue_number}")
    print("=" * 80)
    
    # Step 1: Get issue node ID
    print("\n📝 Step 1: Getting issue details...")
    node_id = get_issue_node_id(issue_number)
    
    if not node_id:
        print(f"❌ Issue #{issue_number} not found")
        return 1
    
    # Step 2: Generate custom instructions
    print("\n📝 Step 2: Generating custom instructions...")
    
    # Sample task data for testing
    task_data = {
        "task": f"Test Task #{issue_number}",
        "description": "This is a test task to verify Copilot agent assignment works correctly.",
        "priority": "p1",
        "effort": 3,
        "ai_effectiveness": "high",
        "agent_notes": {
            "research_findings": "Test research findings - GitHub Copilot can be assigned via GraphQL API using addAssigneesToAssignable mutation with agentAssignment parameter.",
            "implementation_approach": "Use the official GitHub GraphQL API to assign Copilot with custom instructions.",
            "design_decisions": [
                {
                    "decision": "Use GraphQL over REST",
                    "rationale": "GraphQL provides better type safety and flexibility for complex operations"
                },
                {
                    "decision": "Generate custom prompts from YAML",
                    "rationale": "Provides context-rich instructions for better AI performance"
                }
            ]
        }
    }
    
    custom_instructions = generate_copilot_instructions(f"TEST{issue_number}", task_data)
    print(f"✅ Generated instructions ({len(custom_instructions)} characters)")
    print("\n" + "─" * 80)
    print(custom_instructions[:500])  # Preview first 500 chars
    if len(custom_instructions) > 500:
        print(f"\n... (+ {len(custom_instructions) - 500} more characters)")
    print("─" * 80)
    
    # Step 3: Assign Copilot
    print("\n📝 Step 3: Assigning Copilot agent...")
    print(f"   Calling GitHub API...", end=" ", flush=True)
    
    if assign_copilot_agent(node_id, custom_instructions, base_ref="main"):
        print("✅")
        print("\n" + "=" * 80)
        print(f"✅ TEST PASSED: Copilot successfully assigned to issue #{issue_number}")
        print("=" * 80)
        print(f"\n🔗 View issue: https://github.com/neutrico/morpheus-press/issues/{issue_number}")
        print("\n💡 Check the issue on GitHub to see:")
        print("   - Copilot bot should be assigned")
        print("   - Custom instructions should be visible in the assignment")
        return 0
    else:
        print("❌")
        print("\n" + "=" * 80)
        print("❌ TEST FAILED: Copilot assignment failed")
        print("=" * 80)
        print("\n🔍 Possible reasons:")
        print("   - Copilot agent feature not enabled for this repository")
        print("   - Insufficient permissions (requires repo:write, copilot:write)")
        print("   - GitHub Copilot for Issues still in beta (may need waitlist access)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
