# PHASE 7 PROJECT AUDIT REPORT

## 1. Current Repository State
The repository has a well-defined scaffolding for ASR, NMT, and TTS pipelines (`datasets/asr`, `datasets/nmt`, `datasets/tts`). Schemas and validation logic exist for all pipelines, but the `raw` data directories are currently empty.

## 2. What is Actually Working
- **Pydantic Schemas**: ASR, NMT, and TTS data validation structures correctly parse/reject improperly formatted metadata.
- **Python Version**: Confirmed `3.14.2`.
- **Testing Infrastructure**: Pytest suites verify all normalizer and schema functions properly.
- **Architecture Lifecycle**: Sequential load/unload parameters are defined and mathematically verified to keep the system under 2 GB peak RAM.

## 3. What is Only Architecture
- **Model Inference**: Baseline tests run on architectural definitions, but real physical model checkpoints (`.pt` / `.bin`) have not been fully downloaded/cached for all three because of missing data.
- **Audio Loading**: `librosa` pipelines are written but have only been exercised on synthetic `test_audio.wav`.

## 4. What Uses Real Data
- None. Currently, 0 verified Hindi-Santhali text pairs and 0 Santhali audio `.wav` files have been acquired.

## 5. Missing Datasets
- `datasets/nmt/raw/COILD-MT-Corpus`: Missing (Gated).
- `datasets/tts/raw/`: Missing (Gated).
- `datasets/asr/raw/`: Missing.

## 6. Current Blockers & Recommended Resolution
- **Blocker**: Hugging Face API gates prevent automated data download for Santhali. 
- **Resolution**: Deprecate automated dataset reliance. Instead, establish manual curation tools (`nmt_manual_curation_tool.py`) allowing native speakers to input data directly, bypassing third-party access limitations.
