# Copilot Agent ↔ GitHub Actions Integration

## TL;DR: Jak to współdziała?

**Copilot NIE uruchamia testów bezpośrednio** - robi to GitHub Actions. Ale Copilot **reaguje na feedback z testów** i poprawia kod automatycznie.

```
┌─────────────────────────────────────────────────────────────────┐
│  ITERACYJNY CYKL: Code → Test → Feedback → Fix → Repeat         │
└─────────────────────────────────────────────────────────────────┘

1. 🤖 Copilot pushes code → copilot/176-testing-infra
2. ⚡ GitHub Actions triggers automatically
3. 🧪 Tests run, coverage checked, lint/typecheck
4. ❌ IF FAIL:
   → Comment posted on issue with errors
   → 🤖 Copilot READS the comment
   → 🤖 Copilot FIXES the code
   → 🤖 Copilot PUSHES again (back to step 2)
5. ✅ IF PASS:
   → PR auto-created
   → 🚀 Preview deployed to Vercel
   → 👨‍💻 Human review + merge
```

---

## Szczegółowy Flow

### Faza 1: Planning (Human + Planning Agent)

```yaml
User: "Create testing infrastructure"
  ↓
Planning Agent creates plan with test_scenarios.yaml:
  test_scenarios:
    unit:
      - component: "DatabaseService.getBook"
        test_cases:
          - name: "Happy path - returns book"
            arrange: "Mock Supabase..."
            act: "await db.getBook('123')"
            assert:
              - "Returns book object"
              - "Supabase called once"
  ↓
Planning Agent posts to issue #176 as structured comment
  ↓
User reviews and approves plan
```

**Output:** Test scenarios YAML in issue comment (reviewable by humans)

---

### Faza 2: Implementation (Copilot Agent)

```yaml
User: "@copilot implement this"
  ↓
Copilot reads:
  - Issue description
  - Planning agent's comment with test_scenarios.yaml
  - Existing codebase patterns
  ↓
Copilot writes ONLY implementation code (NO tests):
  - services/database.ts
  - routes/books.routes.ts
  - schemas/book.schema.ts
  ↓
Copilot commits to branch: copilot/176-testing-infra
  ↓
Copilot pushes → Triggers GitHub Actions
```

**Output:** Implementation code pushed to branch (NO tests yet)

**Important:** Copilot nie pisze testów - to robi GitHub Actions w następnym kroku!

---

### Faza 3: Test Generation (GitHub Actions - Automated)

```yaml
GitHub Actions workflow: copilot-branch-pipeline.yml
  ↓
Job 1 - detect:
  - Extract issue number from branch name
  - Get changed files (database.ts, books.routes.ts)
  - Download test_scenarios.yaml from issue comment
  ↓
Job 2 - generate-tests:
  - Run: scripts/generate_tests_from_scenarios.py
  - Input:
      scenarios: test_scenarios.yaml
      changed_files: database.ts, books.routes.ts
  - Process:
      For each changed file:
        1. Match scenarios to file
        2. Read source code
        3. Call OpenAI GPT-4o-mini
        4. Generate complete Vitest test file
  - Output:
      apps/backend/src/__tests__/database.test.ts
      apps/backend/src/__tests__/routes/books.test.ts
  ↓
Job 2 - generate-tests (continued):
  - Commit generated tests to same branch
  - Push to copilot/176-testing-infra
```

**Output:** Auto-generated test files committed to branch

**Cost:** ~$0.02-0.05 per file (GPT-4o-mini is cheap)

---

### Faza 4: Quality Gate (GitHub Actions - Decision Point)

```yaml
Job 3 - test-backend:
  - Pull latest code (with generated tests)
  - Run: pnpm test --coverage
  - Collect results
  ↓
Job 4 - quality-gate:
  - Check: Lint ✅/❌
  - Check: Type-check ✅/❌
  - Check: Tests pass ✅/❌
  - Check: Coverage ≥80% ✅/❌
  ↓
DECISION:
  If ALL PASS → Job 5 (create-pr)
  If ANY FAIL → Job 6 (feedback)
```

**Output:** Pass/Fail decision with detailed report

---

### Faza 5A: Success Path (All Tests Pass)

```yaml
Job 5 - create-pr:
  - Check if PR already exists
  - If NO:
      Create new PR:
        Title: Issue title
        Body: Quality gate report + changes summary
        Assignee: Original issue assignee
        Labels: ready-for-review
  - If YES:
      Update existing PR with comment:
        "✅ Quality gate passed! Updated with latest changes."
  ↓
Job 7 - deploy-preview:
  - Build apps (dashboard/storefront)
  - Deploy to Vercel
  - Generate preview URL: https://pr-176-dashboard.vercel.app
  - Comment on issue with preview link
  ↓
👨‍💻 Human reviews PR:
  - Check business logic
  - Test in preview environment
  - Approve and merge
```

