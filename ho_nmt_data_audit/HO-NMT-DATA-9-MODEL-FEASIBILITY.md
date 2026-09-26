# HO-NMT-DATA-9 — MODEL FEASIBILITY

## 1. Current Dataset Count
Exactly **330 verified direct Hindi ? Ho pairs** were loaded from the DATA-7 export.

## 2. Data-Quality Results
- Empty/Malformed: 0
- Exact Match/Identical text: 0
- Length bounds: Retained exactly as authored to preserve morphological diversity.

## 3. Warang Citi Count
Verified **59** pairs explicitly containing the U+118A0–U+118FF Unicode block.

## 4. Latin Ho Count
Verified **271** pairs containing Latin Ho transcriptions.

## 5. Direction Analysis
The dataset contains pairs defined primarily as hin -> hoc on Tatoeba. However, because our architecture requires a single translation capability for bidirectional inference, we will format the supervised records symmetrically (Hindi ? Ho and Ho ? Hindi) without fabricating new linguistic content. 

## 6. Duplicate Analysis
Identified 76 Hindi strings mapping to multiple Ho strings, and 77 Ho strings mapping to multiple Hindi strings. These represent valid translational variations (e.g., synonyms or honorifics).

## 7. Leakage Analysis
To prevent test set leakage, a graph-based connected-components algorithm was used to guarantee that if a specific Hindi or Ho string appears in the train set, its translational variants absolutely do NOT appear in the validation or test sets.

## 8. Tokenizer Results
The tokenizer script yielded profound evidence determining the trajectory of this project:
- **ByT5** successfully resolved Warang Citi into UTF-8 bytes without any <unk> degradation.
- **NLLB, mT5, and mBART** literally destroyed Warang Citi text. Their fixed 250k SentencePiece vocabularies lack the Warang Citi Unicode block entirely, returning catastrophic <unk> token replacements (e.g., ??????????! tokenized as !).

## 9. NLLB Ho Investigation
- **HO_NOT_NATIVE_IN_NLLB**
- NLLB-200 does not possess a Ho (hoc) language code. More critically, its tokenizer strips both Warang Citi characters and certain Latin Ho diacritics (e.g., ?). **NLLB is disqualified for direct Warang Citi processing.**

## 10. ByT5 Investigation
- **ByT5-Small** (300M) operates directly on raw UTF-8 bytes. 
- **SCRIPT_REPRESENTATION**: ByT5 can perfectly *represent* the orthography. 
- **LANGUAGE_PRETRAINING**: ByT5 does *not* possess innate multilingual pretrained knowledge of the Ho language semantics. It will have to learn semantic mappings directly from the supervised Hindi-Ho pairs.

## 11. mT5 Investigation
mT5-Small (300M) possesses a strong Indic multilingual prior but its SentencePiece tokenizer aggressively corrupts Warang Citi. It is feasible for Latin Ho, but useless for the native script.

## 12. mBART Investigation
mBART-Large-50 (610M) supports Hindi beautifully but fails exactly like mT5 on Warang Citi tokenization.

## 13. Model Comparison Table
See model_comparison.csv for detailed architectural and performance trade-offs.

## 14. Colab Feasibility
Both google/byt5-small and google/mt5-small are extremely feasible on a free Google Colab T4 GPU (16GB VRAM). With a batch size of 8-16 and FP16/BF16 mixed precision, training the 173 pairs will only take minutes, requiring ~4-6GB VRAM.

## 15. Dataset Split Statistics
Graph-segregated independent splits:
- **Train**: 173 pairs (incl. ~44 Warang Citi)
- **Validation**: 46 pairs (incl. ~5 Warang Citi)
- **Test**: 111 pairs (incl. ~10 Warang Citi)

## 16. PRIMARY_MODEL
**google/byt5-small** (Only viable candidate for genuine Warang Citi)

## 17. SECONDARY_MODEL
**google/mt5-small** (Fallback candidate if we transition entirely to Latin Ho)

## 18. Risks and Limitations
**CRITICAL RISK**: We have solved the tokenizer barrier, but we are asking ByT5 to learn the semantic grammar of an entire language from only 173 training sentences. The model will successfully *output* Warang Citi, but the translation quality will likely be extremely brittle and overfit.

## 19. Exact Files Created
- ho_nmt_data_audit/HO-NMT-DATA-9-MODEL-FEASIBILITY.md
- ho_nmt_data_audit/model_comparison.csv
- ho_nmt_data_audit/dataset_quality_report.csv
- ho_nmt_data_audit/train.jsonl
- ho_nmt_data_audit/validation.jsonl
- ho_nmt_data_audit/test.jsonl
- ho_nmt_data_audit/train_manifest.json
- ho_nmt_data_audit/validation_manifest.json
- ho_nmt_data_audit/test_manifest.json
- ho_nmt_data_audit/tokenizer_test_results.json
- ho_nmt_data_audit/model_feasibility_summary.json

## FINAL STATUS
**MODEL_FEASIBILITY_RESOLVED**

**PRIMARY_MODEL:** google/byt5-small
**SECONDARY_MODEL:** google/mt5-small

**TRAIN_PAIRS:** 173
**VALIDATION_PAIRS:** 46
**TEST_PAIRS:** 111
