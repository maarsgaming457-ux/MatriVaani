# MatriVaani

## 1. Project Overview
MatriVaani is a Smart India Hackathon (SIH26042) project focused on AI-Powered Vernacular Pedagogy. It enables Hindi-medium/non-native teachers to deliver primary education in tribal languages, specifically starting with Santali. 
The project features an end-to-end classroom workflow integrating Automatic Speech Recognition (ASR), Hindi ↔ Santali Neural Machine Translation (NMT), and an offline-capable Android Flutter application designed for low-resource environments.

## 2. Current Architecture
The current architecture routes voice input from the Android app to a local Windows FastAPI server, which performs ASR and delegates translation to a GPU-accelerated IndicTrans2 endpoint.

Android Flutter -> Windows FastAPI -> ASR / Translation services -> IndicTrans2 external API -> IndicTrans2 320M GPU inference

*Note: The IndicTrans2 external API is currently an online dependency hosted temporarily via Google Colab and ngrok.*

## 3. Project Structure
- pp/ - Core Windows backend application
- pp/api/ - FastAPI routing and endpoints
- pp/services/ - Integration services for ASR, LLMs, and Translation
- pp/prompts/ - System prompts for AI processing
- datasets/ - Directory for offline datasets and caching
- models/ - Directory for offline model weights (e.g., ASR)
- ndroid/ - The MatriVaani Flutter application
- ndroid/lib/ - Flutter source code
- ndroid/lib/screens/ - UI screens (Home, Classroom, Translator)
- ndroid/lib/services/ - Android API, DB, and TTS services

## 4. Backend Setup
1. Open a terminal in the project root: C:\study files\sih project
2. Activate your Python virtual environment.
3. Start the FastAPI backend:
   `ash
   python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000
   `
4. Verify the backend health endpoint: http://127.0.0.1:8000/health

## 5. Environment Configuration
The .env file is LOCAL ONLY and must never be committed to Git. Create a .env in the root directory based on .env.example.
Key configuration required:
- API_BASE_URL=http://10.0.2.2:8000 (In ndroid/.env)
- TRANSLATION_PROVIDER=indictrans2
- INDICTRANS2_API_URL=<IndicTrans2 server URL>
- TTS_PROVIDER=none

*Note: Bhashini TTS credentials remain unconfigured because Bhashini integration is currently ON HOLD.*

## 6. IndicTrans2 Setup
The translation provider uses i4bharat/indictrans2-indic-indic-dist-320M.
The current validated inference environment is:
- Google Colab
- Tesla T4 GPU
- CUDA, float16

The current demonstration uses an external IndicTrans2 API (Colab + ngrok arrangement), which is temporary. It is NOT a production deployment. The API endpoint must be configured via the INDICTRANS2_API_URL environment variable.

## 7. Hugging Face Authentication
The Hugging Face token is stored securely via a local/Colab Secret mechanism. Credentials must NEVER be committed to Git. Do not hardcode your token or authorization headers into the source code.

## 8. Android / Flutter Setup
To run the Android app:
`ash
cd android
flutter pub get
flutter devices
flutter run -d emulator-5554
`
*Note on emulator networking:* The URL 10.0.2.2 is a special alias to your host loopback interface, meaning the Android emulator will reach the Windows host's localhost.

## 9. Emulator Microphone
If testing via the Android Emulator, you MUST enable host microphone input:
1. Open Emulator settings (Extended Controls)
2. Go to **Microphone**
3. Enable **Virtual microphone uses host audio input**
Without this, the emulator will only record digital silence. This is not required for physical Android devices.

## 10. Translation
Supported and validated translation directions:
- Hindi → Santali
- Santali → Hindi
The translation has been validated, but perfect translation accuracy is not claimed due to the low-resource nature of the languages.

## 11. Classroom Workflow
The classroom workflow follows this pipeline:
Microphone -> WAV -> ASR -> 	ranscription -> 	ranslation -> TTS attempt

*TTS State:* Real TTS audio is currently unavailable (TTS_PROVIDER=none).
*Silence Handling:* If no speech is recorded, the ASR returns [SILENCE DETECTED]. This is converted into "No speech detected. Please try again." and downstream translation/TTS is safely skipped.

## 12. Offline / Online Architecture
- **Inference is currently online** (FastAPI backend + remote Colab GPU).
- **Local persistence exists** for classroom jobs (SQLite).
- **Retry/resume exists** for failed translations or connectivity drops.
- **Connectivity queue exists** to manage offline requests.
- Local storage protects classroom jobs from being lost.
- Local Android IndicTrans2 inference is NOT implemented due to hardware constraints.

## 13. TTS / Bhashini Status
TTS is currently disabled/configured as TTS_PROVIDER=none. Bhashini TTS integration is planned for the future but is currently ON HOLD because service credentials and access are not yet configured.

## 14. Models and Large Files
Large ML models and datasets are local assets and are intentionally excluded from GitHub via .gitignore. Do not commit model files (like .safetensors, .bin, .pt) to the repository. Place downloaded ASR models inside the local models/ directory.

## 15. GitHub Safety
- .env must not be committed.
- Secrets and API keys must not be committed.
- Large model files and datasets must not be committed.
- Build outputs (__pycache__, Flutter uild/, APKs) should not be committed.

## 16. Current Limitations
- IndicTrans2 currently depends on an external API.
- The current demo API relies on temporary Colab + ngrok infrastructure.
- TTS is unavailable.
- Bhashini integration is on hold.
- Fully offline ML inference is not implemented.
- Production-scale deployment is not yet established.

## 17. Demo Startup Order
1. Start/verify the IndicTrans2 inference server (e.g., run the Colab notebook).
2. Verify its /health endpoint in a browser.
3. Start Windows FastAPI (uvicorn app.api.main:app).
4. Verify Windows /health endpoint.
5. Verify Windows translation endpoint (manual test).
6. Start Flutter emulator (lutter run).
7. Verify Android microphone host input is enabled (if using emulator).
8. Launch the MatriVaani app and begin the demo.
