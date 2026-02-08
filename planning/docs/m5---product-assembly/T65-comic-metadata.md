---
area: comic
dependsOn: []
effort: 2
iteration: I5
key: T65
milestone: M5 - Product Assembly
priority: p0
title: Comic Metadata
type: Task
---

# Comic Metadata

## Acceptance Criteria

- [ ] **Comic metadata is automatically extracted and stored during generation with title, author, genre, page count, creation date, and technical details**
  - Verification: Generate new comic via ML pipeline, verify metadata populated in database with SELECT * FROM comic_metadata WHERE comic_id = ?;
- [ ] **Dashboard comic editor allows manual metadata editing with real-time updates across platform**
  - Verification: Edit comic metadata in dashboard, verify changes appear in storefront within 2 seconds without page refresh
- [ ] **Full-text search returns relevant comics within 500ms for catalogs up to 10,000 comics**
  - Verification: Load test with 10k comics, measure search response time with 'EXPLAIN ANALYZE SELECT * FROM comics_search_view WHERE search_vector @@ plainto_tsquery(?);'
- [ ] **Comic cards display rich metadata including ratings, progress, and structured data for SEO**
  - Verification: Check storefront comic cards show all metadata fields, validate JSON-LD with Google's Structured Data Testing Tool
- [ ] **API provides CRUD operations for metadata with proper validation and error handling**
  - Verification: Test all API endpoints with invalid data, verify zod validation errors returned with 400 status codes

## Technical Notes

### Approach

Create a comprehensive comic metadata system with a PostgreSQL schema supporting both structured searchable fields and flexible JSONB extensions. Integrate metadata generation into the comic creation pipeline while providing dashboard editing capabilities. Implement full-text search with proper indexing for performance. Use Supabase real-time subscriptions for live metadata updates across the platform and structured data markup for SEO optimization.


### Files to Modify

- **path**: packages/database/supabase/migrations/20240115000000_comic_metadata.sql
- **changes**: Create comic_metadata table, indexes, RLS policies, search view
- **path**: packages/shared/types/comic.ts
- **changes**: Add ComicMetadata, ComicMetadataInput, SearchableMetadata interfaces
- **path**: apps/api/src/routes/comics/index.ts
- **changes**: Add metadata CRUD endpoints, integrate search functionality
- **path**: packages/ml/src/comic-generator/pipeline.ts
- **changes**: Add metadata extraction step using sharp for image analysis
- **path**: apps/dashboard/src/components/ComicEditor/ComicEditor.tsx
- **changes**: Add metadata editing form with real-time validation
- **path**: apps/storefront/src/components/ComicCard/ComicCard.tsx
- **changes**: Display rich metadata, add structured data markup

### New Files to Create

- **path**: packages/shared/src/schemas/comic-metadata.ts
- **purpose**: Zod validation schemas for metadata
- **path**: apps/api/src/services/metadata-service.ts
- **purpose**: Business logic for metadata operations and search
- **path**: apps/api/src/services/metadata-extraction.ts
- **purpose**: Extract technical metadata from comic files
- **path**: apps/api/src/utils/search-builder.ts
- **purpose**: Build PostgreSQL full-text search queries
- **path**: apps/storefront/src/utils/structured-data.ts
- **purpose**: Generate JSON-LD structured data for SEO
- **path**: packages/shared/src/hooks/useComicMetadata.ts
- **purpose**: React hook for metadata operations with real-time updates

### External Dependencies


- **zod** ^3.22.0

  - Runtime validation for metadata schemas and API payloads

- **sharp** ^0.33.0

  - Extract technical metadata from generated comic images

- **@types/mime-types** ^2.1.4

  - File type detection for comic assets

- **date-fns** ^2.30.0

  - Consistent date formatting and manipulation for metadata

## Testing

### Unit Tests

- **File**: `packages/shared/src/__tests__/comic-metadata.test.ts`
  - Scenarios: Metadata validation with zod schemas, Type safety for ComicMetadata interfaces, Default value generation, Invalid metadata handling
