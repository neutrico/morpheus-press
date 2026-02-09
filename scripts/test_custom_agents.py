#!/usr/bin/env python3
"""
Test custom agent selection logic.
"""

from copilot_agent import select_custom_agent

# Test cases
test_cases = [
    {
        "name": "Backend API task",
        "task_data": {
            "task": "Implement Fastify API routes",
            "labels": ["backend", "api"],
            "description": "Create REST API endpoints with Supabase RLS",
        },
        "expected": "backend-specialist",
    },
    {
        "name": "Testing task",
        "task_data": {
            "task": "Add unit tests for services",
            "labels": ["testing", "vitest"],
            "description": "Write comprehensive test coverage",
        },
        "expected": "testing-specialist",
    },
    {
        "name": "Backend in description",
        "task_data": {
            "task": "Setup database",
            "labels": ["infrastructure"],
            "description": "Configure Supabase with RLS policies",
        },
        "expected": "backend-specialist",
    },
    {
        "name": "Frontend task (no agent)",
        "task_data": {
            "task": "Build dashboard UI",
            "labels": ["frontend", "react"],
            "description": "Create React components with shadcn/ui",
        },
        "expected": None,
    },
    {
        "name": "Documentation task (no agent)",
        "task_data": {
            "task": "Write API documentation",
            "labels": ["documentation"],
            "description": "Document REST endpoints",
        },
        "expected": None,
    },
]

print("🧪 Testing Custom Agent Selection\n")
print("=" * 60)

passed = 0
failed = 0

for test in test_cases:
    result = select_custom_agent(test["task_data"])
    expected = test["expected"]
    
    if result == expected:
        print(f"✅ {test['name']}")
        print(f"   Agent: {result or 'default'}")
        passed += 1
    else:
        print(f"❌ {test['name']}")
        print(f"   Expected: {expected or 'default'}")
        print(f"   Got: {result or 'default'}")
        failed += 1
    print()

print("=" * 60)
print(f"\n📊 Results: {passed} passed, {failed} failed")

if failed == 0:
    print("✅ All tests passed!")
    exit(0)
else:
    print("❌ Some tests failed")
    exit(1)
