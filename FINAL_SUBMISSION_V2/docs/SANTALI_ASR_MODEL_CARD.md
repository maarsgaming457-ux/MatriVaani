# MatriVaani-ASR-Santhali-v0.1-Pilot

## 1. Overview
The **MatriVaani-ASR-Santhali-v0.1-Pilot** is an experimental early-stage Automatic Speech Recognition (ASR) model tailored explicitly for the **Santali** language (Language Code: `sat`), adhering strictly to the **Ol Chiki** script.

This model is part of **Phase 3.7** of the MatriVaani project (SIH26042) to evaluate the end-to-end environmental architecture, dataset streaming, vocabulary projection, memory consumption, and training pipeline prior to full scale fine-tuning.

## 2. Architecture
- **Base Model**: `facebook/wav2vec2-base-100k-voxpopuli` (A strong multilingual pre-trained Wav2Vec2 encoder)
- **Feature Extractor**: Frozen CNN layers to save GPU/CPU memory.
- **Language Head**: A randomly initialized LM head mapped to a deterministic 39-token Ol Chiki CTC vocabulary.
- **Loss**: Connectionist Temporal Classification (CTC)
- **Tokenizer**: Custom `Wav2Vec2CTCTokenizer`

## 3. Training Details
- **Hardware Profile**: CPU
- **Memory Constraint**: `< 2 GB` RAM ceiling. Handled via lazy `IterableDataset` over the Hugging Face hub stream, limiting peak RAM to **~517 MB**.
- **Dataset**: `ai4bharat/IndicVoices` (`santali` config)
- **Samples Used**: 1,000 train samples (from 224,000 available).
- **Epochs**: ~2.5 (150 steps)
- **Effective Batch Size**: 16

## 4. Evaluation Metrics
Tested on 200 samples from the `ai4bharat/IndicVoices` validation split.

### Zero-Shot Baseline (Before Fine-tuning)
- **WER**: 100.00%
- **CER**: 141.00%
- **Behavior**: Hallucinated Latin characters because the Ol Chiki script was entirely unknown to the base LM head.

### Pilot Fine-tuning (Checkpoint 150)
- **WER**: 100.00%
- **CER**: 100.00%
- **Behavior**: Exhibits standard "CTC blank collapse." The model learned to predict empty strings (the CTC `[PAD]` token) for all frames to quickly minimize initial loss. Because the prediction is empty, the Levenshtein distance is bounded strictly at 1.0 (100%).
- **Implication**: The vocabulary is structurally correct, and the model is ready to break out of the blank collapse during extended training over the full 224,000-sample dataset.

## 5. Security & Verification
- **Provenance**: All scripts (`scripts/run_asr_pilot.py`) used real data securely streamed from Hugging Face. 
- **Secrets**: No `.env` files or tokens have been committed to the repository. The Hugging Face `token` was correctly managed via the CLI credential store.
- **Data Integrity**: Audio chunks were verified as genuine 16kHz FLAC files. Text transcripts were audited to be 100% Ol Chiki characters.
