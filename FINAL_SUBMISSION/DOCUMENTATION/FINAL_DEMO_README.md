# MatriVaani

MatriVaani is a vernacular classroom and translation platform. This prototype supports speech-to-text, translation, and text-to-speech for regional languages to aid educational efforts.

## Supported Languages
- **Hindi** (Full support: ASR, Translation, TTS)
- **Santali** (Full support: ASR, Translation, TTS)
- **Ho** (Partial support: ASR only)

## Supported Translation Directions
- Hindi -> Santali
- Santali -> Hindi

## Ho ASR Capability
The prototype currently supports an offline **Ho ASR capability**. 
*Note: Ho translation is not yet available in the current prototype. Ho speech output (TTS) is not available in the current prototype.*

## Required Software
- Python 3.10+ (for FastAPI backend)
- WSL2 (for IndicTrans2 offline translation provider)
- Flutter/Android Studio (for Android app compilation/emulator)

## Startup Instructions

### 1. WSL IndicTrans2 Server
In a WSL2 terminal, activate the IndicTrans2 environment and run the server:
cd /path/to/indictrans2
python indictrans2_server.py

### 2. Windows FastAPI Backend
In a Windows terminal at the project root, start the backend:
.\venv\Scripts\python -m uvicorn app.api.main:app --port 8000

### 3. Android App
Run the application on an emulator or physical device:
cd android
flutter run

## Three Demo Flows

**DEMO 1: Hindi -> Santali**
Navigate to the Translator or Classroom screen. Select Hindi as source and Santali as target. Speak or type in Hindi. The app will process ASR, translate to Santali via the WSL-hosted IndicTrans2 provider, and synthesize the result.

**DEMO 2: Ho Speech -> Ho Transcript**
Navigate to the Classroom screen. Select Ho as source. Press the PTT button to record (using a physical device or a pre-recorded WAV bypass for emulator). The app will run local offline Ho ASR and display the Devanagari/WarangCiti transcript. *Note: Translation is automatically bypassed due to unavailability.*

**DEMO 3: Santali -> Hindi**
Similar to Demo 1, select Santali as source and Hindi as target. Input Santali to receive a Hindi transcript and translation via the IndicTrans2 provider.

## Known Limitations
- The Android Emulator cannot securely capture genuine Ho speech through standard microphone inputs; test audio WAV files must be routed manually or a physical device must be used.
- Local IndicTrans2 offline translation currently requires manual WSL server activation to prevent HTTP 500 timeouts.

## Security Instructions & API-Key Setup
API keys must **never** be hardcoded or checked into source control. 

To configure API keys:
1. Copy .env.example to .env.
2. Fill in the .env file with your actual API keys (e.g., OPENAI_API_KEY, GROQ_API_KEY, SARVAM_API_KEY).
3. Ensure .env is listed in .gitignore.

## APK Location
The compiled release APK is located at:
build\app\outputs\flutter-apk\app-release.apk
