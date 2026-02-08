# Effort Re-estimation Workflow for Agents

## Problem Statement

Currently, all **333 story points** are based on **preliminary estimates** created before detailed research/planning. This creates risk of:

- ❌ Underestimating complex tasks (scope creep after research)
- ❌ Overestimating simple tasks (wasted capacity)
- ❌ No validation of initial estimates
- ❌ Planning based on inaccurate data

## Solution: Agent-Driven Re-estimation

### Workflow Overview

```
Initial Estimate → Research Agent → Planning Agent → Validated Effort
   (preliminary)    (adjust ±1-2)     (final check)     (production)
```

---

## Phase 1: Research Agent Re-estimation

**Trigger:** After completing `agent_notes.research_findings`

**Process:**

1. **Compare Initial Assumptions vs Research Findings**
   ```yaml
   # Initial estimate: effort: 3 (simple 1-2 days)
   
   # After research, discovered:
   # - Need to integrate 3rd-party API (not mentioned)
   # - No existing library, must implement from scratch
   # - Complex authentication flow
   # → Reality: 5-day task, not 2-day
   ```

2. **Adjust Effort If Scope Changed**
   
   **When to INCREASE effort (+1 to +3 points):**
   - Hidden complexity discovered
   - New dependencies identified
   - Technical debt must be addressed first
   - Regulatory/security requirements added
   - No reusable code found
   
   **When to DECREASE effort (-1 to -2 points):**
   - Existing library/component found
   - Similar implementation exists in codebase
   - Simpler approach identified
   - Requirements clarified and reduced

3. **Document Justification**
   ```yaml
   agent_notes:
     research_findings: |
       Investigated OAuth2 integration options...
     
     effort_adjustment:
       original_effort: 3
       adjusted_effort: 5
       reason: |
         Initial estimate assumed existing OAuth library.
         Research shows we need custom implementation:
         - Custom token refresh logic (1 day)
         - Rate limiting middleware (0.5 day)
         - Error handling for 5 providers (1 day)
         - Integration tests (0.5 day)
       confidence: medium  # low | medium | high
   ```

4. **Update Task Fields**
   ```yaml
   key: T42
   title: OAuth2 Provider Integration
   effort: 5  # Changed from 3
   ```

---

## Phase 2: Planning Agent Validation

**Trigger:** After completing `acceptance_criteria` and `estimates`

**Process:**

1. **Cross-Check Time Estimates vs Story Points**
   
   **Rule of Thumb (approximate mapping):**
   ```
   Story Points  →  Ideal Days (1 dev, no blockers)
   ─────────────────────────────────────────────────
   1 pt          →  0.5 days   (trivial)
   2 pts         →  1 day      (simple)
   3 pts         →  1-2 days   (standard)
   5 pts         →  3-4 days   (complex)
   8 pts         →  5-7 days   (very complex)
   13 pts        →  1-2 weeks  (epic, should split)
   ```
   
   **Note:** Story points include risk/uncertainty buffer, so days are IDEAL time, not calendar time.

2. **Validate Against Checklist Size**
   ```yaml
   # Example: Task has 12 checklist items
   progress:
     checklist:
       - task: "Set up database schema"
       - task: "Implement API endpoint"
       - task: "Write unit tests"
       - task: "Write integration tests"
       - task: "Add E2E test"
       - task: "Update documentation"
       - task: "Performance testing"
       - task: "Security review"
       - task: "Code review feedback"
       - task: "Refactor based on review"
       - task: "Final QA"
       - task: "Deploy to staging"
   
   # 12 items → likely 5-8 pts, not 2-3 pts
   ```

3. **Check Acceptance Criteria Complexity**
   ```yaml
   acceptance_criteria:
     - criterion: "System handles 10,000 req/sec"
       verification: "Load test with K6"
     - criterion: "99.9% uptime SLA"
       verification: "Monitor for 1 week"
     - criterion: "Complies with GDPR"
       verification: "Legal review + audit"
   
   # Complex acceptance criteria = higher effort
   ```

