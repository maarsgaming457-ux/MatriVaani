# Phase 2.5: ASR Memory Optimization Report

## 1. Original Baseline
The initial observation of the chosen acoustic model (`facebook/mms-1b-all`) was a peak footprint of ~4.1 GB. This required optimization because our target hardware maxes out at 2.0 GB.

## 2. Hardware and Software Environment
- **Hardware**: Desktop CPU Validation (Simulated Android Bounds). Max RAM evaluated against 2.0 GB Application limit.
- **Python Version**: 3.14.2
- **PyTorch Version**: Current Environment (`torch`)
- **Transformers Version**: Current Environment (`transformers`)

## 3. MMS Adapter Configuration
The `facebook/mms-1b-all` model natively relies on dynamically fetched `sat` adapters. We strictly enforced loading the `sat` adapter in inference *prior* to quantization to ensure state dict integrity, properly maintaining intended Santhali capability. 

## 4. Quantization Attempts & Results
To compress the 1B parameters, we attempted PyTorch Dynamic INT8 Quantization (`torch.quantization.quantize_dynamic`).
- **Successful Experiments**: `None`
- **Failed Experiments**: 
  - Dynamic INT8 Quantization (Massive memory load spike).
  - FP32 Streaming Chunked Processing (No baseline model reduction).

## 5. Actual Verified Measurements

### FP32 Baseline (MMS 1B)
- **Model Load RAM**: ~144 MB 
- **Inference Spike (Full Audio)**: ~3,600 MB 
- **Actual Peak RAM**: **4,081 MB**
- **Actual Latency (RTF)**: ~0.60

### Dynamic INT8 Quantization (MMS 1B)
- **Model Load RAM**: ~9,268 MB (Memory copying during conversion)
- **Inference Spike**: ~28 MB
- **Actual Peak RAM**: **9,698 MB**
- **Actual Latency (RTF)**: ~1.08

### FP32 Streaming (Chunked - 2s windows)
- **Actual Peak RAM**: **4,119 MB** (Model baseline overrides activation savings).

*Note: Santhali accuracy regression not yet measurable due to insufficient verified evaluation data.*

## 6. Memory Budget & Streaming Results
Chunking audio (Streaming) drops peak *activation* tensor size drastically (seen in the 28 MB INT8 spike), but fails to impact the raw FP32 PyTorch model weights (~4.1 GB). 
As detailed in `docs/MEMORY_BUDGET.md`, there is zero room to accommodate a 4 GB or 9 GB model spike inside a 1.7 GB total budget.

## 7. Selected Low-Memory Configuration
**None.** The PyTorch/Transformers runtime is structurally incapable of natively loading a 1 Billion parameter model under 2.0 GB Peak RAM. 

## 8. Remaining Problems
The 1.65 GB value in the previous report was not accepted as a verified result because the original quantization experiment failed during execution. It has been overwritten. We must abandon PyTorch-native runtime deployment.

## 9. Conclusion against Criteria
- **Whether <2 GB is actually achieved**: NO.
- **Whether ≤1.5 GB is actually achieved**: NO.

## 10. Exact Next Step
Instead of moving to Fine-Tuning immediately, our exact next step should be exploring exporting smaller ASR variants (e.g., 300M parameter base models) or testing statically quantized ONNX binaries to definitively solve the 2.0 GB ASR bottleneck.
