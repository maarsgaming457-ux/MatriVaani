# MatriVaani — Task 9.1 Complete Project Readiness Audit

## 1. Executive Summary
The MatriVaani project possesses a highly robust, fault-tolerant Android Flutter frontend with sophisticated offline queuing, foreground connectivity triggers, and SQLite-backed checkpoint resume. However, the core Machine Learning backend (ASR, Translation, TTS) is currently hollowed out or lacking critical integration. As of this audit, the SIH Demo is blocked by missing physical model weights, a lack of an integrated translation model, and missing TTS provider credentials.

## 2. Project Structure
- **Backend**: FastAPI structure (pp/api, pp/services). Well-defined.
- **Frontend**: Flutter (ndroid/lib). Highly structured and functional.
- **Models**: The models/ directory contains empty folders for santhali_asr_final_5k and checkpoint-1500. No .safetensors files are physically present.
- **Junk**: Substantial temp files (	emp_12.mp3, 	est_audio.wav, patch.txt, debug_asr_upload.wav, script_queue.py).

## 3. Backend Readiness
- API endpoints (/health, /asr, /translate, /tts) are correctly wired in main.py.
- **Status**: CODE VERIFIED. 

## 4. ASR Readiness
- **ASR STATUS**: C BLOCKER
- The backend points to ASR_PROVIDER=checkpoint and ASR_MODEL_PATH=./models/santhali_asr_final_5k. However, the directory models/santhali_asr_final_5k is completely empty.
- Evaluation Metrics (from 2K Baseline evaluation on checkpoint-1500): WER: 0.605, CER: 0.262, Latency: ~0.96s.
- *Note*: The production model santhali_asr_final_5k has not been evaluated, nor is it present. 

## 5. Translation Readiness
- **TRANSLATION STATUS**: B CANDIDATE / INTEGRATION REQUIRED
- Groq is currently configured in .env but was evaluated as NOT USABLE for Santali.
- IndicTrans2 (i4bharat/indictrans2-indic-indic-dist-320M) was tested successfully in Google Colab (Task 5.8) with a CONDITIONAL PASS but **is completely absent from pp/services/translation_service.py**.

## 6. TTS Readiness
- **TTS STATUS**: C BLOCKER
- TTS_PROVIDER=none in .env.
- Bhashini integration code exists in 	ts_service.py and 	ranslation_service.py but is missing critical BHASHINI_USER_ID and BHASHINI_PIPELINE_ID credentials.

## 7. Flutter Readiness
- Architecturally robust. ClassroomScreen successfully implements audio recording, DB job creation, and delegates backend calls.
- State management and connectivity-triggered foreground queues are cleanly coded.

## 8. Classroom End-to-End Readiness
- The Code-level flow is gapless: Record -> Persist -> Job -> ASR -> Translate -> TTS -> Cleanup.
- Runtime execution will instantly fail at ASR (missing model) and TTS (provider none).

## 9. Offline/Online Architecture
- **OFFLINE**: Audio recording, SQLite job creation (RECORDED state), safe failure retention. No local offline ML inference.
- **ONLINE**: ASR inference, Translation, TTS, queue sequential processing, and 7-day retention cleanup. 

## 10. Database Readiness
- Version 2 SQLite schema with classroom_jobs table.
- CRUD operations, checkpoint updates, and queued retry methods safely coded.

## 11. Storage Readiness
- path_provider handles .wav caching.
- _cleanupOldJobs securely deletes audio and SQLite rows for COMPLETED jobs older than 7 days.

## 12. Connectivity Readiness
- connectivity_plus securely triggers _processQueue upon offline->online transition. 
- Processing is strictly sequential, protected by _isQueueProcessing, and limited to the ClassroomScreen foreground lifecycle.

## 13. API Contract Verification
- Verified mapping between pi_service.dart and main.py.
- Mismatches: None found. Dart properly handles Multipart for ASR, JSON for Translation, and raw bytestreams for TTS.

## 14. Environment / Configuration Status
- GROQ_API_KEY: SECRET FOUND — VALUE NOT SHOWN
- OPENAI_API_KEY: SECRET FOUND — VALUE NOT SHOWN
- BHASHINI_API_KEY: SECRET FOUND — VALUE NOT SHOWN
- BHASHINI_USER_ID: MISSING
- BHASHINI_PIPELINE_ID: MISSING
- TTS_PROVIDER: CONFIGURED (as "none")

## 15. Dependency Audit
- Backend equirements.txt correctly targets 	orch, 	ransformers, astapi.
- Frontend pubspec.yaml targets sqflite, connectivity_plus, udioplayers, ecord.

## 16. Security / Privacy Audit
- **Critical Risk**: pp/api/main.py explicitly dumps all incoming user audio to debug_asr_upload.wav in the project root. This is a massive privacy violation and storage leak for production.
- Keys are hardcoded directly into the .env root file.

## 17. Performance Evidence
- **MEASURED ASR Latency** (2K checkpoint): ~0.96s
- **MEASURED IndicTrans2 Latency** (Colab T4): ~0.167s

## 18. Physical Runtime Status
- PHYSICAL RUNTIME: NOT_VALIDATED
- Items unvalidated on physical device: Android ASR runtime, Android translation runtime, Android TTS runtime, Real offline connectivity triggers.

## 19. SIH Demo Readiness
- WHAT WORKS NOW: Flutter UI, Local Database, Audio Recording.
- WHAT IS BLOCKED: ASR, Translation, TTS.
- WHAT MUST BE FIXED: ML backend integrations and credential acquisition.

## 20. Blocker Prioritization
- **P0 — DEMO BLOCKER**: IndicTrans2 Backend Integration. Groq is known to hallucinate; the system requires a functioning translation provider.
- **P0 — DEMO BLOCKER**: ASR Model Physical Presence. Download santhali_asr_final_5k.zip and extract to models/.
- **P0 — DEMO BLOCKER**: TTS Provider/Bhashini Credentials. Must configure BHASHINI_USER_ID and PIPELINE_ID.
- **P1 — HIGH PRIORITY**: Remove debug_asr_upload.wav hardcoding from main.py.

## 21. Recommended Next Task
**IndicTrans2 production integration**. 
*Reason*: Translation is the literal bridge between ASR and TTS. We have validated that Groq is useless for Santali. Integrating the successfully tested IndicTrans2 model into the FastAPI 	ranslation_service.py is the absolute most critical coding task remaining to make the application functionally translate correctly.

## 22. Files Inspected
- ndroid/lib/screens/classroom_screen.dart
- ndroid/lib/services/db_service.dart
- ndroid/lib/services/api_service.dart
- pp/api/main.py
- pp/services/asr_service.py
- pp/services/translation_service.py
- pp/services/tts_service.py
- .env & .env.example
- Various Phase Reports (Baseline, IndicTrans2 Validation).

## 23. Confirmation of zero modifications
FILES_MODIFIED: NO
PACKAGES_INSTALLED: NO
MODELS_DOWNLOADED: NO
BACKEND_MODIFIED: NO
FLUTTER_MODIFIED: NO
DATABASE_MODIFIED: NO
ENV_MODIFIED: NO
BHASHINI_CALLED: NO
INDICTRANS2_INTEGRATED: NO
FAKE_AUDIO: NO

---

FINAL DECISION:
**C. MAJOR BLOCKERS REMAIN**
