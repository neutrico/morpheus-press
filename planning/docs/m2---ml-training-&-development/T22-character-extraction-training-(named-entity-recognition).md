---
area: ml
dependsOn:
- T19
- T20
effort: 5
iteration: I2
key: T22
milestone: M2 - ML Training & Development
priority: p0
title: Character Extraction Training (Named Entity Recognition)
type: Task
---

# Character Extraction Training (Named Entity Recognition)

## Acceptance Criteria

- [ ] **Character extraction achieves >85% precision and recall on literary test dataset**
  - Verification: Run evaluation script: npm run test:character-extraction -- --benchmark
- [ ] **System correctly resolves character coreferences (pronouns, aliases) with >80% accuracy**
  - Verification: Execute coreference test suite: npm test -- coreference-resolver.test.ts
- [ ] **Character relationship graphs are generated with proper entity linking**
  - Verification: Manual review of relationship visualization and automated graph structure validation
- [ ] **Active learning pipeline successfully improves model performance over 100 training iterations**
  - Verification: Monitor training metrics dashboard showing accuracy improvement curve
- [ ] **API handles full-length novels (100k+ words) within 60 seconds processing time**
  - Verification: Load test with sample novels: npm run test:load -- --target=character-extraction

## Technical Notes

### Approach

Build a two-stage pipeline: (1) Initial character detection using spaCy's transformer-based NER with custom literary training data, (2) Coreference resolution and relationship mapping using graph-based entity linking. Implement active learning to continuously improve model performance through human feedback. Create character profiles with extracted attributes (physical descriptions, relationships, dialogue patterns) stored in Supabase for comic generation consistency.


### Files to Modify

- **path**: apps/ml-service/src/routes/character.ts
- **changes**: Add endpoints for character extraction, training status, and active learning feedback
- **path**: apps/ml-service/package.json
- **changes**: Add spaCy, transformers, torch, networkx dependencies
- **path**: packages/shared/src/types/api.ts
- **changes**: Add character extraction request/response types
- **path**: apps/ml-service/src/config/ml-config.ts
- **changes**: Add NER model paths, training parameters, and performance thresholds

### New Files to Create

- **path**: apps/ml-service/src/services/character-extraction.ts
- **purpose**: Main NER service with spaCy integration and custom model handling
- **path**: apps/ml-service/src/services/coreference-resolver.ts
- **purpose**: Entity linking and coreference resolution using graph algorithms
- **path**: apps/ml-service/src/models/character-ner/trainer.ts
- **purpose**: Custom model training pipeline with active learning capabilities
- **path**: apps/ml-service/src/models/character-ner/evaluator.ts
- **purpose**: Model performance evaluation and benchmarking
- **path**: apps/ml-service/src/training/active-learner.ts
- **purpose**: Active learning strategy implementation for iterative improvement
- **path**: apps/ml-service/src/training/data-preprocessor.ts
- **purpose**: Literary text preprocessing and training data preparation
- **path**: apps/ml-service/src/utils/character-graph.ts
- **purpose**: Character relationship graph construction and manipulation
- **path**: packages/shared/src/types/character.ts
- **purpose**: Character entity types, relationships, and attributes
- **path**: apps/ml-service/src/db/character-repository.ts
- **purpose**: Database operations for character profiles and training data
- **path**: apps/ml-service/python/ner_training.py
- **purpose**: Python training script for spaCy model fine-tuning
- **path**: apps/ml-service/python/requirements.txt
- **purpose**: Python dependencies for ML training pipeline

### External Dependencies


- **spacy** ^3.7.0

  - Production-ready NER with transformer support and custom training capabilities

- **@huggingface/transformers** ^4.35.0

  - Pre-trained transformer models for literary text understanding

- **networkx** ^3.2

  - Character relationship graph modeling and analysis (Python interop via child_process)

- **scikit-learn** ^1.3.0

  - Active learning algorithms and model evaluation metrics

- **datasets** ^2.14.0

  - Training data management and preprocessing pipeline

- **torch** ^2.1.0

  - Custom transformer model fine-tuning and inference

## Testing

### Unit Tests

- **File**: `apps/ml-service/src/__tests__/character-extraction.test.ts`
  - Scenarios: Basic character detection from text passages, Handling of archaic/fantasy character names, Error handling for malformed input text, Character attribute extraction accuracy