4. **Final Adjustment** (if needed)
   ```yaml
   agent_notes:
     planning_validation:
       research_agent_effort: 5
       time_estimate_check: |
         estimates.development: 4d
         + code_review: 1d
         + testing: 1.5d
         = 6.5 days total
         → Aligns with 5-8 pts range
       
       checklist_complexity: high  # 12 items
       acceptance_criteria_complexity: high  # Performance + legal
       
       final_effort: 8  # Increased from 5
       adjustment_reason: |
         Research agent estimated 5 pts based on implementation.
         Planning phase revealed:
         - 12 checklist items (not 5-7)
         - Complex acceptance criteria (performance + GDPR)
         - Time estimates show 6.5 days (closer to 8 pts)
         
         Recommendation: Increase to 8 pts
   ```

---

## Effort Adjustment Guidelines

### Conservative Approach (RECOMMENDED)

**Only adjust if discrepancy is ±2 points or more**

```
Initial: 3 pts, Research shows: 4-5 days
→ Keep at 3 pts (within margin of error)

Initial: 3 pts, Research shows: 8-10 days
→ Increase to 5 or 8 pts (significant discrepancy)
```

### When in Doubt

**Ask these questions:**

1. **Complexity:** Is this harder than initially thought?
2. **Risk:** Are there more unknowns than expected?
3. **Dependencies:** Do we need to wait on external factors?
4. **Effort:** Is implementation time significantly different?

**If 2+ answers are "yes" → Adjust effort**

### Avoid Over-Precision

❌ Don't: Try to map days exactly to points (e.g., 3.7 days → 4 pts)
✅ Do: Use relative sizing (is this harder than Task X?)

---

## Documentation Requirements

### Minimal (for small adjustments ±1 pt)

```yaml
agent_notes:
  effort_adjustment:
    original_effort: 3
    adjusted_effort: 5
    reason: "Additional API integration discovered"
```

### Complete (for large adjustments ±2+ pts)

```yaml
agent_notes:
  effort_adjustment:
    original_effort: 3
    adjusted_effort: 8
    reason: |
      Initial estimate missed key complexity:
      1. Custom OAuth implementation (no library) = +2 pts
      2. Multi-provider support (5 providers) = +1 pt
      3. GDPR compliance requirements = +1 pt
      4. Performance testing (10K req/sec) = +1 pt
    
    confidence: medium
    alternatives_considered:
      - "Split into 2 tasks (3 pts + 3 pts)"
      - "Use 3rd-party auth service (reduces to 3 pts)"
    
    recommendation: |
      Prefer keeping as single 8pt task to maintain context.
      If timeline is tight, consider 3rd-party service alternative.
```

---

## Impact on Project Timeline

### Example: 20% of tasks need adjustment

```
Original plan:  333 pts total
After refinement:
  - 60 tasks unchanged
  - 20 tasks +1 pt each (+20 pts)
  - 10 tasks +2 pts each (+20 pts)
  - 3 tasks -1 pt each (-3 pts)

New total: 370 pts

Impact:
  - Current capacity: 210 pts (7 iterations × 30)
  - New utilization: 370 / 210 = 176% (!!)
  - Need to: Add 2 iterations OR reduce scope by 40 pts
```

### Mitigation Strategies

1. **Baseline Iteration (I1):** Measure actual velocity
   - If team completes 25 pts (not 30), adjust capacity to 25/iteration
   
2. **Scope Reduction:** Defer low-priority tasks
   - Move p2/p3 tasks to "Future" milestone
   
3. **Timeline Extension:** Add iterations
   - 370 pts ÷ 30 pts/iter = 12.3 iterations (vs 7)
   
4. **Resource Scaling:** Increase team capacity
   - Add developer → 40 pts/iteration

---

## Tool Support

### Check Effort Discrepancies

```bash
# Find tasks with large time_estimate vs effort mismatch
python scripts/check-effort-discrepancies.py

# Output:
# T42: effort=3 but estimates.total=6.5d → RECOMMEND 5-8 pts
# T57: effort=8 but estimates.total=2d → RECOMMEND 2-3 pts
```

