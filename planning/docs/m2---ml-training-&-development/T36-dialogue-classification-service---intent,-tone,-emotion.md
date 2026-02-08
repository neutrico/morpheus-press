---
area: ml
dependsOn:
- T21
effort: 5
iteration: I2
key: T36
milestone: M2 - ML Training & Development
priority: p2
title: Dialogue Classification Service - Intent, Tone, Emotion
type: Task
---

# Dialogue Classification Service - Intent, Tone, Emotion

## Acceptance Criteria

- [ ] **Service correctly classifies dialogue intent (question, command, statement) with >80% accuracy on test dataset**
  - Verification: Run test suite with labeled dialogue samples: npm test -- dialogue-classifier.test.ts
- [ ] **Service identifies tone (formal, casual, aggressive) and emotion (happy, sad, angry, etc.) with confidence scores 0-1**
  - Verification: API returns structured JSON with intent, tone, emotion fields and confidence scores for each
- [ ] **Batch processing handles novel-length content (10,000+ dialogue lines) within 5 minutes**
  - Verification: Load test with sample novel data: POST /api/ml/dialogue/batch with 10k samples
- [ ] **Smart routing uses local models for simple cases and OpenAI for complex literary dialogue**
  - Verification: Monitor logs showing model selection logic and verify <30% OpenAI usage on mixed dataset
- [ ] **Classification results are cached and retrievable for identical input**
  - Verification: Second identical request returns cached result within 50ms response time

## Technical Notes

### Approach

Build a dialogue classification service that accepts text input and returns structured analysis of intent, tone, and emotion with confidence scores. Implement a smart routing system that uses local models for straightforward cases and escalates to OpenAI for complex literary dialogue. Create a caching layer using Supabase to store classification results and enable batch processing for novel-length content. Design the service to maintain conversation context windows for improved accuracy.


### Files to Modify

- **path**: apps/api/src/app.ts
- **changes**: Add dialogue classification routes to Express app
- **path**: packages/shared/src/types/index.ts
- **changes**: Export dialogue classification types

### New Files to Create

- **path**: apps/api/src/services/ml/dialogue-classifier.ts
- **purpose**: Main classification service with hybrid model approach
- **path**: packages/shared/src/types/dialogue.ts
- **purpose**: TypeScript interfaces for classification input/output
- **path**: apps/api/src/routes/ml/dialogue.ts
- **purpose**: REST endpoints for single and batch classification
- **path**: packages/ml-utils/src/dialogue/prompt-templates.ts
- **purpose**: GPT-4 prompt templates for complex dialogue analysis
- **path**: packages/ml-utils/src/dialogue/local-classifier.ts
- **purpose**: Local transformers.js models for basic classification
- **path**: packages/ml-utils/src/dialogue/context-manager.ts
- **purpose**: Maintain conversation history windows for context
- **path**: apps/api/src/services/ml/dialogue-cache.ts
- **purpose**: Supabase caching layer for classification results
- **path**: apps/api/src/middleware/batch-processor.ts
- **purpose**: Handle large novel processing with progress tracking

### External Dependencies


- **@huggingface/transformers** ^2.17.2

  - Local sentiment analysis and emotion classification models

- **compromise** ^14.10.0

  - Natural language processing for intent detection and dialogue preprocessing

- **sentiment** ^5.0.2

  - Lightweight sentiment analysis for tone classification fallback

- **string-similarity** ^4.0.4

  - Dialogue similarity matching for cache optimization and context analysis

## Testing

### Unit Tests

- **File**: `apps/api/src/services/ml/__tests__/dialogue-classifier.test.ts`
  - Scenarios: Intent classification accuracy, Tone detection with confidence scores, Emotion analysis for complex literary dialogue, Caching mechanism, Error handling for API failures, Batch processing logic
- **File**: `packages/ml-utils/src/dialogue/__tests__/prompt-templates.test.ts`
  - Scenarios: Prompt generation for different dialogue types, Context window management, Template validation
### Integration Tests

- **File**: `apps/api/src/__tests__/integration/dialogue-classification.test.ts`
  - Scenarios: End-to-end classification pipeline, OpenAI API integration with fallback, Supabase caching integration, Batch processing with real novel data
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

- **task**: Setup project dependencies (@huggingface/transformers, openai, compromise)
- **done**: False
- **task**: Create type definitions and shared interfaces
- **done**: False
- **task**: Implement local classification pipeline with transformers.js
- **done**: False
- **task**: Build OpenAI integration with prompt engineering
- **done**: False
- **task**: Create smart routing logic and confidence thresholding
- **done**: False
- **task**: Implement Supabase caching layer
- **done**: False
- **task**: Build batch processing with progress tracking
- **done**: False
- **task**: Create REST API endpoints
- **done**: False
- **task**: Write comprehensive test suite
- **done**: False
- **task**: Performance testing and optimization
- **done**: False
- **task**: Documentation and API specs
- **done**: False
- **task**: Code review and refinement
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This service analyzes dialogue from novels to classify intent (question, command, statement), tone (formal, casual, aggressive), and emotion (happy, sad, angry, etc.) for comic generation. This is crucial for visual storytelling as it determines character expressions, speech bubble styling, panel composition, and scene atmosphere. Without proper dialogue classification, the generated comics would lose emotional context and narrative impact.

**Technical Approach:**
Implement a hybrid approach using OpenAI's GPT-4 for complex contextual analysis combined with a local classification pipeline using transformers.js for performance optimization. Create a service that processes dialogue in batches, caches results, and provides structured output for the comic generation pipeline. Use sentiment analysis models like cardiffnlp/twitter-roberta-base-sentiment-latest for emotion detection and custom prompt engineering for intent classification.

**Dependencies:**
- External: @huggingface/transformers, openai, compromise (NLP), sentiment
- Internal: Depends on text extraction service (likely from novel parsing), integrates with comic generation pipeline, uses shared ML utilities

**Risks:**
- Model accuracy: Different writing styles may confuse classification - mitigate with ensemble methods and confidence scoring
- Performance bottleneck: Processing large novels could be slow - implement batch processing and caching
- Context loss: Single dialogue analysis without conversation context - maintain dialogue history window
- API costs: OpenAI usage could be expensive - implement smart fallback to local models

**Complexity Notes:**
More complex than initially estimated due to contextual nuances in literary dialogue. Emotion classification especially challenging as literary characters often use subtext, sarcasm, and complex emotional states that simple sentiment analysis cannot capture.

**Key Files:**
- apps/api/src/services/ml/dialogue-classifier.ts: Main classification service
- packages/shared/src/types/dialogue.ts: Type definitions for classification results
- apps/api/src/routes/ml/dialogue.ts: API endpoints for classification
- packages/ml-utils/src/dialogue/: Shared utilities and prompt templates


### Design Decisions

[{'decision': 'Hybrid OpenAI + Local Model Approach', 'rationale': 'Balances accuracy (GPT-4 for complex cases) with cost and performance (local models for simple cases)', 'alternatives_considered': ['Pure OpenAI approach', 'Pure local transformers', 'Rule-based classification']}, {'decision': 'Structured JSON Output Schema', 'rationale': 'Enables reliable parsing for downstream comic generation services and allows confidence scoring', 'alternatives_considered': ['Simple string labels', 'Probability arrays', 'Multi-step classification']}]
