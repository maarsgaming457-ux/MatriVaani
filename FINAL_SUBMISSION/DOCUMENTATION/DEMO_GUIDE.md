# DEMO GUIDE

## PRE-DEMO STARTUP

**Terminal 1 (WSL2 IndicTrans2 Server):**
cd /path/to/indictrans2
python indictrans2_server.py

**Terminal 2 (Windows FastAPI Backend):**
.\venv\Scripts\python -m uvicorn app.api.main:app --port 8000

**Terminal 3 (Android/Flutter):**
cd android
flutter run

---

## DEMO 1 — HINDI -> SANTALI

1. Launch MatriVaani App on Android.
2. Open TranslatorScreen.
3. Select Source: Hindi
4. Select Target: Santali
5. Enter/speak: "नमस्ते बच्चों, आज हम गिनती सीखेंगे।"
6. Tap 'Translate'.
7. Observe the real Santali output generated via IndicTrans2.
8. Tap 'Play Audio' to hear the TTS playback (if available via configuration).

---

## DEMO 2 — HO SPEECH -> HO TRANSCRIPT

1. Open TranslatorScreen or ClassroomScreen.
2. Select Source: Ho.
3. Record Ho speech natively on device (or route backend test audio via emulator).
4. Tap 'Translate' / process ASR.
5. Observe the UI display the "Ho Transcript" accurately.
6. Explain: "MatriVaani performs local Ho speech recognition. Ho translation is not currently available in the prototype."

---

## DEMO 3 — SANTALI -> HINDI

1. Open TranslatorScreen.
2. Select Source: Santali.
3. Select Target: Hindi.
4. Provide a validated Santali sentence from the current testing dataset.
5. Tap 'Translate'.
6. Observe the generated Hindi result.
7. Tap 'Play Audio' for Hindi TTS synthesis via Sarvam.
