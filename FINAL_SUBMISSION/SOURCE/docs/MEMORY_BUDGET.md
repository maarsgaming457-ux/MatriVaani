# PALASH Memory Budget (Corrected)

## Deployment Target
**Hardware**: Low-cost Android Tablet
**Total Physical RAM**: ~2.0 GB
**Available Application RAM**: ~1.7 GB (Assuming ~300 MB reserved for Android OS overhead).

## Empirical ASR Memory Reality
Through strict verification in Phase 2.5, we measured the exact footprint of `facebook/mms-1b-all` when executed directly via the PyTorch/Transformers runtime:

1. **FP32 Baseline**: The model weights natively consume **~4.1 GB** of Peak RAM, instantly exceeding the hardware envelope.
2. **INT8 Dynamic Quantization**: While quantization theoretically shrinks the model, PyTorch's `quantize_dynamic` creates an in-memory copy during conversion. This caused an incredible **9.6 GB RAM spike** during the load sequence, completely ruling out dynamic runtime quantization.
3. **Streaming FP32**: Slicing the audio into 2-second chunks successfully suppresses activation tensor bloat, but the underlying model weights still inherently demand **~4.1 GB**. 

## Adjusted Memory Strategy
Given the empirical evidence, it is physically impossible to run `facebook/mms-1b-all` directly in the native PyTorch/Transformers environment on a 2GB device.

To fit within the **1.7 GB Budget**, we **must** pivot the deployment architecture to one of the following offline strategies in future phases:
1. **ONNX Export & Offline Quantization**: Export the FP32 model to ONNX, quantize the graph to INT8 on a high-RAM desktop machine, and deploy the `.onnx` binary using `onnxruntime-mobile`.
2. **ExecuTorch / PyTorch Mobile**: Export to PTI (PyTorch Edge) and apply static offline quantization.

For now, the ASR memory constraint of < 2 GB is formally marked as **FAILED** for the native PyTorch runtime environment.

## Projected Budget (Assuming Successful ONNX INT8 Conversion)
*If we successfully export to an optimized ONNX INT8 binary later, the budget looks like this:*

| Component | Budget |
|-----------|--------|
| Base UI | 300 MB |
| Audio Buffers | 50 MB |
| ASR Model (ONNX INT8) | 1,200 MB |
| Inference Tensors (Chunked) | 100 MB |
| **Total Peak** | **1,650 MB** |