### Generate Re-estimation Report

```bash
# After research/planning phase
python scripts/generate-reestimation-report.py

# Output:
# Original plan: 333 pts
# After refinement: 365 pts (+32 pts, +9.6%)
# Tasks adjusted: 18 / 93 (19%)
# Largest increase: T42 (3→8 pts, +167%)
```

---

## Best Practices

### For Research Agent

1. ✅ **Be honest:** If task is more complex, increase effort
2. ✅ **Document why:** Future you will thank you
3. ✅ **Consider risk:** Unknowns should increase effort
4. ❌ **Don't pad:** Don't add effort "just to be safe"
5. ❌ **Don't optimize for deadline:** Accurate estimates > wishful thinking

### For Planning Agent

1. ✅ **Validate research:** Cross-check time estimates
2. ✅ **Count checklist items:** 10+ items likely means 5+ pts
3. ✅ **Check acceptance criteria:** Complex criteria = higher effort
4. ❌ **Don't blindly trust:** Research agent may have missed things
5. ❌ **Don't reduce effort without reason:** Conservative is better

### For Both

1. ✅ **Communicate changes:** Big adjustments should be discussed
2. ✅ **Track confidence:** Low confidence = higher effort to be safe
3. ✅ **Reference similar tasks:** "This is like T42 which was 5 pts"
4. ❌ **Don't skip documentation:** Future refinement needs context
5. ❌ **Don't adjust in isolation:** Consider dependencies

---

## Integration with Existing Workflow

### Updated AGENT_WORKFLOWS.md Steps

**Research Phase (ENHANCED):**
```yaml
# BEFORE (old)
- Research technical approach
- Document findings
- ✅ DONE

# AFTER (new)
- Research technical approach
- Document findings
- 🆕 Re-estimate effort based on research
- 🆕 Document adjustment in agent_notes.effort_adjustment
- ✅ DONE
```

**Planning Phase (ENHANCED):**
```yaml
# BEFORE (old)
- Define acceptance criteria
- Create testing strategy
- Generate checklist
- ✅ DONE

# AFTER (new)
- Define acceptance criteria
- Create testing strategy
- Generate checklist
- 🆕 Validate effort vs time_estimates
- 🆕 Validate effort vs checklist size
- 🆕 Final effort adjustment if needed
- ✅ DONE
```

---

## Example: Full Refinement with Re-estimation

**Initial State (before research):**
```yaml
key: T42
title: OAuth2 Provider Integration
effort: 3  # Preliminary estimate
description: "Add OAuth2 authentication"
```

**After Research Agent:**
```yaml
key: T42
title: OAuth2 Provider Integration
effort: 5  # Adjusted from 3
description: |
  **Context:** Users need to authenticate via Google, GitHub, Microsoft
  **Goal:** Implement OAuth2 flow with token refresh
  **Scope:** 5 providers, rate limiting, error handling
  
agent_notes:
  research_findings: |
    Investigated oauth libraries:
    - passport.js (too heavy for Fastify)
    - @fastify/oauth2 (basic, missing features we need)
    
    Decision: Custom implementation using Fastify decorators
    
  effort_adjustment:
    original_effort: 3
    adjusted_effort: 5
    reason: |
      Initial estimate assumed using passport.js.
      Research shows custom implementation needed:
      - Token refresh logic (1 day)
      - Multi-provider support (1 day)
      - Rate limiting (0.5 day)
      - Testing with 5 providers (1 day)
    confidence: medium
```

