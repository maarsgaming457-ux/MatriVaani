# ASR Memory Optimization Decision

## Context
The Phase 2 baseline model `facebook/mms-1b-all` guarantees our hard requirement for Santhali (`sat`) support. We rigorously benchmarked PyTorch Dynamic Quantization and Chunked Streaming to see if we could compress the runtime under 2.0 GB.

## Required Final Table

| Configuration | Adapter | Peak RAM | WER | CER | Latency (RTF) | Status |
|---------------|---------|----------|-----|-----|---------------|--------|
| `mms-1b-all` (FP32) | `sat` | ~4.08 GB | 1.0 (Synth) | 1.0 (Synth) | ~0.60 | **FAILED** |
| `mms-1b-all` (Dynamic INT8) | `sat` | ~9.69 GB | NOT MEASURED | NOT MEASURED | ~1.08 | **FAILED** |
| `mms-1b-all` (Streaming FP32) | `sat` | ~4.11 GB | NOT MEASURED | NOT MEASURED | NOT MEASURED | **FAILED** |

*Note: Santhali accuracy regression not yet measurable due to insufficient verified evaluation data.*

## Optimization Decisions

### 1. PyTorch Dynamic Quantization (INT8)
**Decision**: REJECTED (FAILED)
**Reasoning**: PyTorch runtime dynamic quantization triggers an enormous 9.6 GB memory spike during the weight conversion phase (as it duplicates the model into memory). Android will forcefully terminate any app attempting this.

### 2. Streaming / Chunked Architecture
**Decision**: APPROVED IN PRINCIPLE, BUT INSUFFICIENT
**Reasoning**: Supplying a long 10+ second audio file to the acoustic model generates massive intermediate attention tensors. By slicing the audio locally into 2-second overlapping segments, we cap the tensor size allocation. However, this does nothing to reduce the core model footprint (4.1 GB).

### 3. Native PyTorch Execution
**Decision**: REJECTED
**Reasoning**: No native configuration of the `mms-1b-all` model fits within 2.0 GB when launched via Transformers/PyTorch in Python.

## Decision Rule Outcome
Since NO configuration successfully performed Santhali inference below the 2 GB budget, the native `facebook/mms-1b-all` PyTorch configuration is **NOT a candidate for deployment-ready PALASH ASR**.

## Next Steps Pivot
The strict < 2 GB budget dictates we must abandon runtime quantization. In future phases, we will explore:
1. **ONNX Runtime Export**: Offline static INT8 graph generation.
2. **Smaller Model Finetuning**: Targeting a < 300M parameter architecture.
