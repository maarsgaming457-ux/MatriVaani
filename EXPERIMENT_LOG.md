# Experiment Log

Log all experiments, hyperparameter choices, and outcomes here.

## Template
**Date:** YYYY-MM-DD
**Experiment ID:** EXP-001
**Component:** ASR / NMT / TTS
**Objective:** Describe what is being tested.
**Setup:** Details of the model, data version, hyperparameters.
**Results:** WER, BLEU, Latency, Memory usage, etc.
**Observations:** Notes on failures or successes.
**Next Steps:** Actions to take based on the results.

---

**Date:** 2026-08-26
**Experiment ID:** EXP-NMT-SAN-001
**Component:** NMT
**Objective:** Hindi-Santhali baseline evaluation and fine-tuning on IndicTrans2.
**Setup:** Model: `AI4Bharat/IndicTrans2`, Precision: INT8, Dataset: `MATRI-NMT-HI-SAT-v0.1`
**Results:** FAILED - INSUFFICIENT DATA
**Observations:** No raw CSV/JSONL data was found in the datasets directory. The pipeline gracefully failed, preventing any model training to avoid hallucination. During Phase 5.5 and 5.6, attempts to download `ainlpml-iitp/COILD-MT-Corpus` (20,603 pairs) from Hugging Face failed due to API authentication/gating. Formal verification confirmed the data was not manually placed in `datasets/nmt/raw/COILD-MT-Corpus/`.
**Next Steps:** Proceed to Phase 6 (TTS) while native speakers and project leads manually authenticate and acquire the necessary datasets.

---

**Date:** 2026-08-26
**Experiment ID:** EXP-TTS-SAN-SMOKE-001
**Component:** TTS
**Objective:** Verify VITS architecture forward/backward passes for Santhali.
**Setup:** Model: `VITS`, Dataset: `MatriVaani-TTS-San-v0.1` (0 files)
**Results:** FAILED - INSUFFICIENT DATA
**Observations:** The TTS dataset schemas and text normalizers (Ol Chiki) were built successfully, but the smoke test halted because no `.wav` files were found in `datasets/tts/raw/`.
**Next Steps:** Proceed to Phase 7 (Android Integration).
