#!/usr/bin/env python3
"""
Generate Vitest test files from test_scenarios.yaml

This script is called by GitHub Actions (copilot-branch-pipeline.yml) to automatically
generate test code from human-defined test scenarios in the planning phase.

Usage:
    python scripts/generate_tests_from_scenarios.py --scenarios test_scenarios.yaml --changed-files src/services/database.ts

Environment:
    OPENAI_API_KEY - Required for LLM test generation
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import openai

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    print("❌ Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

class TestGenerator:
    """Generate Vitest test files from YAML scenarios"""
    
    def __init__(self, scenarios_file: str, workspace_root: str = "/workspaces/morpheus"):
        self.scenarios_file = Path(scenarios_file)
        self.workspace_root = Path(workspace_root)
        self.scenarios: Dict[str, Any] = {}
        
    def load_scenarios(self) -> None:
        """Load test scenarios from YAML file"""
        if not self.scenarios_file.exists():
            raise FileNotFoundError(f"Scenarios file not found: {self.scenarios_file}")
        
        with open(self.scenarios_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if 'test_scenarios' not in data:
            raise ValueError("YAML must contain 'test_scenarios' key")
        
        self.scenarios = data['test_scenarios']
        print(f"✅ Loaded scenarios for:")
        print(f"   - Unit tests: {len(self.scenarios.get('unit', []))} components")
        print(f"   - Integration tests: {len(self.scenarios.get('integration', []))} components")
        print(f"   - E2E tests: {len(self.scenarios.get('e2e', []))} components")
    
    def match_scenarios_to_files(self, changed_files: List[str]) -> Dict[str, List[Dict]]:
        """Match changed files to their test scenarios"""
        matched = {}
        
        for file_path in changed_files:
            # Skip non-source files
            if not (file_path.endswith('.ts') or file_path.endswith('.tsx')):
                continue
            
            # Extract component name from file path
            # Example: apps/backend/src/services/database.ts -> DatabaseService
            file_name = Path(file_path).stem
            component_name = self._file_to_component_name(file_name, file_path)
            
            # Find matching scenarios
            matching_scenarios = []
            
            # Check unit tests
            for scenario in self.scenarios.get('unit', []):
                if self._component_matches(scenario['component'], component_name, file_path):
                    matching_scenarios.append({
                        'type': 'unit',
                        'scenario': scenario
                    })
            
            # Check integration tests
            for scenario in self.scenarios.get('integration', []):
                if self._component_matches(scenario['component'], component_name, file_path):
                    matching_scenarios.append({
                        'type': 'integration',
                        'scenario': scenario
                    })
            
            if matching_scenarios:
                matched[file_path] = matching_scenarios
                print(f"   📝 {file_path}: {len(matching_scenarios)} scenarios")
        
        return matched
    
    def _file_to_component_name(self, file_name: str, file_path: str) -> str:
        """Convert file name to likely component name"""
        # database.ts -> DatabaseService
        # chapter-analysis.ts -> ChapterAnalysisService
        # books.routes.ts -> Books API
        
        if 'routes' in file_path:
            return f"{file_name.replace('-', ' ').title()} API"
        elif 'services' in file_path:
            parts = file_name.split('-')
            return ''.join(p.capitalize() for p in parts) + 'Service'
        elif 'components' in file_path:
            parts = file_name.split('-')
            return ''.join(p.capitalize() for p in parts) + ' component'
        else:
            return file_name
    
    def _component_matches(self, scenario_component: str, component_name: str, file_path: str) -> bool:
        """Check if scenario component matches file"""
        # Direct match
        if component_name.lower() in scenario_component.lower():
            return True
        
        # File path match
        file_name = Path(file_path).stem
        if file_name.lower() in scenario_component.lower():
            return True
        
        # API route match
        if 'API Route' in scenario_component and 'routes' in file_path:
            # Extract route file name
            if file_name.replace('-', '') in scenario_component.lower().replace(' ', '').replace('/', ''):
                return True
        
        return False
    
    def generate_test_file(self, source_file: str, scenarios: List[Dict]) -> str:
        """Generate complete test file using OpenAI API"""
        # Read source code
        source_path = self.workspace_root / source_file
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Prepare scenarios text
        scenarios_text = self._format_scenarios_for_llm(scenarios)
        
        # Determine test file type
        is_route = 'routes' in source_file
        is_service = 'services' in source_file
        is_component = 'components' in source_file
        
        # Build prompt based on file type
        prompt = self._build_generation_prompt(
            source_code=source_code,
            source_file=source_file,
            scenarios_text=scenarios_text,
            is_route=is_route,
            is_service=is_service,
            is_component=is_component
        )
        
        print(f"   🤖 Generating tests for {source_file}...")
        print(f"      Using GPT-4o-mini (cost: ~$0.02)")
        
        # Call OpenAI API
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cheap for code generation
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert TypeScript/Vitest test engineer. Generate complete, production-ready test files that follow best practices: AAA pattern, proper mocking, descriptive names, comprehensive coverage."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Low temperature for consistent code
                max_tokens=4000
            )
            
            test_code = response.choices[0].message.content
            
            # Extract code from markdown if wrapped
            if '```typescript' in test_code:
                test_code = test_code.split('```typescript')[1].split('```')[0].strip()
            elif '```ts' in test_code:
                test_code = test_code.split('```ts')[1].split('```')[0].strip()
            
            # Calculate cost
            usage = response.usage
            cost = (usage.prompt_tokens * 0.00015 + usage.completion_tokens * 0.0006) / 1000
            print(f"      ✅ Generated {usage.completion_tokens} tokens (cost: ${cost:.4f})")
            
            return test_code
            
        except Exception as e:
            print(f"      ❌ Error generating tests: {e}")
            raise
    
    def _format_scenarios_for_llm(self, scenarios: List[Dict]) -> str:
        """Format scenarios into readable text for LLM"""
        formatted = []
        
        for item in scenarios:
            scenario_type = item['type']
            scenario = item['scenario']
            
            formatted.append(f"## {scenario_type.upper()} TEST: {scenario['component']}")
            formatted.append(f"Description: {scenario.get('description', 'N/A')}")
            formatted.append("")
            
            for test_case in scenario['test_cases']:
                formatted.append(f"### Test Case: {test_case['name']}")
                formatted.append(f"\n**Arrange:**\n{test_case['arrange']}")
                formatted.append(f"\n**Act:**\n{test_case['act']}")
                formatted.append(f"\n**Assert:**")
                for assertion in test_case['assert']:
                    formatted.append(f"  - {assertion}")
                formatted.append("")
        
        return "\n".join(formatted)
    
    def _build_generation_prompt(
        self,
        source_code: str,
        source_file: str,
        scenarios_text: str,
        is_route: bool,
        is_service: bool,
        is_component: bool
    ) -> str:
        """Build LLM prompt for test generation"""
        
        test_type = "route" if is_route else "service" if is_service else "component" if is_component else "utility"
        
        prompt = f"""Generate a complete Vitest test file for the following TypeScript {test_type}.

