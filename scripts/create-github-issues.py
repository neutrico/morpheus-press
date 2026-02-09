#!/usr/bin/env python3
"""
Create GitHub Issues from Planning System

Usage:
  python scripts/planning/create-github-issues.py              # Create all issues
  python scripts/planning/create-github-issues.py T24          # Create single issue
  python scripts/planning/create-github-issues.py --milestone M1  # Create milestone issues
  python scripts/planning/create-github-issues.py --dry-run    # Preview without creating
"""

import os
import sys
import yaml
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE_ROOT = Path('/workspaces/morpheus-press')

def load_planning_data():
    """Load all planning data"""
    
    # Load effort-map
    effort_map_path = WORKSPACE_ROOT / 'planning/estimates/effort-map.yaml'
    with open(effort_map_path, 'r') as f:
        effort_map = yaml.safe_load(f)
    
    # Load issues
    issues_dir = WORKSPACE_ROOT / 'planning/issues'
    all_issues = []
    
    for issue_file in issues_dir.glob('*.yaml'):
        with open(issue_file, 'r') as f:
            issue_data = yaml.safe_load(f)
        
        for issue in issue_data.get('issues', []):
            all_issues.append(issue)
    
    # Combine data
    enriched_issues = []
    for issue in all_issues:
        key = issue['key']
        estimate = effort_map['estimates'].get(key, {})
        
        enriched_issues.append({
            **issue,
            'estimated_days': estimate.get('estimated_days', 0),
            'ai_effectiveness': extract_ai_effectiveness(estimate.get('reasoning', '')),
            'reasoning': estimate.get('reasoning', ''),
        })
    
    return enriched_issues

def extract_ai_effectiveness(reasoning: str) -> str:
    """Extract AI effectiveness from reasoning"""
    if 'AI Impact: HIGH' in reasoning or 'HIGH AI effectiveness' in reasoning:
        return 'HIGH'
    elif 'AI Impact: MEDIUM' in reasoning or 'MEDIUM AI effectiveness' in reasoning:
        return 'MEDIUM'
    elif 'AI Impact: LOW' in reasoning or 'LOW AI effectiveness' in reasoning:
        return 'LOW'
    return 'UNKNOWN'

def find_docs_for_task(task_key: str) -> Optional[str]:
    """Find markdown doc for task"""
    docs_dir = WORKSPACE_ROOT / 'planning/docs'
    docs_files = list(docs_dir.glob(f'**/{task_key}-*.md'))
    
    if docs_files:
        return str(docs_files[0].relative_to(WORKSPACE_ROOT))
    return None

def create_milestones(dry_run: bool = False) -> Dict[str, int]:
    """Create GitHub milestones via API and return milestone name -> number mapping"""
    
    milestones = [
        {'title': 'M0 - Infrastructure & Setup', 'due_on': '2026-02-28T00:00:00Z', 'description': 'Project setup, CI/CD, devcontainer, Docker'},
        {'title': 'M1 - Backend Services', 'due_on': '2026-03-31T00:00:00Z', 'description': 'Supabase, API routes, services, testing'},
        {'title': 'M2 - Dashboard UI', 'due_on': '2026-04-30T00:00:00Z', 'description': 'Next.js dashboard, shadcn/ui components'},
        {'title': 'M3 - Image Generation', 'due_on': '2026-05-31T00:00:00Z', 'description': 'RunPod, Stable Diffusion, ComfyUI integration'},
        {'title': 'M4 - ML & Publishing', 'due_on': '2026-06-30T00:00:00Z', 'description': 'Propaganda detection, e-commerce, PDF generation'},
    ]
    
    milestone_map = {}
    
    if dry_run:
        print("\n📅 Would create milestones:")
        for ms in milestones:
            print(f"   • {ms['title']} (due: {ms['due_on'][:10]})")
        # Return dummy mapping for dry-run
        return {ms['title']: idx+1 for idx, ms in enumerate(milestones)}
    
    # Get existing milestones
    try:
        result = subprocess.run(
            ['gh', 'api', '/repos/neutrico/morpheus-press/milestones', '--jq', '.[] | "\(.number)\t\(.title)"'],
            capture_output=True, text=True, check=False
        )
        
        existing = {}
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.strip().split('\n'):
                if '\t' in line:
                    num, title = line.split('\t', 1)
                    existing[title] = int(num)
        
        print(f"\n📅 Found {len(existing)} existing milestones")
    except Exception as e:
        print(f"⚠️  Could not fetch existing milestones: {e}")
        existing = {}
    
    # Create missing milestones
    print("\n📅 Creating milestones...")
    for ms in milestones:
        title = ms['title']
        
        if title in existing:
            milestone_map[title] = existing[title]
            print(f"   ✓ {title} (already exists)")
            continue
        
        try:
            result = subprocess.run(
                ['gh', 'api', '/repos/neutrico/morpheus-press/milestones',
                 '-f', f"title={title}",
                 '-f', f"due_on={ms['due_on']}",
                 '-f', f"description={ms['description']}",
                 '--jq', '.number'],
                capture_output=True, text=True, check=True
            )
            
            milestone_num = int(result.stdout.strip())
            milestone_map[title] = milestone_num
            print(f"   ✅ Created: {title} (#{milestone_num})")
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to create {title}: {e.stderr}")
    
    return milestone_map

