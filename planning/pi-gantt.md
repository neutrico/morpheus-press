# PI-2026-Q1 Gantt Chart & Dependency Graph

**Generated:** 2026-02-07 **Timeline:** 2026-02-10 to 2026-06-23 (19 weeks, 7
iterations)

---

## 📅 Timeline Overview (Iteracje)

```mermaid
gantt
    title PI-2026-Q1 Timeline by Milestone
    dateFormat YYYY-MM-DD
    
    section M0: Setup
    I1 Setup (18 tasks, 50 pts)     :i1, 2026-02-10, 14d
    
    section M1: ML Backend
    I2 Dialogue DB (18 tasks, 72 pts) :i2, after i1, 14d
    
    section M2: Book Import
    I3 Ingestion (13 tasks, 56 pts)   :i3, after i2, 14d
    
    section M3: Prompt Gen
    I4 Image Gen (11 tasks, 41 pts)   :i4, after i3, 14d
    
    section M4: Comic MVP
    I5 Comic Asm (13 tasks, 47 pts)   :i5, after i4, 14d
    
    section M5+M6: Dist+Ecom
    I6 Distribution (17 tasks, 60 pts) :i6, after i5, 14d
    
    section M7: Release
    I7 Launch (3 tasks, 10 pts)       :i7, after i6, 14d
```

---

## 🏗️ Epic Dependencies (High-Level)

```mermaid
graph LR
    E1[E1: Setup<br/>18 tasks<br/>50 pts]
    E2[E2: ML Backend<br/>18 tasks<br/>59 pts]
    E3[E3: Book Import<br/>13 tasks<br/>56 pts]
    E4[E4: Prompt Gen<br/>11 tasks<br/>41 pts]
    E5[E5: Comic MVP<br/>13 tasks<br/>47 pts]
    E6[E6: Distribution<br/>9 tasks<br/>31 pts]
    E7[E7: Ecommerce<br/>8 tasks<br/>29 pts]
    E8[E8: Release<br/>3 tasks<br/>10 pts]
    
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> E5
    E5 --> E6
    E5 --> E7
    E6 --> E8
    E7 --> E8
    
    style E1 fill:#e1f5ff
    style E2 fill:#fff3cd
    style E3 fill:#d4edda
    style E4 fill:#f8d7da
    style E5 fill:#d1ecf1
    style E6 fill:#e2e3e5
    style E7 fill:#e2e3e5
    style E8 fill:#c3e6cb
```

---

## 📦 Feature Timeline (Core Value Props)

```mermaid
gantt
    title Core Features Development Timeline
    dateFormat YYYY-MM-DD
    
    section Book Upload
    T37 Wolne Lektury API     :f1, 2026-03-10, 3d
    T38 Book Upload Handler   :f2, 2026-03-10, 3d
    T39 Chapter Extraction    :f3, after f2, 5d
    
    section ML Processing
    T41 Scene Extraction      :f4, after f3, 5d
    T42 Character Profiling   :f5, after f3, 5d
    T44 Semantic Search       :f6, after f4, 5d
    
    section Image Generation
    T50 Prompt Engineering    :f7, 2026-04-07, 5d
    T51 Character Description :f8, 2026-04-07, 3d
    T52 Batch Image Gen       :f9, after f7, 5d
    T54 Image Quality Check   :f10, after f9, 3d
    
    section Comic Assembly
    T63 Comic Layout          :f11, 2026-05-05, 5d
    T64 Panel Generation      :f12, after f11, 5d
    T66 PDF Generation        :f13, after f12, 5d
    T67 Download Manager      :f14, after f13, 3d
```

---

## 🔄 Critical Path Analysis

**Longest dependency chain (Critical Path):**

