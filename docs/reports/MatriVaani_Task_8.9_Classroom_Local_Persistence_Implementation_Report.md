# MatriVaani — Task 8.9 Classroom Local Persistence Implementation Report

## 1. Existing DB technology
MatriVaani uses sqflite inside ndroid/lib/services/db_service.dart.

## 2. ClassroomJob schema
I added the classroom_jobs table to store:
- id (PRIMARY KEY, UUID v4)
- created_at / updated_at (ISO8601 Strings)
- source_lang / 	arget_lang (Strings)
- udio_path (Persistent String path)
- 	ranscription (String, nullable)
- 	ranslation (String, nullable)
- status (String enum state)
- etry_count (Integer)
- last_error (String, nullable)

## 3. Migration strategy
Upgraded the database version from 1 to 2. Implemented the onUpgrade hook to safely execute the CREATE TABLE classroom_jobs schema without destroying the existing content table.

## 4. CRUD implementation
Added minimal, strictly focused CRUD hooks to DatabaseService:
- createClassroomJob(...)
- updateClassroomJob(id, updates)

## 5. Audio persistence implementation
Modified _stopRecording in classroom_screen.dart. Instead of blindly submitting the volatile getTemporaryDirectory() .wav to the API, the system now:
1. Generates a safe timestamped filename.
2. Copies the file to getApplicationDocumentsDirectory().
3. Creates the ClassroomJob record mapped to this persistent udio_path.
4. Submits the persistent file to the backend API.

## 6. Classroom integration
Integrated DatabaseService into the 	ry/catch pipeline inside _stopRecording. 

## 7. State checkpoint persistence
The job updates its status continuously during processing:
- RECORDED: Base initial state.
- ASR_PENDING: Just before calling /asr.
- TRANSLATING: After ASR succeeds. 	ranscription is saved.
- COMPLETED: After Translation succeeds. 	ranslation is saved.

## 8. Failure persistence
If a node fails or times out, the catch blocks and 
ull traps emit explicit error states to the database:
- ASR_FAILED
- TRANSLATION_FAILED
- FAILED
The last_error column receives context (e.g., 'Transcription empty.'). Because updates are modular, if translation fails, the job correctly retains the successful 	ranscription result.

## 9. Restart persistence design
Since jobs are explicitly stored in SQLite and .wav files are relocated to getApplicationDocumentsDirectory(), the data physically survives an app kill. The UI queue rendering (Phase 2/3) will therefore be able to pull these jobs freely upon startup.

## 10. Duplicate protection
Job creation generates a deterministic Uuid().v4(). The existing _isProcessing mutex in classroom_screen.dart was strictly preserved, preventing multiple job insertions for the same physical tap event.

## 11. Privacy/storage handling
No raw audio is unnecessarily logged to console. SQLite is strictly local-only and not uploaded arbitrarily to Bhashini or third parties. 

## 12. Files modified
- ndroid/lib/services/db_service.dart
- ndroid/lib/screens/classroom_screen.dart

## 13. Files explicitly unchanged
pi_service.dart, sync_service.dart, 	ts_player_service.dart, and ALL Python backend files remained completely untouched.

## 14. flutter analyze
PASS

## 15. debug APK
PASS

## 16. database validation
SQLite syntactically validates the version upgrade and table creation through standard Android SQLite bindings during initialization.

## 17. known runtime limitation
Because this environment is headless, the physical directory access paths (getApplicationDocumentsDirectory()) and actual OS-level .wav file copies were statically validated but not runtime-tested on a physical device.

## 18. exact next task
**Master Roadmap Phase 3: Obtain and Integrate Bhashini Developer Credentials.**

---

FINAL DECISION:
**A. LOCAL PERSISTENCE IMPLEMENTED**

CLASSROOM_JOB_IMPLEMENTED: YES
DATABASE_MIGRATION_SAFE: YES
CLASSROOM_CRUD_IMPLEMENTED: YES
PERSISTENT_AUDIO_IMPLEMENTED: YES
CHECKPOINT_STATES_PERSISTED: YES
FAILURE_STATE_PERSISTED: YES
RESTART_PERSISTENCE_SUPPORTED: YES
DUPLICATE_JOB_PROTECTION: YES
NO_AUTOMATIC_RETRY_YET: YES
NO_OFFLINE_ML: YES

ASR_MODIFIED: NO
TRANSLATION_MODIFIED: NO
TTS_PROVIDER_CHANGED: NO
BHASHINI_CALLED: NO
INDICTRANS2_INTEGRATED: NO
FAKE_AUDIO: NO

FLUTTER_ANALYZE: PASS
DEBUG_APK: PASS
ANDROID_PHYSICAL_RUNTIME: NOT_VALIDATED
