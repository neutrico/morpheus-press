---
area: distribution
dependsOn: []
effort: 5
iteration: I6
key: T77
milestone: M6 - Commerce & Distribution
priority: p1
title: Browser Extension
type: Task
---

# Browser Extension

## Acceptance Criteria

- [ ] **Extension allows users to select text on any webpage and transform it into a comic with one click**
  - Verification: Manual test: select text on 5 different websites (news, blog, social media), click extension icon, verify comic generation API is called and preview is shown
- [ ] **Extension authenticates users and syncs with main Morpheus platform account**
  - Verification: Manual test: login through extension popup, verify JWT token stored in chrome.storage.sync, test API calls include proper authentication headers
- [ ] **Extension works across Chrome, Edge, and Firefox with identical functionality**
  - Verification: Automated test: run extension test suite on all three browsers using webextension-polyfill compatibility layer
- [ ] **Content script performance does not degrade page load times by more than 50ms**
  - Verification: Performance test: measure page load time with/without extension on 10 popular websites using Chrome DevTools Performance API
- [ ] **Extension passes store review guidelines and security requirements**
  - Verification: Complete security audit checklist, test all permissions are justified, verify CSP compliance, submit to Chrome Web Store test environment

## Technical Notes

### Approach

Build a Manifest V3 browser extension with TypeScript, featuring a content script for text selection/extraction, a service worker background script for API communication, and a React-based popup interface. Leverage the existing Morpheus API through a shared client package, implement secure authentication via extension storage API, and use PostMessage for component communication. Package as separate builds for Chrome and Firefox with webextension-polyfill for compatibility.


### Files to Modify

- **path**: apps/api/src/routes/index.ts
- **changes**: Add extension routes import and mount at /api/extension
- **path**: packages/shared/src/types/index.ts
- **changes**: Export browser extension types and API interfaces
- **path**: packages/api-client/src/index.ts
- **changes**: Add extension-specific API client methods for authentication and comic generation

### New Files to Create

- **path**: apps/browser-extension/manifest.json
- **purpose**: Manifest V3 configuration with permissions for activeTab, storage, and host permissions
- **path**: apps/browser-extension/src/content-script.ts
- **purpose**: Inject UI overlay, handle text selection, communicate with background script
- **path**: apps/browser-extension/src/background.ts
- **purpose**: Service worker for API communication, storage management, tab coordination
- **path**: apps/browser-extension/src/popup/index.tsx
- **purpose**: React-based popup interface for quick transformations and account management
- **path**: apps/browser-extension/src/popup/components/TextPreview.tsx
- **purpose**: Component to show selected text and transformation options
- **path**: apps/browser-extension/src/popup/components/AuthPanel.tsx
- **purpose**: Handle login/logout and account status display
- **path**: apps/browser-extension/src/shared/messaging.ts
- **purpose**: Type-safe message passing between extension components
- **path**: apps/browser-extension/src/shared/storage.ts
- **purpose**: Wrapper for Chrome storage API with TypeScript types
- **path**: apps/browser-extension/webpack.config.js
- **purpose**: Build configuration for TypeScript compilation and asset bundling
- **path**: apps/browser-extension/package.json
- **purpose**: Extension-specific dependencies and build scripts
- **path**: apps/api/src/routes/extension/auth.ts
- **purpose**: Extension-specific authentication endpoints
- **path**: apps/api/src/routes/extension/transform.ts
- **purpose**: Text-to-comic transformation endpoint for extension
- **path**: packages/shared/src/browser-extension/types.ts
- **purpose**: Shared TypeScript interfaces for extension messages and data structures

### External Dependencies


- **webextension-polyfill** ^0.10.0

  - Cross-browser API compatibility between Chrome and Firefox

- **@types/chrome** ^0.0.254

  - TypeScript definitions for Chrome Extension APIs

- **react** ^18.2.0

  - UI framework for popup interface, consistent with main platform

- **@crxjs/vite-plugin** ^2.0.0

  - Vite integration for extension development and hot reload

## Testing

### Unit Tests

- **File**: `apps/browser-extension/src/__tests__/content-script.test.ts`
  - Scenarios: Text selection extraction from various DOM structures, Message passing between content script and background, Error handling for CSP-blocked operations, Performance with large text selections
