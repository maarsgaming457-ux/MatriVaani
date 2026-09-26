# MATRIVAANI OFFLINE CONVERSION INSPECTION REPORT

## 1. CURRENT ARCHITECTURE: TRANSLATION
- **A. Hindi → Mundari**
  - **File:** `app/services/mundari_translation_service.py`
  - **Class/Method:** `MundariTranslationService.translate()`
  - **Endpoint:** `/translate/hindi-to-mundari`
  - **Model:** IndicTrans2 (Fine-tuned)
  - **Environment:** Local PC (PyTorch)
  - **Paths:** `backend/best_model_main2` (Model & Tokenizer)
  - **Packages:** `torch`, `transformers`
  - **Internet:** NO
  - **Lang Codes:** `hin_Deva` → `unr_Deva`
- **B. Mundari → Hindi**
  - Not currently implemented in the API routing logic.
- **C. Hindi → Santali**
  - **File:** `app/services/translation_service.py`
  - **Method:** `_sarvam_translate()` 
  - **Endpoint:** `/translate`
  - **Model:** Sarvam API
  - **Environment:** Cloud
  - **Internet:** YES
  - **Lang Codes:** `hi-IN` → `sat-IN`
- **D. Santali → Hindi**
  - **File:** `app/services/translation_service.py`
  - **Method:** `_sarvam_translate()` 
  - **Endpoint:** `/translate`
  - **Model:** Sarvam API
  - **Environment:** Cloud
  - **Internet:** YES
  - **Lang Codes:** `sat-IN` → `hi-IN`
- **E. Hindi → Hindi**
  - **File:** `android/lib/screens/translator_screen.dart`
  - **Method:** `_translate()` UI bypass logic
  - **Endpoint:** Bypassed
  - **Environment:** Local Android Client
  - **Internet:** NO

## 2. CURRENT ARCHITECTURE: ASR
- **A. Santali ASR**
  - **Model:** Wav2Vec2 CTC
  - **Path:** `./models/santhali_asr_final_5k` (~377 MB)
  - **Python Service:** `app/services/asr_service.py`
  - **Flutter Service:** `ApiService.transcribeAudio()`
  - **Endpoint:** `/asr`
  - **Inference:** Local PC (PyTorch)
  - **Android Mic:** Uses `record` package to capture `.wav` and send via multipart HTTP POST. It does **not** use the native Android `SpeechRecognizer`.
  - **Internet:** NO
- **B. Hindi ASR**
  - Currently unsupported by local backend. Triggers `ASRError` in `asr_service.py`.

## 3. CURRENT ARCHITECTURE: TTS
- **Files:** `app/api/main.py` (`/tts`), `tts_service.py`, `santali_tts_preprocessor.py`
- **Flow:** Both Santali and Mundari force the language code to `"hi"` and hit the **Sarvam Bulbul:v3** model using the `ritu` speaker. Santali undergoes phonetic Ol-Chiki-to-Devanagari mapping first.
- **Playback:** Flutter `audioplayers` package playing the returned `audio/wav` bytes.
- **Internet:** **YES (Strictly Required).** No local TTS fallback is functional.

## 4. CURRENT ANDROID ↔ FASTAPI ARCHITECTURE
- **Network Dependency:** Flutter strictly relies on `http://10.0.2.2:8000` (Android Emulator loopback) to communicate with the Windows FastAPI server.
- **To make standalone:** The HTTP layer (`api_service.dart`) must be completely replaced. Flutter must invoke C++/JNI bindings (via `tflite_flutter` or `onnxruntime`) to execute models directly on the Android device's CPU/NPU, bypassing networking entirely.

## 5. CURRICULUM / EDUCATION FEATURES
- **Services:** `llm_service.py` leverages Groq API (`openai/gpt-oss-120b`).
- **Features:** Script Generation, Copy Editing, Lesson Generation, Flashcards, Worksheets.
- **Internet:** **YES (Strictly Required).** All dynamic educational generation requires `api.groq.com`.

