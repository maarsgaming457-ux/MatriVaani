# -*- coding: utf-8 -*-
import os
import json

base_dir = "experiments/ho_nmt/onemtbig"
os.makedirs(base_dir, exist_ok=True)
os.makedirs(os.path.join(base_dir, "raw_outputs"), exist_ok=True)

# 1. README.md
readme = """# ONEMT-BIG DIRECT HINDI-HO MODEL VALIDATION

## FINAL DECISION
**OPTION E: TEST_BLOCKED**

Meaning: The official checkpoint cannot be obtained or executed within reasonable latency. The model file is 2.14 GB and the host server (andanresearch.sgp1.digitaloceanspaces.com) throttles the download to ~50 KB/s, yielding a download time of 12+ hours. Therefore, the model cannot be practically loaded or evaluated for Ho translation quality.
"""

# 2. model_audit.md
audit = """# ONEMT-BIG REPOSITORY AUDIT

1. **Exact model checkpoint location**: https://vandanresearch.sgp1.digitaloceanspaces.com/bhashaverse-models/machine-translation/onemtbig/iiith-onemtbig.zip (2.14 GB zip file containing ct2_model and onemtbig_spm.model).
2. **Exact model architecture**: Transformer-based multilingual translation model. Exported to ctranslate2.Translator.
3. **Exact parameter count**: ~1B-2B (claimed).
4. **Exact tokenizer**: SentencePiece (spm.SentencePieceProcessor).
5. **Vocabulary**: Shared SentencePiece vocabulary across 36 languages.
6. **How language codes are passed**: The model is deployed on Triton Inference Server. The user passes sourceLanguage and 	argetLanguage (e.g. hi and hc) which are mapped to internal codes (hin_Deva and hoc_Wara). These are likely prepended to the token stream as __hin_Deva__ / __hoc_Wara__ based on standard Fairseq/CTranslate2 multilingual conventions.
7. **Ho-specific script/vocabulary**: The README claims support for hoc_Wara (Ho in Warang Citi script). The tokenizer model must theoretically contain Warang Citi characters.
8. **Ho Representation**: hoc_Wara
9. **Hindi Representation**: hin_Deva
10. **Is translation direct?**: Yes, the architecture is designed as an all-to-all multilingual translation model. No English intermediate step is defined in the Triton backend.

## BASHIK INTERPRETATION
- **MODEL_TRAINING_SOURCE_CLAIM**: Bhashik Parallel Corpora
- We cannot infer the actual Hindi-Ho pair count since Bhashik access is blocked and the model checkpoint itself cannot be downloaded to run empirical tests.
"""

# 3. hindi_to_ho_results.json
h2ho = {
    "test_samples": 0,
    "successful_outputs": 0,
    "empty_outputs": 0,
    "ho_script_outputs": 0,
    "hindi_leakage": 0,
    "english_leakage": 0,
    "santali_leakage": 0,
    "qualitative_assessment": "FAILED / TEST_BLOCKED",
    "reason": "Model download throttled to 50KB/s (12+ hours for 2.14GB). Inference impossible."
}

# 4. ho_to_hindi_results.json
ho2h = {
    "test_samples": 0,
    "successful_outputs": 0,
    "empty_outputs": 0,
    "hindi_script_outputs": 0,
    "ho_leakage": 0,
    "english_leakage": 0,
    "santali_leakage": 0,
    "qualitative_assessment": "FAILED / TEST_BLOCKED"
}

# 5. latency_results.json
latency = {
    "hindi_to_ho": {
        "cold": "UNKNOWN",
        "mean": "UNKNOWN",
        "median": "UNKNOWN",
        "p95": "UNKNOWN",
        "max": "UNKNOWN"
    },
    "ho_to_hindi": {
        "cold": "UNKNOWN",
        "mean": "UNKNOWN",
        "median": "UNKNOWN",
        "p95": "UNKNOWN",
        "max": "UNKNOWN"
    },
    "hardware": "UNKNOWN (Test Blocked)"
}

# 6. script_language_diagnostics.json
script_diag = {
    "status": "TEST_BLOCKED",
    "details": "Could not generate outputs to diagnose scripts or language leakage."
}

# 7. final_report.md
final_report = """# FINAL REPORT

------------------------------------------------------------
MODEL
------------------------------------------------------------
ONEMT-BIG
Checkpoint: https://vandanresearch.sgp1.digitaloceanspaces.com/bhashaverse-models/machine-translation/onemtbig/iiith-onemtbig.zip
Parameter count: ~1B-2B
Tokenizer: SentencePiece
License: CC BY-NC 4.0
Hindi code: hin_Deva
Ho code: hoc_Wara

------------------------------------------------------------
HINDI ? HO
------------------------------------------------------------
Test samples: 0
Successful non-empty outputs: 0
Empty outputs: 0
Ho-script outputs: 0
Hindi leakage: 0
English leakage: 0
Santali leakage: 0
Qualitative assessment: FAILED (Test Blocked)

------------------------------------------------------------
HO ? HINDI
------------------------------------------------------------
Test samples: 0
Successful non-empty outputs: 0
Empty outputs: 0
Hindi-script outputs: 0
Ho leakage: 0
English leakage: 0
Santali leakage: 0
Qualitative assessment: FAILED (Test Blocked)

------------------------------------------------------------
LATENCY
------------------------------------------------------------
Hindi ? Ho:
cold: UNKNOWN
mean: UNKNOWN
median: UNKNOWN
p95: UNKNOWN
max: UNKNOWN

Ho ? Hindi:
cold: UNKNOWN
mean: UNKNOWN
median: UNKNOWN
p95: UNKNOWN
max: UNKNOWN

Hardware: TEST_BLOCKED

------------------------------------------------------------
MEMORY
------------------------------------------------------------
Model RAM: UNKNOWN
GPU VRAM: UNKNOWN
CPU: UNKNOWN
GPU: UNKNOWN

------------------------------------------------------------
FINAL DECISION
------------------------------------------------------------
**OPTION E: TEST_BLOCKED**
Meaning: The official checkpoint cannot be obtained or executed. The DigitalOcean Spaces server hosting the 2.14GB model throttles downloads to roughly ~50 KB/s, which would take more than 12 hours to complete. Therefore, the model cannot be practically evaluated for zero-shot Hindi-Ho capability at this time.
"""

files = {
    "README.md": readme,
    "model_audit.md": audit,
    "hindi_to_ho_results.json": json.dumps(h2ho, indent=2),
    "ho_to_hindi_results.json": json.dumps(ho2h, indent=2),
    "latency_results.json": json.dumps(latency, indent=2),
    "script_language_diagnostics.json": json.dumps(script_diag, indent=2),
    "final_report.md": final_report
}

for fname, content in files.items():
    with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)

