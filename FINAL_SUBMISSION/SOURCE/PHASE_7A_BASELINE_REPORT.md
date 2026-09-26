# MATRI VAANI — PHASE 7A BASELINE & ARCHITECTURE INVENTORY

## 1. Project Tree Summary
- \pp/\: FastAPI Windows backend containing core APIs and service routers.
- \ndroid/\: Flutter client application.
- \models/\: Local ML models (Santali ASR, Ho ASR).
- \	ools/\: Experimental tools, including the \ho_annotator\.
- \datasets/\: Offline datasets and caching.

## 2. Backend Architecture
- **Framework:** FastAPI (\pp/api/main.py\) running locally on Windows (127.0.0.1:8000).
- **Services:** Service-oriented architecture with dedicated routers for ASR (\sr_service.py\), Translation (\	ranslation_service.py\), TTS (\	ts_service.py\), and Offline Sync (\offline_service.py\).

## 3. Flutter Architecture
- **Framework:** Flutter/Dart inside the \ndroid/\ directory.
- **Entrypoint:** \ndroid/lib/main.dart\.
- **UI Screens:** \	ranslator_screen.dart\ (General text translation) and \classroom_screen.dart\ (Teacher/Student voice translation pipeline).
- **Networking:** Communicates via \ApiService\ to the FastAPI backend.

## 4. Current Language Support
- **Hindi:** Supported (ASR via Groq/Whisper, Translation via IndicTrans2, TTS via Sarvam).
- **Santali:** Supported (ASR via local model, Translation via IndicTrans2).
- **Ho:** Partially supported. Local ASR is integrated and working in the backend, but Ho is NOT currently exposed in the Flutter UI.

## 5. Current Provider / Router Support
- **ASR:** Checkpoint (Local Wav2Vec2), HuggingFace, Mock, Groq (Hindi).
- **Translation:** IndicTrans2 (Remote/Local), Groq, OpenAI, Bhashini, Mock.
- **TTS:** Sarvam, Bhashini, Local (Parler-TTS), Mock.

## 6. Current Ho ASR Integration
- Integrated natively in \pp/services/asr_service.py\. Uses the \./models/ho_asr\ Wav2Vec2 model. Supports inference via PyTorch on CPU/GPU.

## 7. Current IndicTrans2 Integration
- Configured as \indictrans2_local\ in \.env\.
- Inference routes to a WSL2 server running on \http://127.0.0.1:8001/translate\. The \	ranslation_service.py\ manages a 45s timeout to accommodate CPU inference limits.

## 8. Current Sarvam Integration
- Integrated for Hindi TTS in \	ts_service.py\. API key is configured in \.env\. Currently restricted to \hi-IN\ language using the \ulbul:v3\ model.

## 9. Current Bhashini Integration
- Code logic exists for Translation and TTS, but credentials (\BHASHINI_USER_ID\, etc.) remain unconfigured/ON HOLD.

## 10. Android Networking
- Configured in \ndroid/.env\ using \API_BASE_URL=http://10.0.2.2:8000\, allowing the emulator to seamlessly reach the Windows host's localhost.

## 11. Offline Functionality
- Handled by \pp/services/offline_service.py\. Implements a SQLite-based two-way synchronization engine with Last-Write-Wins (LWW) conflict resolution for caching classroom data offline.

## 12. Production-Critical Files
- \pp/api/main.py\ and all \pp/services/*.py\
- \ndroid/lib/**/*.dart\
- \.env\ and \ndroid/.env\
- \models/santhali_asr_final_5k/*\ and \models/ho_asr/*\

## 13. Experimental Files
- \	ools/ho_annotator/*\ (Annotation Pilot Tool)
- \enchmark_*.py\, \	est_*.py\, \evaluate_*.py\
- Extraneous text reports (\sr_result.txt\, etc.)

## 14. Current Known Bugs
- The Flutter UI (Classroom and Translator screens) hardcodes Santali and Hindi, preventing users from selecting or utilizing the functional Ho ASR endpoint.

## 15. Current Known Limitations
- Ho-Hindi machine translation is impossible due to a lack of training data.
- TTS is currently disabled or strictly limited to Hindi (via Sarvam). No Santali or Ho TTS exists.

## 16. Git Status
- Branch: \integration/matrivaani-ui-ho-asr\
- Status: Clean production code. 3 modified files strictly contained within \	ools/ho_annotator/\ (app.py, index.html, annotations.db). Numerous untracked scripts and reports exist in the root directory.

## 17. Recommended Next Implementation Step
- **Step 1:** Modify the Flutter UI (\	ranslator_screen.dart\ and \classroom_screen.dart\) to expose "Ho" as a selectable language.
- **Step 2:** Update \pp/services/translation_service.py\ to gracefully intercept Ho translation requests and return a fallback message (e.g., "Ho translation pending pilot data") so the pipeline doesn't crash.