**After Planning Agent:**
```yaml
key: T42
title: OAuth2 Provider Integration
effort: 8  # Adjusted from 5
description: |
  [same as above]

acceptance_criteria:
  - criterion: "Users can authenticate with 5 providers"
    verification: "Manual test each provider, check DB for token"
  - criterion: "Token refresh works automatically"
    verification: "Let token expire, verify auto-refresh"
  - criterion: "Rate limiting prevents abuse"
    verification: "Load test with 100 req/sec, verify 429 responses"
  - criterion: "GDPR compliant (no PII in logs)"
    verification: "Legal review + log audit"

estimates:
  development: 4d
  code_review: 1d
  testing: 1.5d
  documentation: 0.5d
  total: 7d

progress:
  checklist:
    - task: "Research OAuth2 spec"
    - task: "Implement Google provider"
    - task: "Implement GitHub provider"
    - task: "Implement Microsoft provider"
    - task: "Implement LinkedIn provider"
    - task: "Implement Twitter provider"
    - task: "Token refresh logic"
    - task: "Rate limiting middleware"
    - task: "Error handling"
    - task: "Unit tests (5 providers)"
    - task: "Integration tests"
    - task: "E2E tests"
    - task: "GDPR audit"
    - task: "Documentation"
    - task: "Code review"

agent_notes:
  research_findings: |
    [same as above]
  
  effort_adjustment:
    original_effort: 3
    adjusted_effort: 5  # Research agent
    
  planning_validation:
    research_agent_effort: 5
    time_estimate_total: 7d
    checklist_items: 15
    
    final_effort: 8  # Planning agent increase
    adjustment_reason: |
      Research agent estimated 5 pts.
      Planning revealed:
      - 15 checklist items (not 7-8)
      - 4 complex acceptance criteria (incl. GDPR)
      - Time estimates: 7 days (aligns with 8 pts)
      - High risk: 5 providers, each may have quirks
      
      Recommend: 8 pts (very complex task)
```

---

## Adoption Plan

### Phase 1: Pilot (10 tasks)
- Select 10 high-priority tasks (M0, M1)
- Research + Planning agents refine with re-estimation
- Measure: How many tasks adjusted? By how much?
- Validate: Did estimates improve accuracy?

### Phase 2: Full Rollout (93 tasks)
- Refine all tasks through agent workflow
- Track total effort change (333 → ???)
- Adjust project timeline if needed

### Phase 3: Baseline & Iterate
- Complete I1 (first iteration)
- Measure actual velocity (pts completed)
- Update capacity per iteration
- Re-balance remaining iterations

---

## Success Metrics

### Quality Metrics
- **Estimate Accuracy:** ±20% of actual time (measured in I1)
- **Refinement Rate:** 100% of tasks refined before dev starts
- **Adjustment Rate:** 15-25% of tasks have effort adjusted

### Process Metrics
- **Research Time:** <2 hours per task average
- **Planning Time:** <1 hour per task average
- **Documentation:** All adjustments have `effort_adjustment.reason`

### Outcome Metrics
- **Velocity Stability:** I2-I7 within ±10% of I1 baseline
- **No Surprises:** <5% of tasks require re-estimation during dev
- **Timeline Accuracy:** Project completes within ±1 iteration of plan

---

## FAQ

**Q: What if Planning Agent disagrees with Research Agent's estimate?**
A: Planning agent has final say. Document disagreement in `agent_notes.planning_validation.adjustment_reason`.

**Q: Should we re-estimate during development if task is taking longer?**
A: No. Effort is "frozen" once dev starts. Track actual time separately for velocity calculation.

**Q: What if 50% of tasks need +2 pts increase?**
A: This signals systematic underestimation. Increase base capacity assumption or extend timeline. Discuss with team.

**Q: Can we use AI to auto-estimate effort?**
A: Experimental. Fine-tuned LLM could suggest effort based on description/checklist. But human validation required.

**Q: How to handle epics (13+ pts)?**
A: Split into multiple 3-5 pt tasks. Re-estimation often reveals epics that should be broken down.

---

## Related Documentation

- [AGENT_WORKFLOWS.md](./AGENT_WORKFLOWS.md) - Base workflow for agents
- [ISSUE_TEMPLATE.yaml](./ISSUE_TEMPLATE.yaml) - Task structure
- [pi-metadata.yaml](./pi-metadata.yaml) - Capacity configuration
- [Story Points Guide](https://www.atlassian.com/agile/project-management/estimation) - External reference
