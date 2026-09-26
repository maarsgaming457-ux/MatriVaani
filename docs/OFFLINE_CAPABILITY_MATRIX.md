# Offline Capability Matrix

The following table documents the actual, physically verified offline capabilities of MatriVaani.

> **Note:** A feature is only marked `Yes` under **Offline** if it has been physically tested on an Android device with the internet disabled. Local PC network routing (i.e. Android connecting to a locally hosted FastAPI backend over Wi-Fi) does **not** count as offline.

| Feature | Online | Offline | Current Implementation | Required Work |
|---------|--------|---------|------------------------|---------------|
| Hindi → Mundari translation | Yes | Target: Yes | Python model (`.safetensors`) | Convert to Android runtime (TFLite/ONNX/ExecuTorch) |
| Santali ASR | Yes | Target: Yes | FastAPI/PyTorch | Convert to Android runtime |
| TTS | Yes | Target: Yes | Cloud TTS (Sarvam/Bhashini) | Local TTS engine required |
| Voice Pipeline | Yes | Target: Yes | Server pipeline | Local mobile pipeline integration |
| Flutter UI | Yes | Yes | Flutter | None |

## Language Capability Registry

This registry defines the execution limits per language. The UI will only show capabilities that actually exist in this registry.

```yaml
Mundari:
  online_translation: true
  offline_translation: false

Santali:
  online_asr: true
  offline_asr: false
  online_translation: true
  offline_translation: false
  online_tts: true
  offline_tts: false
```