**Source File:** {source_file}

**Source Code:**
```typescript
{source_code[:3000]}  # Limit to avoid token overflow
```

**Test Scenarios (from planning phase):**
{scenarios_text}

**Requirements:**

1. **Follow AAA Pattern:** Arrange, Act, Assert for every test
2. **Mock External Dependencies:** Mock Supabase, OpenAI, RunPod, etc. using `vi.mock()`
3. **Test File Structure:**
   - Import required modules and types
   - Mock external dependencies at top
   - Use `describe()` blocks to group related tests
   - Use `beforeEach()` / `afterEach()` for setup/cleanup
   - Clear mocks after each test: `vi.clearAllMocks()`

4. **Mocking Patterns:**
   - Supabase: Mock `@supabase/supabase-js` with `createClient` returning mock methods
   - Services: Mock service classes with mock methods
   - LLM providers: Mock with predefined responses
   - Use `vi.fn()` for function mocks
   - Use `mockResolvedValue()` for async mocks

5. **Test Naming:** `it('should <expected behavior> when <condition>', ...)`

6. **Assertions:** Use specific matchers:
   - `expect(result).toEqual(expected)` for objects
   - `expect(fn).toHaveBeenCalledWith(arg)` for calls
   - `expect(result).toMatchObject({{...}})` for partial matches
   - `await expect(promise).rejects.toThrow('message')` for errors

7. **Implement ALL scenarios** from the planning phase above

"""

        if is_route:
            prompt += """
8. **Route Testing Specifics:**
   - Import Fastify app from `../app` or similar
   - Build app in `beforeEach()`
   - Close app in `afterEach()`
   - Use `app.inject()` for requests
   - Test status codes, response bodies, headers
   - Mock database/service layers
"""
        elif is_service:
            prompt += """
8. **Service Testing Specifics:**
   - Mock constructor dependencies
   - Test all public methods
   - Test error handling
   - Verify external API calls
   - Check edge cases (null, empty, invalid)
"""
        elif is_component:
            prompt += """
