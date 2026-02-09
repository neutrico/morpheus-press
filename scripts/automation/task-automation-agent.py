#!/usr/bin/env python3
"""
Task Automation Agent - Generate code for HIGH AI effectiveness tasks

Usage:
  python scripts/automation/task-automation-agent.py T24      # Generate code for specific task
  python scripts/automation/task-automation-agent.py --auto   # Auto-generate all HIGH AI tasks
  python scripts/automation/task-automation-agent.py --dry-run T24  # Preview without creating files

Workflow:
  1. Read task spec from planning/docs/
  2. Identify task pattern (setup/tests/api/database)
  3. Generate code using LLM + templates
  4. Create files + tests
  5. Optional: Create PR for review
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()

# Task Pattern Categories
PATTERNS = {
    'database': ['setup', 'migration', 'schema', 'database', 'supabase', 'rls'],
    'testing': ['test', 'unit test', 'e2e', 'vitest', 'playwright'],
    'api': ['api', 'route', 'endpoint', 'fastify', 'rest'],
    'setup': ['setup', 'config', 'installation', 'infrastructure'],
    'documentation': ['docs', 'documentation', 'readme', 'guide'],
    'component': ['component', 'ui', 'shadcn', 'react'],
}

class TaskAutomationAgent:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.client = anthropic.Anthropic(api_key=self.anthropic_key)
        self.workspace_root = Path('/workspaces/morpheus-press-press')
    
    def load_task_spec(self, task_key: str) -> Optional[Dict[str, Any]]:
        """Load task specification from planning/docs/ and planning/issues/"""
        
        # 1. Load from effort-map.yaml
        effort_map_path = self.workspace_root / 'planning/estimates/effort-map.yaml'
        with open(effort_map_path, 'r') as f:
            effort_map = yaml.safe_load(f)
        
        if task_key not in effort_map['estimates']:
            print(f"❌ Task {task_key} not found in effort-map.yaml")
            return None
        
        task_estimate = effort_map['estimates'][task_key]
        
        # 2. Find task in issues/*.yaml
        issues_dir = self.workspace_root / 'planning/issues'
        task_issue = None
        
        for issue_file in issues_dir.glob('*.yaml'):
            with open(issue_file, 'r') as f:
                issue_data = yaml.safe_load(f)
            
            for issue in issue_data.get('issues', []):
                if issue['key'] == task_key:
                    task_issue = issue
                    break
            
            if task_issue:
                break
        
        if not task_issue:
            print(f"❌ Task {task_key} not found in planning/issues/")
            return None
        
        # 3. Find markdown doc in planning/docs/
        docs_pattern = f"**/{task_key}-*.md"
        docs_files = list((self.workspace_root / 'planning/docs').glob(docs_pattern))
        
        task_doc_content = None
        if docs_files:
            with open(docs_files[0], 'r', encoding='utf-8') as f:
                task_doc_content = f.read()
        
        return {
            'key': task_key,
            'title': task_estimate['title'],
            'estimated_days': task_estimate.get('estimated_days', 0),
            'reasoning': task_estimate.get('reasoning', ''),
            'milestone': task_issue.get('milestone'),
            'area': task_issue.get('area'),
            'description': task_issue.get('description', ''),
            'acceptance_criteria': task_issue.get('acceptance_criteria', []),
            'agent_notes': task_issue.get('agent_notes', {}),
            'doc_content': task_doc_content,
        }
    
    def identify_pattern(self, task_spec: Dict[str, Any]) -> str:
        """Identify task pattern for template selection"""
        title_lower = task_spec['title'].lower()
        desc_lower = task_spec['description'].lower()
        
        for pattern_name, keywords in PATTERNS.items():
            if any(kw in title_lower or kw in desc_lower for kw in keywords):
                return pattern_name
        
        return 'generic'
    
    def generate_code(self, task_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate code using LLM + task specification"""
        
        pattern = self.identify_pattern(task_spec)
        
        # Build comprehensive prompt
        prompt = self._build_generation_prompt(task_spec, pattern)
        
        print(f"🤖 Generating code for {task_spec['key']} (pattern: {pattern})...")
        print(f"   Calling Claude Sonnet 4 (~$0.15)...")
        
        if self.dry_run:
            print("   [DRY RUN] Would generate code with LLM")
            return {'main.ts': '// Generated code would appear here'}
        
        # Call LLM
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            temperature=0.3,  # Lower for more consistent code generation
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response - expect JSON with file paths and content
        response_text = response.content[0].text
        
        # Extract code blocks from response
        files = self._parse_llm_response(response_text)
        
        return files
    
    def _build_generation_prompt(self, task_spec: Dict[str, Any], pattern: str) -> str:
        """Build comprehensive prompt for LLM code generation"""
        
        research_findings = task_spec['agent_notes'].get('research_findings', '')
        acceptance_criteria = '\n'.join(f"- {c}" for c in task_spec['acceptance_criteria'])
        
        prompt = f"""You are a Senior Full-Stack Developer implementing task {task_spec['key']}.

📋 TASK SPECIFICATION:
Title: {task_spec['title']}
Pattern: {pattern}
Estimated Days: {task_spec['estimated_days']}
Milestone: {task_spec['milestone']}
Area: {task_spec['area']}

📝 DESCRIPTION:
{task_spec['description']}

✅ ACCEPTANCE CRITERIA:
{acceptance_criteria}

🔬 RESEARCH FINDINGS:
{research_findings}

📚 FULL DOCUMENTATION:
{task_spec.get('doc_content', 'No detailed docs available')}

🎯 YOUR TASK:
Generate production-ready code for this task following these principles:
1. ✅ Follow SOLID, DRY, KISS principles
2. ✅ Use TypeScript with strict typing
3. ✅ Include comprehensive tests (Vitest)
4. ✅ Add JSDoc comments for public APIs
5. ✅ Follow project structure (see .github/copilot-instructions.md)
6. ✅ Handle errors properly
7. ✅ Log structured data (Pino/console)

📦 OUTPUT FORMAT:
Return a JSON object with file paths and content:

```json
{{
  "files": {{
    "apps/backend/src/services/example.service.ts": "import ...",
    "apps/backend/src/routes/example.routes.ts": "import ...",
    "apps/backend/src/__tests__/example.test.ts": "import ..."
  }},
  "summary": "Brief summary of what was generated",
  "next_steps": ["Manual step 1", "Manual step 2"]
}}
```

IMPORTANT:
- Use relative paths from /workspaces/morpheus-press/
- Don't use placeholders like "...existing code..." - write COMPLETE files
- If task requires manual steps (config changes, DB migrations), list in next_steps
- Prefer creating new files over modifying existing ones

Generate the implementation now:
"""
        
        return prompt
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, str]:
        """Parse LLM response to extract file paths and content"""
        import json
        import re
        
        # Try to extract JSON from response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return data.get('files', {})
            except json.JSONDecodeError:
                pass
        
        # Fallback: extract code blocks
        files = {}
        code_blocks = re.findall(r'```(\w+)?\s*\n(.*?)```', response_text, re.DOTALL)
        
        for i, (lang, code) in enumerate(code_blocks):
            filename = f"generated_{i}.{lang or 'ts'}"
            files[filename] = code
        
        return files
    
    def write_files(self, files: Dict[str, str]) -> List[str]:
        """Write generated files to disk"""
        written = []
        
        for file_path, content in files.items():
            full_path = self.workspace_root / file_path
            
            if self.dry_run:
                print(f"   [DRY RUN] Would write: {file_path} ({len(content)} bytes)")
                continue
            
            # Create directories
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            written.append(str(file_path))
            print(f"   ✅ Written: {file_path}")
        
        return written
    
    def automate_task(self, task_key: str) -> bool:
        """Full automation workflow for a single task"""
        print(f"\n🚀 AUTOMATING TASK: {task_key}")
        print("="*80)
        
        # 1. Load spec
        task_spec = self.load_task_spec(task_key)
        if not task_spec:
            return False
        
        print(f"✅ Loaded task spec: {task_spec['title']}")
        print(f"   Pattern: {self.identify_pattern(task_spec)}")
        print(f"   Estimated: {task_spec['estimated_days']} days")
        
        # 2. Check if HIGH AI effectiveness
        if 'AI Impact: HIGH' not in task_spec['reasoning']:
            print(f"⚠️  Task is not HIGH AI effectiveness - automation may be less effective")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False
        
        # 3. Generate code
        try:
            files = self.generate_code(task_spec)
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
            return False
        
        print(f"\n📦 Generated {len(files)} files")
        
        # 4. Write files
        written = self.write_files(files)
        
        print(f"\n✅ Task {task_key} automated successfully!")
        print(f"   Files created: {len(written)}")
        
        if not self.dry_run:
            print(f"\n📝 Next steps:")
            print(f"   1. Review generated code: git diff")
            print(f"   2. Run tests: pnpm test")
            print(f"   3. Fix any issues manually")
            print(f"   4. Commit: git add . && git commit -m 'feat: {task_spec['title']}'")
        
        return True


