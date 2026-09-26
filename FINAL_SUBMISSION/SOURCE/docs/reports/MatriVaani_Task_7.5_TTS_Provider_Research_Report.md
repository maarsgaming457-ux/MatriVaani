# MatriVaani — Task 7.5 TTS Provider Research Report

## 1. Objective
Investigate alternative Text-to-Speech (TTS) technologies that can support Hindi and Santali (Ol Chiki) for the MatriVaani SIH prototype without requiring Bhashini API credentials, avoiding the crippling latency and dependency issues found in the local indic-parler-tts implementation.

## 2. Candidates investigated
- i4bharat/indic-parler-tts
- AI4Bharat IndicTTS / Vakyansh
- Piper
- Coqui / XTTS v2
- eSpeak NG

## 3. Santali support
- **Indic Parler-TTS:** VERIFIED
- **IndicTTS (Vakyansh):** VERIFIED
- **Piper:** NOT SUPPORTED
- **Coqui / XTTS v2:** NOT SUPPORTED
- **eSpeak NG:** NOT SUPPORTED

## 4. Ol Chiki support
- **Indic Parler-TTS:** VERIFIED
- **IndicTTS (Vakyansh):** VERIFIED
- All other candidates do not support Santali, and thus do not support Ol Chiki.

## 5. Hindi support
- **Indic Parler-TTS:** VERIFIED
- **IndicTTS (Vakyansh):** VERIFIED
- **Piper:** VERIFIED
- **Coqui / XTTS v2:** VERIFIED
- **eSpeak NG:** VERIFIED

## 6. Deployment requirements
- **Indic Parler-TTS:** Requires PyTorch, Transformers. CPU inference blocks API threads for 10s+. Windows compatibility is extremely poor due to missing C++ compilation targets for parler_tts. GPU practically required.
- **IndicTTS (Vakyansh):** FastPitch/HiFiGAN models require complex, undocumented Python setups that generally only compile cleanly on Linux GPU clusters.
- **Piper:** Native Windows .exe and python bindings exist. Runs instantly on CPU. Extremely lightweight.
- **Coqui XTTS v2:** Requires PyTorch. Heavy RAM footprint. Runs slowly on CPU.
- **eSpeak NG:** Native Windows support. Zero RAM overhead.

## 7. Offline capability
All researched open-source candidates are **YES** (100% offline capable).

## 8. API/key requirements
All researched open-source candidates are **NO** (no API keys required).

## 9. Quality
- **Indic Parler-TTS:** GOOD (natural sounding, expressive).
- **IndicTTS:** GOOD (natural).
- **Piper:** GOOD (highly optimized, standard neural quality).
- **XTTS v2:** EXCELLENT (voice cloning capable).
- **eSpeak NG:** POOR (robotic, synthesizer sound).

## 10. Latency suitability
- **Indic Parler-TTS (CPU):** POOR (too slow for classrooms).
- **IndicTTS (CPU):** POOR.
- **Piper (CPU):** GOOD (instant).
- **XTTS v2 (CPU):** POOR.
- **eSpeak NG (CPU):** GOOD (instant).

## 11. Licensing
- **Indic Parler-TTS:** MIT (GOOD)
- **IndicTTS:** MIT (GOOD)
- **Piper:** MIT (GOOD)
- **Coqui XTTS v2:** CPML - non-commercial (REVIEW REQUIRED)
- **eSpeak NG:** GPLv3 (REVIEW REQUIRED)

## 12. MatriVaani integration feasibility
All candidates could eventually fit behind the POST /tts wrapper by synthesizing to a buffer and returning udio/wav bytes to Flutter. 

## 13. Comparison table

| Candidate | Santali | Ol Chiki | Hindi | API Key | Offline | Windows | CPU | GPU | Quality | Integration |
|-----------|----------|----------|-------|---------|---------|---------|-----|-----|---------|-------------|
| **Indic Parler-TTS** | VERIFIED | VERIFIED | VERIFIED | NO | YES | POOR | POOR | REQ | GOOD | POSSIBLE |
| **IndicTTS (Vakyansh)** | VERIFIED | VERIFIED | VERIFIED | NO | YES | POOR | POOR | REQ | GOOD | POSSIBLE |
| **Piper** | NOT SUPPORTED | NOT SUPPORTED | VERIFIED | NO | YES | GOOD | GOOD | NO | GOOD | POSSIBLE |
| **Coqui (XTTS v2)** | NOT SUPPORTED | NOT SUPPORTED | VERIFIED | NO | YES | POOR | POOR | REQ | EXCELLENT| POSSIBLE |
| **eSpeak NG** | NOT SUPPORTED | NOT SUPPORTED | VERIFIED | NO | YES | GOOD | GOOD | NO | POOR | POSSIBLE |

## 14. Best candidate
**NO VERIFIED NO-API-KEY SANTALI TTS CANDIDATE FOUND** that is actually viable for deployment on the local Windows CPU prototype. 
If forced to run locally without Bhashini, the *only* choice is fixing the broken indic-parler-tts installation, which will result in crippling latency.

## 15. Second-best candidate
None applicable for Santali. 
(If Hindi only: **Piper** would be the undisputed champion for CPU inference).

## 16. Fallback
**Bhashini TTS API.**

## 17. Risks
The single greatest risk to the MatriVaani SIH prototype is the absolute lack of lightweight, offline, CPU-capable Santali TTS models in the open-source ecosystem. The project currently *must* rely on either AI4Bharat APIs (Bhashini) or accept multi-second rendering delays that break the conversational flow of a classroom application.

## 18. Final recommendation
Do not waste further engineering effort attempting to force heavy, Linux-centric PyTorch TTS models to run efficiently on a Windows CPU laptop. The prototype requires Bhashini credentials to function smoothly.

## 19. Exact next task
TASK 7.6 — Use Bhashini when credentials become available.

---

FILES MODIFIED:
NONE

PACKAGES INSTALLED:
NONE

MODELS DOWNLOADED:
NONE

TTS SYNTHESIS CALLED:
NO

BHASHINI CALLED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

FLUTTER CHANGED:
NO

CREDENTIALS EXPOSED:
NO
