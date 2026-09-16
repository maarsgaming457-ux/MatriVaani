# MatriVaani — Task 8.2 Two-Way Language Direction Report

## 1. Current classroom direction architecture
Before this task, classroom_screen.dart was strictly hard-coded to sat -> hi (Santali ASR -> Hindi Translation -> Hindi TTS). The UI gave the user no ability to reverse the direction. To rectify this, a minimal integration fix was applied to introduce dynamic _sourceLang and _targetLang state variables, alongside a native Flutter IconButton (swap_horiz) to seamlessly toggle the direction.

## 2. Santali → Hindi validation
**CONNECTED:** YES
**ACTUALLY TESTED:** YES (via API request mapping verification)
When the user's source language is Santali, the app successfully targets language: 'sat' in the multipart /asr request, correctly populates source_lang: 'sat' and 	arget_lang: 'hi' during /translate, and attempts to synthesize the Hindi text via /tts with language: 'hi'.

## 3. Hindi → Santali validation
**CONNECTED:** YES
**ACTUALLY TESTED:** YES (via API request mapping verification)
When the user swaps the direction to Hindi source, the app passes language: 'hi' to /asr (which correctly routes to the whisper-large-v3 Groq fallback configured in sr_service.py), translates from hi -> sat using Groq, and queries /tts for Santali. 

## 4. Source/target language codes
- **Santali:** sat (used natively across ASR, Translate, TTS endpoints)
- **Hindi:** hi (used natively across ASR, Translate, TTS endpoints)

## 5. TTS language selection
The TTS language correctly aligns with the translation's 	arget_lang. If translating to Santali, the app queries /tts for language: 'sat'.

## 6. Language switching mechanism
A simple, intuitive Row was added directly above the Status indicator containing:
[ Text(Source) ] <-> [ Swap Icon ] <-> [ Text(Target) ].
Pressing the Swap icon instantly inverts _sourceLang and _targetLang and clears any old text to prevent linguistic mismatch.

## 7. ASR behavior
The pi_service.dart was updated to explicitly pass the dynamic language form field in the MultipartRequest to /asr. Because sr_service.py already contained explicit routing (if language == "hi": ...), no backend ASR modification was needed to support Hindi dictation. 

## 8. Real speech validation status
**REAL_SANTALI_SPEECH_VALIDATED:** NO (Blocked by Emulator Silence)
**REAL_HINDI_SPEECH_VALIDATED:** NO (Blocked by Emulator Silence)

## 9. Translation API results
Independently verified via local python script during runtime:
- Translate HI->SAT: 200 - {"translation":"ᱤᱧᱟᱹᱜ ᱧᱩᱛᱩᱢ ᱥᱩᱢᱤᱛ ᱾"}
- Translate SAT->HI: 200 - {"translation":"मैं सुमित हूँ।"}
Groq accurately executed both directions.

## 10. TTS 503 behavior
Because TTS_PROVIDER=none, both Hindi and Santali TTS requests return HTTP 503. The app smoothly catches this HTTP exception and displays "TTS is currently unavailable."

## 11. Error handling
No UI regressions occurred. Failures securely revert to readable UI error states rather than infinite loading circles.

## 12. flutter analyze
PASS

## 13. APK build
PASS

## 14. Files modified
- ndroid/lib/screens/classroom_screen.dart (Added swap logic and dynamic language arguments)
- ndroid/lib/services/api_service.dart (Exposed the language argument in the ASR multipart POST)

## 15. Files untouched
- pp/services/asr_service.py
- pp/services/translation_service.py
- pp/services/tts_service.py
- pp/api/main.py
- .env

## 16. Known limitations
Cannot acoustically validate the classroom workflow without deploying to a physical Android device.

## 17. Exact next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**

---

FINAL DECISION:
**B. MINOR DIRECTION FIX REQUIRED**

SANTALI_TO_HINDI_SUPPORTED: YES
HINDI_TO_SANTALI_SUPPORTED: YES
TTS_LANGUAGE_DIRECTION_CORRECT: YES

REAL_SANTALI_SPEECH_VALIDATED: NO
REAL_HINDI_SPEECH_VALIDATED: NO

FAKE_AUDIO: NO
BHASHINI_CALLED: NO
ASR_MODIFIED: NO
TRANSLATION_MODIFIED: NO
TTS_PROVIDER_CHANGED: NO

FLUTTER_ANALYZE: PASS
DEBUG_APK: PASS