- **File**: `apps/api/src/routes/comics/__tests__/metadata.test.ts`
  - Scenarios: CRUD operations success paths, Authorization checks, Database constraint violations, Search query building
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/comic-metadata-flow.test.ts`
  - Scenarios: Comic generation to metadata storage pipeline, Real-time metadata updates via Supabase, Search indexing after metadata changes, File upload with metadata extraction
### Manual Testing


## Estimates

- **Development**: 4
- **Code Review**: 1
- **Testing**: 1.5
- **Documentation**: 0.5
- **Total**: 7

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Design database schema with proper indexing strategy
- **done**: False
- **task**: Create TypeScript interfaces and zod validation schemas
- **done**: False
- **task**: Implement metadata service with CRUD operations
- **done**: False
- **task**: Integrate metadata extraction into comic generation pipeline
- **done**: False
- **task**: Build dashboard metadata editing interface
- **done**: False
- **task**: Add metadata display to storefront comic cards
- **done**: False
- **task**: Implement full-text search with PostgreSQL
- **done**: False
- **task**: Add SEO structured data markup
- **done**: False
- **task**: Set up real-time subscriptions for metadata updates
- **done**: False
- **task**: Performance testing and optimization
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Comic metadata is essential for organizing, searching, displaying, and managing comics in the Morpheus platform. This includes title, author, genre, creation date, page count, reading progress, tags, ratings, and technical details like image formats and resolutions. Proper metadata enables the storefront to show rich comic information, allows users to track reading progress, enables search/filtering functionality, and supports SEO optimization for public comics.

**Technical Approach:**
Implement a comprehensive metadata schema in PostgreSQL with proper indexing for search performance. Use Supabase's real-time features for metadata updates. Create TypeScript interfaces for type safety across frontend/backend. Implement metadata extraction during comic generation pipeline, with manual override capabilities in the dashboard. Use structured data (JSON-LD) for SEO and social media sharing. Consider EPUB/CBZ metadata standards for potential export features.

**Dependencies:**
- External: zod (validation), sharp (image analysis), @types/mime-types, structured-data-testing-tool
- Internal: Database schema migrations, comic generation pipeline, search service, user management system, file storage service

**Risks:**
- Schema evolution: Use flexible JSONB fields for extensible metadata alongside structured columns
- Performance with large catalogs: Implement proper database indexing strategy and pagination
- Metadata consistency: Validate metadata at API boundaries and during generation pipeline
- Search complexity: Consider PostgreSQL full-text search vs external search service (Algolia/ElasticSearch)

**Complexity Notes:**
This is more complex than initially thought due to the need for both structured searchable fields and flexible extensible metadata. The integration with the comic generation pipeline adds complexity, as does the requirement for real-time updates across dashboard and storefront.

**Key Files:**
- packages/database/migrations/: Add comic_metadata table and indexes
- packages/shared/types/comic.ts: Define ComicMetadata interfaces
- apps/api/src/routes/comics/: Metadata CRUD endpoints
- apps/dashboard/src/components/ComicEditor/: Metadata editing forms
- apps/storefront/src/components/ComicCard/: Display metadata
- packages/ml/src/comic-generator/: Integrate metadata creation


### Design Decisions

[{'decision': 'Hybrid metadata storage using both structured PostgreSQL columns and JSONB fields', 'rationale': 'Structured columns for searchable/filterable fields (title, author, genre, created_at) with JSONB for extensible custom metadata and technical details', 'alternatives_considered': ['Pure JSONB storage', 'Separate metadata tables', 'External metadata service']}, {'decision': 'Generate metadata during comic creation pipeline with manual override capability', 'rationale': 'Ensures all comics have consistent metadata while allowing user customization for published works', 'alternatives_considered': ['Manual-only metadata entry', 'Post-generation metadata extraction', 'AI-generated metadata only']}]
