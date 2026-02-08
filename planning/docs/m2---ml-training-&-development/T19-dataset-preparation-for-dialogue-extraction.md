---
area: ml
dependsOn: []
effort: 5
iteration: I2
key: T19
milestone: M2 - ML Training & Development
priority: p0
title: Dataset Preparation for Dialogue Extraction
type: Task
---

# Dataset Preparation for Dialogue Extraction

## Acceptance Criteria

- [ ] **Pipeline can process novel text and extract dialogue with >85% accuracy on validation dataset**
  - Verification: Run `npm test packages/ml/src/__tests__/dialogue-extractor.test.ts` and check accuracy metrics
- [ ] **Annotated training dataset contains at least 10,000 labeled examples across 4 categories (dialogue, narration, inner thoughts, sound effects)**
  - Verification: Query Supabase training_datasets table: `SELECT category, COUNT(*) FROM dialogue_annotations GROUP BY category`
- [ ] **Dataset preprocessing pipeline handles edge cases (nested quotes, multi-paragraph dialogue, mixed narrative styles)**
  - Verification: Execute integration test suite with edge case scenarios and validate 100% completion without errors
- [ ] **Active learning feedback system successfully incorporates user corrections to improve model performance**
  - Verification: Manual test: submit correction through API, verify database update, retrain model, measure accuracy improvement >2%
- [ ] **Complete API documentation and dataset schema documentation available**
  - Verification: Check docs/ml/dialogue-extraction.md exists with API endpoints, schema definitions, and usage examples

## Technical Notes

### Approach

Build a multi-stage pipeline that processes novel text through spaCy NLP models to identify dialogue boundaries, then uses transformer-based classification to categorize speech types. Implement active learning by integrating user feedback from the comic generation process to continuously improve dataset quality. Store processed datasets in Supabase with proper schema versioning for ML experiment tracking.


### Files to Modify

- **path**: packages/database/supabase/migrations/20241201000000_dialogue_training_schema.sql
- **changes**: Add tables for dialogue_annotations, training_datasets, model_experiments, feedback_corrections
- **path**: packages/database/src/types/training.ts
- **changes**: Add TypeScript types for training data schemas and API responses
- **path**: apps/api/src/routes/ml/index.ts
- **changes**: Add routes for dataset upload, annotation, feedback submission

### New Files to Create

- **path**: packages/ml/src/data/dialogue-extractor.ts
- **purpose**: Core spaCy-based dialogue extraction and boundary detection logic
- **path**: packages/ml/src/datasets/preparation.ts
- **purpose**: Hugging Face transformers preprocessing pipeline for token classification
- **path**: packages/ml/src/models/dialogue-classifier.ts
- **purpose**: Model training interface and active learning implementation
- **path**: packages/ml/src/services/annotation-service.ts
- **purpose**: OpenAI/Anthropic auto-labeling with validation workflows
- **path**: packages/ml/src/utils/dataset-validator.ts
- **purpose**: Quality validation, inter-annotator agreement, bias detection
- **path**: packages/ml/src/config/training-config.ts
- **purpose**: Configuration for model hyperparameters, dataset splits, evaluation metrics
- **path**: apps/api/src/controllers/dialogue-training.controller.ts
- **purpose**: API endpoints for dataset management and training pipeline triggers
- **path**: packages/ml/src/__tests__/fixtures/sample-novels.ts
- **purpose**: Test data with various dialogue patterns and edge cases

### External Dependencies


- **spacy** ^3.7.0

  - Advanced NLP processing and custom NER model training

- **@huggingface/transformers** ^2.17.0

  - Pre-trained language models for text classification

- **datasets** ^2.14.0

  - HuggingFace datasets library for ML-ready data formats

- **pandas-js** ^2.0.0

  - Data manipulation and preprocessing in TypeScript environment

- **natural** ^6.5.0

  - Additional NLP utilities for text preprocessing

## Testing

### Unit Tests

- **File**: `packages/ml/src/__tests__/dialogue-extractor.test.ts`
  - Scenarios: Extract simple dialogue with quotes, Handle nested dialogue and attribution, Classify different speech types correctly, Process edge cases (incomplete quotes, formatting issues), Error handling for malformed input
