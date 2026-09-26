# -*- coding: utf-8 -*-
import json

with open('HO_DATA_COLLECTION_PROTOCOL.md', 'w', encoding='utf-8') as f:
    f.write('''# MATRI VAANI - HO DATA COLLECTION PROTOCOL

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
''')

with open('HO_DATA_COLLECTION_PROTOCOL.json', 'w', encoding='utf-8') as f:
    json.dump({
        "protocol": "Ho Data Collection Pilot V1",
        "canonical_script": "Devanagari",
        "language_code": "hoc",
        "scaling_plan": {
            "asr": "1-2h -> 10h -> 25h -> 50h",
            "translation": "1k -> 5k -> 10k -> 25k -> 50k",
            "tts": "1-2h -> 2h -> 5h -> 10h"
        }
    }, f, indent=2)

with open('HO_ASR_COLLECTION_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write('''# HO ASR COLLECTION GUIDE

## Target
1-2 hours of genuine Ho speech across 3-5 native speakers.

## Vocabulary Topics
- Classroom, school, greetings, numbers, colors, family, objects, actions, questions, commands.

## Requirements
- Format: WAV, Mono, 16 kHz.
- Metadata: audio_path, transcript, speaker_id, duration, sample_rate, script, source, human_verified, ground_truth, recording_quality.

## Prompts (Example)
1. "Abua isim chi leka mena?" (How is your name?) -> [Devanagari Ho Representation]
...
''')

with open('HO_TRANSLATION_COLLECTION_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write('''# HO TRANSLATION COLLECTION GUIDE

## Target
1,000 HUMAN-VERIFIED Ho-Hindi sentence pairs.

## Vocabulary
Primary-school classroom language, greetings, objects, actions. No meaningless word substitutions.

## Requirements
- Script: Devanagari for both Ho and Hindi.
- Verification Statuses: HUMAN_GROUND_TRUTH, RESOURCE_SUPPORTED, SYNTHETIC, AI_GENERATED, UNVERIFIED, CORRECTED, REJECTED.
- AI-generated translations MUST NOT be marked as ground truth.
''')

with open('HO_TTS_COLLECTION_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write('''# HO TTS COLLECTION GUIDE

## Target
1-2 hours corpus using ONE consistent native Ho speaker.

## Requirements
- Clean recording environment, consistent microphone, quiet background.
- Format: WAV, Mono, 16 kHz.
- Transcript must EXACTLY match audio.
- Script: Devanagari.
''')

with open('HO_DATA_VERIFICATION_PROTOCOL.md', 'w', encoding='utf-8') as f:
    f.write('''# HO DATA VERIFICATION PROTOCOL

## Workflow
1. **COLLECTED**: Data enters system as UNVERIFIED or SYNTHETIC.
2. **TRANSCRIBED**: Audio is transcribed, or synthetic pair is proposed.
3. **NATIVE REVIEW**: Native Ho speaker reviews the sentence pair / audio transcript.
4. **DECISION**:
   - APPROVED: Upgraded to HUMAN_GROUND_TRUTH.
   - CORRECTED: New corrected record created. Old record becomes REJECTED.
   - REJECTED: Tagged as rejected.

**CRITICAL RULE**: Never overwrite original data. Corrections must preserve the original record by creating a new version.
''')

print('Docs created.')