- **File**: `apps/browser-extension/src/__tests__/background.test.ts`
  - Scenarios: API request proxying with authentication, Storage management for user preferences, Tab communication and activeTab permission handling
### Integration Tests

- **File**: `apps/browser-extension/src/__tests__/integration/extension-flow.test.ts`
  - Scenarios: Complete text-to-comic transformation flow, Authentication flow with OAuth redirect handling, Cross-browser compatibility with webextension-polyfill
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

- **task**: Setup browser extension app structure and webpack build configuration
- **done**: False
- **task**: Implement Manifest V3 configuration with required permissions
- **done**: False
- **task**: Create content script for text selection and DOM interaction
- **done**: False
- **task**: Build background service worker for API communication and storage
- **done**: False
- **task**: Develop React-based popup interface with authentication flow
- **done**: False
- **task**: Integrate with existing Morpheus API through shared client package
- **done**: False
- **task**: Add extension-specific API endpoints for authentication and transformation
- **done**: False
- **task**: Implement cross-browser compatibility with webextension-polyfill
- **done**: False
- **task**: Create comprehensive test suite covering unit and integration scenarios
- **done**: False
- **task**: Package extension builds for Chrome Web Store and Firefox Add-ons submission
- **done**: False

## Agent Notes

### Research Findings

**Context:**
A browser extension for Morpheus serves multiple distribution and engagement purposes:
- Allows users to quickly transform web articles, blog posts, or selected text into comics without leaving their browsing context
- Provides seamless integration with the Morpheus platform for authenticated users
- Creates a new acquisition funnel by capturing users during their natural reading flow
- Enables bookmarking/saving content for later transformation in the main platform
- Supports viral growth through easy sharing of transformed comics directly from any webpage

**Technical Approach:**
- Manifest V3 extension (Chrome/Edge primary, Firefox secondary) using TypeScript
- Content script injection for text selection and UI overlay
- Background service worker for API communication with Morpheus backend
- Popup interface for quick transformations and user account management
- Shared utilities package from main monorepo for API clients and type definitions
- Chrome Extension API for storage, tabs, and activeTab permissions
- PostMessage communication between content script and popup/background

**Dependencies:**
- External: @types/chrome, webextension-polyfill, @morpheus/shared-types, @morpheus/api-client
- Internal: Authentication service integration, Comic generation API endpoints, User preferences/settings service

**Risks:**
- Content Security Policy conflicts: Use extension-specific CSP and avoid inline scripts
- Cross-origin API calls: Implement proper CORS handling and use background script as proxy
- Text extraction complexity: Different websites have varying DOM structures requiring robust selection logic
- Performance on content-heavy sites: Lazy load extension features and minimize DOM manipulation
- Store approval delays: Plan 2-4 week review cycles for Chrome Web Store and Firefox Add-ons

**Complexity Notes:**
Higher complexity than initially estimated due to:
- Multi-browser compatibility requirements
- Complex text extraction and context preservation
- Authentication flow in extension context (OAuth redirect handling)
- Real-time communication between extension components
- Store submission and review processes
However, leveraging existing Morpheus API reduces backend complexity.

**Key Files:**
- apps/browser-extension/manifest.json: Extension configuration and permissions
- apps/browser-extension/src/content-script.ts: Text selection and DOM interaction
- apps/browser-extension/src/background.ts: Service worker for API communication
- apps/browser-extension/src/popup/: React-based popup interface
- packages/shared/src/browser-extension/: Shared types and utilities
- apps/api/src/routes/extension/: Extension-specific API endpoints


### Design Decisions

[{'decision': 'Manifest V3 with service worker architecture', 'rationale': 'Future-proof approach required by Chrome, better security model, persistent background capabilities', 'alternatives_considered': ['Manifest V2 (deprecated)', 'Hybrid V2/V3 approach']}, {'decision': 'React for popup UI with shared components', 'rationale': 'Consistency with main platform, reuse existing design system, faster development', 'alternatives_considered': ['Vanilla JS/HTML', 'Vue.js', 'Svelte']}, {'decision': 'Content script injection vs. always-on presence', 'rationale': 'Better performance, user privacy, and reduced memory footprint', 'alternatives_considered': ['Always-active content script', 'Declarative content API only']}]
