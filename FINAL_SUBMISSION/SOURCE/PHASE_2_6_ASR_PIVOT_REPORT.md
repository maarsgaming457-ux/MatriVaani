# PHASE 2.6: LOW-RAM ASR PIVOT REPORT

## 1. Why MMS-1B Was Rejected
The Meta `mms-1b-all` model was formally rejected because empirical PyTorch runtime profiling proved the base 1B parameters consume **~4.08 GB** of Peak RAM in FP32, and dynamic INT8 quantization triggers a **9.69 GB** memory spike during load. This structurally violates the 2.0 GB absolute memory limit of the PALASH Android deployment target.

## 2. Verified Memory Results
All memory results logged in this phase are explicitly verified via physical desktop simulation scripts (`benchmark_candidates.py`) tracking `psutil.Process` memory peaks at every computational step (Init → Load → Quantize → Inference).

## 3. Candidate Models
We shortlisted three open-source foundational ASR architectures:
1. `openai/whisper-tiny` (39M)
2. `openai/whisper-base` (74M)
3. `facebook/wav2vec2-base` (90M acoustic baseline)

## 4. Candidate Parameters
- **whisper-tiny**: 39M (Encoder-Decoder)
- **whisper-base**: 74M (Encoder-Decoder)
- **wav2vec2-base**: 90M (CTC Feature Extractor)

## 5. Language Support
- **whisper-tiny/base**: Hindi (YES), Santhali (ADAPTABLE - Requires Tokenizer Update).
- **wav2vec2-base**: Hindi (ADAPTABLE), Santhali (ADAPTABLE - Requires Custom CTC Head).

*(Note: Advanced Indian-specific checkpoints like `ai4bharat/indicwav2vec` are gated and therefore excluded from this fully open, automated iteration).*

## 6. Santhali Evidence
There is NO out-of-the-box non-gated Santhali ASR under 300M parameters. Therefore, Santhali support is explicitly designated as **ADAPTABLE**. We will achieve this natively in Phase 3 by extracting a base model and training a dedicated Santhali vocabulary head.

## 7. RAM Measurements (FP32)
- **whisper-tiny**: 483 MB (Load) → 693 MB (Inference Peak)
- **whisper-base**: 486 MB (Load) → 841 MB (Inference Peak)
- **wav2vec2-base**: 485 MB (Load) → 845 MB (Inference Peak)
All comfortably pass the `< 1.5 GB` preference.

## 8. Quantization Measurements
Dynamic PyTorch INT8 runtime quantization proved detrimental on CPU for these compact models.
- **whisper-tiny**: Peak RAM increased to 789 MB.
- **whisper-base**: Peak RAM increased to 1,023 MB.
- **wav2vec2-base**: Peak RAM spiked to 1,441 MB during conversion matrices.
Because pure FP32 already fits perfectly within the budget (~850 MB max), native dynamic quantization is rejected. 

## 9. ONNX Measurements
Not dynamically measured here because the PyTorch FP32 models *already pass* the hardware constraint. ONNX offline static compilation remains a powerful post-training tool to reduce Android battery overhead, but is no longer the sole blocker preventing OOM crashes.

## 10. Latency (RTF Simulation)
- **whisper-tiny**: 0.48s
- **whisper-base**: 0.96s
- **wav2vec2-base**: **0.27s** (Fastest)

## 11. WER / CER
**SANTHALI ACCURACY NOT YET MEASURABLE.**
No native Santhali checkpoint exists for these candidates; evaluation must occur in Phase 3 following fine-tuning.

## 12. Android Feasibility
- **Whisper**: Highly compatible (Whisper.cpp, TFLite ports).
- **Wav2Vec2**: Highly compatible (Torch Mobile, ONNXRuntime Mobile).

## 13. Licensing
- **Whisper**: MIT (Open)
- **Wav2Vec2**: Apache 2.0 (Open)

## 14. Fine-Tuning Feasibility
- **Whisper**: Very difficult for zero-resource languages. Updating the BPE Tokenizer and training the full Seq2Seq decoder requires massive paired datasets.
- **Wav2Vec2**: Much easier. We only need to swap the final linear classification layer (the CTC head) to map to Santhali characters. CTC loss thrives on unaligned transcription data.

## 15. Decision Matrix
See `docs/ASR_MODEL_SELECTION_DECISION.md`. `wav2vec2-base` won due to latency and CTC fine-tuning feasibility.

## 16. Selected Candidate
**`facebook/wav2vec2-base`** (or a similar 90M parameter base architecture).
**Status:** LOW-RAM CANDIDATE — SANTHALI VALIDATION PENDING.

## 17. Rejected Candidates
- `facebook/mms-1b-all`: REJECTED (> 4.0 GB RAM).
- `whisper-tiny` & `whisper-base`: REJECTED (Generative Seq2Seq architecture is too data-hungry and fragile for zero-resource Santhali adaptation compared to CTC).

## 18. Reasons for Rejection
MMS breached hardware limits. Whisper was rejected for fine-tuning inefficiency on unaligned linguistic data.

## 19. Remaining Risks
The burden of Santhali language support has now shifted entirely to the Phase 3 training pipeline. We must successfully construct a Santhali vocabulary list, attach a CTC head, and train it on the Phase 1 dataset without catastrophic forgetting.

## 20. Exact Phase 3 Plan
1. Pull the selected `wav2vec2-base` architecture.
2. Initialize a fresh CTC linear head mapped explicitly to Santhali characters (Ol Chiki or Dev/Roman transliteration depending on dataset).
3. Fine-tune the acoustic model using the validated Phase 1 dataset.
4. Export the resulting model weights and re-evaluate on the memory benchmark to ensure the CTC head did not violate the 2 GB Android limit.
