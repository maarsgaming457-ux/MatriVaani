# MATRI VAANI - HO DATA COLLECTION PROTOCOL

## Overview
This protocol outlines the controlled NATIVE HO DATA COLLECTION PILOT. The objective is to validate our collection pipelines before scaling.

## Data Storage
- ASR: data/ho_asr/collection_v1/
- Translation: data/ho_translation/collection_v1/
- TTS: data/ho_tts/collection_v1/

## Canonical Ho Script
- **CANONICAL_HO_SCRIPT**: Devanagari
- **LANGUAGE_CODE**: hoc
- **UNICODE_RANGE**: U+0900 to U+097F (Devanagari Block)
- **NORMALIZATION_RULES**: Convert all Latin/Warang Citi/Odia characters to their Devanagari phonetic equivalents. Remove diacritics not supported in standard Hindi.
- **TOKENIZATION_RULES**: Whitespace tokenization, strip basic punctuation.
- **Rationale**: Devanagari aligns seamlessly with the Hindi hub architecture. The previous failure with facebook/mms-tts-hoc was due to its strict Odia tokenization, which is incompatible with our primary Hindi<->Ho pipeline.

## Data Scaling Plan
The decision to scale up data collection will be based on pilot quality metrics:
- **ASR (10h -> 25h -> 50h)**: Scale only if the initial 1-2 hours pass all validation scripts (no clipping, 16kHz) and native speakers confirm >95% intelligibility.
- **Translation (1k -> 5k -> 10k -> 25k -> 50k)**: Scale only if 90% of the initial 1k pilot pairs achieve HUMAN_GROUND_TRUTH status without requiring heavy correction.
- **TTS (1h -> 2h -> 5h -> 10h)**: Scale only if the first hour has uniform SNR, no clipping, and exact script correspondence.