- **File**: `packages/ml/src/__tests__/dataset-preparation.test.ts`
  - Scenarios: Preprocessing pipeline transforms raw text correctly, Token classification labeling accuracy, Dataset validation and quality checks, Batch processing performance
### Integration Tests

- **File**: `packages/ml/src/__tests__/integration/dialogue-pipeline.test.ts`
  - Scenarios: End-to-end novel processing to labeled dataset, Supabase storage and retrieval workflow, Active learning feedback integration, Model training data pipeline
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

- **task**: Setup Supabase database schema for training datasets and annotations
- **done**: False
- **task**: Implement spaCy-based dialogue extraction with boundary detection
- **done**: False
- **task**: Build Hugging Face transformers preprocessing pipeline for token classification
- **done**: False
- **task**: Create OpenAI/Anthropic auto-labeling service with validation workflows
- **done**: False
- **task**: Implement dataset validation, quality metrics, and bias detection utilities
- **done**: False
- **task**: Build active learning feedback system with model retraining triggers
- **done**: False
- **task**: Develop API endpoints for dataset upload, annotation, and feedback submission
- **done**: False
- **task**: Create comprehensive test suites with edge cases and integration scenarios
- **done**: False
- **task**: Generate sample annotated datasets with 10k+ examples across 4 categories
- **done**: False
- **task**: Write technical documentation and API reference guides
- **done**: False
- **task**: Performance optimization and error handling implementation
- **done**: False
- **task**: Code review and security audit for data handling
- **done**: False

## Agent Notes

### Research Findings

**Context:**
This task involves preparing training datasets for extracting dialogue from novel text, which is critical for the novel-to-comic transformation pipeline. Comics rely heavily on dialogue bubbles, so we need ML models that can accurately identify, extract, and classify different types of speech (dialogue, narration, inner thoughts, sound effects). This enables proper comic panel layout and visual storytelling structure.

**Technical Approach:**
- Create annotated datasets with dialogue/narration labels using spaCy NLP pipelines
- Implement data preprocessing with Hugging Face Transformers for token classification
- Use pandas/polars for efficient dataset manipulation and validation
- Store processed datasets in Supabase with proper indexing for ML training retrieval
- Implement active learning feedback loops to improve dataset quality over time
- Use OpenAI/Anthropic APIs for initial auto-labeling with human validation

**Dependencies:**
- External: spacy, transformers, datasets (HuggingFace), pandas, scikit-learn, nltk
- Internal: Supabase database schema, novel processing service, ML training pipeline

**Risks:**
- Data quality inconsistency: Implement strict validation schemas and inter-annotator agreement metrics
- Copyright/licensing issues: Ensure training data complies with fair use and licensing terms
- Annotation bias: Use multiple annotators and cross-validation techniques
- Dataset imbalance: Apply stratified sampling and synthetic data generation techniques

**Complexity Notes:**
This is more complex than initially estimated due to the nuanced nature of dialogue extraction (handling nested quotes, implied speech, narrative voice changes). Requires domain expertise in literary analysis and careful consideration of different novel genres and writing styles.

**Key Files:**
- packages/ml/src/data/dialogue-extractor.ts: Core extraction logic
- packages/ml/src/datasets/preparation.ts: Dataset preprocessing pipeline
- packages/database/migrations/: New tables for training data storage
- packages/ml/src/models/dialogue-classifier.ts: Model training interface


### Design Decisions

[{'decision': 'Use spaCy + custom NER models for dialogue extraction', 'rationale': 'spaCy provides robust NLP pipelines with custom entity training capabilities, better than regex-based approaches for handling complex literary text', 'alternatives_considered': ['NLTK-only approach', 'Pure transformer-based solution', 'Rule-based regex system']}, {'decision': 'Store training data in Supabase with JSONB metadata', 'rationale': 'Keeps training data co-located with application data, enables real-time feedback integration, and JSONB allows flexible annotation schemas', 'alternatives_considered': ['Separate ML database', 'File-based storage', 'External ML platform']}]
