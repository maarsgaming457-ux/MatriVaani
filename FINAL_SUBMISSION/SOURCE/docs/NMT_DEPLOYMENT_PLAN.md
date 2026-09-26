# MatriVaani NMT Deployment Plan

To deploy the IndicTrans2-based NMT engine onto low-cost Android hardware (Target: 2GB RAM), MatriVaani must implement a phased deployment architecture.

## Phase 1: Sequential Lifecycle Management (Immediate)
Because ASR (~850MB) and NMT (~1.5GB) cannot reside in RAM simultaneously:
1. **Listen State**: Only ASR is loaded into RAM.
2. **Translate State**: ASR weights are explicitly flushed. NMT is loaded from disk, infers, and is immediately flushed.
3. **Speak State**: TTS is loaded.

*Latency Penalty*: High. Loading ~1.5GB from Android storage into RAM can take 1-3 seconds, severely hampering "real-time" voice-to-voice capabilities.

## Phase 2: Knowledge Distillation (Target)
To achieve true real-time performance, we must shrink the 1.1B parameter IndicTrans2 model into a highly efficient student model.

### Architecture
- **Teacher**: IndicTrans2 (1.1B) fine-tuned on `MATRI-NMT-HI-SAT-EDU-v0.1`
- **Student Target**: A compact Transformer architecture (e.g., ~200M-300M parameters).
- **Process**: The Student will be trained to mimic the softmax probabilities (logits) of the Teacher on Hindi-Santhali pairs, effectively inheriting the Teacher's cross-lingual knowledge but compressing it into a fraction of the parameters.

### Expected Results
- **Student Size (INT8)**: ~200 MB - 300 MB RAM.
- **Latency**: Near instantaneous.
- **Concurrent Execution**: Can reside in RAM *alongside* ASR and TTS, restoring real-time voice-to-voice functionality without swapping.

## Conclusion
Distillation is mandatory for a fluid user experience on low-tier hardware. We will not begin distillation until the baseline IndicTrans2 teacher model is proven highly capable on the Educational test set.
