# NMT Model Comparison for MatriVaani

| Model | Parameters | Hindi Support | Santhali Support | Adaptability | Model Size | Runtime RAM | Latency | Offline | Quantization | Android | License | Fine-tuning |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **facebook/nllb-200-distilled-600M** | 600M | EXPLICIT | UNKNOWN (sat not natively listed) | High via LoRA | ~2.4 GB (FP32) | ~1.5 GB | UNKNOWN | Yes | INT8/INT4 | Possible | MIT | Yes |
| **AI4Bharat/IndicTrans2** (indic-en) | ~1.1B | EXPLICIT | EXPLICIT (sat_Olck) | Native Support | ~4.4 GB (FP32) | ~3.0 GB | UNKNOWN | Yes | INT8/INT4 | Challenging | MIT | Yes |
| **google/mt5-small** | 300M | EXPLICIT | UNKNOWN (mC4) | High | ~1.2 GB (FP32) | ~800 MB | UNKNOWN | Yes | INT8 | Feasible | Apache 2.0 | Yes |

### Analysis

#### NLLB (Meta)
NLLB supports 200 languages, but Santhali (sat) is notoriously missing from the native FLORES-200 benchmark and native tokenizers. While NLLB is extremely adaptable, we would need to replace tokens and essentially train a low-resource adapter for Santhali from scratch. The 600M distilled version is highly suitable for Android if INT8 quantized, but the lack of native Santhali vocabulary is a major hurdle.

#### IndicTrans2 (AI4Bharat)
IndicTrans2 natively supports Santhali (`sat_Olck`) and is the most advanced model for Indian scheduled languages. It excels in Hindi <-> Santhali. However, the model is ~1.1B parameters. At FP32, it requires over 4GB of RAM. With INT8, it requires ~1.5-2.0GB just for the NMT layer. Since our overall application budget is <2GB, running IndicTrans2 simultaneously with ASR (~850MB) and TTS (~300MB) is physically impossible without aggressive swapping or quantization, which breaks the real-time latency requirement.

#### mT5-small (Google)
mT5-small is very compact (300M parameters) and fits comfortably in memory. However, it requires extensive fine-tuning to perform adequate translation, and its tokenization for Ol Chiki is heavily fragmented (falling back to byte-level), which balloons sequence lengths and ruins latency on mobile.

### Recommendation
**Custom NMT architecture or highly quantized IndicTrans2.**
If we use IndicTrans2, we must adopt an asynchronous lifecycle: unload ASR from memory before loading NMT. Alternatively, we could distill a 200M-300M parameter student model from IndicTrans2 exclusively for Hindi <-> Santhali, achieving native Ol Chiki support while fitting into ~300MB of RAM.