## 6. COMPLETE ONLINE DEPENDENCY MAP
| Feature | File | API/Service | Online/Local | Can work offline? | Replacement needed? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Santali NMT | `translation_service.py` | `api.sarvam.ai` | Online | No | Yes (Convert/Train Local Model) |
| Santali/Mundari TTS | `tts_service.py` | `api.sarvam.ai` | Online | No | Yes (VITS/FastSpeech2 Local Model) |
| Educational Content | `llm_service.py` | `api.groq.com` | Online | No | Yes (Pre-generate DB or SLM) |
| DNS Override | `sitecustomize.py` | `4.247.234.152` | Online | No | N/A (Obsolete Offline) |

## 7. COMPLETE LOCAL MODEL MAP
- **Mundari NMT (`backend/best_model_main2`)**
  - **Type:** IndicTrans2 (Transformers)
  - **Size:** ~1.3 GB
  - **Compute:** CPU (AMD Ryzen 7). Consumes 2-4 GB RAM during inference.
  - **Android Feasibility:** **NO.** Too large for a 2GB RAM tablet. Must be quantized (Int8) and exported to ONNX/TFLite.
- **Santali ASR (`models/santhali_asr_final_5k`)**
  - **Type:** Wav2Vec2 CTC
  - **Size:** ~377 MB
  - **Compute:** CPU (PyTorch).
  - **Android Feasibility:** Plausible if converted to TFLite, though still heavy for 2GB RAM.

## 8. PYTHON ENVIRONMENT
- **Python:** 3.14.2
- **Key Packages:** `torch==2.13.0`, `transformers==5.15.1`, `fastapi==0.141.1`.
- **Missing for Conversion:** `onnx`, `onnxruntime`, `optimum` are NOT installed, meaning no export pipeline currently exists.

## 9. HARDWARE
- **Development PC:** AMD Ryzen 7 5800H with Radeon Graphics, ~24 GB RAM. No discrete NVIDIA GPU.

## 10. WHAT MUST CHANGE FOR TRUE OFFLINE OPERATION
1. **Model Conversion:** PyTorch `.safetensors` must be exported to `.tflite` or `.onnx` with INT8 quantization to fit within Android RAM constraints.
2. **Flutter ML Integration:** Re-write `api_service.dart` to load `.tflite` assets using `tflite_flutter` instead of making HTTP requests.
3. **Audio Pre-processing:** Dart must implement Mel-Spectrogram feature extraction locally to feed raw mic data into the ASR models.
4. **Content Generation:** LLM-generated flashcards/worksheets must be pre-generated on Windows, saved to SQLite, and bundled into the APK as an offline static database.

## 11. RISKS
1. **Memory Exhaustion (OOM):** A 1.3 GB IndicTrans2 model will instantly crash a 2GB RAM Android tablet. Heavy distillation and quantization are mandatory.
2. **Dart Audio Processing:** Extracting 16kHz Wav2Vec2 features in Dart is mathematically complex and slow compared to Python `librosa`/`transformers`.
3. **No Offline TTS:** There is currently no local TTS model (e.g., Piper, VITS) trained for Mundari/Santali phonetic output.

## 12. 3-DAY PRIORITY PLAN
- **Day 1: Storage & Content.** Pre-generate all required curriculum (Flashcards, Worksheets) via Groq, freeze the SQLite database, and bundle it directly into the Flutter assets.
- **Day 2: ASR Conversion.** Export `santhali_asr_final_5k` to TFLite. Integrate `tflite_flutter` into the app and port the audio pre-processing logic to Dart.
- **Day 3: NMT Quantization.** Attempt to INT8 quantize `best_model_main2` to ONNX. If it remains too large (>500MB), fallback to a lightweight dictionary-based translation system for offline emergency use.

## 13. EXACT FIRST IMPLEMENTATION TASK
**Task:** *Pre-generate and Bundle the SQLite Database.*
Before touching complex ML models, eliminate the `llm_service.py` cloud dependency by using a script to generate hundreds of flashcards and worksheets via Groq, save them to the `local_offline_data.db`, and package this DB inside the Flutter `assets/` directory for pure offline reading.
