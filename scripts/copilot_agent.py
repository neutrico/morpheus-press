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
) -> bool:
    """
    Assign Copilot agent to an issue with custom instructions.
    
    Args:
        issue_node_id: Node ID of the issue (e.g., "I_kwDORLroa87pUX0B")
        custom_instructions: Custom prompt for Copilot
        target_repo_id: Repository node ID (defaults to issue's repo)
        base_ref: Base branch (defaults to "main")
    
    Returns:
        True if successful, False otherwise
    """
    mutation = """
    mutation($assignableId: ID!, $agentAssignment: AgentAssignmentInput) {
      addAssigneesToAssignable(input: {
        assignableId: $assignableId
        assigneeIds: []
        agentAssignment: $agentAssignment
      }) {
        assignable {
          ... on Issue {
            id
            number
            title
          }
        }
      }
    }
    """
    
    # Build agent assignment input
    agent_assignment = {
        "baseRef": base_ref,
        "customInstructions": custom_instructions,
    }
    
    if target_repo_id:
        agent_assignment["targetRepositoryId"] = target_repo_id
    
    # Execute mutation via gh cli
    variables = {
        "assignableId": issue_node_id,
        "agentAssignment": agent_assignment,
    }
    
    cmd = ["gh", "api", "graphql", "-f", f"query={mutation}"]
    
    # Add variables with -F for JSON types
    for key, value in variables.items():
        cmd.extend(["-F", f"{key}={json.dumps(value)}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Copilot assignment error: {result.stderr}")
        return False
    
    response = json.loads(result.stdout) if result.stdout else {}
    return "data" in response and "addAssigneesToAssignable" in response["data"]


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