**Output:** PR ready for human review + live preview

---

### Faza 5B: Failure Path (Tests Fail) - 🚨 KLUCZ!

```yaml
Job 6 - feedback:
  - Extract quality gate report
  - Post comment on issue #176:
  
❌ **Quality gate failed**

The tests or quality checks did not pass. Please review and fix:

❌ TypeScript error in database.ts:42
   Type 'string | undefined' is not assignable to type 'string'

❌ Test failed: DatabaseService.getBook should return book
   Expected: { id: '123', title: 'Test' }
   Received: { id: '123', title: undefined }

❌ Coverage below threshold: 75% < 80%
   Missing coverage in: database.ts lines 42-55

---

### 🔧 What to do next:

1. @copilot: Review the failures above
2. Fix the issues in your code
3. Push again to `copilot/176-testing-infra`
4. Pipeline will re-run automatically
```

**Output:** Structured feedback comment on issue

---

### Faza 6: Copilot Reads Feedback & Fixes (AUTOMATIC)

**🤖 Copilot Bot Behavior:**

```python
# Copilot agent continuously monitors assigned issues
while issue.assignee == "copilot":
    # Check for new comments
    new_comments = issue.get_comments_since_last_check()
    
    for comment in new_comments:
        if "Quality gate failed" in comment.body:
            # Parse feedback
            errors = extract_errors(comment.body)
            
            # Copilot reads:
            # 1. Error messages
            # 2. Failed test names
            # 3. Coverage gaps
            # 4. Line numbers with issues
            
            # Copilot analyzes code
            for error in errors:
                file = error.file
                line = error.line
                message = error.message
                
                # Find root cause
                context = read_file_context(file, line, radius=10)
                
                # Generate fix
                fix = generate_fix(context, error)
                
                # Apply fix
                apply_code_change(file, line, fix)
            
            # Copilot commits
            git commit -m "fix: Address quality gate failures
            
            - Fixed type error in database.ts:42
            - Added missing field in getBook method
            - Improved coverage in database operations
            
            Responding to: [workflow run link]
            "
            
            # Copilot pushes
            git push origin copilot/176-testing-infra
            
            # 🔄 GOTO Faza 3 - workflow triggers again!
```

**Kluczowe:**
1. ✅ Copilot **automatycznie** czyta komentarze z "Quality gate failed"
2. ✅ Copilot **parsuje** błędy (regex patterns)
3. ✅ Copilot **znajduje** odpowiednie pliki i linie
4. ✅ Copilot **poprawia** kod
5. ✅ Copilot **pushuje** automatycznie
6. ✅ Workflow **re-run** automatycznie przy każdym pushu

---

## Iteracyjny Cykl - Przykład Rzeczywisty

### Iteration 1: Type Error

```
Push 1: Copilot writes initial code
  ↓
Test: ❌ TypeScript error
Feedback: "Type 'string | undefined' not assignable to 'string'"
  ↓
Fix: Copilot adds null check
Push 2: git push (automatic)
```

### Iteration 2: Test Failure

```
Push 2: With null check
  ↓
Test: ❌ Test fails - missing field
Feedback: "Expected book.title, received undefined"
  ↓
Fix: Copilot adds title field mapping
Push 3: git push (automatic)
```

### Iteration 3: Coverage Gap

```
Push 3: With title field
  ↓
Test: ❌ Coverage 75% < 80%
Feedback: "Missing coverage in lines 42-55"
  ↓
Fix: Copilot adds tests for edge cases
Push 4: git push (automatic)
```

### Iteration 4: Success!

```
Push 4: Complete implementation
  ↓
Test: ✅ All tests pass
      ✅ Coverage 82%
      ✅ Lint OK
      ✅ Type-check OK
  ↓
Action: PR auto-created
        Preview deployed
  ↓
Human: Reviews and merges
```

**Total time:** ~30-60 minutes (vs 4-6 hours manual)

---

## Dlaczego Ten Podział Odpowiedzialności?

### Planning Agent → Test Scenarios (Human-Reviewable)

**Pros:**
- ✅ Stakeholders mogą zreviewować "co testujemy"
- ✅ Clear acceptance criteria przed kodem
- ✅ Test scenarios są dokumentacją
- ✅ Można approve bez technical knowledge

**Cons:**
- ⚠️ Wymaga ręcznego review planning phase
- ⚠️ Dodatkowy krok w workflow

### GitHub Actions → Test Code (Automated)

**Pros:**
- ✅ Zero manual test writing
- ✅ Consistent test quality (same LLM)
- ✅ Very cheap ($0.02-0.05 per file)
- ✅ Fast (parallel generation)

