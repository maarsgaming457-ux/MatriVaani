# MatriVaani

MatriVaani is a Mother Tongue Based Primary Education Tool designed for Android, backed by an offline-capable FastAPI backend with state-of-the-art Neural Machine Translation (NMT) and Automatic Speech Recognition (ASR) for Indian tribal languages.

## Problem
Vernacular primary education suffers from a severe lack of digital resources in tribal languages like Santali and Mundari. Teachers and students struggle with language barriers in foundational learning. MatriVaani bridges this gap by offering a fully functional translation and voice-interaction layer directly on Android.

## Features
- **Mundari NMT:** High-accuracy offline translation model fine-tuned for Hindi ↔ Mundari.
- **Santali ASR:** Offline speech recognition for Santali built on a fine-tuned wav2vec2 architecture.
- **FastAPI Backend:** Lightweight API handling offline inference, TTS wrapping, and routing.
- **Flutter Android Application:** Native cross-platform user interface optimized for classroom environments.

## Architecture
```
Flutter Android App
        ↓
FastAPI Backend
        ↓
Translation / ASR / TTS Services
        ↓
Production Models / External APIs
```

## Repository Structure
```
MatriVaani/
├── android/                   # Flutter dependencies and build configurations
├── app/                       # FastAPI application core, routers, and services
├── asr_engine/                # Scripts and APIs to run the Santali ASR pipeline
├── backend/                   # Translation inference and API routes
│   └── best_model_main2/      # LFS-tracked Mundari NMT production model weights
├── models/
│   └── santhali_asr_final_5k/ # LFS-tracked Santali ASR production model weights
├── .env.example               # Environment variable templates
├── .gitignore                 # Strict rules to prevent committing secrets & huge files
├── requirements.txt           # Python backend dependencies
└── README.md                  # This file
```

## Models
### Mundari NMT
- **Purpose:** Translates text between Hindi and Mundari.
- **Model Format:** `.safetensors` (IndicTrans2 architecture).
- **Runtime Location:** `backend/best_model_main2/`
- **Git LFS:** Tracks `model.safetensors` (~1.2 GB).
- **License:** MIT (Fine-tuned from IndicTrans2).

### Santali ASR
- **Purpose:** Transcribes spoken Santali into text (Ol Chiki script).
- **Model Format:** `.safetensors` (Wav2Vec2 / MMS).
- **Runtime Location:** `models/santhali_asr_final_5k/`
- **Git LFS:** Tracks `model.safetensors` (~1.2 GB).
- **License:** Apache 2.0 / CC-BY-NC 4.0 (depending on the base model used).

## Requirements
- **Python:** 3.10+
- **Flutter SDK:** >=2.17.0 <4.0.0
- **Android Studio / SDK:** Required to build the Android application.
- **Git LFS:** Required to download production models.
- **External APIs (Optional fallback):** Sarvam API, Groq API, Bhashini API.

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/maarsgaming457-ux/MatriVaani.git
cd MatriVaani

# 2. Initialize and pull large model files
git lfs install
git lfs pull

# 3. Create a Python virtual environment
python -m venv venv

# Windows activation
venv\Scripts\activate
# Linux/Mac activation
source venv/bin/activate

# 4. Install backend dependencies
pip install -r requirements.txt
```

## Environment Variables
MatriVaani requires environment variables to connect to external fallback services (if used). 
Copy the example environment file:
```bash
cp .env.example .env
```
Fill in the credentials locally. **Never commit `.env` to Git.**

## Backend Setup
Start the local FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Android Setup
1. Ensure the Flutter CLI is installed.
2. Navigate to the `android/` directory (or project root if configured as such) and fetch dependencies:
   ```bash
   flutter pub get
   ```
3. Create a local `.env` file in the Flutter assets directory mapping `API_BASE_URL` to your backend.
   - For an Android Emulator testing the local backend, use: `http://10.0.2.2:8000`
4. Run the application:
   ```bash
   flutter run
   ```

## API Endpoints
- `GET /health` : Returns API health status.
- `POST /translate` : Accepts source text, source lang, target lang. Returns translated text.
- `POST /asr` : Accepts audio binary. Returns transcribed text.
- `POST /tts` : Accepts text and language. Returns synthesized audio binary.

## Deployment
### Backend Deployment
The FastAPI backend can be deployed online using Docker, Render, or Google Cloud Run.
**Important Limitation:** The production models (NMT + ASR) combined consume over 3GB of RAM and ~2.5GB of disk space. Free-tier deployment services will likely crash out of memory. A VPS with at least 8GB of RAM or a dedicated Hugging Face Inference Endpoint is recommended if hosting models locally.

If a deployment server lacks storage, configure the application to call external APIs (Sarvam/Groq) by passing those API keys as Environment Secrets in the deployment dashboard.

## Git LFS
Because GitHub restricts files over 100MB, the `model.safetensors` files for both models are tracked using Git Large File Storage (LFS). 
You must run `git lfs pull` after cloning to retrieve the actual weights, otherwise you will only download 1KB text pointer files.

## Troubleshooting
- **ModuleNotFoundError:** Ensure your virtual environment is activated and `requirements.txt` is installed.
- **Model weights missing / corrupted:** Run `git lfs pull`. Ensure Git LFS is installed globally.
- **Android Emulator Network Error:** Ensure the app points to `10.0.2.2:8000` instead of `localhost:8000`.

## License / Attribution
- Code licensed under MIT.
- Models inherit base model licenses (IndicTrans2 -> MIT, Wav2Vec2/MMS -> Apache 2.0 / CC-BY-NC 4.0).
