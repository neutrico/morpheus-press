# Analiza PI Planning dla Startupu Morpheus

**Data:** 2026-02-07 **Status:** KRYTYCZNA ANALIZA - 93 taski to za dużo na
startup MVP

---

## 🎯 Core Value Proposition: Książka → Komiks (AI)

**Minimalna ścieżka użytkownika:**

1. Upload tekstu książki
2. AI ekstraktuje dialogi + postacie
3. AI generuje ilustracje (SDXL)
4. Złóż w komiks (PDF)
5. Pobierz

---

## 📊 Aktualna Struktura (93 taski, 333 punkty)

| Epic             | Milestone | Taski   | Effort | **Ocena dla MVP**   |
| ---------------- | --------- | ------- | ------ | ------------------- |
| E1: Setup        | M0        | T1-T18  | 50 pts | ⚠️ **50% zbędne**   |
| E2: Dialogue DB  | M1        | T19-T36 | 59 pts | ✅ **Krytyczne**    |
| E3: Book Import  | M2        | T37-T49 | 56 pts | ⚠️ **40% zbędne**   |
| E4: Prompt Gen   | M3        | T50-T60 | 41 pts | ✅ **Krytyczne**    |
| E5: Comic MVP    | M4        | T61-T73 | 47 pts | ✅ **Krytyczne**    |
| E6: Distribution | M5        | T74-T82 | 31 pts | ❌ **Przedwczesne** |
| E7: Ecommerce    | M6        | T83-T90 | 29 pts | ❌ **Przedwczesne** |
| E8: Release      | M7        | T91-T93 | 10 pts | ✅ **Niezbędne**    |

---

## 🚨 Krytyczne Problemy

### 1. **Zbyt Dużo Zadań Setup (E1: 50 punktów)**

**Zbędne dla MVP:**

- ❌ T1: Tech Stack Decision Documentation (2 pts) - startup wie co używa
- ❌ T2: GitHub Milestones (2 pts) - masz to już w pi.yaml
- ❌ T5: Weights & Biases (3 pts) - przedwczesna optymalizacja
- ❌ T7: Mock Mode (2 pts) - nie potrzebne w MVP
- ❌ T8: Timeline & Cost Estimates (2 pts) - robisz to teraz
- ❌ T9: Storybook (3 pts) - overkill, shadcn działa bez tego
- ❌ T10: shadcn audit (2 pts) - używasz co masz
- ❌ T17: SLA/SLO/SLI (2 pts) - nie masz jeszcze userów!
- ❌ T18: Performance Budgets (3 pts) - przedwczesna optymalizacja

**Oszczędność: ~21 punktów (42% Epic E1)**

**Pozostaw tylko:**

- ✅ T3: Database Schema (5 pts) - fundamentalne
- ✅ T4: Testing Infrastructure (3 pts) - CI jest kluczowe
- ✅ T6: CI/CD (3 pts) - automatyzacja deploymentu
- ✅ T11: Test Environments (3 pts) - staging + prod
- ✅ T12: Monitoring (3 pts) - musisz wiedzieć co się dzieje
- ✅ T13: Security & Compliance (5 pts) - GDPR, RLS
- ✅ T14: API Standards (2 pts) - consistency
- ✅ T15: Documentation (2 pts) - API docs
- ✅ T16: Deployment Strategy (3 pts) - jak wrzucać na prod

**Zredukowany E1: 29 punktów (zamiast 50)**

---

### 2. **Nadmiarowe Features Backend (E2: 59 punktów)**

**Zbędne dla MVP:**

- ❌ T28: Mock Mode Backend (2 pts) - nie potrzebne
- ❌ T31: Query Performance Optimization (3 pts) - przedwczesne, zoptymalizuj
  jak będzie problem
- ❌ T33: Code Review Process (1 pt) - to nie task, to kultura
- ❌ T34: Training Data Generator (5 pts) - zrób ręcznie 1000 przykładów
- ❌ T35: Active Learning Loop (3 pts) - v2 feature
- ❌ T36: Dialogue Classification (5 pts) - nice-to-have, nie MVP

**Oszczędność: ~19 punktów (32% Epic E2)**

**Pozostaw:**

- Core ML: T19-T22 (21 pts) ✅
- Backend TS port: T23-T27, T29-T30, T32 (33 pts) ✅

**Zredukowany E2: 40 punktów (zamiast 59)**

---

### 3. **Book Import Overkill (E3: 56 punktów)**

**Zbędne dla MVP:**

- ❌ T48: Literary Cultural Context (5 pts) - nice-to-have, nie core value
- ❌ T49: Book Timeline Extractor (3 pts) - nie krytyczne

**Uproszczenia:**

- ⚠️ T44: Semantic Search (5 pts) → Może być v1.1, nie core flow
- ⚠️ T43: Embedding Generation (3 pts) → Tylko jeśli robisz T44

**Potencjalna oszczędność: 8-16 punktów**

**Zredukowany E3: 40-48 punktów (zamiast 56)**

---

### 4. **Comic Production OK (E4+E5: 88 punktów)**

