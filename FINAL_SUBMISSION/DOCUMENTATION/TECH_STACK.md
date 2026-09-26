# TECHNOLOGY STACK

**Frontend:**
- Flutter / Dart

**Backend:**
- FastAPI / Python

**ASR (Automatic Speech Recognition):**
- Local Ho ASR (Fine-tuned Wav2Vec2-based model)
- Pre-existing paths for Hindi and Santali ASR

**Translation:**
- IndicTrans2 (Deployed via WSL2/Local Network for Hindi <-> Santali)

**Cloud/Online Services:**
- Sarvam (TTS integration for Hindi)
- Bhashini (Configurable pathways present)

**Database:**
- SQLite (Used for offline queue/caching mechanism and annotation tools)

**Offline Capabilities:**
- Local Ho ASR
- Offline Classroom Job caching and queuing behavior
