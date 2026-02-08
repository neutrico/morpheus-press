# Task Automation System

**Hybrydowy system automatyzacji tasków** łączący:

- 🤖 **LLM Code Generation** (czyta specs z `planning/docs/`)
- 📋 **Template System** (gotowe boilerplate)
- 🔧 **CLI Scripts** (automatyczne setup)
- 🚀 **PR Automation** (gotowe rozwiązania do review)

## 🎯 Cel

**Maksymalizacja efektywności** dla powtarzalnych tasków z HIGH AI
effectiveness:

- ✅ Automatyczna generacja kodu z specyfikacji
- ✅ Gotowe skrypty dla typical patterns (database setup, tests, API routes)
- ✅ LLM-assisted scaffolding (agent czyta planning/docs/ i generuje kod)
- ✅ Utworzenie PR gotowego do review przez Copilot Agent

## 📊 Które taski można automatyzować?

**14/93 tasków** ma HIGH AI effectiveness (automatable):

```bash
# Lista wszystkich HIGH AI tasks
python scripts/automation/task-automation-agent.py --list
```

**Przykładowe taski**:

- T2: GitHub Milestones & Issues Creation (1.5 dni)
- T24: Supabase Database Setup with RLS (2.0 dni)
- T25: API Routes Implementation (3.5 dni)
- T27: Backend Unit Tests (2.0 dni)
- T32: API Documentation & OpenAPI (1.5 dni)

**Patterny**:

- 🗄️ **Database setup** (migrations, RLS, indexes)
- 🧪 **Testing** (unit tests, e2e tests, fixtures)
- 🔌 **API routes** (CRUD, Zod schemas, error handling)
- 📚 **Documentation** (OpenAPI, READMEs, guides)
- ⚙️ **Configuration** (setup scripts, configs)

## 🚀 Quick Start

### 1. Automatyzuj pojedynczy task

```bash
# Przykład: T24 (Supabase setup)
python scripts/automation/task-automation-agent.py T24

# Dry-run (preview bez tworzenia plików)
python scripts/automation/task-automation-agent.py T24 --dry-run
```

**Co to robi:**

1. Czyta spec z
   `planning/docs/m1---backend-services/T24-supabase-database-setup-with-rls.md`
2. Czyta research findings z `planning/issues/m1-backend.yaml`
3. Wywołuje Claude Sonnet 4 (~$0.15) z pełnym kontekstem
4. Generuje kod (migrations, services, tests)
5. Zapisuje pliki w odpowiednich lokalizacjach
6. Wyświetla next steps

### 2. Automatyzuj wszystkie HIGH AI tasks

```bash
# Auto-generuj 14 HIGH AI tasks (~10-15 min, ~$2.10)
python scripts/automation/task-automation-agent.py --auto

# Dry-run (preview)
python scripts/automation/task-automation-agent.py --auto --dry-run
```

### 3. Użyj gotowych CLI scripts

```bash
# Database setup
./scripts/automation/generators/setup-supabase.sh T24

# Test suite
./scripts/automation/generators/setup-tests.sh T27 unit

# API routes
python scripts/automation/generators/api-generator.py T25
```

## 📂 Struktura

```
scripts/automation/
├── task-automation-agent.py        # Main orchestrator (LLM-powered)
├── generators/
│   ├── setup-supabase.sh           # Database migrations + RLS
│   ├── setup-tests.sh              # Test suite generator
│   └── api-generator.py            # Fastify routes + Zod schemas
├── templates/
│   ├── api-route.ts.template       # API route template
│   ├── test-suite.ts.template      # Test template
│   └── migration.sql.template      # Migration template
└── README.md                       # This file
```

