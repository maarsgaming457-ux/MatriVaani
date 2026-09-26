# MatriVaani — Task 7.7 TTS Provider-Independent Architecture Report

## 1. Current TTS problem
The existing TTS architecture hardcoded i4bharat/indic-parler-tts directly into 	ts_service.py with massive monkey patches. However, Task 7.6 conclusively proved this model is physically impossible to execute on the current Windows machine. Because no other lightweight Santali open-source model exists, and Bhashini is blocked pending credentials, the API required a safe, explicit mechanism to declare TTS unavailable without crashing, returning fake audio, or changing the POST /tts contract.

## 2. Architecture before
- POST /tts -> 	ts_service.py
- Hardcoded Parler-TTS dependency graph
- No provider switching
- Failed with ModuleNotFoundError during server startup, rendering TTS completely broken and polluting application logs.

## 3. Architecture after
- POST /tts -> TTSProviderBase
- The TTS_PROVIDER environment variable dynamically binds the TTSService to an underlying implementation class.
- Invalid or unconfigured providers explicitly route to UnavailableTTSProvider.
- main.py explicitly traps TTSUnavailableError and safely returns an HTTP 503 Service Unavailable status rather than throwing generic 500 exceptions.

## 4. Provider abstraction
Created TTSProviderBase with a single abstract synthesize(text, language) -> bytes method.
Created explicit subclass implementations:
- UnavailableTTSProvider
- BhashiniTTSProvider (raises "ON HOLD")
- LocalTTSProvider (raises "NOT FEASIBLE")

## 5. Provider selection
The system reads the TTS_PROVIDER value from .env to select the class. The .env file was modified to explicitly declare TTS_PROVIDER=none.

## 6. Current unavailable state
When a user hits /tts with TTS_PROVIDER=none, they receive an explicit and clean 503 Service Unavailable with {"detail": "TTS provider is not configured."}. This truthfully reflects the prototype's current technical limitation without pretending to synthesize speech.

## 7. Language handling
Language codes are cleanly normalized (santali/santhali -> sat, hindi -> hi) prior to synthesis routing. No silent fallbacks to Hindi are performed if Santali TTS is requested.

## 8. /tts behavior
The API contract ({"text": "...", "language": "santali"}) remains 100% unchanged. The endpoint correctly returns 503 under the current state. When a real provider is plugged in, it will return udio/wav bytes exactly as designed.

## 9. Error handling
Introduced TTSUnavailableError (extending TTSError). This allows FastAPI to gracefully return a 503 instead of masking the missing configuration behind an unhandled 500 application crash.

## 10. Testing performed
- Successfully compiled the backend tree.
- Manually verified the POST /tts endpoint rejects traffic with a 503 status when .env is 
one.
- Manually verified POST /tts specifically rejects traffic citing Bhashini credential lack when .env is hashini.
- Healthcheck and translation tests successfully completed.

## 11. ASR regression result
PASSED. The ASR flow (pp/services/asr_service.py) was not modified.

## 12. Translation regression result
PASSED. Translation (pp/services/translation_service.py) successfully handles requests utilizing the Groq fallback.

## 13. Health check result
PASSED. The GET /health endpoint returned 200 OK.

## 14. Files modified
- pp/services/tts_service.py: Completely refactored.
- pp/api/main.py: Added explicit 503 exception handling for TTSUnavailableError.
- .env: Added explicit TTS_PROVIDER=none.

## 15. Files intentionally untouched
- pp/services/asr_service.py
- pp/services/translation_service.py
- All Flutter frontend Dart code
- equirements.txt

## 16. Future Bhashini integration point
When Bhashini API credentials arrive, developers simply replace the body of BhashiniTTSProvider.synthesize() with the standard Bhashini HTTP POST routine, decode the base64, and return bytes.

## 17. Future local TTS integration point
If a compiled .whl or lightweight ONNX graph of a Santali model becomes available, it can securely implement the LocalTTSProvider class.

## 18. Risks
Flutter UI components currently have no robust error handling for 503 TTS responses. The Flutter app may silently fail or freeze when attempting to play back classroom translations until proper frontend error states are built.

## 19. Exact next task
**Master Roadmap Phase 2: Implement Frontend TTS Pipeline (Flutter / audioplayers)**
With the backend safely stubbed, the frontend UI logic should be wired to request audio, handle the 503 explicitly, and play audio gracefully once a real provider is linked.

`	ext
Flutter
   |
   | POST /tts
   v
FastAPI /tts (returns 503 currently)
   |
   v
TTS Service
   |
   +---- TTS Provider Interface
              |
              +---- Bhashini (future)
              |
              +---- Local TTS (future)
              |
              +---- Unavailable Provider (current - active)
   |
   v
audio/wav
`

Bhashini API CALLED:
NO

EXTERNAL TTS API CALLED:
NO

TTS MODEL DOWNLOADED:
NO

FAKE AUDIO GENERATED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

FLUTTER CHANGED:
NO

Bhashini CREDENTIALS ADDED:
NO

SECRETS EXPOSED:
NO

/ASR CONTRACT CHANGED:
NO

/TRANSLATE CONTRACT CHANGED:
NO

/tts ROUTE REMOVED:
NO
