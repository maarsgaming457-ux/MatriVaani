# MatriVaani

**AI-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education**

## SIH Problem Statement
SIH26042

## Overview
MatriVaani (powered by the internal PALASH language engine) is a modular, trainable, low-resource multilingual AI engine designed to enable Hindi-medium/non-native teachers to deliver primary education in tribal languages (starting with Santhali, expanding to Ho and Mundari).

The core engine supports:
- Automatic Speech Recognition (ASR)
- Neural Machine Translation (NMT)
- Text-to-Speech (TTS)
- Voice-to-Voice Real-Time Translation
- Offline operation on low-cost Android devices

## Data Dependencies
MatriVaani's automated data pipeline strictly relies on verifiable `.csv`/`.jsonl` files in `datasets/nmt/raw/`. External datasets like the `COILD-MT-Corpus` are gated behind API authentication and must be manually acquired by the user prior to NMT training.

## Architecture

1. **Phase 1**: Dataset Infrastructure
2. **Phase 2-3**: ASR Research & Validation (Meta MMS 1B -> Wav2Vec2)
3. **Phase 4-5.6**: NMT Research, Ingestion, & Verification (Blocked on data)
4. **Phase 6**: TTS Development (VITS framework deployed, blocked on data)
5. **Phase 7**: Android Integration (Upcoming)

## Repository Structure
- `ai/`: AI models and inference logic for ASR, NMT, TTS
- `datasets/`: Dataset management, raw and processed data, metadata
- `training/`: Training and fine-tuning scripts
- `backend/`: API and services (for initial sync and backend logic)
- `android/`: Android application for offline inference
- `education/`: FLN-aligned educational content, curriculum, worksheets
- `evaluation/`: Benchmarking, accuracy, latency, and memory evaluations
- `tests/`: Unit and integration tests
- `scripts/`: Utility scripts
- `docs/`: Project documentation

## Getting Started
Please refer to the documentation in `docs/` and review the `.md` files in the root directory for specific configurations and strategies.
