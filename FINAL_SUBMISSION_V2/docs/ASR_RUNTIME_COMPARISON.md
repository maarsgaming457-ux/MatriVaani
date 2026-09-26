# ASR Runtime Comparison (Empirical - Phase 2.6)

Below are the empirical memory profiles of the `< 300M parameter` candidate architectures when processed natively in the PyTorch/Transformers engine on the target environment.

## 1. Native FP32 PyTorch Inference (No Compression)

| Candidate Model | Parameters | Model Load RAM (MB) | Peak Inference RAM (MB) | RTF (Latency) | Status for < 2GB Budget |
|-----------------|------------|---------------------|-------------------------|---------------|-------------------------|
| `openai/whisper-tiny` | 39M | 483 | **693** | 0.48s | **PASS (Excellent)** |
| `openai/whisper-base` | 74M | 486 | **841** | 0.96s | **PASS (Very Good)** |
| `facebook/wav2vec2-base-*` | 90M | 485 | **845** | 0.27s | **PASS (Very Good)** |
| *Previous: `mms-1b-all`* | *1000M* | *144* | ***4,081*** | *0.60s* | *FAILED* |

## 2. Dynamic INT8 PyTorch Quantization

*Note: PyTorch runtime dynamic conversion creates temporary memory copies of weight matrices. For small models, this overhead sometimes exceeds the memory saved during active inference.*

| Candidate Model | Peak Conversion Spike (MB) | Peak Inference RAM (MB) | RTF (Latency) | Status for < 2GB Budget |
|-----------------|----------------------------|-------------------------|---------------|-------------------------|
| `openai/whisper-tiny` (INT8) | 884 | **789** | 0.41s | PASS |
| `openai/whisper-base` (INT8) | 1,245 | **1,023** | 0.56s | PASS |
| `facebook/wav2vec2-base-*` (INT8)| 1,371 | **1,441** | 0.18s | PASS |

## Conclusions on Runtime

1. **FP32 is Sufficient:** All three candidate base models inherently stay under 850 MB of Peak RAM in pure FP32. This flawlessly fits the `< 1.5 GB` preference and absolute `< 2.0 GB` hardware limit.
2. **Dynamic INT8 is Unnecessary / Counterproductive:** Because the PyTorch conversion overhead spikes RAM up to 1.4 GB, simply loading the models in native FP32 is paradoxically *more* memory efficient in a raw Python environment than dynamically quantizing them. (Offline ONNX INT8 would still be beneficial, but is no longer strictly mandatory to prevent OOM crashes).
3. **Speed:** The `wav2vec2-base` architecture is significantly faster (0.27s) than Whisper because it acts purely as a CTC extractor rather than an autoregressive Seq2Seq generator.