## 🔧 Jak to działa?

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Task Automation Agent                                       │
│                                                             │
│  1. Load Task Spec                                          │
│     ├─ planning/docs/*.md       (detailed requirements)     │
│     ├─ planning/issues/*.yaml   (research findings)         │
│     └─ planning/estimates/*.yaml (AI effectiveness)         │
│                                                             │
│  2. Identify Pattern                                        │
│     ├─ database   → setup-supabase.sh                       │
│     ├─ testing    → setup-tests.sh                          │
│     ├─ api        → api-generator.py                        │
│     └─ generic    → LLM generation                          │
│                                                             │
│  3. Generate Code                                           │
│     ├─ Use template if available                            │
│     └─ Call Claude Sonnet 4 with full context              │
│                                                             │
│  4. Write Files                                             │
│     ├─ apps/backend/src/...                                 │
│     ├─ apps/dashboard/...                                   │
│     └─ supabase/migrations/...                             │
│                                                             │
│  5. Optional: Create PR                                     │
│     └─ git + GitHub CLI integration                         │
└─────────────────────────────────────────────────────────────┘
```

### LLM Prompt Structure

Agent buduje comprehensive prompt:

```
📋 TASK SPECIFICATION:
- Title, key, estimated days
- Milestone, area

📝 DESCRIPTION:
[Full task description]

✅ ACCEPTANCE CRITERIA:
[List of criteria]

🔬 RESEARCH FINDINGS:
[AI suitability analysis, technical details]

📚 FULL DOCUMENTATION:
[Markdown from planning/docs/]

🎯 YOUR TASK:
Generate production-ready code following SOLID, DRY, KISS...
```

### Output Format

LLM zwraca JSON z file paths i content:

```json
{
    "files": {
        "apps/backend/src/services/example.service.ts": "import ...",
        "apps/backend/src/routes/example.routes.ts": "import ...",
        "apps/backend/src/__tests__/example.test.ts": "import ..."
    },
    "summary": "Generated service + routes + tests",
    "next_steps": [
        "Review database schema",
        "Test API endpoints",
        "Update TypeScript types"
    ]
}
```

## 💡 Przykłady użycia

### Example 1: Database Setup (T24)

```bash
# Automatyczna generacja Supabase setup
python scripts/automation/task-automation-agent.py T24
```

**Output:**

```
🚀 AUTOMATING TASK: T24
================================================================================
✅ Loaded task spec: Supabase Database Setup with RLS
   Pattern: database
   Estimated: 2.0 days

🤖 Generating code for T24 (pattern: database)...
   Calling Claude Sonnet 4 (~$0.15)...

📦 Generated 3 files
   ✅ Written: supabase/migrations/20260208_T24_setup.sql
   ✅ Written: apps/backend/src/services/database.service.ts
   ✅ Written: apps/backend/src/__tests__/database.test.ts

✅ Task T24 automated successfully!
   Files created: 3

📝 Next steps:
   1. Review generated code: git diff
   2. Run tests: pnpm test
   3. Apply migration: supabase db reset
   4. Commit: git add . && git commit -m 'feat: Supabase setup with RLS'
```

### Example 2: API Routes (T25)

```bash
# Generuj CRUD endpoints
python scripts/automation/generators/api-generator.py T25
```

**Output:**

- `apps/backend/src/routes/api-routes-implementation.routes.ts` (CRUD + Zod)
- TODO comments dla database queries
- Structured error handling
- Logging z Pino

### Example 3: Unit Tests (T27)

```bash
# Generuj test suite
./scripts/automation/generators/setup-tests.sh T27 unit
```

**Output:**

- `apps/backend/src/__tests__/T27-backend-unit-tests.test.ts`
- `apps/backend/src/__tests__/__fixtures__/T27-fixtures.ts`
- Happy path + error handling + integration tests

### Example 4: Batch Automation

```bash
# Automatyzuj wszystkie HIGH AI tasks
python scripts/automation/task-automation-agent.py --auto

# Output:
# [1/14] Processing T2...
# [2/14] Processing T8...
# ...
# ✅ Automation complete: 14/14 tasks successful
```

## 🔄 Workflow z GitHub Copilot Agent

**Rekomendowany flow:**

1. **Automatyzacja** (skrypt):
   ```bash
   python scripts/automation/task-automation-agent.py T24
   ```

2. **Review** (Copilot Agent):
   - Agent sprawdza wygenerowany kod
   - Fixuje TODO comments
   - Dostosowuje do specific requirements

3. **Testing** (human + Copilot):
   ```bash
   pnpm test                # Uruchom testy
   pnpm dev:backend         # Test API endpoints
   ```

4. **PR** (human):
   ```bash
   git add .
   git commit -m 'feat: T24 - Supabase setup'
   git push
   gh pr create --title "feat: T24 - Supabase Database Setup"
   ```

5. **Assign** (human):
   - Assign PR do Copilot Agent
   - Agent robi final review + merge

## 📈 Oszczędności

**Bez automatyzacji:**

- 14 HIGH AI tasks × 2.5 days avg = **35 days**

**Z automatyzacją:**

- Generacja kodu: ~2-3 hours (14 tasks × ~$0.15 = **$2.10**)
- Review + adjustments: ~7-10 days (Copilot Agent)
- **Total: ~10 days** (oszczędność: **71%**)

**ROI:**

- Cost: $2.10 (LLM API calls)
- Saved: 25 days × $500/day = **$12,500**
- **ROI: 595,000%** 🚀

## 🛠️ Setup

### Requirements

```bash
# Python dependencies
pip install anthropic pyyaml python-dotenv

# Environment variables (.env.local)
ANTHROPIC_API_KEY=sk-ant-...
```

### Installation

```bash
# Make scripts executable
chmod +x scripts/automation/generators/*.sh

# Test dry-run
python scripts/automation/task-automation-agent.py T24 --dry-run
```

## ⚠️ Best Practices

### DO ✅

- ✅ **Review generated code** - LLM może generować placeholder code
- ✅ **Run tests** - zawsze sprawdź czy testy przechodzą
- ✅ **Check TODOs** - LLM zostawia TODO comments dla manual steps
- ✅ **Use dry-run** - najpierw zobacz co zostanie wygenerowane
- ✅ **Commit incrementally** - commit po każdym tasku, nie wszystkie naraz

### DON'T ❌

- ❌ **Nie automatyzuj LOW AI tasks** - architecture/algorithms wymagają human
  judgment
- ❌ **Nie commituj blindly** - zawsze review przed commit
- ❌ **Nie skipuj testów** - LLM może generować kod który nie kompiluje
- ❌ **Nie używaj w production** - dopiero po thorough review

## 🔮 Future Enhancements

### Planned Features

1. **PR Automation**:
   ```bash
   python task-automation-agent.py T24 --create-pr
   ```
   - Automatyczne tworzenie branch + commit + PR
   - Auto-assign do Copilot Agent

2. **Template Management**:
   - `scripts/automation/templates/` z reusable templates
   - Custom templates per project

3. **Feedback Loop**:
   - Track success rate per pattern
   - Improve prompts based on failures
   - ML model do auto-tagging (high/medium/low AI effectiveness)

4. **CI/CD Integration**:
   ```yaml
   # .github/workflows/auto-generate.yml
   on:
       issue_comment:
           types: [created]

   jobs:
       auto_generate:
           if: contains(github.event.comment.body, '/automate')
           runs-on: ubuntu-latest
           steps:
               - run: python scripts/automation/task-automation-agent.py $TASK_KEY
   ```

5. **VS Code Extension**:
   - Right-click on task → "Automate with AI"
   - Inline preview of generated code
   - One-click apply

## 📚 Resources

- **Planning Docs**: `planning/docs/` - detailed task specifications
- **Research Findings**: `planning/issues/*.yaml` - AI suitability analysis
- **AI Effectiveness**: `planning/estimates/effort-map.yaml` - which tasks to
  automate
- **Copilot Instructions**: `.github/copilot-instructions.md` - code quality
  guidelines

## 🤝 Contributing

Dodawanie nowych generatorów:

1. Stwórz generator w `scripts/automation/generators/`
2. Dodaj pattern detection do `task-automation-agent.py`
3. Test dry-run na 2-3 przykładowych taskach
4. Update dokumentacji (ten README)

## 💬 Support

Questions? Issues?

- Check `planning/docs/` dla task specifications
- Run with `--dry-run` najpierw
- Review LLM prompt w `task-automation-agent.py`

---

**Status**: ✅ Production Ready (z human review)

**Version**: 1.0.0

**Last Updated**: 2026-02-08