def create_issue_body(issue: Dict) -> str:
    """Generate GitHub issue body"""
    
    key = issue['key']
    title = issue['title']
    description = issue.get('description', '')
    milestone = issue.get('milestone', '')
    estimated_days = issue.get('estimated_days', 0)
    ai_effectiveness = issue.get('ai_effectiveness', 'UNKNOWN')
    acceptance_criteria = issue.get('acceptance_criteria', [])
    deps = issue.get('dependsOn', [])
    
    # Find docs
    docs_path = find_docs_for_task(key)
    
    # Build body
    body = f"""## 📋 Task Information

**Task Key:** {key}  
**Milestone:** {milestone}  
**Estimated Days (AI-aware):** {estimated_days} days  
**AI Effectiveness:** {ai_effectiveness}

## 📚 Specification

"""
    
    if docs_path:
        body += f"**Location:** `{docs_path}`\n\n"
    
    body += f"**Brief Description:**\n{description}\n\n"
    
    # Acceptance criteria
    if acceptance_criteria:
        body += "## ✅ Acceptance Criteria\n\n"
        for criterion in acceptance_criteria:
            body += f"- [ ] {criterion}\n"
        body += "\n"
    
    # Automation hint
    body += """## 🤖 Automation Available

<!-- 
🚨 COPILOT: Check this before starting implementation!

If AI Effectiveness = HIGH:
  1. Comment "/automate" below to trigger auto-generation
  2. Wait for bot to create PR with starter code
  3. Review PR, fix TODO comments
  4. Test and refine

If AI Effectiveness = MEDIUM/LOW:
  1. Read planning/docs/[task-key]*.md
  2. Implement manually
  3. Use patterns from similar tasks
-->

**Automation Status:**
"""
    
    if ai_effectiveness == 'HIGH':
        body += "- [x] ✅ Automation available for this task type\n"
        body += "- [ ] Auto-generation triggered (comment `/automate`)\n"
    else:
        body += "- [ ] ⚠️  Automation not recommended (manual implementation preferred)\n"
    
    body += "- [ ] PR created with generated code\n"
    body += "- [ ] Code reviewed and refined\n\n"
    
    # Dependencies
    if deps:
        body += "## 🔗 Dependencies\n\n"
        for dep in deps:
            body += f"- [ ] {dep}\n"
        body += "\n"
    
    # Implementation notes
    body += f"""## 🔧 Implementation Notes

**Related Files:**
- Spec: `{docs_path or 'planning/docs/[milestone]/[task-key]-*.md'}`
- Research: `planning/issues/*.yaml` (search for {key})
- Estimate: `planning/estimates/effort-map.yaml` ({key})

## 🧪 Testing

- [ ] Unit tests passing (`pnpm test`)
- [ ] Integration tests (if applicable)
- [ ] Manual testing completed
- [ ] Edge cases covered

## 📝 Implementation Checklist

- [ ] Read task specification from `planning/docs/`
"""
    
    if ai_effectiveness == 'HIGH':
        body += "- [ ] Check for auto-generated PR (comment `/automate` if needed)\n"
    
    body += """- [ ] Implement or refine generated code
- [ ] Add/fix TODO comments
- [ ] Write/update tests
- [ ] Run `pnpm test` and verify passing
- [ ] Update documentation if needed
- [ ] Request review

---

"""
    
    if ai_effectiveness == 'HIGH':
        body += "**🤖 Automation Trigger:** Comment `/automate` to trigger code generation\n\n"
    
    body += "**📖 Documentation:** See [Task Automation README](../scripts/automation/README.md)\n"
    
    return body