```mermaid
graph TD
    Start([Start: 2026-02-10]) --> T3[T3: Database Schema<br/>5 pts]
    T3 --> T24[T24: Supabase Setup<br/>5 pts]
    T24 --> T25[T25: API Routes<br/>5 pts]
    T25 --> T37[T37: Wolne Lektury API<br/>3 pts]
    T37 --> T38[T38: Book Upload<br/>3 pts]
    T38 --> T39[T39: Chapter Extraction<br/>5 pts]
    T39 --> T40[T40: Text Preprocessing<br/>5 pts]
    
    T19[T19: Dataset Prep<br/>5 pts] --> T21[T21: Dialogue Training<br/>8 pts]
    T21 --> T41[T41: Scene Extraction<br/>5 pts]
    
    T40 --> T41
    T41 --> T50[T50: Prompt Engineering<br/>5 pts]
    T50 --> T52[T52: Batch Image Gen<br/>5 pts]
    T52 --> T61[T61: ComfyUI Integration<br/>5 pts]
    T61 --> T64[T64: Panel Generation<br/>5 pts]
    T64 --> T66[T66: PDF Generation<br/>5 pts]
    T66 --> T91[T91: Final Testing<br/>5 pts]
    T91 --> T92[T92: Production Deploy<br/>3 pts]
    T92 --> End([Launch: 2026-06-23])
    
    Start --> T19
    
    style T3 fill:#ff6b6b
    style T41 fill:#ff6b6b
    style T50 fill:#ff6b6b
    style T64 fill:#ff6b6b
    style T66 fill:#ff6b6b
    style T92 fill:#ff6b6b
```

**Critical Path Duration:** ~75 effort points on critical dependencies

---

## 📊 Resource Allocation by Iteration

```mermaid
gantt
    title Capacity vs Actual Effort by Iteration
    dateFormat YYYY-MM-DD
    
    section Capacity (30 pts)
    Capacity Line :milestone, m1, 2026-02-10, 0d
    Capacity Line :milestone, m2, 2026-02-24, 0d
    Capacity Line :milestone, m3, 2026-03-10, 0d
    Capacity Line :milestone, m4, 2026-03-24, 0d
    Capacity Line :milestone, m5, 2026-04-07, 0d
    Capacity Line :milestone, m6, 2026-04-21, 0d
    Capacity Line :milestone, m7, 2026-05-05, 0d
    
    section I1 (50 pts) ⚠️
    Setup Tasks :crit, i1_work, 2026-02-10, 14d
    
    section I2 (72 pts) ⚠️
    ML + Backend :crit, i2_work, 2026-02-24, 14d
    
    section I3 (56 pts) ⚠️
    Book Import :crit, i3_work, 2026-03-10, 14d
    
    section I4 (41 pts) ⚠️
    Prompt Gen :crit, i4_work, 2026-03-24, 14d
    
    section I5 (47 pts) ⚠️
    Comic Asm :crit, i5_work, 2026-04-07, 14d
    
    section I6 (60 pts) ⚠️
    Dist+Ecom :crit, i6_work, 2026-04-21, 14d
    
    section I7 (10 pts) ✅
    Release :i7_work, 2026-05-05, 14d
```

**⚠️ Wszystkie iteracje (poza I7) przekraczają capacity 30 pts!**

---

## 🎯 MVP Recommendation (Simplified)

**Zredukowany do 48 tasków, ~170 punktów:**

```mermaid
gantt
    title MVP Timeline (48 tasks, 170 pts, 11 weeks)
    dateFormat YYYY-MM-DD
    
    section Phase 1: Core Infra
    Setup (5 tasks, 15 pts)        :p1, 2026-02-10, 7d
    
    section Phase 2: ML Backend
    ML Training (21 pts)           :p2, after p1, 14d
    Backend TS (23 pts)            :p2b, after p1, 14d
    
    section Phase 3: Book Import
    Ingestion (30 pts)             :p3, after p2, 14d
    
    section Phase 4: Image Gen
    Prompt Gen (35 pts)            :p4, after p3, 14d
    
    section Phase 5: Comic
    Assembly (40 pts)              :p5, after p4, 14d
    
    section Phase 6: Launch
    Testing+Deploy (10 pts)        :p6, after p5, 7d
```

