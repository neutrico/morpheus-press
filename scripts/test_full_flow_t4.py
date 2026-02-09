#!/usr/bin/env python3
"""
Create single task T4 from planning YAML and test full custom agent flow.
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from copilot_agent import (
    assign_copilot_agent,
    generate_copilot_instructions,
    select_custom_agent,
)

REPO_OWNER = "neutrico"
REPO_NAME = "morpheus-press"
PLANNING_FILE = Path("/workspaces/morpheus-press/planning/issues/m0-infrastructure.yaml")

print("\n🚀 Full Flow Test: Create Task T4 with Custom Agent")
print("=" * 70)

# Step 1: Load task data from YAML
print("\n📝 Step 1: Loading task T4 from planning YAML...")
with open(PLANNING_FILE) as f:
    planning_data = yaml.safe_load(f)

task_t4 = None
for task in planning_data.get("issues", []):
    if task.get("key") == "T4":
        task_t4 = task
        break

if not task_t4:
    print("❌ Task T4 not found in planning file")
    exit(1)

print(f"✅ Loaded task: {task_t4['title']}")
print(f"   Priority: {task_t4.get('priority', 'N/A')}")
print(f"   Effort: {task_t4.get('effort', 'N/A')} points")
print(f"   Area: {task_t4.get('area', 'N/A')}")

# Step 2: Select custom agent
print(f"\n📝 Step 2: Selecting custom agent...")
selected_agent = select_custom_agent(task_t4)
print(f"✅ Selected agent: {selected_agent or 'default (general Copilot)'}")

# Step 3: Generate custom instructions
print(f"\n📝 Step 3: Generating custom instructions...")
custom_instructions = generate_copilot_instructions("T4", task_t4)
print(f"✅ Generated {len(custom_instructions)} characters")
print(f"\n--- Instructions Preview (first 400 chars) ---")
print(custom_instructions[:400])
print("...")

# Step 4: Create GitHub issue
print(f"\n📝 Step 4: Creating GitHub issue...")

# Build issue body from planning data
body_parts = []

if task_t4.get("agent_notes", {}).get("research_findings"):
    findings = task_t4["agent_notes"]["research_findings"]
    # Truncate if too long
    if len(findings) > 2000:
        findings = findings[:1997] + "..."
    body_parts.append(f"## Research Findings\n\n{findings}")

if task_t4.get("technical_notes", {}).get("approach"):
    approach = task_t4["technical_notes"]["approach"]
    body_parts.append(f"## Technical Approach\n\n{approach}")

# Add metadata
body_parts.append(f"\n## Task Metadata\n")
body_parts.append(f"- **Priority**: {task_t4.get('priority', 'p2')}")
body_parts.append(f"- **Effort**: {task_t4.get('effort', '?')} points")
body_parts.append(f"- **Area**: {task_t4.get('area', 'N/A')}")
body_parts.append(f"- **Iteration**: {task_t4.get('iteration', 'N/A')}")

issue_body = "\n\n".join(body_parts)

# Create issue
cmd_create = [
    "gh", "issue", "create",
    "--title", f"T4: {task_t4['title']}",
    "--body", issue_body,
    "--label", "task,from-planning,automation:ready",
    "--milestone", task_t4.get("milestone", "M0 - Infrastructure & Setup"),
]

result_create = subprocess.run(cmd_create, capture_output=True, text=True, cwd="/workspaces/morpheus-press")

if result_create.returncode != 0:
    print(f"❌ Failed to create issue: {result_create.stderr}")
    exit(1)

issue_url = result_create.stdout.strip()
issue_number = int(issue_url.split("/")[-1])
print(f"✅ Created issue #{issue_number}")
print(f"   URL: {issue_url}")

# Step 5: Get issue node ID
print(f"\n📝 Step 5: Getting issue node ID...")
cmd_node_id = ["gh", "issue", "view", str(issue_number), "--json", "id"]
result_node_id = subprocess.run(cmd_node_id, capture_output=True, text=True, cwd="/workspaces/morpheus-press")

if result_node_id.returncode != 0:
    print(f"❌ Failed to get node ID: {result_node_id.stderr}")
    exit(1)

node_id_data = json.loads(result_node_id.stdout)
node_id = node_id_data["id"]
print(f"✅ Node ID: {node_id}")

# Step 6: Assign Copilot with custom agent
print(f"\n📝 Step 6: Assigning Copilot agent...")
agent_info = f" with {selected_agent}" if selected_agent else ""
print(f"   Assigning{agent_info}...")

success = assign_copilot_agent(
    node_id,
    custom_instructions,
    base_ref="main",
    repo_owner=REPO_OWNER,
    repo_name=REPO_NAME,
    custom_agent=selected_agent,
)

if not success:
    print("❌ Assignment failed")
    exit(1)

print("✅ Assignment succeeded!")

# Step 7: Verify final state
print(f"\n📝 Step 7: Verifying final state...")
cmd_verify = ["gh", "issue", "view", str(issue_number), "--json", "number,title,assignees,labels,milestone,url"]
result_verify = subprocess.run(cmd_verify, capture_output=True, text=True, cwd="/workspaces/morpheus-press")

if result_verify.returncode != 0:
    print(f"⚠️  Could not verify: {result_verify.stderr}")
else:
    verify_data = json.loads(result_verify.stdout)
    assignees = [a["login"] for a in verify_data.get("assignees", [])]
    labels = [l["name"] for l in verify_data.get("labels", [])]
    milestone = verify_data.get("milestone", {}).get("title", "N/A")
    
    print(f"✅ Issue #{verify_data['number']}: {verify_data['title']}")
    print(f"   Assignees: {assignees}")
    print(f"   Labels: {labels}")
    print(f"   Milestone: {milestone}")
    print(f"   URL: {verify_data['url']}")
    
    if "Copilot" in assignees or "copilot-swe-agent" in assignees:
        print("\n🎉 SUCCESS! Copilot bot is assigned!")
    else:
        print("\n⚠️  Bot not yet visible (may take a moment)")

print("\n" + "=" * 70)
print("✅ FULL FLOW TEST COMPLETE!")
print(f"\nSummary:")
print(f"- Task: T4 - {task_t4['title']}")
print(f"- Issue: #{issue_number}")
print(f"- Custom Agent: {selected_agent or 'default'}")
print(f"- Instructions: {len(custom_instructions)} chars")
print(f"- Status: {'✅ Assigned' if success else '❌ Failed'}")
print(f"\n🔗 View issue: {issue_url}")
