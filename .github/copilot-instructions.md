# Morpheus - AI Agent Instructions

> Novel-to-comic transformation platform: Upload book → LLM extracts
> scenes/characters → Stable Diffusion generates art → Download printable comic

## Instruction Priority

When instructions conflict, follow this order:

1. User request (highest priority)
2. This repository instructions (this file)
3. Global/system instructions

## Code Quality Principles

**You are a Senior Developer** - Always follow these principles:

**🚨 MANDATORY: ALL generated code MUST follow SOLID, KISS, and DRY principles**

**SOLID Principles:**

- **Single Responsibility**: One component/function = one purpose
- **Open/Closed**: Extend via composition, not modification
- **Liskov Substitution**: Derived types must be substitutable
- **Interface Segregation**: Small, focused interfaces over large ones
- **Dependency Inversion**: Depend on abstractions, not concretions

**Core Best Practices:**

- **DRY** (Don't Repeat Yourself): Extract reusable logic, avoid duplication
- **KISS** (Keep It Simple, Stupid): Simplest solution that works
- **Separation of Concerns**: UI ≠ business logic ≠ data fetching

**Code Generation Rules:**

- ✅ Extract duplicated code into functions/constants/components
- ✅ Keep functions small and focused (Single Responsibility)
- ✅ Use descriptive names that explain intent
- ✅ Favor composition over inheritance
- ✅ Write code that's easy to test and maintain
- ❌ NO copy-paste programming - refactor duplicates
- ❌ NO god classes/functions doing too many things
- ❌ NO magic numbers/strings - use named constants

**React Performance:**

- ✅ Use `React.memo()` for expensive components
- ✅ `useMemo()` for expensive calculations
- ✅ `useCallback()` for functions passed as props
- ✅ Avoid inline functions/objects in JSX props
- ✅ Keep state as close as possible to where it's used
- ✅ Split large components into smaller ones
- ❌ NO unnecessary rerenders - always check deps arrays
- ❌ NO object/array literals as props (causes rerender)

**Fastify Backend Specifics:**

- ✅ Services are singletons injected via constructor DI
- ✅ Routes are async functions registered via `app.register()`
- ✅ Use typed Zod schemas for request/response validation
- ✅ Always add error handlers to routes (try/catch with proper status codes)
- ✅ Log structured data: `fastify.log.info({ userId, action, details })`
- ❌ NO middleware for cross-cutting concerns; use plugins instead
- ❌ NO direct Supabase calls in routes; use `DatabaseService`
- ❌ NO hard-coded model names; use config/env variables

**Before committing code, verify:**

1. Does it follow SOLID principles?
2. Is there any duplication (DRY)?
3. Is it as simple as possible (KISS)?
4. Are concerns properly separated?
5. Will React components rerender unnecessarily?
6. Can any function be split for better readability?
7. Are all magic numbers/strings extracted to constants?

## Task Automation System

**🤖 CRITICAL: Check for pre-generated code before starting implementation!**

When assigned a task (issue), **ALWAYS CHECK FIRST** if starter code was
auto-generated:

### 1. Check for Auto-Generated PR

```bash
# Look for PR with "[AUTO-GENERATED]" tag linked to your issue
gh pr list --search "is:pr is:open label:auto-generated"
```

**If automation PR exists:**

- ✅ Use it as starting point (saves 30-50% time)
- ✅ Review TODO comments - these need manual implementation
- ✅ Verify business logic correctness
- ✅ Run tests: `pnpm test`
- ✅ Fix placeholder code
- ⚠️ **NEVER merge auto-generated code without review!**

### 2. Available Automation Tools

If NO auto-generated PR exists, you can trigger automation:

**Option A: Trigger via comment** (recommended):

```
# In the issue, comment:
/automate
```

**Option B: Manual CLI** (if you have access):

```bash
# Full automation (LLM-powered)
python scripts/automation/task-automation-agent.py T24

# Or use specific generators:
./scripts/automation/generators/setup-supabase.sh T24    # Database
./scripts/automation/generators/setup-tests.sh T27 unit  # Tests
python scripts/automation/generators/api-generator.py T25 # API routes
```

### 3. Task Patterns & Automation

**HIGH AI Effectiveness** (use automation):

- 🗄️ **Database setup** (migrations, RLS, indexes) → `setup-supabase.sh`
- 🧪 **Testing** (unit tests, fixtures, mocks) → `setup-tests.sh`
- 🔌 **API routes** (CRUD, Zod schemas, error handling) → `api-generator.py`
- 📚 **Documentation** (OpenAPI, READMEs) → manual with templates

**MEDIUM AI Effectiveness** (partial automation):

- ⚙️ **Integration work** → use templates + manual logic
- 🐛 **Debugging** → manual investigation required
- 🔧 **Refactoring** → automated suggestions + manual review

**LOW AI Effectiveness** (manual implementation):

- 🏗️ **Architecture decisions** → human judgment required
- 🧮 **Complex algorithms** → manual implementation
- 🎨 **UX design** → human creativity needed

### 4. Task Specification Locations

**Always read these FIRST before implementing:**

1. **Detailed Docs**: `planning/docs/[milestone]/[task-key]-*.md`
   - Full requirements
   - Acceptance criteria
   - Implementation notes

2. **Research Findings**: `planning/issues/*.yaml`
   - Look for `agent_notes.research_findings`
   - AI suitability analysis
   - Technical recommendations

3. **Estimations**: `planning/estimates/effort-map.yaml`
   - `estimated_days` (with AI acceleration)
   - `ai_effectiveness: high|medium|low`
   - Risk assessment

**Example workflow:**

```bash
# 1. Read task spec
cat planning/docs/m1---backend-services/T24-supabase-database-setup-with-rls.md

# 2. Check if automation exists
gh pr list --search "T24"

# 3. If yes: review PR
# 4. If no: trigger automation or implement manually
```

### 5. Working with Auto-Generated Code

**DO ✅:**

- ✅ Review ALL generated files before modifying
- ✅ Search for `TODO` comments - these are placeholders
- ✅ Run tests after changes: `pnpm test`
- ✅ Verify Zod schemas match database schema
- ✅ Check error handling is comprehensive
- ✅ Add logging for debugging
- ✅ Update auto-generated comments with actual implementation

**DON'T ❌:**

- ❌ Blindly accept generated code without review
- ❌ Skip tests - auto-generated tests may have placeholders
- ❌ Ignore TODO comments
- ❌ Merge without manual verification
- ❌ Assume business logic is correct

### 6. Automation Workflow (for reference)

```
GitHub Issue Created
         ↓
Assigned to @copilot OR comment /automate
         ↓
GitHub Actions Workflow Triggered
         ↓
Extract task key (T24, T25, etc.)
         ↓
Check AI effectiveness (effort-map.yaml)
         ↓
Run automation generator
         ↓
Create branch: automation/T24-YYYYMMDD
         ↓
Commit generated files
         ↓
Create PR with [AUTO-GENERATED] tag
         ↓
Assign PR to @copilot
         ↓
@copilot reviews + fixes TODOs
         ↓
Human review + approval
         ↓
Merge
```

### 7. Common Auto-Generated Patterns

**Database Setup (T24-style):**

- `supabase/migrations/YYYYMMDDHHMMSS_[task]_setup.sql`
- RLS policies (user-based access control)
- Indexes for performance
- Triggers for updated_at
- Grants for anon/authenticated roles

**API Routes (T25-style):**

- `apps/backend/src/routes/*.routes.ts`
- CRUD endpoints (GET, POST, PUT, DELETE)
- Zod request/response schemas
- Error handling (try/catch)
- Structured logging
- TODO: Database queries (you implement)

**Unit Tests (T27-style):**

- `apps/backend/src/__tests__/*.test.ts`
- Happy path tests
- Error handling tests
- Integration tests structure
- Fixtures in `__fixtures__/*.ts`
- TODO: Actual assertions (you implement)

### 8. When Automation Fails

If automation fails or generated code is unusable:

1. **Check automation log** in GitHub Actions
2. **Read task spec manually** from `planning/docs/`
3. **Implement manually** following patterns from similar tasks
4. **Report issue** if automation should have worked

**Fallback patterns:**

- Copy from similar completed task
- Use templates in `scripts/automation/templates/`
- Follow architecture in existing code

### 9. Automation Cost/Benefit

**Benefits:**

- ⏱️ 30-50% time savings on boilerplate
- ✅ Consistent code patterns
- 🧪 Test scaffolding included
- 📝 Reduces copy-paste errors

**Limitations:**

- ⚠️ Generated code needs review
- ⚠️ TODO comments require manual implementation
- ⚠️ Business logic may be placeholder
- ⚠️ Not suitable for LOW AI effectiveness tasks

**When to use:**

- ✅ HIGH AI effectiveness tasks (database, tests, CRUD APIs)
- ✅ Starting point for complex tasks
- ✅ When following established patterns

**When NOT to use:**

- ❌ Architecture/design decisions
- ❌ Novel algorithms
- ❌ UX/UI design work
- ❌ Tasks requiring deep domain knowledge

## Technology Stack

**Frontend & UI:**

- TypeScript + Next.js 16 + React (Dashboard @ :3000, Storefront @ :3001)
- shadcn/ui components (Dashboard)
- next-intl for i18n (Storefront)
- Tailwind CSS for styling
- React Query (`@tanstack/react-query`) for server state (Dashboard)

**Backend & API:**

- TypeScript + Fastify 5 (Backend API @ :3002)
- Supabase + PostgreSQL for database (port 54322 in Docker, +10000 offset in
  devcontainer)
- `@supabase/supabase-js` client (SSR via `lib/supabase/server.ts`, browser via
  `lib/supabase/client.ts`)
- Zod for validation (request/response schemas in `schemas/`)
- Pino for structured logging

**ML & Image Generation:**

- **LLM Providers**: OpenAI (GPT-4o, GPT-4o-mini) / Anthropic (Claude 3.5 Haiku
  recommended - best cost/quality)
- **Vector Embeddings**: OpenAI Embeddings API
- **Image Gen**: RunPod Stable Diffusion (serverless, API @
  `https://api.runpod.io/graphql`)
- **Propaganda Detection**: Custom ML models (PropagandaMLService, evaluated
  with Vitest)

**Python Usage** (limited scope only):

- ✅ RunPod deployment scripts (`scripts/*.py`)
- ✅ ML model evaluation (`train_model.py`, test evaluation tests)
- ✅ ComfyUI workflow automation
- ❌ NO Python for backend API logic
- ❌ NO Python for business logic
- ❌ NO Python for data processing (use TypeScript)

## Test-Driven Development (TDD)

**🚨 DEFAULT TDD WORKFLOW** - Apply for new features and business-logic changes:

**1. Test Planning Phase** (before coding):

- Create test scenarios covering happy path, edge cases, and errors
- Outline unit + E2E tests
- **GET USER APPROVAL** on test scenarios before implementation (unless user
  explicitly says to proceed)

**2. Implementation Phase**:

- Write unit tests FIRST (Red phase)
- Implement feature to pass tests (Green phase)
- Refactor while keeping tests green (Refactor phase)
- Add E2E tests for critical user flows

**3. Verification Phase** (before completing task):

- Run relevant tests for the scope of change
- Report test results to the user

**Fast-path (small changes)**:

- For docs/formatting/typos/small refactors with no logic changes:
  - Tests are optional unless user requests
  - Still report what was (or wasn't) run

**Test Coverage Requirements:**

- ✅ **MANDATORY**: Unit tests for all business logic
- ✅ **HIGHLY RECOMMENDED**: E2E tests for user-facing features
- ✅ Test services, utilities, and API routes
- ✅ Test error handling and edge cases
- ✅ Mock external dependencies (Supabase, OpenAI, RunPod)

**Testing Tools & Commands:**

- **Unit Tests**: Vitest (`pnpm test:backend`, `pnpm test` for all)
- **E2E Tests**: Playwright (`cd apps/dashboard && pnpm test:e2e`)
- **Component Tests**: React Testing Library + Vitest
- **Test Config**: [vitest.config.ts](apps/backend/vitest.config.ts) (node env),
  [storefront vitest.config.ts](apps/storefront/vitest.config.ts) (jsdom)

**Vitest-Specific Patterns:**

```typescript
// Mock external services using vi.fn()
vi.mock("../services/toxicity.service", () => ({
  ToxicityService: class {
    async analyzeToxicity(text: string) {
      return { score: 0.5 };
    }
  },
}));

// For routes, build Fastify instance
const app = await build();
const response = await app.inject({
  method: "POST",
  url: "/api/books",
  payload: { title: "Test" },
});

// Use describe.skipIf() for conditional tests
const SKIP = !process.env.OPENAI_API_KEY;
describe.skipIf(SKIP)("Expensive API tests", () => {
  // Only runs with API key set
});
```

**Example TDD Workflow:**

```typescript
// 1. Write test first
describe("ChapterAnalysisService", () => {
  it("should extract scenes from chapter text", async () => {
    const service = new ChapterAnalysisService(mockLlmProvider);
    const result = await service.analyzeChapter({ text: "Sample..." });
    expect(result.scenes).toHaveLength(3);
  });
});

// 2. Implement feature
class ChapterAnalysisService {
  async analyzeChapter(chapter) {
    // Implementation
  }
}

// 3. Verify all tests pass
// pnpm test
```

**Never skip testing** for business logic and behavior changes.

## Critical Environment Rules

**🐳 DevContainer + Docker-in-Docker Supabase** - ALWAYS remember:

- 🚨 **CRITICAL**: Supabase ports have **+10000 offset** in devcontainer → Use
  **64xxx NOT 54xxx**
- 🚨 **NEVER use ports starting with 54xxx** - they are NOT accessible in
  devcontainer!
- ❌ NO Prisma - Use `@supabase/supabase-js` directly
- ❌ NO manual server starts - Use **VSCode Launch Tasks** (F5); hot reload
  handles restarts
- ❌ NO destructive DB ops without asking - Always confirm before
  `DELETE`/`TRUNCATE`/`.env` changes
- ❌ NO middleware.ts in Storefront - Next.js 16 uses next-intl routing, NOT
  Supabase middleware
- ✅ Migrations in `supabase/migrations/YYYYMMDDHHMMSS_desc.sql` via
  `docker exec -i supabase-db psql -U postgres -d postgres < file.sql`
- ✅ All ports configured in **root `.env`** - single source of truth (see
  `docs/PORT_CONFIGURATION.md`)

**Supabase URLs in Docker/Devcontainer:**

- Server-side (backend API): `SUPABASE_URL=http://kong:8000` (Docker network,
  internal)
- Client-side (browser): `NEXT_PUBLIC_SUPABASE_URL=http://localhost:64321`
  (devcontainer offset)
- Dashboard/Storefront: `NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:64321` or
  `http://localhost:64321`

**🚨 ML Training Rules:**

- ❌ **NEVER TRAIN LOCALLY** - CPU training is too slow and blocks devcontainer
- ✅ **ALWAYS use RunPod GPU** - keep trying different approaches until it works
- ✅ RunPod troubleshooting: try different GPU types, datacenters, deployment
  methods
- ✅ If RunPod API fails: use `runpodctl` CLI, manual SSH, or dashboard
  deployment

**🚀 Common Development Commands:**

```bash
# Start dev environment (all apps: dashboard, storefront, backend)
pnpm dev

# Start only backend
pnpm dev:backend

# Run all tests
pnpm test

# Run backend tests only
pnpm test:backend

# Type check
pnpm type-check

# Build for production
pnpm build
```

## Performance & Best Practices

- Use `next/image` with proper width/height for all images
- Lazy load heavy components with `next/dynamic`
- Keep bundle sizes small - avoid importing entire libraries
- Use `loading.tsx` and `error.tsx` for loading states
- Prefer CSS for animations over JavaScript when possible
- Test responsiveness on mobile, tablet, and desktop

## Accessibility (A11y)

- Pixel fonts (Press Start 2P) only for headers and CTAs
- Use readable fonts (Silkscreen, Geist Sans) for body text
- Maintain 4.5:1 contrast ratio minimum
- Add proper ARIA labels to interactive elements
- Test keyboard navigation
- Ensure focus states are visible

## Git & Development

- Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`
- Test locally before committing
- Run `pnpm dev` from project root to start dev server
- Use `pnpm build` to verify production builds
- Check for TypeScript errors with `pnpm type-check`

**PR/Commit Workflow**:

- Only create commits or comment on PRs when explicitly asked
- Summarize changes and tests in the response

**Supabase URLs in Docker**:

- Server-side (API routes): `SUPABASE_URL=http://kong:8000` (Docker network)
- Client-side (browser): `NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321` (NOT
  54321!)

**Ports** (configured in root `.env`):

- Apps: Dashboard `:3000` | Storefront `:3001` | Backend `:3002` | Docs `:3003`
- Supabase: Studio `:54323` | API `:54321` | DB `:54322` | Inbucket `:54324` |
  Edge Runtime `:54327`

## Architecture Overview

```
apps/
├── backend/          # Fastify 5 + TypeScript
│   ├── src/
│   │   ├── routes/           # Route handlers (registered as plugins)
│   │   ├── services/         # Business logic services (30+ services)
│   │   ├── providers/        # LLM abstraction (OpenAI/Anthropic factory)
│   │   ├── validators/       # Toxicity, PII guardrails
│   │   ├── schemas/          # Zod request/response schemas
│   │   ├── types/database.ts # Auto-generated from Supabase schema
│   │   └── __tests__/        # Unit + integration tests (Vitest)
│   └── package.json
├── dashboard/        # Next.js 16 App Router
│   ├── app/          # Route segments + layouts
│   ├── components/   # shadcn/ui + custom components
│   ├── lib/          # Supabase client (server.ts, client.ts)
│   ├── __tests__/    # Component + page tests
│   └── e2e/          # Playwright E2E tests
├── storefront/       # Next.js 16 (i18n + Stripe)
│   ├── app/          # next-intl routing (NO middleware.ts!)
│   ├── components/   # Radix UI components
│   ├── lib/          # Supabase SSR auth
│   └── e2e/          # Playwright E2E tests
└── docs/             # Nextra documentation site

services/             # 30+ backend services for:
├── Database operations (DatabaseService)
├── LLM orchestration (ChapterAnalysisService, DialogueExtractionService)
├── Image generation (RunPodImageService, FalAiService)
├── Content safety (ToxicityService, PropagandaDetectorService)
├── Vector embeddings (EmbeddingService)
└── External APIs (WolneLekturyService, RunPodService)

**Data Flow: Book Upload → Analysis → Image Generation → Comic Assembly**
1. Dashboard: User uploads book → DatabaseService stores metadata
2. Backend: ChapterAnalysisService extracts scenes/characters via LLM
3. Backend: RunPodImageService generates images (Stable Diffusion)
4. Dashboard: Comic assembly UI shows progress + preview
```

## Database Patterns

```typescript
// Backend: apps/backend/src/services/database.ts
const db = new DatabaseService(userAccessToken); // RLS-enabled
const book = await db.getBook(id);

// Dashboard/Storefront: lib/supabase/server.ts (SSR) or client.ts (browser)
const supabase = await createClient();
const { data } = await supabase.from("Book").select("*");
```

Types: [types/database.ts](apps/backend/src/types/database.ts) (auto-generated
from Supabase schema)

**Database Naming Conventions** (Mixed - Historical):

- Core tables use PascalCase: `Book`, `Character`, `Scene`, `User`
- Feature tables use snake_case: `store_products`, `ml_training_sessions`
- **New tables**: Always use snake_case with prefixes (`store_*`, `ml_*`)
- TypeScript mapping: `user_subscriptions` → `UserSubscription` interface
- See
  [docs/DATABASE_NAMING_CONVENTIONS_ANALYSIS.md](docs/DATABASE_NAMING_CONVENTIONS_ANALYSIS.md)
  for full details

## LLM Provider Pattern

```typescript
// apps/backend/src/providers/factory.ts
const factory = new LlmProviderFactory({ openaiApiKey, anthropicApiKey });
const provider = factory.getProvider("openai"); // or 'anthropic'
const response = await provider.generateCompletion({ prompt, model });
```

Services use providers via routes: `routes/*.ts` → `services/*.ts` →
`providers/*.ts`

## Key Services

| Service                      | Purpose                               | Location                                                                                                                      |
| ---------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `DatabaseService`            | Supabase CRUD with RLS                | [backend/src/services/database.ts](apps/backend/src/services/database.ts)                                                     |
| `LlmProviderFactory`         | OpenAI/Anthropic abstraction          | [backend/src/providers/factory.ts](apps/backend/src/providers/factory.ts)                                                     |
| `RunPodImageService`         | Serverless SDXL generation            | [backend/src/services/runpod-image.service.ts](apps/backend/src/services/runpod-image.service.ts)                             |
| `EmbeddingService`           | Vector embeddings for semantic search | [backend/src/services/embedding.service.ts](apps/backend/src/services/embedding.service.ts)                                   |
| `ChapterAnalysisService`     | LLM scene/dialogue extraction         | [backend/src/services/chapter-analysis.service.ts](apps/backend/src/services/chapter-analysis.service.ts)                     |
| `PropagandaDetectorService`  | LLM-based propaganda analysis         | [backend/src/services/propaganda-detector.service.ts](apps/backend/src/services/propaganda-detector.service.ts)               |
| `ToxicityService`            | Content safety validation             | [backend/src/services/toxicity.service.ts](apps/backend/src/services/toxicity.service.ts)                                     |
| `DialogueExtractionPipeline` | Hybrid LLM + ML dialogue detection    | [backend/src/services/dialogue-extraction-hybrid.service.ts](apps/backend/src/services/dialogue-extraction-hybrid.service.ts) |
| `WolneLekturyService`        | Polish public domain book catalog     | [backend/src/services/wolne-lektury.ts](apps/backend/src/services/wolne-lektury.ts)                                           |
| `PreprocessingService`       | Text cleaning & normalization         | [backend/src/services/preprocessing.ts](apps/backend/src/services/preprocessing.ts)                                           |

## RunPod Integration

**GraphQL API**: `https://api.runpod.io/graphql` with
`Authorization: Bearer {RUNPOD_API_KEY}`

```python
# scripts/utils.py - RunPodClient handles deployment
from scripts.utils import RunPodClient
client = RunPodClient()  # Reads from .env

# Smart GPU selection: query gpuTypes, sort by lowestPrice, deploy cheapest available
```

Network Volume `ql5tygu36a` stores SD models; pods mount at
`/workspace/network-storage`

## Testing

```bash
pnpm test                         # All tests (Vitest)
pnpm test:backend                 # Backend only
cd apps/dashboard && pnpm test:e2e  # Playwright E2E
```

## Environment Variables

**Backend** uses `.env.local` (dev) / `.env.production` (prod):

```bash
# apps/backend/.env.local
PORT=3002
NODE_ENV=development
SUPABASE_URL=http://kong:8000        # Docker network in devcontainer
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
RUNPOD_API_KEY=rpa_...
```

**Dashboard/Storefront** use `.env.local` (dev):

```bash
# Client-side (browser)
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:64321
NEXT_PUBLIC_SUPABASE_ANON_KEY=...

# Server-side (Next.js in devcontainer)
SUPABASE_URL=http://kong:8000
SUPABASE_ANON_KEY=...

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:3002
```

## Common Patterns & Conventions

**Route Handlers** - Register routes as Fastify plugins:

```typescript
// apps/backend/src/routes/chapter-analysis.ts
export async function chapterAnalysisRoutes(fastify: FastifyInstance) {
  fastify.post<{ Body: AnalyzeChapterRequest }>(
    "/api/analyze-chapter",
    async (request, reply) => {
      try {
        const service = new ChapterAnalysisService(db);
        const result = await service.analyzeChapter(request.body);
        reply.status(200).send(result);
      } catch (error) {
        fastify.log.error(error);
        reply.status(500).send({ error: error.message });
      }
    },
  );
}
```

**Service Constructor Injection** - Services receive dependencies in
constructors:

```typescript
export class ChapterAnalysisService {
  constructor(
    private db: DatabaseService,
    private factory: LlmProviderFactory,
  ) {}

  async analyzeChapter(input: ChapterInput): Promise<ChapterOutput> {
    // Use injected dependencies
    const provider = this.factory.getProvider("openai");
    const book = await this.db.getBook(input.bookId);
    // ...
  }
}
```

**Response Validation** - Use Zod schemas for type safety:

```typescript
// apps/backend/src/schemas/chapter.ts
export const analyzeChapterSchema = z.object({
  bookId: z.string().uuid(),
  chapterText: z.string().min(100),
  model: z.enum(["gpt-4o", "gpt-4o-mini", "claude-3-5-haiku-20241022"]),
});

type AnalyzeChapterRequest = z.infer<typeof analyzeChapterSchema>;
```

## Architecture Patterns

**Monorepo with Turbo** - Single `pnpm` workspace, Turbo for task orchestration:

- `pnpm dev` - Runs all dev servers in parallel
- `pnpm build` - Builds all packages in dependency order
- `pnpm test` - Runs all tests across monorepo

**Service Layer Pattern** - Business logic stays in services, routes remain
thin:

```
routes/ (async HTTP handlers, request validation)
  ↓
services/ (business logic, DB queries, LLM calls)
  ↓
providers/ (external API abstractions)
  ↓
types/ (TypeScript interfaces, enums)
```

**Dependency Injection** - Services depend on abstractions, not concretions:

```typescript
// ✅ Good - Depends on abstraction
constructor(private llmProvider: LlmProvider) {}

// ❌ Bad - Hard-coded concrete dependency
constructor() { this.openai = new OpenAI(...); }
```

## Frontend Patterns (Dashboard & Storefront)

**Server Components by Default** - Next.js 16 uses Server Components:

```typescript
// ✅ Good - Runs on server
export default async function BookPage() {
  const book = await db.getBook(params.id); // Direct DB access
  return <BookDisplay book={book} />;
}

// ❌ Avoid - Unnecessary client component
"use client";
const [book, setBook] = useState(null);
useEffect(() => {
  fetchBook();
}, []);
```

**React Query for Data Fetching** (Dashboard only):

```typescript
function BookList() {
  const { data, isLoading } = useQuery({
    queryKey: ["books"],
    queryFn: () => fetch("/api/books").then((r) => r.json()),
  });

  if (isLoading) return <Skeleton />;
  return <ul>{data.map((b) => <li key={b.id}>{b.title}</li>)}</ul>;
}
```

**Form Handling with React Hook Form:**

```typescript
const form = useForm<BookFormData>({ resolver: zodResolver(bookSchema) });

// Zod schema validates on submit
const onSubmit = async (data: BookFormData) => {
  const result = await api.createBook(data);
  if (result.error) form.setError("title", { message: result.error });
};
```
