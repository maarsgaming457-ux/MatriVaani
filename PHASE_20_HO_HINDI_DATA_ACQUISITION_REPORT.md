# PHASE 20: HO ↔ HINDI TRANSLATION DATA ACQUISITION & MODEL PLAN

## 1. Discovered Resources
Exhaustive evidence-based searches were repeated across CIIL, Bharatavani, Bhashini/ULCA, AI4Bharat, Hugging Face, OPUS, and Tatoeba. No genuine sentence-level parallel corpus exists for Ho ↔ Hindi.

| Resource | Source | Data Type | Sentences | Aligned? | Ho? | Hindi? | Verified? | Class | Usable? |
|----------|--------|-----------|-----------|----------|-----|--------|-----------|-------|---------|
| Bhashik Generic | LTRC/HuggingFace | Synthetic | Unknown | Unknown | Yes | Yes | No | E | No |
| Ho Dictionaries | Glosbe / Digital Ho | Lexical | N/A | No | Yes | Yes | No | E | No |
| Educational Primers | CIIL/Bharatavani | Educational | N/A | No | Yes | Yes | No | F | No |

## 2. Provenance
No legitimate Ho ↔ Hindi parallel data exists. Therefore, no data was downloaded and the data/ho_hindi/ workspace was **not** created to prevent contamination.

## 3. License
N/A (No dataset exists).

## 4. Number of Usable Pairs
**0 verified pairs.**

## 5. Human Verification Status
No machine-generated pseudo-ground-truth was generated.

## 6. Existing 100 Ho Records Analysis
The recovered manifest (ho_asr_recovery_manifest_100.jsonl) contains the 100 Ho records. An inspection of the fields (source_dataset, source_record_id, udio_id, aw_asr_text) confirmed that there are **no** English translations or any hidden Hindi alignments. They are strictly monolingual Ho speech + text (Devanagari). 

## 7. Recommended Dataset Construction Route
Because 0 pairs exist, the immediate next step is to initiate a manual annotation pilot. We must use the existing 100 Ho records and commission a qualified bilingual Ho-Hindi speaker to manually translate the Ho transcripts into Hindi. This will achieve the "100 pairs = initial experiment" threshold. 

## 8. Model Architecture Options
Given the extreme low-resource nature of Ho, training from scratch is impossible. The model must be fine-tuned from a massively multilingual encoder-decoder checkpoint:
- **IndicTrans2 (AI4Bharat):** Best candidate. Highly optimized for Indian languages, handles Devanagari efficiently, and supports Hindi robustly. We can add a custom language token (<2hoc>).
- **NLLB (Meta):** Very strong baseline for low-resource zero-shot transfer, but heavier.
- **mT5 (Google):** Good baseline but less optimized specifically for Indian regional scripts than IndicTrans2.

## 9. Hindi→Ho Design
A unified bidirectional Seq2Seq model (IndicTrans2 architecture). For Hindi to Ho, the model receives Hindi text appended with a <2hoc> token to instruct the decoder to output Ho in Devanagari.

## 10. Ho→Hindi Design
The same unified bidirectional model. The model receives Ho (Devanagari) text appended with a <2hin> token to instruct the decoder to output Hindi text.

## 11. Ho TTS Integration Plan
**Model:** acebook/mms-tts-hoc (VITS)
- **License:** CC-BY-NC 4.0
- **Input Script:** Odia
- **Output:** 16kHz WAV
- **Performance:** CPU inference latency ~0.33s. Very lightweight.
- **Integration:** To be integrated into 	ts_service.py once script mapping is complete.

## 12. Devanagari→Odia Script Issue
The existing models/ho_asr transcribes speech into **Devanagari** Ho. However, acebook/mms-tts-hoc expects **Odia** script Ho. 
Before we can construct a complete voice pipeline (Hindi Speech → Hindi Text → Ho Text → Ho Speech), we must implement a deterministic, rule-based transliterator mapping Ho Devanagari characters to Ho Odia characters. This mapping must be verified by a native speaker to ensure phonetic correctness.

## 13. Hardware Requirements
Fine-tuning the translation model (IndicTrans2) on 100 pairs will require a GPU (e.g., Google Colab T4/L4). Inference for both the final translation model and MMS-TTS can comfortably run on CPU (local Windows environment or Android if quantized).

## 14. Exact Next Training Step
**Blocked.** The exact next step is NOT training. The next step is strictly **Dataset Construction Phase**. We must provide the 100 Ho records to human annotators via an annotation tool, collect the Hindi translations, and verify them.

## 15. Files Changed
- PHASE_20_HO_HINDI_DATA_ACQUISITION_REPORT.md (Created)

## 16. Files Protected
Absolutely no production files or existing models were modified. data/ho_hindi/ was intentionally not created to avoid empty/synthetic data artifacts.

## 17. Remaining Blockers
- **Data:** 0 human-verified Ho ↔ Hindi sentence pairs exist.
- **Script Converter:** A Devanagari-to-Odia transliterator is required to bridge the future Translation model and the TTS model.
