# ASR Model Selection Decision Matrix (Phase 2.6)

Given the hardware constraint (< 2 GB Peak RAM), we pivoted away from `facebook/mms-1b-all` (which demanded 4.1+ GB) and benchmarked three `< 300M` parameter candidates. Because no <300M model natively supports Santhali out-of-the-box in the open-source Hub (excluding gated/restricted repos), Santhali capability is rated by **Adaptability**.

## Weighted Matrix

| Criteria (Weight) | `whisper-tiny` (39M) | `whisper-base` (74M) | `wav2vec2-base` (90M) |
|-------------------|----------------------|----------------------|-----------------------|
| **Santhali Capability** (VERY HIGH) | ADAPTABLE (Seq2Seq Tokenizer Expansion) | ADAPTABLE (Seq2Seq Tokenizer Expansion) | **ADAPTABLE (CTC Head)** |
| **Peak RAM** (VERY HIGH) | **693 MB** (FP32) | 841 MB (FP32) | 845 MB (FP32) |
| **Offline Capability** (VERY HIGH) | Excellent | Excellent | Excellent |
| **Fine-tuning Capability** (HIGH) | Hard (Requires massive paired data & Seq2Seq) | Hard (Requires massive paired data) | **Easier (CTC loss handles unaligned data)** |
| **Latency** (HIGH) | 0.48s | 0.96s | **0.27s (Fastest)** |
| **Android Feasibility** (HIGH) | C++ / TFLite native ports exist | C++ / TFLite native ports exist | Torch Mobile / ONNX |
| **Hindi Capability** (MEDIUM) | Excellent | Excellent | Requires Hindi Finetune/Base |

## Analysis of Architecture
While `whisper-tiny` has the lowest RAM footprint (693 MB), fine-tuning a Seq2Seq Whisper model for a completely new, unseen zero-resource language like Santhali is notoriously difficult. It requires updating a complex Byte-Level BPE tokenizer and training an encoder-decoder attention mechanism on massive datasets.

Conversely, the `wav2vec2-base` architecture relies on **Connectionist Temporal Classification (CTC)**. We can simply swap the final linear layer (the CTC head) to output Santhali characters, and fine-tune it efficiently using a fraction of the paired data. This is the exact same architectural approach used by Meta's original `mms` project.

## Final Selection
**Selected Model:** `facebook/wav2vec2-base` (or equivalent open 90M Wav2Vec2 variant)
**Status:** LOW-RAM CANDIDATE — SANTHALI VALIDATION PENDING

**Why?**
1. It comfortably fits the memory envelope (845 MB Peak RAM < 2,000 MB Limit).
2. It has the lowest inference latency (0.27s).
3. CTC-based architectures are proven to be the most data-efficient and robust mechanism for adapting to zero-resource languages like Santhali compared to generative Seq2Seq models.
