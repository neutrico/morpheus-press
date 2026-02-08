---
area: ml
dependsOn:
- T19
- T20
effort: 8
iteration: I2
key: T21
milestone: M2 - ML Training & Development
priority: p0
title: Dialogue Extraction Model Training
type: Task
---

# Dialogue Extraction Model Training

## Acceptance Criteria

- [ ] **Model accurately extracts dialogue with >85% precision/recall on test dataset**
  - Verification: Run evaluation script: python apps/ml/src/evaluation/dialogue_eval.py --test-data data/test/annotated_novels.json
- [ ] **Speaker attribution correctly identifies characters in >80% of dialogue instances**
  - Verification: Execute speaker evaluation: python apps/ml/src/evaluation/speaker_eval.py and check attribution_accuracy metric
- [ ] **API processes novel chapters and returns structured dialogue data within 30 seconds for 10k word texts**
  - Verification: Load test: curl -X POST /api/ml/extract-dialogue with sample chapter, verify response time <30s
- [ ] **Training pipeline successfully fine-tunes BERT model and saves versioned artifacts**
  - Verification: Run training: python apps/ml/src/training/dialogue-trainer.py --config configs/dialogue_config.yaml, verify model saved to storage
- [ ] **Integration with backend service provides dialogue extraction endpoint with proper error handling**
  - Verification: Test API endpoint: POST /api/novels/{id}/extract-dialogue returns 200 with dialogue array or appropriate error codes

## Technical Notes

### Approach

Build a dialogue extraction service that preprocesses novel text through spaCy NER for character identification, then applies a fine-tuned BERT model to classify dialogue vs narrative sentences. Create training datasets from annotated literary works, implementing active learning to improve model accuracy over time. Deploy the trained model as a FastAPI microservice that integrates with the main Morpheus backend, providing structured dialogue data with speaker attribution and emotional context tags.


### Files to Modify

- **path**: apps/backend/src/routes/ml.ts
- **changes**: Add dialogue extraction endpoint with proper request validation and error handling
- **path**: apps/backend/src/services/ml/base-ml-service.ts
- **changes**: Extend base service to support dialogue model loading and inference
- **path**: packages/shared/src/types/ml.ts
- **changes**: Add dialogue extraction request/response types

### New Files to Create

- **path**: apps/ml/src/models/dialogue-extractor.ts
- **purpose**: Main dialogue extraction model interface with NER and classification components
- **path**: apps/ml/src/training/dialogue-trainer.py
- **purpose**: Training pipeline for fine-tuning BERT model on dialogue detection task
- **path**: apps/ml/src/preprocessing/text-processor.ts
- **purpose**: Text preprocessing utilities for novel format handling and tokenization
- **path**: apps/ml/src/data/dataset-builder.py
- **purpose**: Build training datasets from Project Gutenberg novels with dialogue annotation
- **path**: apps/backend/src/services/ml/dialogue-service.ts
- **purpose**: Backend service for dialogue extraction API integration
- **path**: packages/shared/src/types/dialogue.ts
- **purpose**: TypeScript interfaces for dialogue data structures and API contracts
- **path**: apps/ml/src/evaluation/dialogue_eval.py
- **purpose**: Model evaluation scripts for precision/recall metrics on dialogue extraction
- **path**: apps/ml/src/evaluation/speaker_eval.py
- **purpose**: Speaker attribution accuracy evaluation and analysis
- **path**: apps/ml/configs/dialogue_config.yaml
- **purpose**: Training configuration for model hyperparameters and data paths
- **path**: apps/ml/src/utils/model-storage.ts
- **purpose**: Model versioning and artifact management with Supabase integration

### External Dependencies


- **spacy** ^3.7.0

  - Industrial-strength NLP with custom model training capabilities

- **transformers** ^4.36.0

  - Hugging Face transformers for BERT/RoBERTa fine-tuning

- **datasets** ^2.14.0

  - Efficient data loading and preprocessing for training

- **torch** ^2.1.0

  - PyTorch backend for transformer model training

- **wandb** ^0.16.0

  - Experiment tracking and model versioning

- **nltk** ^3.8.0

  - Text preprocessing utilities and sentence tokenization

## Testing

### Unit Tests

