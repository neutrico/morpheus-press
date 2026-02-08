---
area: distribution
dependsOn:
- T77
effort: 3
iteration: I6
key: T78
milestone: M6 - Commerce & Distribution
priority: p1
title: Extension Comics Viewer
type: Task
---

# Extension Comics Viewer

## Acceptance Criteria

- [ ] **Extension successfully authenticates users with existing Morpheus accounts**
  - Verification: Manual test: Install extension, click popup, login with test account, verify authentication state persists
- [ ] **Users can view their purchased comics library in the extension popup**
  - Verification: Manual test: After login, popup displays list of purchased comics with thumbnails and titles from API
- [ ] **Comics open in dedicated reader tabs with full navigation controls**
  - Verification: Manual test: Click comic from popup, new tab opens with reader showing pages, navigation arrows work
- [ ] **Comic pages load progressively without blocking the UI**
  - Verification: Performance test: Monitor network tab, verify pages load in chunks, UI remains responsive during loading
- [ ] **Extension works offline for previously cached comics**
  - Verification: Manual test: Read comic online, disconnect internet, reopen comic, verify pages still display

## Technical Notes

### Approach

Create a new Turborepo workspace for the browser extension using React and TypeScript. Extract comic viewer components from the storefront into shared packages. Implement a Chrome extension with popup interface for library browsing and dedicated tabs for comic reading. Use Chrome Storage API for metadata sync and IndexedDB for comic page caching. Create extension-specific API endpoints in the Fastify backend with proper CORS configuration and Supabase Auth integration adapted for extension context.


### Files to Modify

- **path**: packages/ui/src/comic-viewer/ComicViewer.tsx
- **changes**: Extract into extension-compatible component, remove Next.js dependencies
- **path**: packages/auth/src/supabase.ts
- **changes**: Add extension-specific auth methods and session management
- **path**: apps/api/src/routes/comics.ts
- **changes**: Add CORS headers for extension origin, extension-specific endpoints

### New Files to Create

- **path**: apps/extension/manifest.json
- **purpose**: Chrome extension manifest V3 configuration
- **path**: apps/extension/src/background/service-worker.ts
- **purpose**: Handle API calls, auth state, and cross-tab communication
- **path**: apps/extension/src/popup/Popup.tsx
- **purpose**: Main popup interface for library browsing
- **path**: apps/extension/src/reader/Reader.tsx
- **purpose**: Full-page comic reader component
- **path**: apps/extension/src/services/storage.ts
- **purpose**: Chrome storage API wrapper and caching logic
- **path**: apps/extension/src/services/comics-sync.ts
- **purpose**: Sync purchased comics metadata with backend
- **path**: apps/extension/webpack.config.js
- **purpose**: Webpack configuration for extension build
- **path**: packages/extension-auth/src/index.ts
- **purpose**: Shared authentication utilities for extension context
- **path**: apps/api/src/routes/extension/auth.ts
- **purpose**: Extension-specific authentication endpoints
- **path**: apps/api/src/routes/extension/comics.ts
- **purpose**: Extension-optimized comics API with metadata focus

### External Dependencies


- **@types/chrome** ^0.0.246

  - TypeScript definitions for Chrome extension APIs

- **webextension-polyfill** ^0.10.0

  - Cross-browser compatibility for extension APIs with Promise support

- **@crxjs/vite-plugin** ^2.0.0

  - Vite plugin for building Chrome extensions with HMR support

- **idb** ^7.1.1

  - IndexedDB wrapper for efficient comic page storage and retrieval

## Testing

### Unit Tests

- **File**: `apps/extension/src/__tests__/auth.test.ts`
  - Scenarios: Successful authentication flow, Token refresh handling, Logout cleanup, Authentication errors
- **File**: `apps/extension/src/__tests__/storage.test.ts`
  - Scenarios: Comics metadata sync, Page caching and retrieval, Storage quota management, Cache invalidation
### Integration Tests

- **File**: `apps/extension/src/__tests__/integration/reader.test.ts`
  - Scenarios: Full comic reading flow, Cross-tab communication, API integration with auth
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1.5
- **Testing**: 2
- **Documentation**: 1
- **Total**: 12.5

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup extension workspace and build configuration
- **done**: False
- **task**: Extract and adapt comic viewer components to shared package
- **done**: False
- **task**: Implement extension authentication service with Supabase integration
- **done**: False
- **task**: Create popup interface with comics library display
- **done**: False
- **task**: Build comic reader tab with progressive loading
- **done**: False
- **task**: Implement Chrome storage integration and offline caching
- **done**: False
- **task**: Add extension-specific API endpoints with CORS support
- **done**: False
- **task**: Create background service worker for cross-tab communication
- **done**: False
- **task**: Comprehensive testing across Chrome extension contexts
- **done**: False
- **task**: Documentation and deployment preparation
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task involves building a browser extension that allows users to read comics purchased through the Morpheus platform directly in their browser. This is critical for M6 (Commerce & Distribution) as it provides a seamless reading experience post-purchase, potentially increasing user engagement and retention. The extension would integrate with the existing comic viewer from the storefront but as a standalone reading application, similar to how Kindle Cloud Reader works for eBooks.

**Technical Approach:**
Build a Manifest V3 browser extension using React + TypeScript with a popup interface and dedicated comic reader tab/window. Use the existing comic viewer components from the Next.js storefront as a foundation. Implement secure authentication via Supabase Auth with extension-specific session management. Create a dedicated comics sync service that fetches purchased comics metadata and handles offline caching using Chrome Storage API. Implement progressive loading for comic pages to optimize performance.

**Dependencies:**
- External: @types/chrome@^0.0.246, webextension-polyfill@^0.10.0, react@^18, @supabase/supabase-js@^2
- Internal: Shared UI components from storefront, authentication utilities, comic viewer components, API client for Morpheus backend

**Risks:**
- Cross-origin security: Chrome's strict CSP policies may block image loading from Supabase storage
- Storage limitations: Chrome extension storage limits may impact offline comic caching
- Authentication complexity: Managing Supabase sessions across extension contexts (popup, content script, background)
- Performance issues: Large comic files may cause memory issues in extension context

**Complexity Notes:**
This is more complex than initially estimated due to browser extension security constraints, cross-origin policies, and the need to adapt existing React components to extension architecture. The authentication flow alone requires significant custom work to bridge Supabase Auth with Chrome extension APIs.

**Key Files:**
- apps/extension/: New workspace for the browser extension
- apps/extension/src/popup/: React-based popup interface
- apps/extension/src/background/: Service worker for API calls and auth
- apps/extension/src/content/: Content scripts if needed
- packages/ui/comic-viewer/: Extract and adapt existing comic viewer components
- apps/api/src/routes/extension/: New API endpoints for extension-specific needs


### Design Decisions

[{'decision': 'Use Manifest V3 with React in popup and separate reader tab', 'rationale': 'Manifest V3 is required for Chrome Web Store, React provides familiar development experience and component reuse from storefront', 'alternatives_considered': ['Vanilla JS popup', 'Single-page extension in popup only', 'Manifest V2']}, {'decision': 'Chrome Storage API for comic metadata caching with IndexedDB for large assets', 'rationale': 'Chrome Storage syncs across devices, IndexedDB handles large comic page images efficiently', 'alternatives_considered': ['localStorage only', 'Chrome Storage for everything', 'External cloud sync']}, {'decision': 'Dedicated extension API endpoints with CORS-enabled authentication', 'rationale': 'Extensions need specific CORS headers and may require different auth flows than web apps', 'alternatives_considered': ['Reuse existing API endpoints', 'Proxy through background script', 'Direct Supabase calls']}]
