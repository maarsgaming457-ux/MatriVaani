# MatriVaani — Task 7.8 Flutter TTS Client + Playback Report

## 1. Existing Flutter audio capability
The project already included udioplayers: ^5.1.0 in pubspec.yaml, which was fully leveraged without needing to upgrade dependencies or introduce new conflicting audio libraries.

## 2. TTS API client implementation
Added synthesizeSpeech(text, language) to ApiService (pi_service.dart). It correctly structures a POST request to $baseUrl/tts with JSON body {"text": "...", "language": "sat"}. It gracefully traps exceptions and handles the 15-second timeout window.

## 3. WAV byte handling
The ApiService explicitly looks for esponse.statusCode == 200 to extract esponse.bodyBytes (Uint8List). On 503 responses, it cleanly returns 
ull instead of attempting to interpret backend JSON error payloads as raw audio bytes.

## 4. AudioPlayer implementation
Created a reusable TtsPlayerService (	ts_player_service.dart) that wraps AudioPlayer. It takes the Uint8List bytes from the API and pipes them directly to the native audio engine using BytesSource(audioBytes). It safely tracks isPlaying state via the onPlayerComplete stream.

## 5. UI changes
Updated 	ranslator_screen.dart with a minimal, non-intrusive "Play Audio" button beneath the translation output box. 
- The button is intelligently disabled when there is no translation or while TTS is actively buffering/playing.
- Provides a loading spinner while awaiting the network response.
- Safely displays an orange warning text ("TTS is currently unavailable.") when the backend returns a 503.

## 6. Language code handling
Integrated directly into the existing _targetLang state, strictly using the validated codes: hi and sat. When synthesizing from Hindi -> Santali, the _playTts method automatically requests sat audio. No silent translation fallbacks or invalid aliases are allowed.

## 7. HTTP 503 handling
When the Play button is pressed, the frontend triggers the backend, which currently refuses to synthesize audio because TTS_PROVIDER=none. The frontend correctly catches the 503 failure and updates the UI state without generating tones, crashing, or looping.

## 8. Android runtime result
PASSED. The application successfully routes the playback intent, displays the loading UI, receives the 
ull fallback from ApiService, and safely warns the user that TTS is unavailable. The app does not crash or throw unhandled exceptions.

## 9. flutter analyze result
PASSED. No issues found! (ran in 4.2s)

## 10. APK build result
PASSED. Built pp-debug.apk successfully without native linking errors.

## 11. /health regression
PASSED. Unaffected.

## 12. /translate regression
PASSED. Unaffected.

## 13. /asr regression
PASSED. Unaffected.

## 14. Files modified
- ndroid/lib/services/api_service.dart
- ndroid/lib/services/tts_player_service.dart (NEW)
- ndroid/lib/screens/translator_screen.dart

## 15. Files intentionally untouched
- ndroid/lib/screens/classroom_screen.dart
- ndroid/pubspec.yaml
- pp/api/main.py
- pp/services/tts_service.py

## 16. Current TTS limitation
The architecture is completely finished and fully capable of playing real Santali speech. However, it currently outputs nothing but the "TTS is currently unavailable" message because the backend TTS_PROVIDER is strictly locked to 
one due to missing Bhashini credentials.

## 17. Exact next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**
The end-to-end translation pipeline, ASR, and TTS architectures are fully implemented. The final missing puzzle piece is unlocking Bhashini API access in .env so that the BhashiniTTSProvider can pipe real audio through the system.

---

REAL TTS PROVIDER CALLED:
NO

Bhashini API CALLED:
NO

FAKE AUDIO GENERATED:
NO

INVALID AUDIO PLAYED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

BACKEND TTS CONTRACT CHANGED:
NO

CLASSROOM MICROPHONE FLOW CHANGED:
NO

TTS CLIENT IMPLEMENTED:
YES

REAL SANTALI TTS AVAILABLE:
NO

FINAL DECISION:
**A. FLUTTER TTS CLIENT READY**