To core value - **zostaw wszystko**.

**Feature assignments:**

- T50-T60: Prompt generation - wszystkie **type: feature** (user-facing)
- T61-T73: Comic assembly - wszystkie **type: feature** (user-facing)

Wyjątki (implementacyjne):

- T56: Prompt Caching - **type: task** (performance)
- T57: Progress Tracking - **type: task** (infrastructure)
- T70: QC Dashboard - **type: feature** (user tool)

---

### 5. **Distribution = Przedwczesne (E6: 31 punktów)**

**❌ USUŃ CAŁKOWICIE dla MVP:**

- T74-T82: Discord bot, Reddit, Browser Extension, WordPress

**Dlaczego:**

- Nie masz jeszcze product-market fit
- Dystrybucja zanim masz 100 happy userów = strata czasu
- Możesz dodać w v2 jak zobaczysz traction

**Oszczędność: 31 punktów (100% Epic E6)**

---

### 6. **E-commerce = Przedwczesne (E7: 29 punktów)**

**❌ USUŃ WIĘKSZOŚĆ:**

**Zamiast Stripe + cart + checkout + fulfillment, użyj:**

- Gumroad ($10/miesiąc, 0% setup)
- Ko-fi (free, 5% fee)
- LemonSqueezy (MoR service)

**Zostaw TYLKO jeśli robisz własny:**

- T83: Stripe Integration (5 pts) - minimum
- T87: Checkout Flow (5 pts) - redirect do Stripe Checkout

**Usuń:**

- ❌ T84: Webhooks (3 pts) - Stripe Checkout hostedowany
- ❌ T85: Storefront UI (5 pts) - masz już dashboard
- ❌ T86: Cart Management (3 pts) - single product na start
- ❌ T88: Order Management (3 pts) - Stripe Dashboard
- ❌ T89: Inventory Tracking (2 pts) - digital product
- ❌ T90: Fulfillment (3 pts) - automatic download

**Opcja A (recommended): Użyj Gumroad → 0 tasków** **Opcja B (własny): T83 + T87
→ 10 punktów**

**Oszczędność: 19-29 punktów**

---

## 📋 Rekomendowane Type Assignments

### **FEATURES** (user-facing functionality):

```yaml
# Book Import & Processing
T37: Wolne Lektury API → type: feature
    T38: Book Upload → type: feature
        T39: Chapter Extraction → type: feature
            T40: Text Preprocessing → type: task (infrastructure)
                T41: Scene Extraction → type: feature
                    T42: Character Profiling → type: feature
                        T44: Semantic Search → type: feature
                            T45: Book Status Tracking → type: feature

                                # Prompt Generation
                                T50: Prompt Engineering → type: feature
                                    T51: Character Description → type: feature
                                        T52: Batch Image Generation → type: feature
                                            T53: Location & Environment → type: feature
                                                T54: Image Quality Assessment → type: feature
                                                    T55: Mood & Atmosphere → type: feature
                                                        T59: Prompt Validation → type: feature

                                                            # Comic Assembly
                                                            T61: ComfyUI Integration → type: task (infrastructure)
                                                                T62: Image Enhancement → type: feature
                                                                    T63: Comic Layout → type: feature
                                                                        T64: Panel Generation → type: feature
                                                                            T66: PDF Generation → type: feature
                                                                                T67: Download Manager → type: feature
                                                                                    T68: Archive Creation → type: feature
                                                                                        T69: Print-Ready Output → type: feature
                                                                                            T70: QC Dashboard → type: feature
                                                                                                T72: Comic Preview → type: feature
                                                                                                    T73: Variant Generation → type: feature
```

### **TASKS** (implementation/infrastructure):

```yaml
# Setup & Infrastructure (wszystkie E1)
T1-T18 → type: task (ale większość usuń)

# Backend & ML Infrastructure
T19: Dataset Prep → type: task
    T20: Model Selection → type: task
        T21: Model Training → type: task
            T22: NER Training → type: task
                T23: TS Port → type: task
                    T24: Supabase Setup → type: task
                        T25: API Routes → type: task
                            T26: Authentication → type: task
                                T27: Unit Tests → type: task
                                    T29: Error Handling → type: task
                                        T30: Logging → type: task
                                            T32: API Docs → type: task
                                                T40: Text Preprocessing → type: task
                                                    T43: Embeddings → type: task
                                                        T46: Error Recovery → type: task
                                                            T47, T60, T71: Integration Testing → type: task
                                                                T56: Prompt Caching → type: task
                                                                    T57: Progress Tracking → type: task
                                                                        T61: ComfyUI Integration → type: task
                                                                            T65: Comic Metadata → type: task
```

---

## 🎯 Zredukowana Ścieżka MVP (48 tasków, ~160 punktów)

### **Phase 1: Core Infrastructure (15 pts, 1 tydzień)**

- T3: Database Schema (5 pts)
- T4: Testing Infrastructure (3 pts)
- T6: CI/CD (3 pts)
- T12: Monitoring (3 pts)
- T13: Security (wybrane aspekty, 3 pts zamiast 5)

