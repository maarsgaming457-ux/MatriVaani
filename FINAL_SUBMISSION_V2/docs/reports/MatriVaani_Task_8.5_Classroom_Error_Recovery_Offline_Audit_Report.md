# MatriVaani — Task 8.5 Classroom Error & Recovery Audit Report

## 1. Current classroom state machine
The pipeline explicitly enforces a strict sequence:
RECORDING → TRANSCRIBING → TRANSLATING → PLAYING
If any node yields an exception, null, or empty data, the machine aborts the sequence, halts the loading state (_isProcessing = false), and falls back to a readable Error state.

## 2. Backend-unavailable behavior
**BACKEND_FAILURE_HANDLED: YES**
If http://10.0.2.2:8000 is down, ApiService.transcribeAudio throws an exception which is caught in the 	ry/catch block. It returns 
ull. The _stopRecording catch block traps it, displaying "Error processing audio (Online required)" and cleanly resetting _isProcessing = false. The user can tap the mic again once the network returns.

## 3. ASR failure behavior
**ASR_FAILURE_HANDLED: YES**
A 500/503 from /asr causes ApiService.transcribeAudio to return 
ull. The UI displays "Error: Transcription failed." and aborts translation.

## 4. Empty-ASR behavior
**EMPTY_ASR_HANDLED: YES**
*Fix Applied:* If the ASR returns "" or whitespace, a new guard if (transcript.trim().isEmpty) prevents the app from querying /translate. The UI displays "Error: Transcription empty." and resets.

## 5. Translation failure behavior
**TRANSLATION_FAILURE_HANDLED: YES**
A 500/503 from /translate returns 
ull. The UI displays "Error: Translation failed." and aborts the TTS request.

## 6. Empty-translation behavior
**EMPTY_TRANSLATION_HANDLED: YES**
*Fix Applied:* If translation yields "", a new guard if (translation.trim().isEmpty) aborts the TTS request. The UI displays "Error: Translation empty." and resets.

## 7. TTS 503 behavior
**TTS_503_HANDLED: YES**
Because TTS_PROVIDER=none, the backend intentionally returns 503 Service Unavailable. ApiService.synthesizeSpeech handles the non-200 code gracefully, returning 
ull. The UI interprets this as playback failure, safely exiting the loading spinner and displaying "TTS is currently unavailable." 

## 8. TTS malformed-response behavior
**TTS_FAILURE_HANDLED: YES**
If /tts returns 200 OK but with 0 bytes of payload, TtsPlayerService.playTts traps if (audioBytes == null || audioBytes.isEmpty) and immediately returns alse. This protects the native udioplayers library from attempting to decode an empty byte buffer, which could hang the engine.

## 9. Recording failure behavior
**RECORDING_FAILURE_HANDLED: YES**
If Permission.microphone is denied, it displays "Microphone Permission Denied!" and halts. If _audioRecorder.stop() returns an empty file (0 bytes), the filesystem check aborts the pipeline with "Error: Recorded file is empty."

## 10. Playback failure behavior
**PLAYBACK_FAILURE_HANDLED: YES**
If _audioPlayer.play() throws an exception (e.g. corrupt wav bytes), catch (e) explicitly sets _isPlaying = false and returns alse to the UI, allowing the user to immediately start a new recording.

## 11. Retry/recovery analysis
**RETRY_RECOVERY_SAFE: YES**
In all scenarios (ASR failure, translation failure, TTS 503), _isProcessing securely flips back to alse. This unlocks the microphone button, allowing the user to initiate a brand-new workflow immediately without needing to restart the application.

## 12. Offline behavior
**OFFLINE_BEHAVIOR_DOCUMENTED: YES**
- ASR: NOT IMPLEMENTED OFFLINE (Requires API)
- Translation: NOT IMPLEMENTED OFFLINE (Requires API)
- TTS: NOT IMPLEMENTED OFFLINE (Requires API)
If the user loses internet, the very first POST to /asr times out and drops them into "Error processing audio (Online required)". No fake offline data is fabricated.

## 13. API service error handling
ApiService safely swallows exceptions and raw HTTP text, returning structured 
ulls for the UI to consume. The UI avoids displaying raw stack traces or JSON blobs to the end-user.

## 14. Downstream-request prevention
**NO_DOWNSTREAM_REQUEST_AFTER_FAILURE: YES**
Strict sequential guards ensure that no upstream failure triggers a downstream request.

## 15. State reset matrix
| Failure | Transcription | Translation | Error | Processing | Playback |
|---------|---------------|-------------|-------|------------|----------|
| ASR failure | Unchanged | Unchanged | "Error: Transcription failed." | alse | None |
| Empty ASR | Unchanged | Unchanged | "Error: Transcription empty." | alse | None |
| Translation failure | Visible | Unchanged | "Error: Translation failed." | alse | None |
| Empty translation | Visible | Unchanged | "Error: Translation empty." | alse | None |
| TTS 503 | Visible | Visible | "TTS is currently unavailable."| alse | None |
| TTS failure | Visible | Visible | "TTS is currently unavailable."| alse | None |
| Playback failure| Visible | Visible | "TTS is currently unavailable."| alse | alse |
| Recording failure| Unchanged | Unchanged | "Error: Recorded file is empty."| alse | None |

## 16. Changes made
Modified ndroid/lib/screens/classroom_screen.dart to include two new fast-fail guards:
- if (transcript.trim().isEmpty)
- if (translation.trim().isEmpty)
These explicitly prevent meaningless /translate and /tts API queries if the upstream node produces silence or whitespace.

## 17. flutter analyze result
PASS

## 18. debug APK build result
PASS

## 19. Backend regression checks
No modifications were made to sr_service.py, 	ranslation_service.py, 	ts_service.py, .env, or TTS_PROVIDER.

## 20. Known runtime-validation limitation
Validation is based on static flow analysis and API mocking. Physical Android testing was not possible because the AI operates in a headless execution environment.

## 21. Exact next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**

---

FINAL DECISION:
**B. MINOR RECOVERY FIX REQUIRED**

BACKEND_FAILURE_HANDLED: YES
ASR_FAILURE_HANDLED: YES
EMPTY_ASR_HANDLED: YES
TRANSLATION_FAILURE_HANDLED: YES
EMPTY_TRANSLATION_HANDLED: YES
TTS_503_HANDLED: YES
TTS_FAILURE_HANDLED: YES
RECORDING_FAILURE_HANDLED: YES
PLAYBACK_FAILURE_HANDLED: YES
RETRY_RECOVERY_SAFE: YES
OFFLINE_BEHAVIOR_DOCUMENTED: YES
NO_DOWNSTREAM_REQUEST_AFTER_FAILURE: YES
ASYNC_DISPOSE_SAFE: YES

ASR_MODIFIED: NO
TRANSLATION_MODIFIED: NO
TTS_PROVIDER_CHANGED: NO
BHASHINI_CALLED: NO
FAKE_AUDIO: NO

FLUTTER_ANALYZE: PASS
DEBUG_APK: PASS
ANDROID_PHYSICAL_RUNTIME: NOT_VALIDATED
