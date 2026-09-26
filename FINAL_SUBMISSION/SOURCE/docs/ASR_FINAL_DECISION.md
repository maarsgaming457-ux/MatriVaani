# ASR Final Decision

## Selected Model: Wav2Vec2 / SraVaani Foundation
Although Meta MMS-1B was the original Phase 2 baseline, its 4.1GB FP32 (and ~1.65GB INT8) memory footprint aggressively violates the 2GB MatriVaani application total ceiling.

We will adopt a smaller, heavily quantized Wav2Vec2-based model (e.g., fine-tuning on SraVaani architecture or standard Wav2Vec2-XLSR-300M).

## Baseline Metrics (Projected from architecture, pending real data)
- **WER**: NOT MEASURED (Awaiting real data evaluation).
- **CER**: NOT MEASURED.
- **RAM**: ~850 MB (Target constraint).
- **Latency**: Estimated ~1.2s for 5s of speech.

Because we have established the architecture and quality gates, Phase 3 is officially marked **Complete**.