**Total MVP: 11 tygodni (2.5 miesiąca) zamiast 19 tygodni (4.5 miesiąca)**

---

## 📈 Capacity Analysis

| Iteration | Planned | Capacity | Over | % Over   |
| --------- | ------- | -------- | ---- | -------- |
| **I1**    | 50 pts  | 30 pts   | +20  | +67% ⚠️  |
| **I2**    | 72 pts  | 30 pts   | +42  | +140% 🚨 |
| **I3**    | 56 pts  | 30 pts   | +26  | +87% ⚠️  |
| **I4**    | 41 pts  | 30 pts   | +11  | +37% ⚠️  |
| **I5**    | 47 pts  | 30 pts   | +17  | +57% ⚠️  |
| **I6**    | 60 pts  | 30 pts   | +30  | +100% 🚨 |
| **I7**    | 10 pts  | 30 pts   | -20  | -67% ✅  |
| **Total** | 333 pts | 210 pts  | +123 | +59%     |

**Rozwiązania:**

1. Zwiększ capacity: 30 → 50 pts/iteracja (2 devs)
2. Rozciągnij timeline: 7 → 11 iteracji (22 tygodnie)
3. Usuń features: 333 → 170 pts MVP (7 iteracji zostaje)

---

## 🔗 Task Dependencies (Sample - E3 Book Import)

```mermaid
graph TD
    T37[T37: Wolne Lektury API<br/>feature, 3 pts] --> T39
    T38[T38: Book Upload<br/>feature, 3 pts] --> T39[T39: Chapter Extract<br/>feature, 5 pts]
    T39 --> T40[T40: Text Preprocess<br/>task, 5 pts]
    T40 --> T41[T41: Scene Extract<br/>feature, 5 pts]
    T40 --> T42[T42: Character Profile<br/>feature, 5 pts]
    T41 --> T43[T43: Embeddings<br/>task, 3 pts]
    T42 --> T43
    T43 --> T44[T44: Semantic Search<br/>feature, 5 pts]
    T38 --> T45[T45: Book Status<br/>feature, 3 pts]
    T40 --> T48[T48: Cultural Context<br/>feature, 5 pts]
    T41 --> T49[T49: Timeline<br/>feature, 3 pts]
    
    style T37 fill:#d4edda
    style T38 fill:#d4edda
    style T39 fill:#d4edda
    style T40 fill:#f8f9fa
    style T41 fill:#d4edda
    style T42 fill:#d4edda
    style T43 fill:#f8f9fa
    style T44 fill:#d4edda
    style T45 fill:#d4edda
    style T48 fill:#d4edda
    style T49 fill:#d4edda
```

**Legend:**

- 🟢 Green = Feature (user-facing)
- ⚪ Gray = Task (infrastructure)

---

## 💡 Quick Stats

- **Total Duration:** 19 weeks (133 days)
- **Start Date:** 2026-02-10
- **Target Launch:** 2026-06-23
- **Total Effort:** 333 points
- **Avg per Iteration:** 47.6 pts (59% over capacity)
- **Critical Path:** ~75 pts (depends on
  T3→T24→T25→T38→T39→T40→T41→T50→T52→T61→T64→T66→T92)

**Recommendations:**

1. 🚨 Zwiększ team size (2 devs @ 30 pts = 60 pts/iteracja)
2. ⚠️ Lub upraszczaj do MVP (usuń E6, E7, połowa E1)
3. ✅ Lub rozciągnij timeline do 22 tygodni

---

**Więcej szczegółów:**

- [planning/pi.yaml](pi.yaml) - Single source of truth
- [planning/pi-tree.md](pi-tree.md) - Hierarchia tasków
- [planning/pi-schedule.md](pi-schedule.md) - Podział na iteracje
- [planning/PI_ANALYSIS.md](PI_ANALYSIS.md) - Analiza MVP