**Cons:**
- ⚠️ Wymaga OpenAI API key
- ⚠️ Może generować suboptimal tests (ale Copilot poprawi)

### Copilot Agent → Implementation (Iterative)

**Pros:**
- ✅ Automatyczne poprawki po każdym fail
- ✅ Nie blokuje human reviewers
- ✅ Learns from feedback loop
- ✅ Działa 24/7

**Cons:**
- ⚠️ Może wejść w infinite loop (max 10 iterations)
- ⚠️ Wymaga dobrze napisanych error messages

---

## Konfiguracja Wymagana

### 1. GitHub Secrets

```bash
# W repozytorium Settings → Secrets and variables → Actions
OPENAI_API_KEY=sk-...              # Dla generate_tests_from_scenarios.py
VERCEL_TOKEN=...                   # Dla Vercel previews
VERCEL_ORG_ID=...                  # Vercel organization
VERCEL_PROJECT_ID=...              # Dashboard project ID
```

### 2. Copilot Agent Configuration

```yaml
# .github/agents/testing-specialist.agent.md lub planning-agent.agent.md
monitoring:
  watch_for_comments: true
  react_to_patterns:
    - "Quality gate failed"
    - "Tests failed"
    - "Coverage below threshold"
  
  action_on_match:
    - Read full comment
    - Parse errors (regex)
    - Fix code
    - Commit + push
```

### 3. Issue Assignment

```
When Copilot is assigned to issue:
  1. Planning agent creates test scenarios
  2. User approves
  3. Copilot implements code
  4. Workflow runs tests
  5. If fail → Copilot fixes (loop)
  6. If pass → PR created
```

---

## Monitoring & Debugging

### Check Pipeline Status

```bash
# W GitHub UI:
Actions → Copilot Branch Pipeline
  → See all runs for copilot/** branches
  
# Każdy push triggeruje nowy run
# Możesz zobaczyć:
  - Które testy się popsuly
  - Coverage metrics
  - Deployment logs
```

### Check Copilot Activity

```bash
# W Issue #176:
  - Timeline pokazuje wszystkie Copilot commits
  - Comments pokazują feedback z workflow
  - Labels pokazują status (ready-for-review, needs-work)
```

### Manual Override

```bash
# Jeśli Copilot nie może naprawić:
git checkout copilot/176-testing-infra
# Fix manually
git commit -m "fix: Manual fix for failing test"
git push
# Workflow re-runs automatically
```

---

## FAQ

**Q: Co jeśli Copilot wejdzie w infinite loop?**
A: Workflow ma max 10 iterations, potem fail i manual review required

**Q: Czy mogę wyłączyć auto-test generation?**
A: Tak, usuń job `generate-tests` z workflow lub nie dodawaj test_scenarios.yaml

**Q: Co jeśli testy są słabej jakości?**
A: Copilot je poprawi w kolejnych iterations, lub human może poprawić ręcznie

**Q: Czy to działa dla E2E testów?**
A: Nie, E2E są w osobnym Playwright workflow (nie auto-generated)

**Q: Ile to kosztuje w API calls?**
A: ~$0.02-0.05 per file dla test generation, ~$0.50-1.00 per iteration dla Copilot fixes

**Q: Czy mogę użyć lokalnie?**
A: Tak, `python scripts/generate_tests_from_scenarios.py --local`

---

## Comparison: Before vs After

### Before (Manual)

```
Developer writes code (2h)
  ↓
Developer writes tests (2h)
  ↓
Developer runs tests locally (5min)
  ↓
Fix errors (30min)
  ↓
Push to PR
  ↓
CI runs (10min)
  ↓
Code review (1h)
  ↓
Human merges

Total: 5.5h + human time
```

### After (Automated)

```
Planning agent: test scenarios (15min + human review)
  ↓
Copilot writes code (20min)
  ↓
Push → GitHub Actions:
  - Generate tests (2min)
  - Run tests (3min)
  - Deploy preview (5min)
  ↓
Auto-feedback to Copilot if fail (instant)
  ↓
Copilot fixes automatically (10min per iteration)
  ↓
PR auto-created when pass
  ↓
Human review (30min)
  ↓
Human merges

Total: 45min-1h + human review (if 2-3 iterations)
```

**Time savings: 75-80%**
**Cost: ~$2-5 per task (API costs)**

---

## Summary

✅ **Copilot pisze kod, NIE testy**
✅ **GitHub Actions generuje testy z scenarios**
✅ **GitHub Actions uruchamia testy**
✅ **GitHub Actions daje feedback**
✅ **Copilot czyta feedback automatycznie**
✅ **Copilot poprawia kod automatycznie**
✅ **Cykl repeats aż do sukcesu**
✅ **Human tylko review final PR**

**To jest pełna automatyzacja z human oversight na krytycznych momentach!** 🚀
