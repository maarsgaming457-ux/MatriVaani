# -*- coding: utf-8 -*-
import os
import json

# 1. Create directories
dirs = [
    'data/ho_asr/collection_real_v1/audio',
    'data/ho_asr/collection_real_v1/metadata',
    'data/ho_asr/collection_real_v1/manifests',
    'data/ho_asr/collection_real_v1/verification',
    'data/ho_translation/collection_real_v1/pairs',
    'data/ho_translation/collection_real_v1/metadata',
    'data/ho_translation/collection_real_v1/manifests',
    'data/ho_translation/collection_real_v1/verification',
    'data/ho_tts/collection_real_v1/audio',
    'data/ho_tts/collection_real_v1/metadata',
    'data/ho_tts/collection_real_v1/manifests',
    'data/ho_tts/collection_real_v1/verification'
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 2. Create empty real manifests
manifests = [
    'data/ho_asr/collection_real_v1/manifests/ho_asr_real_collection_v1.jsonl',
    'data/ho_translation/collection_real_v1/manifests/ho_translation_real_collection_v1.jsonl',
    'data/ho_tts/collection_real_v1/manifests/ho_tts_real_collection_v1.jsonl'
]
for m in manifests:
    if not os.path.exists(m):
        with open(m, 'w', encoding='utf-8') as f:
            pass # Keep empty, as no new physical data has been collected yet

# 3. Create protocol deliverables
protocol_md = """# MATRI VAANI - HO DATA COLLECTION PROTOCOL V1 (STRICT PHYSICAL REALITY)

## 1. ABSOLUTE RULES
- **NO SIMULATION**: Synthetic, simulated, or duplicated data must never enter the real collection manifests.
- **NO FABRICATION**: Transcripts, audio, and reviewer identities must correspond to physical reality.
- **PROVENANCE FIRST**: Every record must track its origin, session, collection date, and speaker ID.

## 2. ASR PROTOCOL
- **Target**: 5-10 REAL hours across 10+ speakers.
- **Spec**: 16 kHz, Mono, WAV, clean speech.
- **Verification**: Must be independently reviewed by a qualified native Ho speaker (VERIFIED or CORRECTED_AND_VERIFIED).
- **Data Structure**: udio_path, 	ranscript, speaker_id, duration, script (Devanagari), source, ecording_session, collection_date, 	ranscript_verification_status, erifier_id, provenance_status, sha256.

## 3. TRANSLATION PROTOCOL
- **Target**: 1,000 REAL HUMAN_GROUND_TRUTH pairs.
- **Spec**: Ho (Devanagari) ? Hindi (Devanagari).
- **Verification**: AI suggestions are drafted as SYNTHETIC or UNVERIFIED. A human MUST review them. Only pairs explicitly approved by a recorded eviewer_id with a erification_date can enter the dataset as HUMAN_GROUND_TRUTH.

## 4. TTS PROTOCOL
- **Target**: 1 REAL hour from 1 consistent speaker (HO_TTS_SPK_001).
- **Spec**: Studio quality, 16kHz, Mono, WAV.
- **Verification**: Transcripts must be verified to perfectly match the acoustic realization by a native reviewer.

## 5. IMMUTABLE PROVENANCE & DUPLICATE AVOIDANCE
All audio files receive a SHA256 hash upon ingestion to prevent silent duplication. Provenance fields cannot be overwritten. Records failing verification are moved to separate audit structures, never silently discarded or merged into ground truth.
"""

protocol_json = {
  "protocol": "Real Native Ho Data Collection V1",
  "rules": ["NO SIMULATION", "NO FABRICATION", "PROVENANCE FIRST"],
  "asr": {
    "target_hours": "5-10",
    "target_speakers": 10,
    "spec": "16kHz Mono WAV",
    "script": "Devanagari"
  },
  "translation": {
    "target_pairs": 1000,
    "required_status": "HUMAN_GROUND_TRUTH",
    "script": "Devanagari"
  },
  "tts": {
    "target_hours": 1.0,
    "target_speakers": 1,
    "spec": "Studio 16kHz Mono WAV",
    "script": "Devanagari"
  }
}

with open('HO_DATA_COLLECTION_PROTOCOL_V1.md', 'w', encoding='utf-8') as f: f.write(protocol_md)
with open('HO_DATA_COLLECTION_PROTOCOL_V1.json', 'w', encoding='utf-8') as f: json.dump(protocol_json, f, indent=2)

# 4. Create status deliverables (Strictly based on REAL new collection)
# Since we just created the framework and didn't simulate anything, the new collection is exactly 0.
status_md = """# MATRI VAANI - HO DATA COLLECTION STATUS (REAL DATA ONLY)

*Note: This dashboard tracks ONLY the new collection_real_v1 drive. It does not include the historical 0.079 hours from project-boli.*

## ASR STATUS
- **Real Hours**: 0.0
- **Real Utterances**: 0
- **Unique Speakers**: 0
- **Verified Transcripts**: 0
- **Unverified Transcripts**: 0
- **Rejected Records**: 0
- **Duplicate Records**: 0
- **TRAINING GATE**: **NOT READY - REAL DATA INSUFFICIENT**

## TRANSLATION STATUS
- **HUMAN-GROUND-TRUTH Pairs**: 0
- **Ho ? Hindi Pairs**: 0
- **Hindi ? Ho Pairs**: 0
- **Unverified Pairs**: 0
- **Rejected Pairs**: 0
- **Synthetic/Draft Pairs**: 0
- **Duplicate Pairs**: 0
- **TRAINING GATE**: **NOT READY - REAL DATA INSUFFICIENT**

## TTS STATUS
- **Real Hours**: 0.0
- **Utterances**: 0
- **Unique Speakers**: 0
- **Verified Transcripts**: 0
- **Unverified Transcripts**: 0
- **Duplicates**: 0
- **TRAINING GATE**: **NOT READY - REAL DATA INSUFFICIENT**

## CRITICAL SUMMARY
No simulations have been performed. The physical collection framework is structured and ready for field deployment. We are currently blocked pending the physical ingestion of genuine human recordings and human-verified sentence pairs.
"""

status_json = {
  "dashboard": "Real Native Collection Status V1",
  "asr": {
    "real_hours": 0.0,
    "real_utterances": 0,
    "unique_speakers": 0,
    "verified_transcripts": 0,
    "unverified_transcripts": 0,
    "rejected_records": 0,
    "duplicate_records": 0,
    "gate": "NOT READY - REAL DATA INSUFFICIENT"
  },
  "translation": {
    "human_ground_truth_pairs": 0,
    "ho_to_hi_pairs": 0,
    "hi_to_ho_pairs": 0,
    "unverified": 0,
    "rejected": 0,
    "synthetic": 0,
    "duplicates": 0,
    "gate": "NOT READY - REAL DATA INSUFFICIENT"
  },
  "tts": {
    "real_hours": 0.0,
    "utterances": 0,
    "unique_speakers": 0,
    "verified_transcripts": 0,
    "unverified": 0,
    "duplicates": 0,
    "gate": "NOT READY - REAL DATA INSUFFICIENT"
  }
}

with open('HO_DATA_COLLECTION_STATUS.md', 'w', encoding='utf-8') as f: f.write(status_md)
with open('HO_DATA_COLLECTION_STATUS.json', 'w', encoding='utf-8') as f: json.dump(status_json, f, indent=2)

print("Framework setup and physical reality reporting complete.")
