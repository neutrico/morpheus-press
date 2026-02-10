#!/usr/bin/env python3
"""
TT2 Test Validation Script

Validates GitHub GraphQL API integration for Copilot assignment.
Tests connectivity, authentication, and mutation execution.

Usage:
    python scripts/test/validate-tt2.py --check-connectivity
    python scripts/test/validate-tt2.py --test-assignment ISSUE_ID
    python scripts/test/validate-tt2.py --full-test
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional
import json

try:
    from gql import gql, Client
    from gql.transport.requests import RequestsHTTPTransport
    from gql.transport.exceptions import TransportQueryError
except ImportError:
    print("⚠️  Error: gql library not installed")
    print("Install with: pip install 'gql[requests]'")
    sys.exit(1)


class GitHubAPITester:
    """Test GitHub GraphQL API for Copilot integration."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with GitHub token."""
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var.")
        
        self.transport = RequestsHTTPTransport(
            url="https://api.github.com/graphql",
            headers={"Authorization": f"Bearer {self.token}"},
            verify=True,
            retries=3,
        )
        
        self.client = None
    
    def connect(self) -> bool:
        """Test API connectivity."""
        try:
            print("🔌 Testing GitHub API connectivity...")
            self.client = Client(
                transport=self.transport,
                fetch_schema_from_transport=False
            )
            
            # Simple viewer query
            query = gql("""
                query {
                  viewer {
                    login
                    name
                  }
                  rateLimit {
                    limit
                    cost
                    remaining
                    resetAt
                  }
                }
            """)
            
            result = self.client.execute(query)
            
            print(f"✅ Connected as: {result['viewer']['login']}")
            print(f"   Name: {result['viewer']['name']}")
            print(f"   Rate Limit: {result['rateLimit']['remaining']}/{result['rateLimit']['limit']}")
            print(f"   Reset At: {result['rateLimit']['resetAt']}")
            
            return True
            
        except TransportQueryError as e:
            print(f"❌ GraphQL Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return False
    
    def get_issue_info(self, owner: str, repo: str, issue_number: int) -> Optional[Dict[str, Any]]:
        """Get issue information."""
        try:
            print(f"\n📋 Getting issue info: {owner}/{repo}#{issue_number}...")
            
            query = gql("""
                query($owner: String!, $repo: String!, $number: Int!) {
                  repository(owner: $owner, name: $repo) {
                    issue(number: $number) {
                      id
                      number
                      title
                      state
                      assignees(first: 10) {
                        nodes {
                          login
                        }
                      }
                    }
                  }
                }
            """)
            
            result = self.client.execute(query, variable_values={
                "owner": owner,
                "repo": repo,
                "number": issue_number
            })
            
            issue = result["repository"]["issue"]
            
            print(f"✅ Found issue:")
            print(f"   ID: {issue['id']}")
            print(f"   Title: {issue['title']}")
            print(f"   State: {issue['state']}")
            print(f"   Assignees: {[a['login'] for a in issue['assignees']['nodes']]}")
            
            return issue
            
        except TransportQueryError as e:
            print(f"❌ GraphQL Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def test_copilot_assignment(self, issue_id: str, dry_run: bool = True) -> bool:
        """Test Copilot assignment mutation."""
        try:
            print(f"\n🤖 Testing Copilot assignment (dry_run={dry_run})...")
            
            # Generate sample instructions
            instructions = self._generate_test_instructions()
            
            if dry_run:
                print("📝 Mutation that would be executed:")
                print(json.dumps({
                    "mutation": "addAssigneesToAssignable",
                    "variables": {
                        "issueId": issue_id,
                        "assigneeIds": ["copilot"],
                        "instructions": instructions[:100] + "..."
                    }
                }, indent=2))
                print("\n✅ Dry run successful (no mutation executed)")
                return True
            
            # Execute actual mutation
            mutation = gql("""
                mutation AssignCopilot($issueId: ID!, $instructions: String!) {
                  addAssigneesToAssignable(
                    input: {
                      assignableId: $issueId
                      assigneeIds: ["copilot"]
                      agentAssignment: {
                        instructions: $instructions
                      }
                    }
                  ) {
                    assignable {
                      ... on Issue {
                        id
                        number
                        assignees(first: 10) {
                          nodes {
                            login
                          }
                        }
                      }
                    }
                  }
                }
            """)
            
            result = self.client.execute(mutation, variable_values={
                "issueId": issue_id,
                "instructions": instructions
            })
            
            assignable = result["addAssigneesToAssignable"]["assignable"]
            assignees = [a["login"] for a in assignable["assignees"]["nodes"]]
            
            print(f"✅ Assignment successful!")
            print(f"   Issue #{assignable['number']}")
            print(f"   Assignees: {assignees}")
            
            if "copilot" in assignees:
                print("   ✅ Copilot successfully assigned!")
                return True
            else:
                print("   ⚠️  Copilot not in assignee list")
                return False
            
        except TransportQueryError as e:
            print(f"❌ GraphQL Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _generate_test_instructions(self) -> str:
        """Generate sample instructions for testing."""
        return """# Task: TT2 - Backend Core API Test

## Context
This is a test task to validate GitHub Issues + Projects v2 integration
with Copilot agent assignment workflow.

## Technical Requirements
- Priority: P1
- AI Effectiveness: HIGH
- Estimated Effort: 2 days

## Implementation Approach
1. Create test specification documents
2. Validate GraphQL API integration
3. Test automation pipeline
4. Document findings

## Quality Standards
- Follow SOLID, DRY, KISS principles
- Create comprehensive documentation
- Use existing repository patterns

## Expected Files
- planning/test/tt2.md
- planning/test/tt2-test-config.yaml
- planning/test/tt2-results.md
- docs/GITHUB_COPILOT_INTEGRATION.md
"""


def main():
    """Main test execution."""
    parser = argparse.ArgumentParser(description="TT2 Test Validation")
    parser.add_argument("--check-connectivity", action="store_true",
                        help="Test GitHub API connectivity")
    parser.add_argument("--get-issue", metavar="NUMBER", type=int,
                        help="Get issue information")
    parser.add_argument("--test-assignment", metavar="ISSUE_ID",
                        help="Test Copilot assignment (dry run)")
    parser.add_argument("--assign", metavar="ISSUE_ID",
                        help="Actually assign Copilot (LIVE)")
    parser.add_argument("--owner", default="neutrico",
                        help="Repository owner (default: neutrico)")
    parser.add_argument("--repo", default="morpheus-press",
                        help="Repository name (default: morpheus-press)")
    parser.add_argument("--full-test", action="store_true",
                        help="Run all tests")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("TT2 Test Validation - GitHub Copilot Integration")
    print("=" * 70)
    
    try:
        tester = GitHubAPITester()
        
        if args.check_connectivity or args.full_test:
            if not tester.connect():
                print("\n❌ Connectivity test failed")
                sys.exit(1)
        
        if args.get_issue:
            issue = tester.get_issue_info(args.owner, args.repo, args.get_issue)
            if not issue:
                print("\n❌ Could not get issue info")
                sys.exit(1)
        
        if args.test_assignment:
            success = tester.test_copilot_assignment(args.test_assignment, dry_run=True)
            if not success:
                print("\n❌ Assignment test failed")
                sys.exit(1)
        
        if args.assign:
            print("\n⚠️  WARNING: This will actually assign Copilot to the issue!")
            confirm = input("Continue? (yes/no): ")
            if confirm.lower() == "yes":
                success = tester.test_copilot_assignment(args.assign, dry_run=False)
                if not success:
                    print("\n❌ Assignment failed")
                    sys.exit(1)
            else:
                print("Cancelled.")
        
        if args.full_test:
            print("\n" + "=" * 70)
            print("✅ All tests completed!")
            print("=" * 70)
        
        if not any([args.check_connectivity, args.get_issue, 
                    args.test_assignment, args.assign, args.full_test]):
            parser.print_help()
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
