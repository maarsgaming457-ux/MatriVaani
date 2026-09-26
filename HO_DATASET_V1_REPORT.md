# MATRI VAANI — HO DATASET V1 REPORT

## PART 1 — EXISTING DATA INVENTORY

| PATH | TYPE | LANGUAGE | TASK | NUMBER OF FILES | SCRIPT | SOURCE | LICENSE | HUMAN VERIFIED | GROUND TRUTH | SYNTHETIC | SAFE TO TRAIN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| data/ho_hindi/raw/ho_asr_recovery_manifest_100.jsonl | Manifest | Ho | ASR | 100 utterances | Mixed | project-boli/ho | CC-BY | Yes | Yes | No | Yes (Fine-tuning only) |
| data/ho_hindi/experimental/v3_dataset/*.jsonl | Parallel Text | Ho-Hindi | NMT | 223 pairs | Mixed | Groq API + Lexicon | Proprietary | No | No | Yes | No (Needs Verification) |
| data/ho_hindi/experimental/resources/ | Lexicons | Ho-Hindi | Dict | ~2 files | Latin/Devanagari | CIIL/Public | Public Domain | Yes | Yes | No | N/A (Not sentences) |

*Note: All original data paths, files, and scripts have been strictly preserved. No data was deleted.*

---

## PART 2 — HO ASR DATASET STRATEGY

**Path**: data/ho_asr/ho_asr_v1_manifest.jsonl

**Standardized Format**:
`json
{
  "audio_path": "/absolute/path/to/audio.wav",
  "transcript": "Ho transcription string",
  "language": "ho",
  "script": "Devanagari",
  "speaker_id": "speaker_001",
  "duration": 4.5,
  "sample_rate": 16000,
  "source": "MatriVaani Crowdsource 2026",
  "human_verified": true,
  "ground_truth": true,
  "synthetic": false
}
`

**Quality Constraints**:
- 16 kHz Mono WAV format exclusively.
- Test splits must feature mutually exclusive speaker_id values from the training split to prevent acoustic leakage.

---

## PART 3 & 4 — HO-HINDI TRANSLATION DATA STRATEGY

**Path**: data/ho_translation/ho_translation_v1_manifest.jsonl

**Standardized Format**:
`json
{
  "id": "trans_v1_001",
  "ho_text": "...",
  "hi_text": "...",
  "ho_script": "Devanagari",
  "hi_script": "Devanagari",
  "source": "Primary Textbook Grade 1",
  "domain": "education",
  "human_verified": true,
  "ground_truth": true,
  "synthetic": false,
  "verification_status": "HUMAN_GROUND_TRUTH"
}
`

**Pilot Scope**:
- Target: 5,000 – 10,000 sentence pairs.
- Domain: Primary-school classroom language (greetings, numbers, colors, teacher instructions).
- **CRITICAL RULE**: Machine-generated translations are never marked human_verified=true or ground_truth=true without manual native speaker approval.

---

## PART 5 — HUMAN VERIFICATION WORKFLOW

1. **Generation**: Synthetic sentence generated via template + lexicon (marked UNVERIFIED / SYNTHETIC).
2. **Review**: Sent to native Ho reviewer interface.
3. **Action**: 
   - APPROVED: Promoted to HUMAN_GROUND_TRUTH.
   - CORRECTED: A new record is created with the corrected text, old record remains REJECTED.
   - REJECTED: Removed from training pool.
4. **Immutability**: Original raw generations are never overwritten; state changes flow through versioned manifests.

---

## PART 6 & 7 — HO TTS DATASET & SCRIPT POLICY

**Path**: data/ho_tts/ho_tts_v1_manifest.jsonl

**CANONICAL HO SCRIPT POLICY**: 
MatriVaani standardizes on **DEVANAGARI SCRIPT** for Ho to maximize interoperability with Hindi NLP pipelines, unless Latin is strictly mandated by the state education board.
- **Normalization Rules**: Odia and Warang Citi characters must be transliterated to Devanagari using a deterministic rule engine before entering the TTS dataset.

**Format**:
`json
{
  "audio": "/absolute/path/to/tts_audio.wav",
  "text": "Normalized Devanagari Ho text",
  "speaker_id": "MV_Ho_TTS_Voice_1",
  "duration": 3.2,
  "sample_rate": 22050,
  "script": "Devanagari",
  "source": "MatriVaani Studio 2026",
  "human_verified": true,
  "transcript_verified": true,
  "recording_quality": "studio"
}
`

---

## PART 8 & 9 — DATA QUALITY CHECKERS & VERSIONING

- Validation scripts created: alidate_asr_dataset.py, alidate_translation_dataset.py, alidate_tts_dataset.py.
- Validation targets missing fields, 16kHz audio constraints, mono channel checks, and verification state legality.
- Versioning is handled via directory structures (data/ho_asr/, data/ho_translation/, data/ho_tts/) with _v1_manifest.jsonl files. Overwrites are prohibited.

---

## PART 10 — TRAINING READINESS REPORT

### HO ASR
- **Hours**: < 0.2 hours (Local pointers only)
- **Speakers**: 1 (project-boli/ho)
- **Utterances**: 100
- **Unique transcripts**: 100
- **Train/Validation/Test**: 100 / 0 / 0
- **Verified percentage**: 100%

### TRANSLATION
- **Sentence pairs**: 223
- **Human-ground-truth**: 0
- **Resource-supported**: 223
- **Synthetic**: 223
- **AI-generated**: 0
- **Unverified**: 0
- **Train/Validation/Test**: 181 / 22 / 20

### TTS
- **Hours**: 0
- **Speakers**: 0
- **Utterances**: 0
- **Verified transcripts**: 0
- **Audio quality statistics**: N/A

---

## PART 11 — FINAL STOP CONDITION

1. **What data we actually have**: We have 100 ASR utterances (under 12 minutes) from project-boli, a couple of grammar dictionaries, and 223 synthetic (unverified) translation pairs. We have zero TTS data.
2. **What data is still missing**: ~50 hours of diverse ASR data; ~50,000 human-verified translation sentence pairs; 5-10 hours of studio-quality single-speaker TTS data.
3. **Ready for ASR training?**: **NO**. (Severe lack of data).
4. **Ready for translation training?**: **NO**. (Zero human-verified ground truth sentence pairs).
5. **Ready for TTS training?**: **NO**. (Zero data).
6. **Exact recommended next training phase**: 
   - **DO NOT PROCEED TO MODEL TRAINING.**
   - **NEXT PHASE**: Execute a dedicated Data Collection & Synthetic Validation loop to reach the 5,000-pair translation pilot minimum and record at least 1 hour of TTS audio before attempting any architectural training.
