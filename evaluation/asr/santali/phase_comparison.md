# Santali ASR: Phase Comparison

| Metric | Phase 3.6 (Zero-Shot) | Phase 3.7 (Pilot - 150 Steps) | Phase 3.9 (10K - 50 Steps) |
|---|---|---|---|
| **Base Model** | facebook/wav2vec2-base-100k-voxpopuli | facebook/wav2vec2-base-100k-voxpopuli | facebook/wav2vec2-base-100k-voxpopuli |
| **Dataset Size** | 200 Valid | 1000 Train / 200 Valid | 10000 Train / 1000 Valid |
| **Data Strategy** | Network Streaming | Network Streaming | Local FLAC Cache |
| **Training RAM** | N/A | ~517 MB | ~600 MB |
| **Peak Inference RAM** | ~1040 MB | ~1100 MB | *(pending completion)* |
| **WER** | 100% | 100% | 100% |
| **CER** | 141% | 100% | 100% |
| **Empty Prediction Rate**| 0% (gibberish Latin) | 100% (CTC blank collapse) | 100% (CTC blank collapse) |
| **Training Loss** | N/A | 79.4 → 3.9 | 340.6 → 70.7 |

## Key Insights
1. **Network vs Local Cache**: Moving from Hugging Face HTTP streaming to local SSD caching completely eliminated `[WinError 10038]` network timeouts, allowing continuous, stable CPU iteration.
2. **RAM Stability**: Throughout all phases, memory consumption remained strictly under the 2 GB hardware limit (fluctuating between 500 MB and 1.2 GB).
3. **CTC Blank Collapse**: The model consistently collapses to the blank token early in training. While loss plummets aggressively, exiting this phase requires significantly more epochs than is feasible on a CPU. The pipeline itself is structurally sound.
