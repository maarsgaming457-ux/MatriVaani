# MatriVaani Architecture

MatriVaani is designed using a **Dual-Mode Architecture**. It provides a fully connected experience via cloud APIs when the internet is available, and an on-device fallback when offline.

## Core Architecture Tree

```text
                         MATRI VAANI
                              │
                    ┌─────────┴─────────┐
                    │                   │
               ONLINE MODE         OFFLINE MODE
                    │                   │
             Internet available     No Internet
                    │                   │
             Cloud FastAPI API       Android device
                    │                   │
          ┌─────────┼─────────┐      Local models
          │         │         │         │
       Translation  ASR      TTS       ASR/NMT/TTS
          │         │         │         │
          └─────────┴─────────┘         │
                    │                   │
                 Response          Response
                    │                   │
                    └─────────┬─────────┘
                              │
                       Flutter UI
```

## Online Mode Layer
When the internet is available, the Flutter application queries the Cloud FastAPI instance.
- **Backend Framework:** FastAPI (`0.0.0.0`, configurable `$PORT`)
- **Pipeline:** HTTPS → Translation/ASR/TTS endpoints → Response

## Offline Mode Layer
True offline means no internet, no cloud API, no PC hosting the FastAPI server.
- **Pipeline:** Android Microphone/Text → Local On-Device Inference (TFLite/ONNX) → Native App Response.

## Mode Manager Abstraction
The application utilizes a central execution-mode abstraction, avoiding scattered logic inside UI widgets:

```text
ExecutionMode
 ├── automatic (Fallback preferred)
 ├── online    (Force cloud)
 └── offline   (Force local)
```

And corresponding internal engines:
```text
TranslationEngine
 ├── OnlineTranslationEngine
 └── OfflineTranslationEngine

ASREngine
 ├── OnlineASREngine
 └── OfflineASREngine

TTSEngine
 ├── OnlineTTSEngine
 └── OfflineTTSEngine
```

## Automatic Fallback Flow
```text
Internet available
       ↓
     ONLINE
       ↓
 request fails?
    /       \
  no         yes (with short timeout)
  ↓           ↓
response    OFFLINE
```
