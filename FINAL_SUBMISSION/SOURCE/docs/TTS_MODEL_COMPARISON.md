# TTS Model Comparison

This document evaluates Text-to-Speech architectures for MatriVaani's Santhali capabilities.

| Model | Parameters | Santhali Support | Multilingual Support | Training Data Required | Inference RAM | Latency | Audio Quality | Model Size | Fine-tuning | Quantization | ONNX | Android Feasibility | License |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Indic Parler-TTS (AI4Bharat)** | ~800M+ | EXPLICIT (sat) | Yes (22 languages) | High | ~2.5 GB+ | High (without ORT) | Very High | > 1.5 GB | Yes | Yes (INT8) | Unknown | VERY LOW (Fails 2GB ceiling) | Gated / Research |
| **VITS (End-to-End)** | ~30M-80M | ADAPTABLE | Yes (via Phonemizer) | Medium (10-20 hrs) | ~150 MB | Low | High | ~150 MB | Yes | Yes | Yes | HIGH | Open (MIT/Apache) |
| **FastSpeech2 + HiFi-GAN** | ~50M (Acoustic) + 15M (Vocoder) | ADAPTABLE | Yes | Medium | ~200 MB | Low | High | ~250 MB | Yes | Yes | Yes | HIGH | Open |
| **SraVaani (ARTPARK)** | Unknown | EXPLICIT (sat) | Yes | High | Unknown | Unknown | Unknown | Unknown | Yes | Unknown | Unknown | LOW (Likely heavy) | Gated |
| **Google/Azure APIs** | N/A (Cloud) | EXPLICIT (Azure) | Yes | None | N/A | Variable (Network) | Very High | N/A | No | N/A | N/A | EXCLUDED (Offline requirement) | Proprietary |

## Conclusion
While **Indic Parler-TTS** offers state-of-the-art Santhali capability, its sheer size makes it fundamentally incompatible with MatriVaani's strict 2GB Android RAM ceiling alongside ASR and NMT models.

**VITS** (Variational Inference with adversarial learning for end-to-end Text-to-Speech) is the strongly recommended architecture. It provides high-quality end-to-end synthesis, is easily exported to ONNX, operates smoothly on Android CPUs, and typically requires <200MB of RAM. We must fine-tune a VITS model using a Santhali dataset.
