# PHASE 14 PRE-HARDENING INVENTORY

**Date/time:** 2026-09-16 18:00:12

## Verification of Current Capabilities

1. **Hindi speech → Hindi ASR**: Implemented via Sarvam API (pp/services/speech/sarvam_asr.py).
2. **Ho speech → Ho ASR**: Implemented via local Whisper-based model (pp/services/speech/ho_asr_local.py).
3. **Hindi → Santali translation**: Implemented via WSL IndicTrans2 local API (pp/services/translation/indictrans2_provider.py).
4. **Santali → Hindi translation**: Implemented via WSL IndicTrans2 local API.
5. **Hindi TTS**: Implemented via Sarvam API (pp/services/speech/sarvam_tts.py).
6. **Sarvam integration**: Active for Hindi ASR and TTS.
7. **Bhashini integration/status**: Kept as fallback/reference for Indic language translation.
8. **Offline SQLite queue**: Implemented in Android Flutter app (pp_flutter/lib/core/database.dart).
9. **Android microphone recording**: Active (pp_flutter/lib/services/audio_service.dart).
10. **Android → FastAPI communication**: Active via Dio/HTTP (pp_flutter/lib/services/api_service.dart).
11. **Windows FastAPI → WSL IndicTrans2**: Active via proxy requests to WSL IP port 8000.
12. **Ho translation warning**: Implemented in backend (pp/api/endpoints/translate.py) which explicitly blocks ho as source/target.
