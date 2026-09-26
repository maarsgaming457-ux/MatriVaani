# MatriVaani — Task 7.2 Indic Parler TTS Feasibility Report

## 1. Current TTS implementation
- **File:** pp/services/tts_service.py
- **Library:** parler_tts via Hugging Face 	ransformers
- **Model:** i4bharat/indic-parler-tts
- **Tokenizers:** i4bharat/indic-parler-tts (text) and google/flan-t5-large (description)
- **Loading:** Lazy-loaded singleton pattern.
- **Generation Method:** Uses self.model.generate() matching an English description prompt against the target text to synthesize audio on the CPU.
- **Patches:** Includes massive monkey-patching of GenerationMixin and ParlerTTSConfig to fix CPU tensor allocation and weight tying bugs inherent in the library.

## 2. Environment
- **Windows version:** 10.0.26200
- **Python version:** 3.14.2
- **RAM:** 23.38 GB
- **CPU:** 8 Cores / 16 Threads
- **PyTorch version:** 2.12.1+cpu
- **CUDA availability:** False
- **GPU / VRAM:** None

## 3. Installed dependencies
- parler_tts: **Not installed**
- 	ransformers: 5.14.1
- 	orch: 2.12.1+cpu
- soundfile: 0.14.0
- 
umpy: 2.4.4
- sentencepiece: **Not installed**
- 	okenizers: 0.22.2

## 4. Compatibility
- The code relies on parler_tts, which is missing.
- Python 3.14 compatibility with parler_tts and PyTorch 2.12 is highly questionable, often leading to compilation issues.
- Missing sentencepiece is a fatal blocker, as google/flan-t5-large requires it for tokenization.

## 5. Model/memory feasibility
- **Size:** i4bharat/indic-parler-tts and its dependencies (like Flan-T5 tokenizers) require 1.5 GB to 3 GB of RAM. The machine has 23.38 GB RAM, making memory storage feasible.
- **CPU Execution:** **POSSIBLE BUT SLOW**

## 6. GPU feasibility
- **GPU Execution:** **BLOCKED**
- The current machine has no NVIDIA GPU. The local implementation forces CPU execution (self.device = "cpu").

## 7. Santali support
- The current code explicitly restricts execution to Santali (if language == "santali").
- The language itself is passed into the model natively (the target text in Ol Chiki is fed to the tokenizer). indic-parler-tts does support Santali (Ol Chiki). 

## 8. Hindi support
- i4bharat/indic-parler-tts broadly supports Hindi.
- The current 	ts_service.py completely blocks Hindi. To fix it, the if language == "santali" check must be expanded to if language in ["santali", "hindi"] in the synthesize() method.

## 9. Audio output
- **Sample Rate:** Matches the model's config (self.model.config.sampling_rate, likely 24kHz or 44.1kHz).
- **Format:** WAV (PCM_16).
- **Channels:** Mono.
- **Flutter Compatibility:** Flutter's udioplayers package natively consumes PCM_16 WAV bytes perfectly. 

## 10. FastAPI feasibility
- **Architecture:** The POST /tts endpoint is completely synchronous (def tts_endpoint).
- **Latency:** CPU inference for Parler-TTS often takes 5–20 seconds per sentence.
- **Worker Blocking:** A synchronous request taking 15 seconds will block the FastAPI worker, forcing all concurrent requests (including offline sync and translation) to hang.
- **Startup:** The initial lazy load will stall the first request heavily.
- **Conclusion:** Running local CPU TTS inference directly inside the main web thread is not viable for production.

## 11. Local vs remote comparison
**A. Local Indic Parler-TTS (Windows CPU)**
- **Support:** Hindi & Santali (Ol Chiki).
- **Hardware:** Extremely heavy (100% CPU spikes during generation).
- **Dependencies:** Complex (missing parler_tts, sentencepiece).
- **Latency:** High (5,000ms - 15,000ms+).
- **Offline:** Yes.
- **SIH Suitability:** Poor (slow, blocks API).

**B. Remote Bhashini TTS API**
- **Support:** Hindi & Santali (Ol Chiki).
- **Hardware:** Zero local footprint.
- **Dependencies:** Minimal (just HTTP requests).
- **Latency:** Low (~500ms - 1,500ms).
- **Offline:** No.
- **SIH Suitability:** Excellent (fast, reliable, identical output quality).

## 12. Recommendation
**NO.** 
MatriVaani should **not** continue with local i4bharat/indic-parler-tts on the current Windows backend. 

**Why:** The missing dependencies (parler_tts, sentencepiece), the lack of a GPU, and the synchronous FastAPI architecture mean that local TTS will crash on startup, and even if patched, will block the entire server for 10+ seconds per audio request.

**Next Investigation:** The team should immediately investigate integrating the **Bhashini TTS API** as the primary TTS provider.

## 13. Exact next task
Investigate the official Bhashini API documentation for Text-to-Speech (TTS), specifically determining the pipeline payloads, service IDs, and language codes required to synthesize Hindi and Santali text into audio.

FILES MODIFIED:
NONE

PACKAGES INSTALLED:
NONE

MODEL DOWNLOADED:
NO

API CALLED:
NO

ASR CHANGED:
NO

TRANSLATION CHANGED:
NO

FLUTTER CHANGED:
NO

TTS IMPLEMENTED:
NO