- **File**: `apps/ml-service/src/__tests__/coreference-resolver.test.ts`
  - Scenarios: Pronoun resolution to correct characters, Alias mapping and entity linking, Multiple character disambiguation, Cross-chapter character tracking
- **File**: `apps/ml-service/src/__tests__/character-training.test.ts`
  - Scenarios: Training data preparation and validation, Active learning sample selection, Model serialization and loading
### Integration Tests

- **File**: `apps/ml-service/src/__tests__/integration/character-pipeline.test.ts`
  - Scenarios: End-to-end character extraction from novel upload to character profiles, Integration with LLM orchestration service, Database storage and retrieval of character data, Performance with varying novel lengths and styles
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

- **task**: Setup Python environment and install spaCy, transformers dependencies
- **done**: False
- **task**: Implement character extraction service with pre-trained model integration
- **done**: False
- **task**: Build coreference resolution system with graph-based entity linking
- **done**: False
- **task**: Create training data pipeline and active learning infrastructure
- **done**: False
- **task**: Develop custom NER model training with literary domain adaptation
- **done**: False
- **task**: Implement character relationship graph generation and storage
- **done**: False
- **task**: Build evaluation framework and performance benchmarking
- **done**: False
- **task**: Create API endpoints and integrate with existing LLM pipeline
- **done**: False
- **task**: Implement sliding window processing for large novels
- **done**: False
- **task**: Setup monitoring, logging, and error handling for production deployment
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Character extraction is critical for Morpheus to identify and track main characters, supporting characters, and their relationships throughout a novel. This enables consistent visual representation across comic panels, character-specific dialogue styling, and narrative continuity. Without accurate character extraction, the comic transformation would lose coherence and character development arcs.

**Technical Approach:**
Implement a hybrid NER approach combining pre-trained models (spaCy's transformer models) with custom training on literary texts. Use active learning to iteratively improve character detection accuracy. Create character relationship graphs and coreference resolution to handle pronouns and character aliases. Integration with existing LLM pipeline for context-aware character attribute extraction (appearance, personality traits).

**Dependencies:**
- External: spaCy v3.7+, transformers, datasets, torch, scikit-learn, networkx
- Internal: Novel preprocessing service, LLM orchestration service, character database schema, training data pipeline

**Risks:**
- Model drift: Regular retraining needed as literary styles vary significantly
- Coreference resolution complexity: Pronouns and aliases create ambiguity - use graph-based entity linking
- Training data quality: Limited annotated literary datasets - implement active learning with human-in-the-loop
- Performance at scale: Large novels may exceed context windows - implement sliding window approach

**Complexity Notes:**
More complex than initially estimated due to literary text nuances (archaic names, fantasy characters, multiple aliases). Requires domain-specific training data and sophisticated coreference resolution. However, leveraging pre-trained models reduces training time significantly.

**Key Files:**
- apps/ml-service/src/services/character-extraction.ts: Main NER service
- apps/ml-service/src/models/character-ner/: Custom model training pipeline
- apps/ml-service/src/training/: Training data preparation and active learning
- packages/shared/src/types/character.ts: Character entity types
- apps/ml-service/src/services/coreference-resolver.ts: Entity linking service


### Design Decisions

[{'decision': 'Use spaCy with custom transformer training rather than pure OpenAI API', 'rationale': 'Better control over model behavior, cost efficiency for batch processing, and ability to fine-tune on domain-specific literary data', 'alternatives_considered': ['Pure LLM prompting', 'BERT-based custom training', 'Rule-based regex extraction']}, {'decision': 'Implement character relationship graph using NetworkX', 'rationale': 'Enables complex relationship modeling, supports graph algorithms for character importance scoring, and integrates well with visualization tools', 'alternatives_considered': ['Simple adjacency lists', 'Graph databases like Neo4j', 'Custom graph implementation']}, {'decision': 'Use active learning with human feedback loop', 'rationale': 'Literary character extraction requires domain expertise, limited labeled data available, and quality is critical for downstream comic generation', 'alternatives_considered': ['Fully automated training', 'Crowdsourced labeling', 'Transfer learning only']}]
