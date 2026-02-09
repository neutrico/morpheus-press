#!/usr/bin/env python3
"""
Test custom agent assignment on real issue #174.
"""

import json
import subprocess
from copilot_agent import assign_copilot_agent, select_custom_agent, generate_copilot_instructions

# Issue #174 data
issue_number = 174
repo_owner = "neutrico"
repo_name = "morpheus-press"

print("\n🧪 Testing Custom Agent Assignment on Real Issue")
print("=" * 60)

# Step 1: Get issue details
print(f"\n📝 Step 1: Getting issue #{issue_number} details...")
cmd_issue = ["gh", "issue", "view", str(issue_number), "--json", "id,number,title,body,labels"]
result = subprocess.run(cmd_issue, capture_output=True, text=True, cwd="/workspaces/morpheus-press")

if result.returncode != 0:
    print(f"❌ Failed to get issue: {result.stderr}")
    exit(1)

issue_data = json.loads(result.stdout)
node_id = issue_data["id"]
title = issue_data["title"]
body = issue_data["body"]
labels = [label["name"] for label in issue_data.get("labels", [])]

print(f"✅ Found issue: {title}")
print(f"   Node ID: {node_id}")
print(f"   Labels: {labels}")
print(f"   Body preview: {body[:100]}...")

# Step 2: Create task_data for agent selection
print(f"\n📝 Step 2: Selecting custom agent...")
task_data = {
    "task": title,
    "description": body,
    "labels": labels,
}

selected_agent = select_custom_agent(task_data)
print(f"✅ Selected agent: {selected_agent or 'default (general Copilot)'}")

# Step 3: Generate custom instructions
print(f"\n📝 Step 3: Generating custom instructions...")
custom_instructions = generate_copilot_instructions("TEST", task_data)
print(f"✅ Generated instructions ({len(custom_instructions)} characters)")
print(f"\n--- Preview ---")
print(custom_instructions[:300])
print("...")

# Step 4: Assign Copilot with custom agent
print(f"\n📝 Step 4: Assigning Copilot agent...")
agent_info = f" with {selected_agent}" if selected_agent else ""
print(f"   Calling GitHub API{agent_info}...")

success = assign_copilot_agent(
    node_id,
    custom_instructions,
    base_ref="main",
    repo_owner=repo_owner,
    repo_name=repo_name,
    custom_agent=selected_agent,
)

if success:
    print("✅ Assignment succeeded!")
else:
    print("❌ Assignment failed")
    exit(1)

# Step 5: Verify assignment
print(f"\n📝 Step 5: Verifying assignment...")
cmd_verify = ["gh", "issue", "view", str(issue_number), "--json", "number,title,assignees,url"]
result_verify = subprocess.run(cmd_verify, capture_output=True, text=True, cwd="/workspaces/morpheus-press")

if result_verify.returncode != 0:
    print(f"⚠️  Could not verify: {result_verify.stderr}")
else:
    verify_data = json.loads(result_verify.stdout)
    assignees = [a["login"] for a in verify_data.get("assignees", [])]
    
    print(f"   Assignees: {assignees}")
    
    if "Copilot" in assignees or "copilot-swe-agent" in assignees:
        print("✅ Bot successfully assigned!")
    else:
        print("⚠️  Bot not yet visible (expected for beta)")
    
    print(f"\n🔗 View issue: {verify_data['url']}")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE!")
print("\nSummary:")
print(f"- Issue: #{issue_number}")
print(f"- Agent: {selected_agent or 'default'}")
print(f"- Instructions: {len(custom_instructions)} chars")
print(f"- Status: {'✅ Assigned' if success else '❌ Failed'}")
