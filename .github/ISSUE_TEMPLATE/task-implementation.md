---
name: Task Implementation (from Planning)
about: Implementation task from planning/docs/ with automation support
title: "[TASK_KEY]: Task Title"
labels: ["task", "from-planning"]
assignees: []
---

## 📋 Task Information

**Task Key:** T[XX]\
**Milestone:** M[X] - [Milestone Name]\
**Estimated Days (AI-aware):** [X.X] days\
**AI Effectiveness:** [HIGH/MEDIUM/LOW]

## 📚 Specification

**Location:** `planning/docs/[milestone]/[task-key]-*.md`

**Brief Description:** [One sentence description of what needs to be
implemented]

## ✅ Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 🤖 Automation Available

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

- [ ] Automation available for this task type
- [ ] Auto-generation triggered (comment `/automate`)
- [ ] PR created with generated code
- [ ] Code reviewed and refined

## 🔧 Implementation Notes

**Related Files:**

- Spec: `planning/docs/[milestone]/[task-key]-*.md`
- Research: `planning/issues/*.yaml` (search for task key)
- Estimate: `planning/estimates/effort-map.yaml` (task key)

**Dependencies:**

- [ ] Task 1 (if any)
- [ ] Task 2 (if any)

## 🧪 Testing

- [ ] Unit tests passing (`pnpm test`)
- [ ] Integration tests (if applicable)
- [ ] Manual testing completed
- [ ] Edge cases covered

## 📝 Implementation Checklist

- [ ] Read task specification from `planning/docs/`
- [ ] Check for auto-generated PR (if HIGH AI effectiveness)
- [ ] Implement or refine generated code
- [ ] Add/fix TODO comments
- [ ] Write/update tests
- [ ] Run `pnpm test` and verify passing
- [ ] Update documentation if needed
- [ ] Request review

---

**🤖 Automation Trigger:** Comment `/automate` to trigger code generation (HIGH
AI tasks only)

**📖 Documentation:** See
[Task Automation README](../scripts/automation/README.md)
