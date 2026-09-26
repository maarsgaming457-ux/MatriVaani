# NMT Final Decision

## Selected Model: IndicTrans2 (Quantized)
IndicTrans2 remains our baseline due to its explicit Ol Chiki Santhali token support.

## Model Lifecycle
To fit within our memory constraints, IndicTrans2 will NOT remain resident in RAM. It will be loaded only when ASR completes text generation, and explicitly released after generating the translated string.

## Baseline Metrics (Projected)
- **BLEU**: NOT MEASURED (Awaiting human-curated data from Phase 5.5).
- **chrF**: NOT MEASURED.
- **RAM**: ~1.5 GB (INT8 Load overhead).
- **Latency**: Estimated 1-2 seconds load + decode.

With the Manual Curation Tooling pipeline unblocking our reliance on COILD, Phase 5 (Fine-tuning framework) is marked as Complete and ready for actual data entry.
