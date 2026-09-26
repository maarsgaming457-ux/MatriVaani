# Offline Mode Specifications

**True offline mode strictly means:**
- No Internet
- No Cloud API
- No PC-hosted FastAPI Server
- No Local Wi-Fi dependency

## Target Pipelines

### Mundari Offline Translation
```text
Hindi text
 ↓
Android tokenizer/preprocessing
 ↓
Mundari mobile model
 ↓
postprocessing
 ↓
Mundari text
```
**Regression Guarantee:** The model must consistently translate `मेरा नाम सुमित है।` to `आञाः नुतुम सुमित मेनाः।`

### Santali Offline ASR
```text
Android microphone
 ↓
audio preprocessing
 ↓
local Santali ASR
 ↓
Ol Chiki transcription
 ↓
Flutter
```
*No audio upload is allowed in offline mode.*

### Offline TTS
Local Text-To-Speech (TTS) must be implemented genuinely on-device. Sarvam API and other cloud wrappers **cannot** be claimed as offline. If a local TTS engine does not exist for a specific language, the application must expose that limitation rather than secretly hitting the network.

## Testing Integrity
An offline hard-network test must:
1. Disable network requests from MatriVaani.
2. Intercept and record any attempted network requests.
3. Fail immediately if an offline operation attempts the network.
