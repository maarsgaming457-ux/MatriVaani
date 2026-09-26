# Santhali TTS Dataset Audit Protocol

This document details the quality assurance gates applied to Santhali TTS audio data before fine-tuning a VITS model.

## 1. Status
**INSUFFICIENT DATA**. As of Phase 6, there are no Santhali `.wav` files available locally.

## 2. Audio Validation (Future)
When dataset files are provided manually by the project lead, `scripts/tts_dataset_audit.py` will enforce the following:
- **Audio Exists**: Checks that every audio path listed in the transcript file exists on disk.
- **Transcript Exists**: Checks that every audio file has a corresponding transcript.
- **Duration**: Drops clips `< 1 second` or `> 15 seconds`.
- **Sample Rate**: Asserts all files are processed to exactly `22050 Hz`.
- **Clipping/Silence**: Warns on excessive silence padding or extreme amplitude clipping (using `librosa` analysis).

## 3. Script Validation
All target text must pass through `ai/tts/text_normalizer.py`. If a transcript contains Devanagari or Roman mixed improperly without phoneme handling, it will be flagged as `INVALID SCRIPT`.

## 4. Final Audit JSON
The audit script outputs `evaluation/accuracy/tts/dataset_audit.json` to formally block or allow `EXP-TTS-SAN-001`.