8. **Component Testing Specifics:**
   - Import `render, screen, fireEvent, waitFor` from '@testing-library/react'
   - Wrap in providers if needed (QueryClient, Router)
   - Test user interactions
   - Test async data loading
   - Test error states
"""
        
        prompt += """

**Output:** Complete TypeScript test file ready to run with Vitest. Include all imports, mocks, and test cases.

**CRITICAL:** Generate ONLY the test file code. No explanations, no markdown formatting (except code fences if needed).
"""
        
        return prompt
    
    def save_test_file(self, source_file: str, test_code: str) -> str:
        """Save generated test file to appropriate location"""
        source_path = Path(source_file)
        
        # Determine test file location
        if 'backend' in source_file:
            # apps/backend/src/services/database.ts -> apps/backend/src/__tests__/database.test.ts
            app_root = self.workspace_root / 'apps' / 'backend' / 'src'
            test_dir = app_root / '__tests__'
            
            # Preserve subdirectory structure
            if 'services' in source_file:
                test_dir = test_dir  # Flat structure for backend
            elif 'routes' in source_file:
                test_dir = test_dir / 'routes'
            
        elif 'dashboard' in source_file or 'storefront' in source_file:
            # apps/dashboard/components/BookCard.tsx -> apps/dashboard/__tests__/components/BookCard.test.tsx
            parts = source_path.parts
            app_idx = parts.index('dashboard') if 'dashboard' in parts else parts.index('storefront')
            app_root = Path(*parts[:app_idx+1])
            test_dir = self.workspace_root / app_root / '__tests__'
            
            # Preserve component subdirectory
            if 'components' in source_file:
                test_dir = test_dir / 'components'
        else:
            # Default: same directory with __tests__ subfolder
            test_dir = source_path.parent / '__tests__'
        
        # Create test directory
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate test file name
        test_file_name = source_path.stem + '.test.ts'
        if source_path.suffix == '.tsx':
            test_file_name = source_path.stem + '.test.tsx'
        
        test_file_path = test_dir / test_file_name
        
        # Save test file
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        print(f"   ✅ Saved: {test_file_path.relative_to(self.workspace_root)}")
        
        return str(test_file_path.relative_to(self.workspace_root))
    
    def generate_all(self, changed_files: List[str]) -> List[str]:
        """Generate test files for all changed files"""
        
        print("\n🔍 Matching scenarios to changed files...")
        matched = self.match_scenarios_to_files(changed_files)
        
        if not matched:
            print("⚠️  No scenarios matched to changed files")
            print("   This might be okay if changes are docs/config only")
            return []
        
        print(f"\n📝 Generating tests for {len(matched)} files...\n")
        
        generated_files = []
        total_cost = 0.0
        
        for source_file, scenarios in matched.items():
            try:
                test_code = self.generate_test_file(source_file, scenarios)
                test_file = self.save_test_file(source_file, test_code)
                generated_files.append(test_file)
                
            except Exception as e:
                print(f"   ❌ Failed to generate tests for {source_file}: {e}")
                continue
        
        print(f"\n✅ Generated {len(generated_files)} test files")
        print(f"   Estimated total cost: ${total_cost:.4f}")
        
        return generated_files


def main():
    parser = argparse.ArgumentParser(
        description='Generate Vitest tests from YAML scenarios'
    )
    parser.add_argument(
        '--scenarios',
        required=True,
        help='Path to test_scenarios.yaml file'
    )
    parser.add_argument(
        '--changed-files',
        required=True,
        help='Comma-separated list of changed files'
    )
    parser.add_argument(
        '--workspace',
        default='/workspaces/morpheus',
        help='Workspace root directory'
    )
    
    args = parser.parse_args()
    
    # Parse changed files
    changed_files = [f.strip() for f in args.changed_files.split(',')]
    
    print("=" * 60)
    print("🧪 Test Generation from Scenarios")
    print("=" * 60)
    print(f"Scenarios: {args.scenarios}")
    print(f"Changed files: {len(changed_files)}")
    print()
    
    # Run generation
    generator = TestGenerator(args.scenarios, args.workspace)
    
    try:
        generator.load_scenarios()
        generated_files = generator.generate_all(changed_files)
        
        if generated_files:
            print("\n📋 Summary:")
            for test_file in generated_files:
                print(f"   ✅ {test_file}")
            
            print("\n🎉 Test generation complete!")
            print("\nNext steps:")
            print("  1. Review generated tests")
            print("  2. Run tests: pnpm test")
            print("  3. Adjust if needed")
            sys.exit(0)
        else:
            print("\n⚠️  No tests generated")
            sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
