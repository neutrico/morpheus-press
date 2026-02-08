# Workflow PI Planning z Agentami Copilot

**Status:** ✅ Wszystkie agenty gotowe do użycia

---

## 🎯 Przegląd Systemu

System składa się z **3 agentów** działających w sekwencji:

```
planning/pi.yaml
     ↓
[@research] Research Agent → .copilot-tracking/research/
     ↓
[@task-planner] Task Planner → .copilot-tracking/plans/ + details/ + prompts/
     ↓
[Implementacja] → kod produkcyjny
     ↓
[@issue-publisher] Issue Publisher → GitHub Issues (opcjonalnie)
```

---

## 📋 Krok 1: Wybierz Zadanie z pi.yaml

### Najpierw wygeneruj strukturę:

```bash
pnpm pi:plan
```

To utworzy:

- `planning/pi-tree.md` - hierarchia wszystkich zadań
- `planning/pi-schedule.md` - harmonogram iteracji

### Wybierz zadanie do implementacji:

Otwórz [pi-tree.md](pi-tree.md) i znajdź zadanie, np.:

```markdown
- [ ] T1: Define Book schema in Supabase with RLS policies
  - Effort: 2 | Priority: p0
  - Depends On: None
```

---

## 🔍 Krok 2: Research Agent

### Uruchom Research Agent:

W Copilot Chat napisz:

```
@research-technical-spike

Zbadaj T1: Define Book schema in Supabase with RLS policies

Sprawdź:
- Istniejące schematy w supabase/migrations/
- Konwencje nazewnictwa (PascalCase vs snake_case)
- Przykłady RLS policies w projekcie
- Best practices dla Book metadata (ISBN, wydawca, rok)
```

### Co zrobi Research Agent:

1. **Analizuje kod projektu** (#codebase, #search)
2. **Szuka istniejących implementacji** (#githubRepo dla Supabase patterns)
3. **Czyta dokumentację** (#fetch Supabase docs)
4. **Tworzy spike document**:
   `.copilot-tracking/research/20260207-book-schema-research.md`

### Przykładowy output Research Agent:

```markdown
# Research: Book Schema with RLS

## Investigation Results

### Project Analysis

- Current naming: `Book`, `Character`, `Scene` use PascalCase (legacy)
- NEW convention: snake_case (`store_products`, `ml_training_sessions`)
- RLS examples: apps/backend/src/services/database.ts uses service_role key

### External Research

- Supabase RLS docs: https://supabase.com/docs/guides/auth/row-level-security
- ISBN validation: ISBN-10 or ISBN-13 formats required

## Recommended Approach

1. Create `books` table (snake_case, NEW standard)
2. Add RLS policies: SELECT (public), INSERT/UPDATE/DELETE (authenticated users
   only)
3. Metadata fields: isbn TEXT, publisher TEXT, publication_year INTEGER
```

---

## 📝 Krok 3: Task Planner Agent

### Uruchom Task Planner:

```
@task-planner

Stwórz plan implementacji dla T1: Define Book schema in Supabase with RLS policies

Bazuj na research: .copilot-tracking/research/20260207-book-schema-research.md
```

### Co zrobi Task Planner:

1. **Weryfikuje research** (czy istnieje i jest kompletny)
2. **Tworzy 3 pliki**:
   - `.copilot-tracking/plans/20260207-book-schema-plan.instructions.md` -
     checklist z fazami
   - `.copilot-tracking/details/20260207-book-schema-details.md` - szczegółowa
     specyfikacja
   - `.copilot-tracking/prompts/implement-book-schema.prompt.md` - prompt dla
     implementacji

### Przykładowy plan.instructions.md:

```markdown
---
applyTo: ".copilot-tracking/changes/20260207-book-schema-changes.md"
---

# Task Checklist: Define Book Schema

## Implementation Checklist

### [ ] Phase 1: Create Migration File

- [ ] Task 1.1: Create
      `supabase/migrations/20260207123000_create_books_table.sql`
  - Details: .copilot-tracking/details/20260207-book-schema-details.md (Lines
    15-30)

### [ ] Phase 2: Add RLS Policies

- [ ] Task 2.1: Add SELECT policy for public access
  - Details: .copilot-tracking/details/20260207-book-schema-details.md (Lines
    32-45)

### [ ] Phase 3: Update TypeScript Types

- [ ] Task 3.1: Regenerate apps/backend/src/types/database.ts
  - Details: .copilot-tracking/details/20260207-book-schema-details.md (Lines
    47-60)
```

---

## 🚀 Krok 4: Implementacja

### Opcja A: Automatyczna (Prompt File)

Otwórz
[.copilot-tracking/prompts/implement-book-schema.prompt.md](.copilot-tracking/prompts/implement-book-schema.prompt.md)
i uruchom jako agent prompt:

1. Kliknij prawym przyciskiem na plik
2. Wybierz **"Run as Copilot Agent"** (jeśli dostępne)
3. LUB skopiuj zawartość i wklej do Copilot Chat

### Opcja B: Manualna (Krok po kroku)

Otwórz plan i details, następnie w Copilot Chat:

```
Zaimplementuj Phase 1 z planu:
#file:.copilot-tracking/plans/20260207-book-schema-plan.instructions.md

Szczegóły:
#file:.copilot-tracking/details/20260207-book-schema-details.md
```

### Tracking zmian:

Copilot automatycznie utworzy:
`.copilot-tracking/changes/20260207-book-schema-changes.md` - log wszystkich
zmian

---

## 🎫 Krok 5: Publikacja na GitHub (Opcjonalnie)

### Gdy zadania są gotowe do publikacji:

```
@issue-publisher

Opublikuj taski z iteracji I1 na GitHub

PI file: planning/pi.yaml
Zakres: E1:F1 (Epic 1, Feature 1)
```

### Co zrobi Issue Publisher:

1. **Pre-flight Validation**:
   - Sprawdza pi.yaml
   - Weryfikuje GITHUB_TOKEN w env
   - Sprawdza czy Copilot-generated artifacts istnieją

2. **Generuje Publication Spec**:
   - Tworzy `.copilot-tracking/publish/20260207-pi-2026-q1-publish.md`
   - Pokazuje dokładnie co zostanie utworzone (issues, labels, milestones)

3. **User Approval Gate**:
   ```
   Review the spec at: .copilot-tracking/publish/20260207-pi-2026-q1-publish.md

   Type "APPROVED" to proceed with publishing.
   ```

4. **Wykonuje publikację**:
   - Uruchamia `pnpm pi:publish` (gdy będzie zaimplementowany)
   - Tworzy issues na GitHub z properties (Priority, Effort, Iteration)

5. **Post-Publishing Report**:
   - `.copilot-tracking/publish/20260207-results.md` z mapowaniem T1→#123,
     T2→#124, etc.

---

## 🔄 Typowy Workflow (Przykład)

### Dzień 1: Planning Iteration

```bash
# 1. Przegląd planów
pnpm pi:validate
pnpm pi:plan

# 2. Wybierz 3 taski na dziś: T1, T2, T3
```

### Dzień 1-2: Research (T1)

```
@research-technical-spike

Zbadaj T1: Define Book schema in Supabase with RLS policies
```

**Output**: `.copilot-tracking/research/20260207-book-schema-research.md`

### Dzień 2: Planning (T1)

```
@task-planner

Plan dla T1 bazując na research: #file:.copilot-tracking/research/20260207-book-schema-research.md
```

**Output**: 3 pliki (plan, details, implement prompt)

### Dzień 2-3: Implementation (T1)

```
Implementuj #file:.copilot-tracking/prompts/implement-book-schema.prompt.md
```

**Output**: Migration file, types, RLS policies + changes.md

### Powtórz dla T2, T3...

### Koniec Iteracji: Publikacja

```
@issue-publisher

Opublikuj wszystkie ukończone taski z I1 na GitHub
```

**Output**: Issues #123-#127 utworzone na GitHub

---

## 📁 Struktura Plików

Po pełnym workflow dla 1 zadania:

```
.copilot-tracking/
├── research/
│   └── 20260207-book-schema-research.md          # Output Research Agent
├── plans/
│   └── 20260207-book-schema-plan.instructions.md # Output Task Planner
├── details/
│   └── 20260207-book-schema-details.md           # Output Task Planner
├── prompts/
│   └── implement-book-schema.prompt.md           # Output Task Planner
├── changes/
│   └── 20260207-book-schema-changes.md           # Auto-created podczas impl
└── publish/
    ├── 20260207-pi-2026-q1-publish.md            # Publication spec
    └── 20260207-results.md                       # Issue numbers mapping
```

---

## 🎓 Best Practices

### 1. **Research ZAWSZE pierwszy**

- Nigdy nie skip research phase
- Research Agent unika hallucinations (bazuje na faktach z kodu/docs)

### 2. **Używaj hashtagów w Copilot Chat**

```
@research-technical-spike                  # Wywołaj agenta
#file:path/to/file.md                     # Link do pliku
#codebase search term                     # Szukaj w kodzie
#githubRepo:"owner/repo search terms"     # Szukaj w GitHub
```

### 3. **Iteruj na planach**

- Plan nie jest doskonały za pierwszym razem
- Możesz poprosić Task Planner o aktualizację:
  ```
  @task-planner

  Zaktualizuj plan dla T1 - dodaj Phase 4: Testing z E2E tests
  ```

### 4. **Tracking jest kluczowy**

- `.copilot-tracking/changes/*.md` to historia wszystkich zmian
- Używaj tego do code review i dokumentacji

### 5. **GitHub Publishing opcjonalny**

- Możesz pracować bez publikowania na GitHub
- Publikuj batch tasków na koniec iteracji, nie pojedynczo

---

## ❓ FAQ

### Q: Czy muszę używać wszystkich 3 agentów?

**A:** Nie! Możesz używać tylko Research + Task Planner bez Issue Publisher.
Niektóre proste taski mogą nie wymagać research (wtedy Task Planner poprosi o
research gdy potrzeba).

### Q: Co jeśli research jest niekompletny?

**A:** Task Planner automatycznie wykryje i poprosi Research Agent o
uzupełnienie.

### Q: Czy mogę modyfikować pi.yaml podczas pracy?

**A:** Tak! Po każdej zmianie uruchom `pnpm pi:validate` i `pnpm pi:plan` aby
wygenerować nowe plany.

### Q: Jak wybrać które taski publikować na GitHub?

**A:** Issue Publisher pyta o zakres (np. "I1" = iteracja 1, "E1:F1" = epic 1
feature 1). Możesz wybrać kilka iteracji naraz.

### Q: Co z zależnościami między taskami?

**A:** pi.yaml definiuje `dependsOn`. Validation wykryje cykle. Plan generation
pokazuje kolejność (topological sort). Issue Publisher utworzy linki między
issues.

---

## 🚀 Zaczynaj Tutaj

```bash
# 1. Wygeneruj plany
pnpm pi:plan

# 2. Otwórz planning/pi-tree.md

# 3. Wybierz pierwsze zadanie (T1)

# 4. W Copilot Chat:
@research-technical-spike

Zbadaj T1: Define Book schema in Supabase with RLS policies
```

**Gotowe! System poprowadzi Cię przez resztę.**