- **File**: `apps/ml/src/__tests__/dialogue-extractor.test.ts`
  - Scenarios: Text preprocessing and tokenization, NER character extraction, Dialogue classification accuracy, Speaker attribution logic, Error handling for malformed input
- **File**: `apps/backend/src/__tests__/services/dialogue-service.test.ts`
  - Scenarios: Service initialization and model loading, API request/response formatting, Database interaction for training data, Caching mechanism
### Integration Tests

- **File**: `apps/ml/src/__tests__/integration/training-pipeline.test.ts`
  - Scenarios: End-to-end training from data ingestion to model export, Model versioning and artifact storage, Integration with Supabase for training data
- **File**: `apps/backend/src/__tests__/integration/dialogue-api.test.ts`
  - Scenarios: Complete dialogue extraction workflow, ML service communication, Error propagation and handling
### Manual Testing


## Estimates

- **Development**: 8
- **Code Review**: 1
- **Testing**: 2
- **Documentation**: 1
- **Total**: 12

## Progress

- **Status**: not-started
- **Started**: 
- **Completed**: 

### Checklist

- **task**: Setup Python ML environment with spaCy, transformers, and dependencies
- **done**: False
- **task**: Create training dataset from Project Gutenberg novels with dialogue annotation
- **done**: False
- **task**: Implement text preprocessing pipeline with NER character identification
- **done**: False
- **task**: Build and train BERT-based dialogue classification model
- **done**: False
- **task**: Develop dialogue extraction service with speaker attribution logic
- **done**: False
- **task**: Create backend API integration with proper error handling and validation
- **done**: False
- **task**: Implement model evaluation pipeline with precision/recall metrics
- **done**: False
- **task**: Add model versioning and artifact storage to Supabase
- **done**: False
- **task**: Setup monitoring and logging with WandB integration
- **done**: False
- **task**: Create comprehensive test suite covering unit and integration scenarios
- **done**: False

## Agent Notes

### Research Findings

**Context:**
Dialogue extraction is critical for converting novels to comics, as it separates character speech from narrative text. This enables proper comic panel layout where dialogue appears in speech bubbles while narrative becomes captions or is omitted. The model must identify speakers, extract clean dialogue, and preserve emotional context for visual storytelling. This is foundational for the comic generation pipeline.

**Technical Approach:**
Use a two-stage approach: 1) Named Entity Recognition (NER) to identify characters and speakers, 2) Dialogue classification to extract speech patterns. Implement using spaCy for NER with custom training on literary texts, combined with a fine-tuned transformer model (BERT/RoBERTa) for dialogue detection. Create a training pipeline using Hugging Face transformers with custom datasets from Project Gutenberg novels. Store training data and models in Supabase with versioning.

**Dependencies:**
- External: spaCy, transformers, datasets, torch, wandb, nltk
- Internal: Database models for training data, ML service infrastructure, text preprocessing utilities

**Risks:**
- Training data bias: Literary styles vary greatly; mitigation through diverse dataset curation
- Speaker attribution accuracy: Complex novels with many characters; use context windows and speaker tracking
- Performance overhead: Large models impact inference speed; implement model quantization and caching
- Training costs: GPU requirements for fine-tuning; use incremental training and smaller model variants

**Complexity Notes:**
More complex than initially estimated due to nuanced speaker attribution in literary text. Unlike screenplay format, novels have inconsistent dialogue patterns, indirect speech, and complex narrative structures. Requires sophisticated NLP preprocessing and custom training data annotation.

**Key Files:**
- apps/ml/src/models/dialogue-extractor.ts: Main model interface
- apps/ml/src/training/dialogue-trainer.py: Training pipeline
- packages/shared/src/types/dialogue.ts: Type definitions
- apps/backend/src/services/ml/dialogue-service.ts: API integration


### Design Decisions

[{'decision': 'Use spaCy + Transformers hybrid approach instead of pure LLM', 'rationale': 'Better control over training data, faster inference, and more accurate speaker attribution than prompt-based LLM approaches', 'alternatives_considered': ['Pure OpenAI API calls', 'Custom LSTM model', 'Rule-based regex extraction']}, {'decision': 'Implement training pipeline with Weights & Biases tracking', 'rationale': 'Need experiment tracking for model iterations and hyperparameter optimization in ML development', 'alternatives_considered': ['MLflow', 'TensorBoard only', 'Custom logging']}]
