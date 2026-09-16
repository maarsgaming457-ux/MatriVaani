# MatriVaani — Task 8.8 Classroom Local Persistence & Queue Design Report

## 1. Existing DB architecture
DatabaseService (ndroid/lib/services/db_service.dart) utilizes sqflite with a single content table (id, content_type, 	opic, language, data, created_at, updated_at, deleted, dirty). It uses standard CRUD operations but currently lacks any tables, schema, or queries to store Classroom/Voice interactions. There are no schema migration frameworks (like sqflite_common_ffi or similar onUpgrade handlers) configured.

## 2. Existing Sync architecture
SyncService (ndroid/lib/services/sync_service.dart) is explicitly built to pull dirty = 1 rows from the content table and POST them via ApiService.syncData. It lacks a retry queue for voice jobs, has no background connectivity listener (it executes manually via HomeScreen), and does not support sequenced state machine recovery (e.g. ASR -> Translate -> TTS).

## 3. Current classroom data lifecycle
The entire Voice/Translation lifecycle lives in volatile RAM via _ClassroomScreenState variables (_sourceLang, _targetLang, _transcript, _translation, _status). The .wav file is saved to the OS getTemporaryDirectory(). If the backend drops, the RAM state hits 
ull and resets. If the user closes the app, all progress and audio are permanently wiped.

## 4. Proposed ClassroomJob model
To make the classroom resilient to network loss, we need a local entity.
**Schema: ClassroomJob**
- id (String UUID): Primary key.
- created_at (ISO8601): Sorting/UI presentation.
- source_lang / 	arget_lang (String): Routing.
- udio_path (String): Crucial to retain the recording for later ASR upload. Needs to be copied from getTemporaryDirectory() to getApplicationDocumentsDirectory().
- 	ranscription (String, nullable): State checkpoint.
- 	ranslation (String, nullable): State checkpoint.
- status (String): Tracks the current execution node.
- last_error (String, nullable): User-visible context.
- updated_at (ISO8601): For sync conflict resolution.

## 5. Persistent state machine
Valid transitions for the queue:
- RECORDED: Audio saved locally. Ready for ASR.
- ASR_PENDING: In flight to backend.
- ASR_FAILED: Network dropped. Reverts to RECORDED for retry.
- TRANSLATING: Transcription saved locally. Ready for NMT.
- TRANSLATION_FAILED: Reverts to TRANSLATING for retry.
- COMPLETED: NMT completed. TTS_PENDING is unnecessary because TTS 503 is expected and TTS bytes do not need database persistence.
- *Invalid Transitions:* ASR_FAILED -> TRANSLATING (Cannot translate silence).

## 6. Offline queue semantics
- **CASE A (Online Success):** Job progresses linearly to COMPLETED and remains locally cached for Classroom History.
- **CASE B (Backend Offline):** Job hangs at RECORDED. Sync service picks it up later.
- **CASE C (Network fails mid-stream):** ASR completes, saves 	ranscription, job is marked TRANSLATING. Sync service later resumes from Translation step, skipping ASR.
- **CASE E/F (App Restart):** UI queries sqflite on initState(), displaying pending jobs and automatically pushing them to the queue.

## 7. Audio lifecycle
Audio files currently written to getTemporaryDirectory() are subject to arbitrary deletion by Android. For queued jobs, the .wav MUST be moved to getApplicationDocumentsDirectory(). The file can be safely purged when the job hits COMPLETED (if storage is a concern) or retained for the user's local "History" tab.

## 8. Retry policy
- **HTTP 500/503 (Translation/ASR):** Keep job in queue. Rely on manual sync button or application restart for now to prevent battery drain.
- **Empty File/0 Bytes:** Mark as FAILED_PERMANENTLY. Do not retry.
- **TTS 503:** Do not queue. Mark job COMPLETED (Translation finished successfully).

## 9. Connectivity model
Currently, ApiService.isOnline() performs a standard GET /health timeout check. There is no continuous network listener (like connectivity_plus). To achieve automatic background resumption, a network stream listener package would be needed. Otherwise, offline sync remains manual via the "Sync Data" button.

## 10. App restart/crash behavior
With local sqflite persistence, if the app is killed during ASR_PENDING, the database still holds the job as RECORDED (since the transaction only updates to TRANSLATING upon successful HTTP return). On reboot, the UI renders the pending block, and the user can manually tap it to resume.

## 11. Duplicate-job protection
A SyncQueueManager singleton is required. Before taking a job from sqflite, it sets a volatile in_flight_ids = Set<String>(). If a job ID is locked in the set, the sync engine skips it. This prevents the user and the background sync from double-posting the same audio file.

## 12. Storage/privacy analysis
Persisting .wav files and translated text locally poses a privacy footprint. ClassroomJob tables should be clearly visible to the user via a "History" interface so they can explicitly delete items. Plaintext storage is acceptable for this prototype, as the data is standard classroom dictation.

## 13. SIH architecture comparison
- **Existing:** Flutter Classroom -> Online API -> ASR/NMT.
- **Missing:** Local Classroom Storage table, Offline Pending Queue, Local History UI, Sync/Retry loop for ML requests.

## 14. Phased implementation plan
**Phase 1:** Update db_service.dart schema with classroom_jobs table.
**Phase 2:** Update classroom_screen.dart to copy udio.wav to persistent storage and INSERT a RECORDED job.
**Phase 3:** Break _stopRecording into sequenced DB updates (UPDATE transcription -> UPDATE translation).
**Phase 4:** Build ClassroomHistoryUI to list pending/completed jobs from sqflite.
**Phase 5:** Extend SyncService to parse pending jobs and resume them.

## 15. Risks
- Managing orphaned .wav files when users uninstall or force-quit.
- SQLite database migrations breaking existing content tables.

## 16. Files expected to change
ndroid/lib/services/db_service.dart, ndroid/lib/screens/classroom_screen.dart, ndroid/lib/services/sync_service.dart.

## 17. Code changes actually made
ZERO code modifications made.

## 18. flutter analyze
PASS

## 19. debug APK
PASS

## 20. runtime limitation
Validation is strictly based on static/code-level architecture design.

## 21. exact next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**

---

FINAL DECISION:
**A. LOCAL PERSISTENCE DESIGN READY**

DB_ARCHITECTURE_AUDITED: YES
SYNC_ARCHITECTURE_AUDITED: YES
CLASSROOM_DATA_LIFECYCLE_AUDITED: YES
CLASSROOM_JOB_MODEL_DESIGNED: YES
PERSISTENT_STATE_MACHINE_DESIGNED: YES
OFFLINE_QUEUE_SEMANTICS_DESIGNED: YES
RETRY_POLICY_DESIGNED: YES
AUDIO_LIFECYCLE_DESIGNED: YES
APP_RESTART_BEHAVIOR_DESIGNED: YES
DUPLICATE_JOB_PROTECTION_DESIGNED: YES
STORAGE_PRIVACY_AUDITED: YES
PHASED_IMPLEMENTATION_PLAN_CREATED: YES
PRODUCTION_CODE_MODIFIED: NO

ASR_MODIFIED: NO
TRANSLATION_MODIFIED: NO
TTS_PROVIDER_CHANGED: NO
BHASHINI_CALLED: NO
INDICTRANS2_INTEGRATED: NO
FAKE_AUDIO: NO

FLUTTER_ANALYZE: PASS
DEBUG_APK: PASS
ANDROID_PHYSICAL_RUNTIME: NOT_VALIDATED
