<div align="center">
  <img src="https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white" alt="Flutter">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android">
</div>

# MatriVaani 

MatriVaani is a **Mother Tongue Based Primary Education Tool** designed natively for Android. It bridges the digital divide in vernacular primary education by offering a fully functional translation, Text-To-Speech (TTS), and Automatic Speech Recognition (ASR) layer for Indian tribal languages like **Santali** and **Mundari**.

Our core mission is to enable seamless dual-mode execution, ensuring that students and teachers can interact with the app utilizing **Cloud APIs** when an internet connection is present, or fallback securely to **Genuine On-Device Inference** in zero-connectivity environments.

---

## 🎯 Project Purpose

Vernacular primary education suffers from a severe lack of digital resources in tribal languages. Teachers and students struggle with language barriers in foundational learning. 

MatriVaani bridges this gap by offering a fully functional translation and voice-interaction layer directly on Android, allowing:
- **Teachers** to translate state-curriculum material from Hindi/English to local tribal languages.
- **Students** to interact via voice natively in their mother tongue.
- **Remote Schools** to operate offline without requiring expensive internet infrastructure.

---

## ✨ Features Actually Implemented

| Feature | Description | Status |
| :--- | :--- | :---: |
| **Mundari NMT** | High-accuracy translation model fine-tuned for Hindi ↔ Mundari based on IndicTrans2. | ✅ Active |
| **Santali ASR** | Speech recognition for Santali built on a fine-tuned wav2vec2 architecture (Ol Chiki output). | ✅ Active |
| **Dual-Mode Flutter UI** | Native cross-platform user interface optimized for classroom environments. | ✅ Active |
| **Cloud FastAPI Backend** | Lightweight API handling online inference, TTS wrapping, and HTTP routing. | ✅ Active |
| **On-Device True Offline Mode** | Full on-device model execution without a PC dependency. | 🚧 In Progress |

---

## 🏗️ Architecture (Dual-Mode)

MatriVaani dynamically shifts between **Online Mode** and **Offline Mode** to provide the best user experience. 
*(Note: PC-hosted FastAPI connecting to Android over Local Wi-Fi is considered an intermediate Developer Mode, not true offline).*

```text
                         MATRI VAANI
                              │
                    ┌─────────┴─────────┐
                    │                   │
               ONLINE MODE         OFFLINE MODE
                    │                   │
             Internet available     No Internet
                    │                   │
             Cloud FastAPI API       Android device
                    │                   │
          ┌─────────┼─────────┐      Local models
          │         │         │         │
       Translation  ASR      TTS       ASR/NMT/TTS
          │         │         │         │
          └─────────┴─────────┘         │
                    │                   │
                 Response          Response
                    │                   │
                    └─────────┬─────────┘
                              │
                       Flutter UI
```

---

## 📂 Repository Structure

```text
MatriVaani/
├── android/                   # Flutter dependencies and build configurations
├── app/                       # FastAPI application core, routers, and services
├── asr_engine/                # Scripts and APIs to run the Santali ASR pipeline
├── backend/                   # Translation inference and API routes
│   └── best_model_main2/      # LFS-tracked Mundari NMT production model weights
├── models/
│   └── santhali_asr_final_5k/ # LFS-tracked Santali ASR production model weights
├── docs/                      # Extensive project architecture and deployment guides
├── .env.example               # Environment variable templates
├── .gitignore                 # Strict rules to prevent committing secrets & huge files
├── requirements.txt           # Python backend dependencies
└── README.md                  # Master documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python:** 3.10+ (C++ Build Tools required on Windows for `IndicTransToolkit`)
- **Flutter SDK:** >=2.17.0 <4.0.0
- **Git LFS:** Required to download production models natively.

### 1. Clone & Pull Models
Because GitHub restricts files over 100MB, the `model.safetensors` files for our models are tracked using **Git Large File Storage (LFS)**. You must run `git lfs pull` after cloning.

```bash
git clone https://github.com/maarsgaming457-ux/MatriVaani.git
cd MatriVaani

git lfs install
git lfs pull
```

### 2. Backend Setup & `.env`
MatriVaani uses environment variables to connect to external fallback services safely. **Never commit `.env` to Git.**

```bash
# Copy template securely
cp .env.example .env

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Flutter Setup
1. Ensure the Flutter CLI is installed.
2. Navigate to the project root (where `pubspec.yaml` is located) and fetch dependencies:
   ```bash
   flutter pub get
   ```
3. Run the application:
   ```bash
   flutter run
   ```
*(For Android Emulator testing, point your Flutter backend URL to `http://10.0.2.2:8000`)*

---

## 🌐 Online Deployment

The FastAPI backend can be deployed online via VPS or managed services (Docker, Google Cloud Run). 
**⚠️ Important limitation:** The production local models (NMT + ASR) consume over **3.5 GB of RAM** combined when loaded into PyTorch. Free-tier deployment services will encounter Out Of Memory (OOM) errors. A VPS with at least **8GB of RAM** is required for hosting models locally on the cloud.

See [ONLINE_DEPLOYMENT.md](docs/ONLINE_DEPLOYMENT.md) for full hosting instructions.

---

## 📱 Offline Requirements

The project is moving towards genuine on-device execution (LiteRT/TFLite/ONNX/ExecuTorch). 
True offline mode strictly means:
- No internet.
- No cloud API.
- No PC-hosted FastAPI server.

We are currently tracking mobile inference feasibility. See [OFFLINE_CAPABILITY_MATRIX.md](docs/OFFLINE_CAPABILITY_MATRIX.md) and [MODEL_RUNTIME.md](docs/MODEL_RUNTIME.md) for implementation roadmaps.

---

## 🛠️ Troubleshooting

- **ModuleNotFoundError for IndicTransToolkit (Windows):** Ensure you have installed Microsoft C++ Build Tools before running `pip install`.
- **Model weights missing or 1KB in size:** You forgot to run `git lfs pull`. Ensure Git LFS is installed globally.
- **Android Emulator Network Error:** Ensure the app points to `10.0.2.2:8000` instead of `localhost:8000`.

---

## 📄 License & Attribution

- Application Code is licensed under **MIT**.
- Models inherit base model licenses:
  - **IndicTrans2** → MIT
  - **Wav2Vec2/MMS** → Apache 2.0 / CC-BY-NC 4.0 (varies by base).
