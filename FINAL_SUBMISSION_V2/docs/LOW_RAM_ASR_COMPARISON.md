# Low RAM ASR Model Comparison (Empirical)

## Objective
Identify an ASR architecture that maintains Santhali recognition support but remains below the absolute 2.0 GB RAM footprint budget on Android hardware.

## Evaluated Configurations (Verified via Runtime Hooks)

| Model | Variant | Quantization | Size on Disk (MB) | Peak RAM (MB) | Santhali (`sat`) Support | Latency (RTF) | Status |
|-------|---------|--------------|-------------------|---------------|--------------------------|---------------|--------|
| `mms-1b-all` | Full 1B | None (FP32) | ~3,800 MB | ~4,081 MB | Yes (Native) | ~0.60 | **FAILED** (>2GB) |
| `mms-1b-all` | Full 1B | Dynamic INT8 | ~1,200 MB | ~9,698 MB | Yes (Native) | ~1.08 | **FAILED** (9.6GB Load Spike) |
| `mms-1b-all` (Chunked) | Full 1B | None (FP32) | ~3,800 MB | ~4,119 MB | Yes (Native) | ~0.60 | **FAILED** (>2GB) |
| `whisper-tiny` | Tiny | None (FP32) | ~150 MB | ~591 MB | No | ~2.90 | **FAILED** (No Santhali) |

## Analysis
- **Whisper**: Fits the memory profile flawlessly, but entirely lacks Santhali.
- **MMS 1B FP32**: PyTorch inherently pulls the 4.1 GB model weights into memory directly, blowing the 2 GB budget by 2x.
- **MMS 1B INT8 Dynamic**: `torch.quantization.quantize_dynamic` creates a copy of the model in memory *during* conversion at runtime. While the inference footprint shrinks drastically, the 9.6 GB Peak RAM spike during load completely disqualifies this approach for edge deployment natively via PyTorch.
- **Streaming FP32**: Slicing the audio into 2-second chunks successfully suppresses activation tensor bloat, but cannot shrink the base weight requirement of ~4.1 GB.

## Android Feasibility Reality
We **cannot** run `facebook/mms-1b-all` natively via the PyTorch/Transformers engine on a 2GB tablet. The Android application would be immediately OOM killed during initialization.

The only remaining feasibility paths are offline structural changes:
- Exporting to ONNX and compiling it offline with static INT8 quantization (bypassing PyTorch memory bloat).
- Fine-tuning a smaller acoustic model (e.g., `wav2vec2-base` 90M) exclusively for Santhali.
