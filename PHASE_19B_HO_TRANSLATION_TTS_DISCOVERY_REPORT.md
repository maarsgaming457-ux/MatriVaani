# PHASE 19B HO TRANSLATION + TTS DISCOVERY REPORT

## 1. Existing Ho ASR model
models/ho_asr is a Connectionist Temporal Classification (CTC) ASR model using the Wav2Vec2 architecture. It strictly maps audio to Devanagari text tokens and possesses absolutely no translation capabilities.

## 2. Ho translation model inventory
No genuine Ho ↔ Hindi translation model exists. The previous BhashaVerse experiment failed. Hugging Face search revealed no functional Seq2Seq models capable of this translation pair.

## 3. Ho-Hindi dataset inventory
No verified Ho ↔ Hindi sentence-level parallel data could be recovered. The existing 100 Ho ASR transcripts lack legitimate Hindi sentence-level alignment. No public resource (AI4Bharat, OPUS, Bhashini, CIIL) provides sentence-aligned data. Therefore, data/ho_hindi/ was NOT created, adhering strictly to the rule against faking or machine-generating data.

## 4. Ho TTS model inventory
A legitimate Ho TTS model was discovered on Hugging Face: acebook/mms-tts-hoc. This is part of the Massively Multilingual Speech (MMS) project. It utilizes a VITS architecture and generates 16kHz audio. Notably, its tokenizer expects Ho text written in the Odia script (\u0b15\u0b3e).

## 5. Isolated tests
An isolated test (	est_mms_tts.py) was executed for acebook/mms-tts-hoc. 
- **Input:** Odia characters \u0b15\u0b3e (representing Ho phonemes).
- **Result:** Successfully generated a valid 16000 Hz, single-channel WAV file (ho_tts_output.wav) with a duration of 0.37 seconds.
- **Latency:** 0.33 seconds (CPU inference).

## 6. Model licenses
- models/ho_asr: Assumed Custom/Project License
- acebook/mms-tts-hoc: CC-BY-NC 4.0

## 7. Data provenance
The existing 100 ASR records remain monolingual (Ho Audio -> Ho Text). There is no provenance for any Ho-Hindi translation pairs. 

## 8. Hardware requirements
The MMS-TTS model is extremely lightweight and runs rapidly on the CPU (0.33 seconds for a short phrase). It requires minimal RAM/VRAM footprint, making it perfectly suitable for the MatriVaani architecture.

## 9. Latencies
- Ho TTS (MMS-TTS): ~0.33 seconds per short phrase on CPU.
- Ho Translation: N/A (Does not exist).

## 10. Exact implementation path
- **Ho TTS:** We can securely integrate acebook/mms-tts-hoc into 	ts_service.py. A critical pre-processing step is required: mapping the application's internal Devanagari Ho text (used by Ho ASR) into Odia script to feed into the MMS-TTS tokenizer.
- **Ho Translation:** Completely blocked. We must build a human-verified Ho-Hindi parallel corpus before any translation model can be fine-tuned or implemented.

## 11. Files changed
- PHASE_19B_MODEL_INVENTORY.md (Created)
- PHASE_19B_HO_TRANSLATION_TTS_DISCOVERY_REPORT.md (Created)
- 	est_mms_tts.py (Created isolated test script)
- ho_tts_output.wav (Generated test artifact)

## 12. Files protected
All production files were fiercely protected. No modifications were made to pp/services/, Flutter UI, or existing offline models.

## 13. Exact remaining blockers
- **LACK OF PARALLEL DATA:** There is no ground truth Ho ↔ Hindi dataset. Without it, we cannot train a translation model.
- **SCRIPT MISMATCH:** The existing Ho ASR outputs Devanagari script, but the Ho TTS model expects Odia script. A reliable transliteration function must be implemented to connect these pipelines once translation is solved.

---

### CAPABILITY STATUS MATRIX
- **Ho Speech → Ho Text (ASR):** AVAILABLE NOW
- **Ho Text → Ho Speech (TTS):** EXPERIMENTAL (Model isolated, requires script transliteration for integration)
- **Hindi Text → Ho Text (Translation):** REQUIRES DATA and REQUIRES TRAINING
- **Ho Text → Hindi Text (Translation):** REQUIRES DATA and REQUIRES TRAINING