### **Phase 2: ML Backend (40 pts, 2.5 tygodnia)**

- T19-T22: ML Training (21 pts)
- T23-T27: Backend TS (23 pts)
- T29-T30: Error & Logging (4 pts)

### **Phase 3: Book Import (30 pts, 2 tygodnie)**

- T37-T42: Ingestion Pipeline (24 pts)
- T45-T47: Status + Testing (11 pts)
- Pomiń: T43-T44 (semantic search - v1.1), T48-T49 (context/timeline)

### **Phase 4: Prompt & Image Gen (35 pts, 2.5 tygodnia)**

- T50-T55: Prompt Engineering (22 pts)
- T59-T60: Validation + Testing (7 pts)
- Pomiń: T56 (caching - v1.1), T57 (progress - nice-to-have), T58 (LoRA - v2)

### **Phase 5: Comic Assembly (40 pts, 2.5 tygodnia)**

- T61-T69: Full Production Pipeline (33 pts)
- T70: QC Dashboard (3 pts)
- T71: Testing (5 pts)
- Pomiń: T72-T73 (preview/variants - v1.1)

### **Phase 6: Launch (10 pts, 1 tydzień)**

- T91: Final Testing (5 pts)
- T92: Production Deploy (3 pts)
- T93: Release Notes (2 pts)

**Total MVP: ~170 punktów (zamiast 333)** **Timeline: ~11 tygodni (2.5 miesiąca)
przy 1 dev @ 30 pts/tydzień**

---

## 💡 Recommenda

cje dla Startupu

### **Priorytet 1: Ship Fast (MVP w 3 miesiące)**

1. ✅ Usuń: E6 (Distribution), większość E7 (Ecommerce)
2. ✅ Użyj Gumroad dla płatności ($10/m, 0 setup)
3. ✅ Uproszcz setup (połowa E1)
4. ✅ Pomiń advanced ML features (T34-T36)
5. ✅ Core flow: Upload → Process → Generate → Download

### **Priorytet 2: Validate PMF (Product-Market Fit)**

1. Ship MVP do 10 beta userów
2. Zobacz czy płacą (Gumroad link)
3. Zbierz feedback na core flow
4. Dopiero **wtedy** dodawaj:
   - Discord integration (jeśli community się tworzy)
   - Advanced search (jeśli users tego chcą)
   - Custom payment flow (jeśli Gumroad problematic)

### **Priorytet 3: Dobra Architektura, Ale Nie Overkill**

✅ **Zostaw:**

- Testing infrastructure
- CI/CD
- Monitoring (basic)
- Security (GDPR, RLS)
- Error handling

❌ **Usuń:**

- Storybook
- Performance budgets
- SLA/SLO/SLI
- Complex monitoring
- Mock modes

---

## 📝 Action Items

### **Opcja A: Agresywna redukcja (recommended)**

Stwórz `planning/pi-mvp.yaml` z 48 taskami:

```bash
pnpm pi:validate planning/pi-mvp.yaml
```

**Effort: ~170 punktów** **Timeline: 11 tygodni @ 1 dev, 30pts/week** **lub: 6
tygodni @ 2 devs**

### **Opcja B: Moderate cut**

Usuń tylko E6+E7, uproszcz E1: **Effort: ~240 punktów** **Timeline: 16 tygodni @
1 dev**

### **Opcja C: Keep everything (not recommended)**

**Effort: 333 punkty** **Timeline: 23 tygodnie (5.5 miesiąca) @ 1 dev** **Risk:
Konkurencja wypuści MVP szybciej**

---

## 🎪 Type Classification Summary

**Z 93 tasków:**

- **~25 Features** (user-facing): T37-T45, T50-T55, T59, T62-T64, T66-T70,
  T72-T73, T83, T87
- **~65 Tasks** (infrastructure): Setup, backend, ML, testing, deployment
- **~3 Epics można usunąć** (E6, większość E7, połowa E1)

**Dla startupu:**

- **Focus na 15-20 key features** (core value prop)
- **Support z 30-40 taskami** (infrastructure)
- **Total: ~50 tasków zamiast 93**

---

## ⚡ Quick Win: Start Tu

**Week 1-2: Setup Basics (zamiast 18 tasków → 5 tasków)**

```yaml
- T3: Database Schema (5 pts)
- T4: Testing Infrastructure (3 pts)
- T6: CI/CD (3 pts)
- T12: Basic Monitoring (3 pts)
- T13: Security essentials (3 pts)
```

**Week 3-5: ML Backend (choose path)**

- Path A: Port existing Python → TS (T23, 8 pts)
- Path B: Keep Python API, thin TS wrapper (4 pts)

**Week 6-8: Core Flow**

- Upload → Extract → Generate → Assemble

**Week 9-11: Polish & Launch**

- Testing, deployment, docs

**🚀 MVP in Market: Week 12**

---

**Decyzja należy do Ciebie. Ale pamiętaj: "Perfect is the enemy of shipped."**

Chcesz żebym wygenerował `planning/pi-mvp.yaml` z 48 taskami?