def main():
    parser = argparse.ArgumentParser(description='Task Automation Agent')
    parser.add_argument('task_key', nargs='?', help='Task key to automate (e.g., T24)')
    parser.add_argument('--auto', action='store_true', help='Auto-generate all HIGH AI tasks')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating files')
    parser.add_argument('--list', action='store_true', help='List all HIGH AI effectiveness tasks')
    
    args = parser.parse_args()
    
    agent = TaskAutomationAgent(dry_run=args.dry_run)
    
    if args.list:
        # List all HIGH AI tasks
        effort_map_path = Path('/workspaces/morpheus-press/planning/estimates/effort-map.yaml')
        with open(effort_map_path, 'r') as f:
            effort_map = yaml.safe_load(f)
        
        high_ai_tasks = [
            (key, data) for key, data in effort_map['estimates'].items()
            if 'AI Impact: HIGH' in data.get('reasoning', '')
        ]
        
        print(f"\n🤖 HIGH AI EFFECTIVENESS TASKS ({len(high_ai_tasks)} total):")
        print("="*80)
        
        for key, data in high_ai_tasks:
            print(f"\n{key}: {data['title']}")
            print(f"   Estimated: {data.get('estimated_days', 0)} days")
            pattern_hint = "setup" if "setup" in data['title'].lower() else \
                          "test" if "test" in data['title'].lower() else \
                          "api" if "api" in data['title'].lower() else "generic"
            print(f"   Pattern: {pattern_hint}")
        
        return
    
    if args.auto:
        # Auto-generate all HIGH AI tasks
        print("🚀 AUTO-GENERATING ALL HIGH AI TASKS")
        print("="*80)
        print("⚠️  This will generate code for 14+ tasks - may take 10-15 minutes")
        
        if not args.dry_run:
            response = input("Continue? (y/n): ")
            if response.lower() != 'y':
                return
        
        # Load all HIGH AI tasks
        effort_map_path = Path('/workspaces/morpheus-press/planning/estimates/effort-map.yaml')
        with open(effort_map_path, 'r') as f:
            effort_map = yaml.safe_load(f)
        
        high_ai_tasks = [
            key for key, data in effort_map['estimates'].items()
            if 'AI Impact: HIGH' in data.get('reasoning', '')
        ]
        
        print(f"\nFound {len(high_ai_tasks)} HIGH AI tasks to automate")
        
        success_count = 0
        for i, task_key in enumerate(high_ai_tasks, 1):
            print(f"\n[{i}/{len(high_ai_tasks)}] Processing {task_key}...")
            
            if agent.automate_task(task_key):
                success_count += 1
            else:
                print(f"⚠️  Skipped {task_key}")
        
        print(f"\n✅ Automation complete: {success_count}/{len(high_ai_tasks)} tasks successful")
        return
    
    if not args.task_key:
        parser.print_help()
        return
    
    # Single task automation
    agent.automate_task(args.task_key)


if __name__ == '__main__':
    main()
