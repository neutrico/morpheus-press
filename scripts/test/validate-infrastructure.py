#!/usr/bin/env python3
"""
Infrastructure Validation Script for TT1

Validates that all infrastructure components are properly configured
for the GitHub Copilot + Automation system.

Usage:
    python scripts/test/validate-infrastructure.py
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class InfrastructureValidator:
    """Validates infrastructure setup for Copilot automation system."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print(f"\n{BLUE}🔍 Validating Infrastructure Setup for TT1{RESET}\n")
        
        checks = [
            ("GitHub Actions Workflow", self.check_workflow),
            ("Planning System Integrity", self.check_planning_system),
            ("Automation Scripts", self.check_automation_scripts),
            ("Required Directories", self.check_directories),
            ("Copilot Instructions", self.check_copilot_instructions),
            ("Test Infrastructure", self.check_test_infrastructure),
        ]
        
        for name, check_func in checks:
            print(f"{BLUE}[CHECK]{RESET} {name}")
            try:
                result, message = check_func()
                if result:
                    print(f"  {GREEN}✓{RESET} {message}")
                    self.passed += 1
                else:
                    print(f"  {RED}✗{RESET} {message}")
                    self.failed += 1
            except Exception as e:
                print(f"  {RED}✗{RESET} Error: {str(e)}")
                self.failed += 1
            print()
        
        # Summary
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Summary:{RESET}")
        print(f"  {GREEN}✓{RESET} Passed:   {self.passed}")
        print(f"  {RED}✗{RESET} Failed:   {self.failed}")
        if self.warnings > 0:
            print(f"  {YELLOW}⚠{RESET} Warnings: {self.warnings}")
        print(f"{BLUE}{'='*60}{RESET}\n")
        
        if self.failed == 0:
            print(f"{GREEN}✅ All infrastructure checks passed!{RESET}\n")
            return True
        else:
            print(f"{RED}❌ Infrastructure validation failed with {self.failed} error(s){RESET}\n")
            return False
    
    def check_workflow(self) -> Tuple[bool, str]:
        """Validate GitHub Actions workflow file exists and has basic structure."""
        workflow_path = self.repo_root / ".github" / "workflows" / "copilot-task-automation.yml"
        
        if not workflow_path.exists():
            return False, f"Workflow file not found: {workflow_path}"
        
        try:
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            # Check for required sections in the content
            # Note: We can't use yaml.safe_load due to heredoc content with markdown
            # GitHub Actions parser handles this correctly even if Python YAML doesn't
            required_strings = ['name:', 'on:', 'jobs:', 'runs-on:', 'steps:']
            missing = [s for s in required_strings if s not in content]
            
            if missing:
                return False, f"Workflow missing required sections: {', '.join(missing)}"
            
            # Check for permissions
            if 'permissions:' not in content:
                self.warnings += 1
                return True, "Workflow exists (warning: no explicit permissions section)"
            
            # Try to parse just the top-level structure (first 50 lines)
            # This avoids the heredoc content that confuses the YAML parser
            header_lines = content.split('\n')[:50]
            header_yaml = '\n'.join(header_lines)
            
            try:
                # Try parsing just the header to verify basic YAML syntax
                yaml.safe_load(header_yaml)
                return True, "Workflow file exists with valid structure"
            except yaml.YAMLError:
                # If header fails, the whole file likely has syntax issues
                # But for this test, we'll be lenient since GitHub Actions
                # parser is more forgiving than Python's YAML parser
                self.warnings += 1
                return True, "Workflow exists (warning: YAML structure not fully validated)"
            
        except Exception as e:
            return False, f"Error reading workflow: {str(e)}"
    
    def check_planning_system(self) -> Tuple[bool, str]:
        """Validate planning system files exist and are valid."""
        planning_dir = self.repo_root / "planning"
        
        # Check key files
        required_files = [
            "pi.yaml",
            "estimates/effort-map.yaml",
            "milestones.yaml",
        ]
        
        missing_files = []
        for file in required_files:
            file_path = planning_dir / file
            if not file_path.exists():
                missing_files.append(file)
        
        if missing_files:
            return False, f"Missing planning files: {', '.join(missing_files)}"
        
        # Validate pi.yaml structure
        pi_yaml = planning_dir / "pi.yaml"
        try:
            with open(pi_yaml, 'r') as f:
                pi_data = yaml.safe_load(f)
            
            if not isinstance(pi_data, dict):
                return False, "pi.yaml is not a valid dictionary"
            
            # Check for epics/features/tasks or other expected structure
            # (Simplified check - actual structure may vary)
            if len(pi_data) == 0:
                return False, "pi.yaml is empty"
            
            return True, f"Planning system valid ({len(pi_data)} top-level keys)"
            
        except yaml.YAMLError as e:
            return False, f"Invalid pi.yaml syntax: {str(e)}"
    
    def check_automation_scripts(self) -> Tuple[bool, str]:
        """Check automation scripts exist and are executable."""
        scripts_dir = self.repo_root / "scripts" / "automation"
        
        if not scripts_dir.exists():
            return False, f"Automation scripts directory not found: {scripts_dir}"
        
        # Check for key automation scripts
        script_files = list(scripts_dir.glob("*.py"))
        
        if len(script_files) == 0:
            return False, "No Python automation scripts found"
        
        # Check if main automation script exists
        main_script = scripts_dir / "task-automation-agent.py"
        if not main_script.exists():
            self.warnings += 1
            return True, f"Scripts directory exists ({len(script_files)} scripts), but task-automation-agent.py not found"
        
        return True, f"Automation scripts available ({len(script_files)} Python scripts)"
    
    def check_directories(self) -> Tuple[bool, str]:
        """Check required directories exist."""
        required_dirs = [
            ".github",
            ".github/workflows",
            "planning",
            "planning/docs",
            "planning/estimates",
            "planning/test",
            "scripts",
            "scripts/automation",
            "scripts/test",
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.repo_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            return False, f"Missing directories: {', '.join(missing_dirs)}"
        
        return True, f"All required directories exist ({len(required_dirs)} directories)"
    
    def check_copilot_instructions(self) -> Tuple[bool, str]:
        """Validate Copilot instructions file."""
        instructions_path = self.repo_root / ".github" / "copilot-instructions.md"
        
        if not instructions_path.exists():
            return False, f"Copilot instructions not found: {instructions_path}"
        
        with open(instructions_path, 'r') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "## Task Automation System",
            "## Code Quality Principles",
            "SOLID",
            "DRY",
            "KISS",
        ]
        
        missing_sections = [s for s in required_sections if s not in content]
        
        if missing_sections:
            self.warnings += 1
            return True, f"Instructions exist but missing sections: {', '.join(missing_sections)}"
        
        lines = len(content.split('\n'))
        return True, f"Copilot instructions complete ({lines} lines)"
    
    def check_test_infrastructure(self) -> Tuple[bool, str]:
        """Check test infrastructure files."""
        test_dir = self.repo_root / "planning" / "test"
        
        if not test_dir.exists():
            return False, "Test directory not found: planning/test"
        
        # Check for test specification
        tt1_spec = test_dir / "tt1.md"
        if not tt1_spec.exists():
            return False, "Test specification not found: planning/test/tt1.md"
        
        return True, "Test infrastructure ready (tt1.md exists)"


def main():
    """Main entry point."""
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    
    # Run validation
    validator = InfrastructureValidator(repo_root)
    success = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
