# PHASE 6 SANTHALI TTS REPORT

## 1. TTS Objective
To establish a memory-efficient `<200MB` Text-to-Speech (TTS) engine capable of synthesizing Santhali audio (Ol Chiki script) as the final step in the MatriVaani Voice-to-Voice pipeline.

## 2. Candidate Models
- **Indic Parler-TTS**: State-of-the-art multilingual TTS (Santhali supported natively). Rejected due to massive memory footprint (800M+ params).
- **VITS**: Lightweight end-to-end TTS architecture (~30M params). **Selected** as the primary candidate for fine-tuning.

## 3. Santhali Support
VITS supports Santhali implicitly if fine-tuned on a high-quality Santhali `.wav` dataset and paired with an Ol Chiki text-normalizer/phonemizer.

## 4. Dataset Sources Investigated
- Mozilla Common Voice v17 (sat)
- AI4Bharat / Rasa
- ARTPARK / Vaani

## 5. Dataset Availability
**INSUFFICIENT DATA**. All identified datasets are either gated behind Hugging Face authentication tokens or require manual web downloads. We have acquired 0 files.

## 6. Dataset Metrics
- **Hours**: 0
- **Speakers**: 0
- **Script**: Ol Chiki (Strictly enforced by schema)
- **Quality**: NOT MEASURED

## 7. Model Baseline
- **RAM**: NOT MEASURED (VITS estimated < 150MB)
- **Latency**: NOT MEASURED (Target RTF < 0.2)
- **Model Size**: NOT MEASURED (VITS estimated ~150MB)
- **Audio Evaluation**: NOT MEASURED
- **Native Evaluation**: Planned for EXP-TTS-SAN-001 (Blocked).

## 8. Limitations & Problems Discovered
Similar to Phase 5.5, the TTS training loop cannot be initiated because we cannot automatically circumvent academic dataset gates. A human must manually provide the Santhali speech `.wav` files and transcripts to unblock TTS training.

## 9. Android & Memory Recommendation
We **must** utilize Sequential Lifecycle Management. The 2GB limit will instantly crash if ASR, NMT, and TTS are loaded concurrently. The sequence must be: Load ASR -> Unload ASR -> Load NMT -> Unload NMT -> Load TTS -> Speak.

## 10. Phase 7 Recommendation
Proceed to **Phase 7: Android Integration**. We have successfully established the backend schemas, evaluation tools, and architectural lifecycles for ASR, NMT, and TTS. We can build the Android client app to communicate with these pipelines while we wait for human educators to supply the raw datasets!
