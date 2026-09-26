# HO DATASET AUDIT FINAL

## 1. ALL DISCOVERED DATASETS
- project-boli/ho
- karya/endangered-recipes-translated-500
- google/smol

## 2. USABLE DATASETS
- None yield NEW usable data for the current architecture.

## 3. PARTIALLY USABLE DATASETS
- None.

## 4. REJECTED DATASETS
- karya/endangered-recipes-translated-500 (Gated / Restricted access).
- google/smol (Suspicious web-scraped text, wrong script, lacks parallel Hindi).
- project-boli/ho (Rejected as DUPLICATE, since we already physically own these exact 100 recordings).

## 5. WHY REJECTED
- **KARYA**: Dataset access is restricted. Even if granted, it's English parallel, not Hindi.
- **SMOL**: Violates ground-truth requirements (unverified web data).
- **BOLI**: Would cause double-counting of the same 0.079 hours.

## 6. UNIQUE HO ASR HOURS
- **TOTAL_EXTERNAL_ASR_HOURS**: 0.0
- **TOTAL_EXISTING_REAL_PILOT_HOURS**: 0.07905
- **TOTAL_UNIQUE_ASR_HOURS_AFTER_DEDUPLICATION**: 0.07905

## 7. UNIQUE HO ASR UTTERANCES
- 100 (from existing pilot). 0 new external.

## 8. UNIQUE SPEAKERS
- 1 (from existing pilot).

## 9. VALID TRANSLATION PAIRS
- **TOTAL_EXTERNAL_HO_TRANSLATION_PAIRS**: 0
- **TOTAL_HUMAN_DOCUMENTED_PAIRS**: 0
- **TOTAL_UNVERIFIED_PAIRS**: 0
- **TOTAL_DUPLICATES**: 0
- **TOTAL_VALID_PAIRS**: 0

## 10. TRANSLATION DIRECTIONS
- Ho -> English: 0 (accessible)
- Ho -> Hindi: 0

## 11. USABLE HO TTS HOURS
- **TOTAL_HO_TTS_HOURS**: 0.0
- **TOTAL_HO_TTS_SPEAKERS**: 0
- **TOTAL_VERIFIED_TTS_UTTERANCES**: 0
- **REPORT**: NO SUITABLE PUBLIC HO TTS DATA FOUND

## 12. REMAINING DATA GAPS
- Everything. We physically lack ASR, Translation, and TTS data in sufficient volumes for training.

## 13. DATA SOURCE BREAKDOWN
- **OUR PHYSICAL DATA**: 100 ASR utterances (0.079h). 0 Translation. 0 TTS.
- **EXTERNAL PUBLIC DATA**: 0 usable ASR. 0 usable Ho-Hindi Translation. 0 usable TTS.
- **SYNTHETIC DATA**: 223 Translation pairs (isolated in quarantine).
- **SIMULATED DATA**: 9,300 quarantined records.
- **UNVERIFIED DATA**: 0 records.
- **REJECTED DATA**: All external Hugging Face records searched today.

## 14. TRAINING GATES
- **HO ASR**: **NOT READY - INSUFFICIENT VERIFIED DATA**
- **HO TRANSLATION**: **NOT READY - INSUFFICIENT VERIFIED DATA**
- **HO TTS**: **NOT READY - INSUFFICIENT VERIFIED DATA**
