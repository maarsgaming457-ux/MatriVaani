# MATRI VAANI - HO DATA COLLECTION PROTOCOL V1 (STRICT PHYSICAL REALITY)

## 1. ABSOLUTE RULES
- **NO SIMULATION**: Synthetic, simulated, or duplicated data must never enter the real collection manifests.
- **NO FABRICATION**: Transcripts, audio, and reviewer identities must correspond to physical reality.
- **PROVENANCE FIRST**: Every record must track its origin, session, collection date, and speaker ID.

## 2. ASR PROTOCOL
- **Target**: 5-10 REAL hours across 10+ speakers.
- **Spec**: 16 kHz, Mono, WAV, clean speech.
- **Verification**: Must be independently reviewed by a qualified native Ho speaker (VERIFIED or CORRECTED_AND_VERIFIED).
- **Data Structure**: udio_path, 	ranscript, speaker_id, duration, script (Devanagari), source, 
ecording_session, collection_date, 	ranscript_verification_status, erifier_id, provenance_status, sha256.

## 3. TRANSLATION PROTOCOL
- **Target**: 1,000 REAL HUMAN_GROUND_TRUTH pairs.
- **Spec**: Ho (Devanagari) ? Hindi (Devanagari).
- **Verification**: AI suggestions are drafted as SYNTHETIC or UNVERIFIED. A human MUST review them. Only pairs explicitly approved by a recorded 
eviewer_id with a erification_date can enter the dataset as HUMAN_GROUND_TRUTH.

## 4. TTS PROTOCOL
- **Target**: 1 REAL hour from 1 consistent speaker (HO_TTS_SPK_001).
- **Spec**: Studio quality, 16kHz, Mono, WAV.
- **Verification**: Transcripts must be verified to perfectly match the acoustic realization by a native reviewer.

## 5. IMMUTABLE PROVENANCE & DUPLICATE AVOIDANCE
All audio files receive a SHA256 hash upon ingestion to prevent silent duplication. Provenance fields cannot be overwritten. Records failing verification are moved to separate audit structures, never silently discarded or merged into ground truth.
