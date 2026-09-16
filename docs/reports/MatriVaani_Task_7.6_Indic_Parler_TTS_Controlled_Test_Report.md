# MatriVaani — Task 7.6 Indic Parler-TTS Controlled Test Report

## 1. Objective
To perform a controlled local feasibility test of i4bharat/indic-parler-tts to determine if it can practically serve MatriVaani's Hindi and Santali (Ol Chiki) TTS requirements on the current Windows development environment.

## 2. Test environment
- **Windows version:** 10.0.26200
- **Python version:** 3.14.2
- **CPU:** 8 Cores / 16 Threads
- **RAM:** 23.38 GB
- **GPU availability:** None
- **CUDA availability:** False
- **PyTorch version:** 2.12.1+cpu
- **Transformers version:** 5.14.1

## 3. Existing dependencies
- 	orch: INSTALLED
- 	ransformers: INSTALLED
- soundfile: INSTALLED
- 
umpy: INSTALLED
- parler_tts: **MISSING**
- sentencepiece: **MISSING**

## 4. Installation feasibility
Attempted to install parler_tts into an isolated temporary workspace (	ts_test_workspace\venv).
The installation **FAILED FATALLY**. 
The installation of parler_tts requires 	okenizers<0.21, which attempts to compile native Rust/C++ bindings from source due to the absence of pre-built wheels for Python 3.14. The compilation crashed with:

ote: the msvc targets depend on the msvc linker but link.exe was not found. please ensure that Visual Studio 2017 or later, or Build Tools for Visual Studio were installed with the Visual C++ option

## 5. Model loading result
**FAILED.** The model cannot be loaded because the required library (parler_tts) is impossible to install on this machine without a multi-gigabyte manual Visual Studio C++ Build Tools installation.

## 6. Santali test
**FAILED TO EXECUTE** (Blocked by installation failure)

## 7. Ol Chiki test
**FAILED TO EXECUTE** (Blocked by installation failure)

## 8. Hindi test
**FAILED TO EXECUTE** (Blocked by installation failure)

## 9. Audio validation
**FAILED TO EXECUTE** (No audio generated)

## 10. Performance measurements
**FAILED TO EXECUTE** (N/A)

## 11. Resource usage
**FAILED TO EXECUTE** (N/A)

## 12. Quality assessment
- Santali: **FAILED**
- Hindi: **FAILED**
- *LISTENING QUALITY NOT VERIFIED*

## 13. Errors/blockers
- **Missing MSVC C++ Build Tools:** Prevents parler_tts and 	okenizers compilation.
- **Python 3.14 Wheel Availability:** Severely limits PyTorch/Hugging Face ecosystem compatibility out-of-the-box on Windows.
- **No GPU:** Even if compilation succeeded, inference would crash or block the thread indefinitely due to CPU limits.

## 14. Production suitability
**D. NOT FEASIBLE ON CURRENT HARDWARE**

## 15. SIH demo suitability
**D. NOT FEASIBLE ON CURRENT HARDWARE**

## 16. Final decision
**D. NOT FEASIBLE ON CURRENT HARDWARE**
The software dependency chain for i4bharat/indic-parler-tts fundamentally conflicts with the current Windows development machine. It cannot be used locally.

## 17. Exact next task
**TASK 7.7 — Implement Fallback Architecture (Bhashini Mock/Wait)**
Since no local TTS model can be executed on this laptop, the project must either mock the TTS layer entirely for UI development, or wait for Bhashini API credentials to become available.

| Test | Result | Evidence |
|------|--------|----------|
| Model loading | FAILED | Blocked by fatal \	okenizers\ MSVC C++ compilation error during \parler_tts\ installation. |
| Santali | FAILED | N/A |
| Ol Chiki | FAILED | N/A |
| Hindi | FAILED | N/A |
| Audio generation | FAILED | N/A |
| CPU inference | FAILED | N/A |
| GPU inference | FAILED | No GPU available. |
| Performance | FAILED | N/A |

FILES MODIFIED:
NONE

MATRI VAANI SOURCE MODIFIED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

FLUTTER CHANGED:
NO

API CONTRACT CHANGED:
NO

REQUIREMENTS.TXT CHANGED:
NO

.ENV CHANGED:
NO

EXTERNAL TTS API CALLED:
NO

BHASHINI CALLED:
NO

CREDENTIALS EXPOSED:
NO

MODEL INTEGRATED:
NO
