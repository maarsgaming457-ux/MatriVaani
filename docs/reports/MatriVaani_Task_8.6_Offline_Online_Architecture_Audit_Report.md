# MatriVaani — Task 8.6 Offline/Online Architecture Audit Report

## 1. Current architecture
The MatriVaani Classroom workflow relies on a strictly **ONLINE-ONLY** architecture. The local Flutter application serves as a lightweight HTTP client. All Machine Learning inference (ASR, NMT Translation, TTS) occurs on the FastAPI backend via synchronous REST API calls (POST /asr, POST /translate, POST /tts). There are no local ML models embedded in the Android APK.

## 2. DbService audit
The ndroid/lib/services/db_service.dart utilizes sqflite to manage a table called content. This table tracks standard fields (	opic, language, data, dirty flag) and implements createContentOffline and saveServerRecords.
**Audit Finding:** DatabaseService is currently ONLY scaffolded for generic content (Worksheets/Flashcards). It is completely disconnected from the Voice Pipeline. Neither ClassroomScreen nor TranslatorScreen invoke the database. Classroom history is NOT persisted locally.

## 3. SyncService audit
The ndroid/lib/services/sync_service.dart attempts to upload "dirty" database records to the backend when ApiService.syncData() is called. 
**Audit Finding:** Like the database, it operates entirely outside the ML translation pipeline. It has no queue for failed API translation/ASR requests. It is triggered manually via a button on the HomeScreen ("Sync Data") rather than a background isolation service.

## 4. ApiService network dependency
ndroid/lib/services/api_service.dart acts as the direct network interface.
- 	ranscribeAudio(): **ONLINE-ONLY** (requires POST /asr). Fails gracefully if connection drops.
- 	ranslateText(): **ONLINE-ONLY** (requires POST /translate). Fails gracefully if connection drops.
- synthesizeSpeech(): **ONLINE-ONLY** (requires POST /tts). Fails gracefully if connection drops.
None of these methods utilize local caching, retry logic, or the DbService.

## 5. Classroom offline matrix
| Feature | Works Offline? | Evidence | Current Status |
|---------|----------------|----------|----------------|
| Microphone recording | YES | udio.wav is written to local getTemporaryDirectory() | IMPLEMENTED |
| Local audio file creation | YES | File exists locally prior to API upload | IMPLEMENTED |
| ASR | NO | Network http.MultipartRequest strictly required | ONLINE-ONLY |
| Translation | NO | Network http.post strictly required | ONLINE-ONLY |
| TTS | NO | Network http.post strictly required | ONLINE-ONLY |
| Audio playback | YES | Native udioplayers decodes memory bytes locally | IMPLEMENTED (Requires Online TTS bytes) |
| Classroom history | NO | UI state wiped on exit; DbService unused | NOT IMPLEMENTED |
| Local result storage | NO | Results held only in volatile RAM (setState) | NOT IMPLEMENTED |
| Sync | NO | SyncService does not handle ML data | NOT IMPLEMENTED |
| Retry | NO | User must manually restart recording | NOT IMPLEMENTED |
| Connectivity detection | PARTIAL | Implicit via HTTP timeouts and catch (e) traps | PARTIALLY IMPLEMENTED |

## 6. No-network behavior
If the user opens the Classroom and starts recording with no Wi-Fi/cellular connection:
1. The microphone records locally and generates udio.wav.
2. ApiService.transcribeAudio executes the HTTP POST.
3. The POST request immediately times out or refuses connection.
4. The Catch block returns 
ull.
5. The UI halts with "Error processing audio (Online required)".
No data is queued for later upload. The workflow cleanly aborts.

## 7. Online/offline transition behavior
If the network drops mid-workflow (e.g., ASR succeeds, but network fails before Translation), the system behaves identically to a standard failure. 	ranslateText times out, returning 
ull. The UI displays "Error: Translation failed." There is no background system monitoring for network restoration to automatically resume the task. The user must manually record again once online.

## 8. Offline-first gap analysis
The desired SIH architectural blueprint specifies an Offline-First approach.
**Existing Blocks:** Flutter Classroom, Backend API, Classroom UI.
**Missing/Disconnected Blocks:** Local ML inference execution, Classroom Sync Queue, Offline Results Cache, Local Classroom Storage.

## 9. Offline-first readiness assessment
**C. NOT READY**
While the local DbService and SyncService scaffolding exists, it is isolated from the core Voice/Translation operations. To achieve true Offline-First functionality, MatriVaani would need either local ONNX/TFLite models for embedded inference, or a robust persistent queue architecture that stores user voice notes and executes them in the background upon network restoration.

## 10. Data-loss analysis
Because _transcript and _translation exist only in the Stateful Widget's volatile RAM:
- Navigating away from ClassroomScreen permanently destroys the transcription.
- A failed translation destroys the transcription (the user must speak again).
- Closing the application permanently destroys the session.

## 11. Security/privacy findings
No sensitive API keys, auth tokens, or Bhashini credentials are hard-coded in the Flutter source code. The .env file solely contains the API_BASE_URL. The temporary udio.wav is continuously overwritten in the OS-level temporary cache, leaving no permanent unprotected raw audio footprint on the user's filesystem.

## 12. Changes made
None. The architecture was audited passively.

## 13. flutter analyze result
PASS

## 14. debug APK result
PASS

## 15. Backend regression checks
Verified. No modifications were made to sr_service.py, 	ranslation_service.py, 	ts_service.py. No Bhashini integration or IndicTrans2 integration was accidentally applied.

## 16. Runtime-validation limitation
Validation is based strictly on static code analysis. Physical offline testing was not possible due to the headless execution context.

## 17. Recommended next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**

---

FINAL DECISION:
**B. PARTIALLY READY — GAPS DOCUMENTED**
*(The DB/Sync scaffolding exists, but the core classroom pipeline is entirely ONLINE-ONLY).*

DB_SERVICE_AUDITED: YES
SYNC_SERVICE_AUDITED: YES
API_NETWORK_DEPENDENCIES_AUDITED: YES
CLASSROOM_OFFLINE_MATRIX_CREATED: YES
OFFLINE_FAILURE_PATH_DOCUMENTED: YES
ONLINE_OFFLINE_TRANSITION_DOCUMENTED: YES
DATA_LOSS_ANALYSIS_COMPLETED: YES
SECURITY_PRIVACY_AUDITED: YES

OFFLINE_ML_IMPLEMENTED: NO
LOCAL_ASR_IMPLEMENTED: NO
LOCAL_TRANSLATION_IMPLEMENTED: NO
LOCAL_TTS_IMPLEMENTED: NO
SYNC_QUEUE_IMPLEMENTED: NO

ASR_MODIFIED: NO
TRANSLATION_MODIFIED: NO
TTS_PROVIDER_CHANGED: NO
BHASHINI_CALLED: NO
INDICTRANS2_INTEGRATED: NO
FAKE_AUDIO: NO

FLUTTER_ANALYZE: PASS
DEBUG_APK: PASS
ANDROID_PHYSICAL_RUNTIME: NOT_VALIDATED
