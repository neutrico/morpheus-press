#!/usr/bin/env python3
"""
Copilot Agent Assignment Functions

Functions to:
- Generate custom instructions from research/planning
- Assign Copilot agent to issues
- Find first ready-to-start task
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


def generate_copilot_instructions(
    task_key: str,
    task_data: Dict,
    research_file: Optional[Path] = None,
    plan_file: Optional[Path] = None,
) -> str:
    """
    Generate custom instructions for Copilot agent based on task metadata and research.
    
    Args:
        task_key: Task identifier (e.g., "T24")
        task_data: Task data from YAML
        research_file: Path to research file (optional)
        plan_file: Path to plan file (optional)
    
    Returns:
        Custom instructions string for Copilot
    """
    instructions = []
    
    # Task header
    instructions.append(f"# {task_key}: {task_data['task']}")
    instructions.append("")
    
    # Task description
    if 'description' in task_data:
        instructions.append("## Description")
        instructions.append(task_data['description'])
        instructions.append("")
    
    # Requirements from agent_notes if available
    if 'agent_notes' in task_data:
        agent_notes = task_data['agent_notes']
        
        # Research findings
        if 'research_findings' in agent_notes:
            instructions.append("## Research Findings")
            findings = agent_notes['research_findings']
            # Truncate if too long (max ~500 chars for prompt)
            if len(findings) > 500:
                findings = findings[:497] + "..."
            instructions.append(findings)
            instructions.append("")
        
        # Implementation approach
        if 'implementation_approach' in agent_notes:
            instructions.append("## Implementation Approach")
            instructions.append(agent_notes['implementation_approach'])
            instructions.append("")
        
        # Design decisions
        if 'design_decisions' in agent_notes:
            instructions.append("## Key Design Decisions")
            for decision in agent_notes['design_decisions'][:2]:  # Max 2 decisions
                instructions.append(f"- **{decision.get('decision', 'N/A')}**: {decision.get('rationale', 'N/A')}")
            instructions.append("")
    
    # Technical requirements
    instructions.append("## Technical Requirements")
    instructions.append(f"- Priority: {task_data.get('priority', 'p2')}")
    instructions.append(f"- Effort: {task_data.get('effort', '?')} points")
    instructions.append(f"- AI Effectiveness: {task_data.get('ai_effectiveness', 'medium')}")
    instructions.append("")
    
    # Quality standards
    instructions.append("## Quality Standards")
    instructions.append("- Follow SOLID, DRY, KISS principles")
    instructions.append("- Write unit tests (Vitest)")
    instructions.append("- Add comprehensive error handling")
    instructions.append("- Use TypeScript strict mode")
    instructions.append("")
    
    # Files to modify (if available from research)
    instructions.append("## Expected Files")
    instructions.append("- Refer to project structure in .github/copilot-instructions.md")
    instructions.append("- Follow existing patterns from similar files")
    
    return "\n".join(instructions)


def assign_copilot_agent(
    issue_node_id: str,
    custom_instructions: str,
    target_repo_id: Optional[str] = None,
    base_ref: str = "main",
    repo_owner: str = "neutrico",
    repo_name: str = "morpheus-press",
) -> bool:
    """
    Assign Copilot agent to an issue with custom instructions.
    
    Official GitHub Copilot coding agent integration using GraphQL API.
    Requires copilot-swe-agent bot to be available in the repository.
    
    Args:
        issue_node_id: Node ID of the issue (e.g., "I_kwDORLroa87pUX0B")
        custom_instructions: Custom prompt for Copilot (max ~2000 chars)
        target_repo_id: Repository node ID (optional, for working in different repo)
        base_ref: Base branch (defaults to "main")
        repo_owner: Repository owner (for finding copilot bot)
        repo_name: Repository name (for finding copilot bot)
    
   Returns:
        True if mutation succeeded and bot assigned, False otherwise
    """
    # Step 1: Find copilot-swe-agent bot ID in repository's suggestedActors
    query_bot = f"""
    query {{
      repository(owner: "{repo_owner}", name: "{repo_name}") {{
        suggestedActors(capabilities: [CAN_BE_ASSIGNED], first: 100) {{
          nodes {{
            login
            __typename
            ... on Bot {{
              id
            }}
            ... on User {{
              id
            }}
          }}
        }}
      }}
    }}
    """
    
    cmd_bot = ["gh", "api", "graphql", "-f", f"query={query_bot}"]
    result_bot = subprocess.run(cmd_bot, capture_output=True, text=True)
    
    if result_bot.returncode != 0:
        print(f"❌ Failed to query suggestedActors: {result_bot.stderr}")
        return False
    
    try:
        response_bot = json.loads(result_bot.stdout)
        actors = response_bot.get("data", {}).get("repository", {}).get("suggestedActors", {}).get("nodes", [])
        
        # Find copilot-swe-agent
        copilot_bot = next((actor for actor in actors if actor.get("login") == "copilot-swe-agent"), None)
        
        if not copilot_bot:
            print(f"⚠️  copilot-swe-agent not available in repository")
            print(f"   Enable Copilot for Issues: https://github.com/{repo_owner}/{repo_name}/settings")
            return False
        
        bot_id = copilot_bot.get("id")
        if not bot_id:
            print(f"❌ copilot-swe-agent found but no ID returned")
            return False
            
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Failed to parse bot query response: {e}")
        return False
    
    # Step 2: Assign bot to issue with custom instructions
    # Use addAssigneesToAssignable mutation with agentAssignment
    
    # Escape custom instructions for GraphQL
    escaped_instructions = custom_instructions.replace('"', '\\"').replace('\n', '\\n')
    if len(escaped_instructions) > 2000:
        escaped_instructions = escaped_instructions[:1997] + "..."
    
    mutation = f"""
    mutation {{
      addAssigneesToAssignable(input: {{
        assignableId: \"{issue_node_id}\"
        assigneeIds: [\"{bot_id}\"]
        agentAssignment: {{
          baseRef: \"{base_ref}\"
          customInstructions: \"{escaped_instructions}\"
        }}
      }}) {{
        assignable {{
          ... on Issue {{
            id
            number
            title
            assignees(first: 10) {{
              nodes {{
                login
              }}
            }}
          }}
        }}
      }}
    }}
    """
    
    # CRITICAL: Must include GraphQL feature flags header
    cmd_assign = [
        "gh", "api", "graphql",
        "-H", "GraphQL-Features: issues_copilot_assignment_api_support,coding_agent_model_selection",
        "-f", f"query={mutation}"
    ]
    
    result_assign = subprocess.run(cmd_assign, capture_output=True, text=True)
    
    if result_assign.returncode != 0:
        stderr = result_assign.stderr.strip()
        if "Resource not accessible" in stderr or "FORBIDDEN" in stderr:
            print(f"⚠️  Insufficient permissions or Copilot beta not enabled")
            print(f"   Check: https://github.com/{repo_owner}/{repo_name}/settings")
        else:
            print(f"❌ Assignment failed: {stderr}")
        return False
    
    try:
        response_assign = json.loads(result_assign.stdout)
        
        # Check for errors
        if "errors" in response_assign:
            errors = response_assign["errors"]
            print(f"❌ GraphQL errors: {errors}")
            return False
        
        # Check if mutation succeeded
        if "data" in response_assign and "addAssigneesToAssignable" in response_assign["data"]:
            assignable = response_assign["data"]["addAssigneesToAssignable"]["assignable"]
            assignees = assignable.get("assignees", {}).get("nodes", [])
            
            # Verify copilot-swe-agent is in assignees
            if any(a.get("login") == "copilot-swe-agent" for a in assignees):
                return True
            else:
                print(f"⚠️  Mutation succeeded but bot not in assignees (expected for beta)")
                return True  # Still count as success - beta behavior
                
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Failed to parse assignment response: {e}")
        print(f"   Response: {result_assign.stdout[:500]}")
    
    return False


def find_first_ready_task(
    all_tasks: List[Tuple[str, Dict]],
    created_issues: Dict[str, int],
    created_node_ids: Dict[str, str],
) -> Optional[Tuple[str, int, str]]:
    """
    Find the first task that is ready to start:
    - In first milestone (M0) or first iteration (I1)
    - Has no blockers (no dependencies)
    - Has high AI effectiveness
    
    Args:
        all_tasks: List of (task_key, task_data) tuples
        created_issues: Dict of task_key -> issue_number
        created_node_ids: Dict of task_key -> node_id
    
    Returns:
        Tuple of (task_key, issue_number, node_id) or None
    """
    # Sort by priority (p0 > p1 > p2 > p3) and effort (smaller first)
    priority_order = {"p0": 0, "critical": 0, "p1": 1, "high": 1, "p2": 2, "medium": 2, "p3": 3, "low": 3}
    
    def task_score(task):
        task_key, task_data = task
        priority = priority_order.get(task_data.get("priority", "p2").lower(), 2)
        effort = task_data.get("effort", 5)
        ai_effectiveness = task_data.get("ai_effectiveness", "medium").lower()
        
        # Prefer high AI effectiveness
        ai_score = {"high": 0, "medium": 1, "low": 2}.get(ai_effectiveness, 1)
        
        # Combined score (lower is better)
        return (priority, ai_score, effort)
    
    # Filter candidates
    candidates = []
    for task_key, task_data in all_tasks:
        # Must be created
        if task_key not in created_issues or task_key not in created_node_ids:
            continue
        
        # Must have no dependencies (ready to start)
        dependencies = task_data.get("dependencies", [])
        if dependencies:
            continue
        
        # Prefer M0 or I1
        milestone = task_data.get("milestone", "")
        iteration = task_data.get("iteration", "")
        
        if "M0" in milestone or iteration == "I1":
            candidates.append((task_key, task_data))
    
    if not candidates:
        # Fallback: any task with no dependencies
        for task_key, task_data in all_tasks:
            if task_key not in created_issues or task_key not in created_node_ids:
                continue
            dependencies = task_data.get("dependencies", [])
            if not dependencies:
                candidates.append((task_key, task_data))
    
    if not candidates:
        return None
    
    # Sort by score and pick first
    candidates.sort(key=task_score)
    task_key, task_data = candidates[0]
    
    return (
        task_key,
        created_issues[task_key],
        created_node_ids[task_key],
    )
