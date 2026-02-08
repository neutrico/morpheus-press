#!/bin/bash
# Test Suite Generator
# Usage: ./setup-tests.sh [task_key] [test_type]
# Example: ./setup-tests.sh T27 unit
# Test types: unit, integration, e2e

set -e

TASK_KEY=${1:-"T27"}
TEST_TYPE=${2:-"unit"}
WORKSPACE_ROOT="/workspaces/morpheus"

echo "🧪 Test Suite Generator for $TASK_KEY"
echo "======================================"
echo "Test type: $TEST_TYPE"

# 1. Determine test directory based on type
case $TEST_TYPE in
    unit)
        TEST_DIR="$WORKSPACE_ROOT/apps/backend/src/__tests__"
        ;;
    integration)
        TEST_DIR="$WORKSPACE_ROOT/apps/backend/src/__tests__/integration"
        ;;
    e2e)
        TEST_DIR="$WORKSPACE_ROOT/apps/dashboard/e2e"
        ;;
    *)
        echo "❌ Unknown test type: $TEST_TYPE"
        exit 1
        ;;
esac

mkdir -p "$TEST_DIR"

# 2. Read task spec
DOCS_DIR="$WORKSPACE_ROOT/planning/docs"
TASK_DOC=$(find "$DOCS_DIR" -name "${TASK_KEY}-*.md" | head -1)

if [ -z "$TASK_DOC" ]; then
    echo "⚠️  Task documentation not found - using generic template"
    TASK_TITLE="Generated Test Suite"
else
    echo "✅ Found task doc: $(basename "$TASK_DOC")"
    TASK_TITLE=$(basename "$TASK_DOC" .md | sed 's/^[^-]*-//')
fi

# 3. Generate test file
TEST_FILENAME="${TASK_KEY}-${TASK_TITLE,,}.test.ts"
TEST_FILENAME=$(echo "$TEST_FILENAME" | tr ' ' '-')
TEST_FILE="$TEST_DIR/$TEST_FILENAME"

echo ""
echo "📝 Generating test file: $TEST_FILENAME"

if [ "$TEST_TYPE" == "unit" ]; then
cat > "$TEST_FILE" << 'EOF'
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

/**
 * Test Suite: ${TASK_TITLE}
 * Task: ${TASK_KEY}
 * Generated: $(date -Iseconds)
 */

describe('${TASK_TITLE}', () => {
  // Setup & Teardown
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Cleanup
  });

  describe('Happy Path', () => {
    it('should handle basic scenario', async () => {
      // Arrange
      const input = 'test';
      
      // Act
      const result = input.toUpperCase();
      
      // Assert
      expect(result).toBe('TEST');
    });

    it('should handle edge cases', async () => {
      // Arrange
      const input = '';
      
      // Act
      const result = input.toUpperCase();
      
      // Assert
      expect(result).toBe('');
    });
  });

  describe('Error Handling', () => {
    it('should throw on invalid input', async () => {
      // Arrange
      const input = null;
      
      // Act & Assert
      expect(() => {
        if (input === null) throw new Error('Invalid input');
      }).toThrow('Invalid input');
    });

    it('should handle async errors gracefully', async () => {
      // Arrange
      const errorMessage = 'Network error';
      
      // Act & Assert
      await expect(
        Promise.reject(new Error(errorMessage))
      ).rejects.toThrow(errorMessage);
    });
  });

  describe('Integration', () => {
    it('should work with dependencies', async () => {
      // Test integration with other services/modules
      expect(true).toBe(true);
    });
  });

  describe('Performance', () => {
    it('should complete within reasonable time', async () => {
      // Arrange
      const startTime = Date.now();
      
      // Act
      await new Promise(resolve => setTimeout(resolve, 10));
      
      // Assert
      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(100); // 100ms max
    });
  });
});
EOF
elif [ "$TEST_TYPE" == "e2e" ]; then
cat > "$TEST_FILE" << 'EOF'
import { test, expect } from '@playwright/test';

/**
 * E2E Test Suite: ${TASK_TITLE}
 * Task: ${TASK_KEY}
 * Generated: $(date -Iseconds)
 */

test.describe('${TASK_TITLE} - E2E', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the page
    await page.goto('/');
  });

  test('should load the page', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Morpheus/);
  });

  test('should display main content', async ({ page }) => {
    // Check for critical elements
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();
  });

  test('should handle user interaction', async ({ page }) => {
    // Click button
    await page.click('button[data-testid="example-button"]');
    
    // Verify result
    const result = page.locator('[data-testid="result"]');
    await expect(result).toHaveText('Success');
  });

  test('should be accessible', async ({ page }) => {
    // Check ARIA labels
    const mainContent = page.locator('main');
    await expect(mainContent).toHaveAttribute('role', 'main');
  });
});
EOF
fi

echo "✅ Generated test file: $TEST_FILE"

# 4. Generate test fixtures if needed
FIXTURES_DIR="$TEST_DIR/__fixtures__"
mkdir -p "$FIXTURES_DIR"

FIXTURE_FILE="$FIXTURES_DIR/${TASK_KEY}-fixtures.ts"

cat > "$FIXTURE_FILE" << 'EOF'
/**
 * Test Fixtures for ${TASK_TITLE}
 * Task: ${TASK_KEY}
 */

export const mockData = {
  validInput: {
    id: '123e4567-e89b-12d3-a456-426614174000',
    name: 'Test Item',
    createdAt: new Date('2026-01-01'),
  },
  invalidInput: {
    id: null,
    name: '',
  },
};

export const mockResponses = {
  success: {
    status: 200,
    data: { message: 'Success' },
  },
  error: {
    status: 500,
    error: 'Internal Server Error',
  },
};
EOF

echo "✅ Generated fixtures: $FIXTURE_FILE"

# 5. Update test runner config if needed
echo ""
echo "📝 Next steps:"
echo "   1. Review test file: $TEST_FILE"
echo "   2. Add actual test cases based on acceptance criteria"
echo "   3. Run tests: pnpm test (unit) or pnpm test:e2e (e2e)"
echo "   4. Check coverage: pnpm test:coverage"
echo ""
echo "✅ Test setup complete for $TASK_KEY!"
