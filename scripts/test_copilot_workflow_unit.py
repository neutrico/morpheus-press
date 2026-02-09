#!/usr/bin/env python3
"""
Unit tests for TEST172 Copilot workflow functions.

Tests the individual components without requiring GitHub API access.
Can be run in CI/CD environments without authentication.

Usage:
  python3 scripts/test_copilot_workflow_unit.py
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from copilot_agent import (
    generate_copilot_instructions,
    find_first_ready_task,
)


class TestGenerateCopilotInstructions(unittest.TestCase):
    """Test custom instruction generation."""
    
    def test_basic_instructions(self):
        """Test basic instruction generation without agent notes."""
        task_data = {
            "task": "Test Task",
            "description": "This is a test description",
            "priority": "p1",
            "effort": 3,
            "ai_effectiveness": "high",
        }
        
        instructions = generate_copilot_instructions("TEST172", task_data)
        
        # Verify basic structure
        self.assertIn("# TEST172: Test Task", instructions)
        self.assertIn("This is a test description", instructions)
        self.assertIn("Priority: p1", instructions)
        self.assertIn("Effort: 3 points", instructions)
        self.assertIn("AI Effectiveness: high", instructions)
        
        # Verify quality standards
        self.assertIn("SOLID, DRY, KISS", instructions)
        self.assertIn("Vitest", instructions)
        self.assertIn("TypeScript strict mode", instructions)
    
    def test_instructions_with_research_findings(self):
        """Test instruction generation with research findings."""
        task_data = {
            "task": "Database Setup",
            "priority": "p0",
            "effort": 5,
            "ai_effectiveness": "high",
            "agent_notes": {
                "research_findings": "Use PostgreSQL with RLS policies for security",
            }
        }
        
        instructions = generate_copilot_instructions("T24", task_data)
        
        self.assertIn("Research Findings", instructions)
        self.assertIn("PostgreSQL with RLS", instructions)
    
    def test_instructions_with_implementation_approach(self):
        """Test instruction generation with implementation approach."""
        task_data = {
            "task": "API Routes",
            "priority": "p1",
            "effort": 3,
            "ai_effectiveness": "high",
            "agent_notes": {
                "implementation_approach": "Create RESTful endpoints with Zod validation",
            }
        }
        
        instructions = generate_copilot_instructions("T25", task_data)
        
        self.assertIn("Implementation Approach", instructions)
        self.assertIn("RESTful endpoints", instructions)
    
    def test_instructions_with_design_decisions(self):
        """Test instruction generation with design decisions."""
        task_data = {
            "task": "LLM Integration",
            "priority": "p1",
            "effort": 5,
            "ai_effectiveness": "high",
            "agent_notes": {
                "design_decisions": [
                    {
                        "decision": "Use factory pattern",
                        "rationale": "Supports multiple LLM providers"
                    },
                    {
                        "decision": "Abstract API calls",
                        "rationale": "Easy to swap providers"
                    }
                ]
            }
        }
        
        instructions = generate_copilot_instructions("T26", task_data)
        
        self.assertIn("Key Design Decisions", instructions)
        self.assertIn("Use factory pattern", instructions)
        self.assertIn("Supports multiple LLM providers", instructions)
    
    def test_instructions_truncate_long_research(self):
        """Test that long research findings are truncated."""
        long_text = "A" * 600  # Longer than 500 char limit
        
        task_data = {
            "task": "Test",
            "priority": "p2",
            "effort": 2,
            "ai_effectiveness": "medium",
            "agent_notes": {
                "research_findings": long_text,
            }
        }
        
        instructions = generate_copilot_instructions("T1", task_data)
        
        # Should be truncated with "..."
        self.assertIn("...", instructions)
        # Full text should not be present
        self.assertNotIn("A" * 600, instructions)
    
    def test_instructions_format(self):
        """Test that instructions are well-formatted markdown."""
        task_data = {
            "task": "Test Formatting",
            "priority": "p2",
            "effort": 1,
            "ai_effectiveness": "medium",
        }
        
        instructions = generate_copilot_instructions("T999", task_data)
        
        # Check for proper markdown structure
        lines = instructions.split("\n")
        
        # First line should be title
        self.assertTrue(lines[0].startswith("# T999:"))
        
        # Should have section headers
        self.assertTrue(any("## Technical Requirements" in line for line in lines))
        self.assertTrue(any("## Quality Standards" in line for line in lines))


class TestFindFirstReadyTask(unittest.TestCase):
    """Test task selection logic."""
    
    def test_find_task_with_no_dependencies(self):
        """Test finding task with no dependencies."""
        tasks = [
            ("T1", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
            ("T2", {
                "dependencies": ["T1"],
                "milestone": "M0",
                "priority": "p1",
                "effort": 2,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"T1": 100, "T2": 101}
        created_node_ids = {"T1": "id1", "T2": "id2"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, issue_num, node_id = result
        self.assertEqual(task_key, "T1")
        self.assertEqual(issue_num, 100)
        self.assertEqual(node_id, "id1")
    
    def test_find_task_prefers_m0(self):
        """Test that M0 tasks are preferred."""
        tasks = [
            ("T1", {
                "dependencies": [],
                "milestone": "M1",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
            ("T2", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"T1": 100, "T2": 101}
        created_node_ids = {"T1": "id1", "T2": "id2"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, _, _ = result
        self.assertEqual(task_key, "T2")  # M0 task preferred
    
    def test_find_task_prefers_high_ai_effectiveness(self):
        """Test that high AI effectiveness tasks are preferred."""
        tasks = [
            ("T1", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "low"
            }),
            ("T2", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"T1": 100, "T2": 101}
        created_node_ids = {"T1": "id1", "T2": "id2"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, _, _ = result
        self.assertEqual(task_key, "T2")  # High AI effectiveness preferred
    
    def test_find_task_skips_uncreated_issues(self):
        """Test that uncreated tasks are skipped."""
        tasks = [
            ("T1", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
            ("T2", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 2,
                "ai_effectiveness": "high"
            }),
        ]
        
        # T1 not created yet
        created_issues = {"T2": 101}
        created_node_ids = {"T2": "id2"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, _, _ = result
        self.assertEqual(task_key, "T2")  # Only created task
    
    def test_find_task_returns_none_when_all_blocked(self):
        """Test that None is returned when all tasks have dependencies."""
        tasks = [
            ("T1", {
                "dependencies": ["T0"],  # Blocked
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"T1": 100}
        created_node_ids = {"T1": "id1"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNone(result)
    
    def test_find_task_sorts_by_priority(self):
        """Test that tasks are sorted by priority."""
        tasks = [
            ("T1", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p2",
                "effort": 1,
                "ai_effectiveness": "high"
            }),
            ("T2", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p0",
                "effort": 5,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"T1": 100, "T2": 101}
        created_node_ids = {"T1": "id1", "T2": "id2"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, _, _ = result
        self.assertEqual(task_key, "T2")  # p0 priority preferred over p2


class TestWorkflowIntegration(unittest.TestCase):
    """Integration tests for workflow components."""
    
    def test_complete_workflow_data_flow(self):
        """Test that data flows correctly through workflow functions."""
        # Step 1: Generate instructions
        task_data = {
            "task": "TEST172 Workflow",
            "description": "Complete workflow test",
            "priority": "p1",
            "effort": 3,
            "ai_effectiveness": "high",
            "agent_notes": {
                "research_findings": "Test findings",
                "implementation_approach": "Test approach",
                "design_decisions": [
                    {"decision": "Test decision", "rationale": "Test rationale"}
                ]
            }
        }
        
        instructions = generate_copilot_instructions("TEST172", task_data)
        
        # Verify instructions contain all components
        self.assertIn("TEST172", instructions)
        self.assertIn("Complete workflow test", instructions)
        self.assertIn("Test findings", instructions)
        self.assertIn("Test approach", instructions)
        self.assertIn("Test decision", instructions)
        
        # Step 2: Find ready task
        tasks = [
            ("TEST172", {
                "dependencies": [],
                "milestone": "M0",
                "priority": "p1",
                "effort": 3,
                "ai_effectiveness": "high"
            }),
        ]
        
        created_issues = {"TEST172": 172}
        created_node_ids = {"TEST172": "I_kwDOTest172"}
        
        result = find_first_ready_task(tasks, created_issues, created_node_ids)
        
        self.assertIsNotNone(result)
        task_key, issue_num, node_id = result
        
        self.assertEqual(task_key, "TEST172")
        self.assertEqual(issue_num, 172)
        self.assertEqual(node_id, "I_kwDOTest172")


def run_tests():
    """Run all unit tests."""
    print("=" * 80)
    print("TEST172: Unit Tests for Copilot Workflow Components")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateCopilotInstructions))
    suite.addTests(loader.loadTestsFromTestCase(TestFindFirstReadyTask))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All unit tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
