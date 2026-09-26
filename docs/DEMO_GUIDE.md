# Demo Guide

This document outlines the strict architecture constraints and acceptance criteria for demonstrating MatriVaani.

## 1. Online Demo Architecture
The online demo simulates a standard cloud-connected experience.

```text
Phone
 ↓
Wi-Fi / Mobile data
 ↓
HTTPS
 ↓
Cloud FastAPI
 ↓
Models / External APIs
```
**Test Requirement:** Must be successfully tested from multiple separate networks (not just the developer's local Wi-Fi).

## 2. Offline Demo Architecture
The offline demo proves true edge execution without cheating.

```text
Phone
 ↓
Airplane Mode Enabled
 ↓
MatriVaani App
 ↓
Offline • On-device Mode
 ↓
Local Native Inference
```
**Test Requirement:** The offline demo must not require a PC running in the background.

## 3. Acceptance Checklist

### Online
- [ ] Cloud FastAPI deployed and reachable
- [ ] HTTPS routing works
- [ ] `/health` check responds
- [ ] Flutter app connects successfully
- [ ] Translation functions normally
- [ ] ASR transcribes accurately
- [ ] TTS streams audio back
- [ ] Environment secrets remain safely on the server side
- [ ] Verified across multiple Wi-Fi/LTE networks

### Offline
- [ ] Internet fully disabled (Airplane Mode)
- [ ] No PC or local server connected
- [ ] Android properly detects offline state
- [ ] Local model successfully loads into RAM
- [ ] Supported offline translation executes
- [ ] Supported offline ASR executes
- [ ] Local TTS outputs audio (if implemented natively)
- [ ] Zero blocked network requests logged
- [ ] Application safely restarts while offline
- [ ] Verified to work on a secondary Android device

### Fallback System
- [ ] Automatic online selection when internet is detected
- [ ] Fast, automatic offline fallback when requests fail/timeout
- [ ] Manual mode override toggle functions
- [ ] Application does not get stuck in infinite retry loops
- [ ] Status indicator accurately displays the current mode

### Model Integrity
- [ ] Frozen Mundari SHA256 matches exactly `D3B7536F64B42EE7EA5F6D48F0D87461B3398ACBD3B84D5B8A233370812986B5`
- [ ] Original `.safetensors` models are preserved
- [ ] Converted mobile artifacts (`.tflite`, `.onnx`) are securely separated