def create_github_issue(issue: Dict, milestone_map: Dict[str, int], dry_run: bool = False) -> bool:
    """Create GitHub issue using gh CLI"""
    
    key = issue['key']
    title = f"{key}: {issue['title']}"
    body = create_issue_body(issue)
    milestone = issue.get('milestone', '')
    priority = issue.get('priority', 'Medium')
    ai_effectiveness = issue.get('ai_effectiveness', 'UNKNOWN')
    
    # Labels
    labels = ['task', 'from-planning']
    
    if ai_effectiveness == 'HIGH':
        labels.append('automation:ready')
    elif ai_effectiveness == 'MEDIUM':
        labels.append('automation:partial')
    
    if priority == 'Critical':
        labels.append('priority:critical')
    elif priority == 'High':
        labels.append('priority:high')
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"WOULD CREATE ISSUE: {title}")
        print(f"{'='*80}")
        print(f"Labels: {', '.join(labels)}")
        print(f"Milestone: {milestone}")
        print(f"\nBody Preview (first 500 chars):")
        print(body[:500] + "...")
        return True
    
    # Create issue via gh CLI
    try:
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
        ]
        
        for label in labels:
            cmd.extend(['--label', label])
        
        # Add milestone if exists
        if milestone:
            # Extract M0, M1, etc. and find full milestone title
            milestone_prefix = milestone.split(' ')[0]  # e.g., 'M0' from 'M0 - Infrastructure'
            milestone_title = None
            for ms_title in milestone_map.keys():
                if ms_title.startswith(milestone_prefix):
                    milestone_title = ms_title
                    break
            
            if milestone_title and milestone_title in milestone_map:
                # gh CLI accepts milestone NAME, not number
                cmd.extend(['--milestone', milestone_title])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        issue_url = result.stdout.strip()
        print(f"✅ Created: {title}")
        print(f"   URL: {issue_url}")
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create {key}: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create GitHub Issues from Planning')
    parser.add_argument('task_key', nargs='?', help='Specific task key (e.g., T24)')
    parser.add_argument('--milestone', help='Filter by milestone (e.g., M1)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating')
    parser.add_argument('--ai-high-only', action='store_true', help='Only HIGH AI effectiveness tasks')
    
    args = parser.parse_args()
    
    print("🚀 GitHub Issue Creator")
    print("="*80)
    
    # Create milestones first
    milestone_map = create_milestones(dry_run=args.dry_run)
    
    # Load planning data
    issues = load_planning_data()
    
    # Filter
    if args.task_key:
        issues = [i for i in issues if i['key'] == args.task_key]
    
    if args.milestone:
        issues = [i for i in issues if i.get('milestone', '').startswith(args.milestone)]
    
    if args.ai_high_only:
        issues = [i for i in issues if i.get('ai_effectiveness') == 'HIGH']
    
    if not issues:
        print("❌ No issues found matching criteria")
        return
    
    print(f"\nFound {len(issues)} issue(s) to create")
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No issues will be created\n")
    else:
        response = input(f"\nCreate {len(issues)} GitHub issue(s)? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return
    
    # Create issues
    success = 0
    for issue in issues:
        if create_github_issue(issue, milestone_map, dry_run=args.dry_run):
            success += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Complete: {success}/{len(issues)} issues {'would be' if args.dry_run else ''} created")
    
    if not args.dry_run and success > 0:
        print(f"\n📝 Next steps:")
        print(f"   1. Review issues on GitHub")
        print(f"   2. Assign HIGH AI tasks to @copilot")
        print(f"   3. Or comment /automate to trigger automation")

if __name__ == '__main__':
    main()
