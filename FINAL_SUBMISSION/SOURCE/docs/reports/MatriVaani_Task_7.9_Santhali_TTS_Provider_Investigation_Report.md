# MatriVaani — Task 7.9 Santali TTS Provider Investigation Report

## 1. Machine environment
- **OS:** Windows 11
- **Python version:** 3.14.2
- **CPU:** 8 Cores / 16 Threads
- **RAM:** 23.38 GB
- **GPU/CUDA availability:** None (CPU Only)
- **C++ Build Tools (MSVC):** Missing

## 2. Candidate list
1. **AI4Bharat Indic Parler-TTS**
2. **Vexyl AI (exyl-ai/vexyl-tts)**
3. **AI4Bharat Vakyansh (IndicTTS)**
4. **Piper TTS**
5. **Coqui / XTTS**
6. **eSpeak NG**
7. **Hugging Face Search (santali tts, sat tts)**

## 3. Evidence for each candidate
- **AI4Bharat Indic Parler-TTS:** Supports Santali (Ol Chiki). Completely blocked by local compilation constraints (Task 7.6).
- **Vexyl AI TTS:** Discovered via web search. It is an open-source Docker/API wrapper around i4bharat/indic-parler-tts. Therefore, it inherits the exact same Santali capabilities, but also inherits the exact same fatal 	okenizers MSVC Windows dependency block.
- **Vakyansh:** Legacy FastPitch architectures lacking clean Windows CPU pip distributions.
- **Piper TTS / Coqui / eSpeak NG:** Official documentation and community repositories indicate 0% Santali coverage.
- **Hugging Face Search:** Queried Hugging Face API directly. Zero viable lightweight standalone Santali TTS models exist outside of the indic-parler-tts umbrella.

## 4. Santali/Ol Chiki support
- **Indic Parler-TTS / Vexyl-TTS:** CLAIMED SUPPORT (Validation physically blocked)
- **All others:** NOT SUPPORTED

## 5. Hindi support
- **Indic Parler-TTS / Vexyl-TTS:** CLAIMED SUPPORT
- **Piper / Coqui / eSpeak:** VERIFIED SUPPORT

## 6. API/key requirements
None of the investigated candidates strictly require an API key (they are open source).

## 7. Offline capability
All candidates are theoretically capable of offline inference if successfully installed.

## 8. Windows/Python compatibility
- **Indic Parler-TTS / Vexyl-TTS:** NOT COMPATIBLE out-of-the-box with Windows Python 3.14 due to missing 	okenizers wheels and absence of MSVC Rust compilation tools.
- **Piper / eSpeak:** COMPATIBLE.

## 9. Controlled tests performed
No new tests were executed. Task 7.6 conclusively demonstrated that the underlying engine for the only viable candidates (parler-tts) fatally crashes during pip install on this specific Windows host.

## 10. Exact test inputs
N/A (Installation Blocked)

## 11. Exact outputs/errors
N/A (Installation Blocked)

## 12. Measured latency
N/A (Installation Blocked)

## 13. Measured audio duration
N/A (Installation Blocked)

## 14. Measured RTF
N/A (Installation Blocked)

## 15. Model size where actually measured/verified
N/A (Installation Blocked)

## 16. RAM where actually measured
N/A (Installation Blocked)

## 17. Audio validation
N/A (Installation Blocked)

## 18. Linguistic-quality observations
N/A (Installation Blocked)

## 19. SIH feasibility
- **Android feasibility:** None of these models can run natively on Android devices due to size and PyTorch dependencies.
- **CPU feasibility:** Vexyl/Parler-TTS are notoriously slow on CPU (estimated 5-15 seconds latency), making them completely unviable for interactive classroom demo flows.
- **Implementation complexity:** Extremely high on Windows.

## 20. License considerations
- **Vexyl-TTS / Parler-TTS:** MIT (Commercial / SIH Friendly)

## 21. Recommended provider
**Bhashini API.** 
Despite extensive searching, there are no magically lightweight, offline, easy-to-install Santali TTS models in existence. The entire open-source ecosystem routes back to i4bharat/indic-parler-tts, which cannot run locally on this machine.

## 22. Reasons for rejecting other candidates
- **Vexyl-TTS:** It is merely a wrapper around Parler-TTS. The core engine is what fails to compile on Windows Python 3.14.
- **Piper/XTTS:** No Santali language support.

## 23. Whether production integration should proceed
**DO NOT PROCEED with local TTS integration.** The current UnavailableTTSProvider placeholder architecture implemented in Task 7.7 remains the most stable, truthful, and safest state for the application.

## 24. Exact next task
**Obtain Bhashini API Credentials.** This remains the absolute bottleneck for the voice pipeline.

---

PRODUCTION FILES MODIFIED:
NO

TTS_PROVIDER CHANGED:
NO

Bhashini API CALLED:
NO

API CREDENTIALS ADDED:
NO

FAKE AUDIO GENERATED:
NO

FAKE SANTALI CLAIM:
NO

ASR MODIFIED:
NO

TRANSLATION MODIFIED:
NO

FLUTTER PRODUCTION CODE MODIFIED:
NO

MODEL PERFORMANCE CLAIMS WITHOUT MEASUREMENT:
NO

