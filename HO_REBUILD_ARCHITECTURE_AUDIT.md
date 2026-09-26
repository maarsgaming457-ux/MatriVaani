# MATRI VAANI — HO REBUILD ARCHITECTURE AUDIT

## PART 1 — SANTALI AS REFERENCE

### Current Santali Implementation Runtime Path
1. **Android**: ClassroomScreen invokes ApiService.processAudio().
2. **ASR**: POST /asr routes to ASRService._load_model('santali').
3. **Translation**: POST /translate routes to TranslationService (using IndicTrans2/Sarvam/Bhashini).
4. **TTS**: POST /tts routes to SarvamTTSProvider (raises TTSUnavailableError for Santali).

### Component Details
1. **Santali ASR model**: Fine-tuned Wav2Vec2ForCTC.
2. **Santali ASR dataset**: Private/unlisted dataset.
3. **ASR preprocessing**: Wav2Vec2Processor.
4. **Santali script**: Ol Chiki (confirmed via ocab.json).
5. **Hindi ? Santali NMT**: IndicTrans2 (via Ngrok/Local) + API fallbacks.
6. **Santali ? Hindi NMT**: IndicTrans2 (via Ngrok/Local) + API fallbacks.
7. **Translation datasets**: Bharat Parallel Corpus Collection (BPCC).
8. **Translation tokenizer**: IndicTransTokenizer.
9. **Santali TTS model**: **None**.
10. **TTS input script**: N/A.
11. **TTS output format**: N/A.
12. **FastAPI endpoints**: /asr, /translate, /tts.
13. **Service classes**: ASRService, TranslationService, TTSService, OfflineService.
14. **Android Dart code**: API calls chained in UI logic.
15. **Language routing**: Santali maps to sat.
16. **Error handling**: Raised as HTTP 400/500 via FastAPI exception handlers.
17. **Online/offline fallback**: Local ASR and local IndicTrans2 API exist. 
18. **Model files**: /models/santhali_asr_final_5k/ (model.safetensors).
19. **Training scripts**: None in repository.
20. **Google Colab scripts**: Linked to Google Drive paths in config.py (/content/drive/MyDrive/MatriVaani_ASR/).

---

## PART 2 — SANTALI DATASET INVENTORY

### ASR DATA
- **Name**: Unknown Internal Santali Dataset
- **Task**: Automatic Speech Recognition
- **Script**: Ol Chiki
- **License**: Unknown

### TRANSLATION DATA
- **Name**: Bharat Parallel Corpus Collection (BPCC)
- **Task**: NMT (Hindi ? Santali)
- **Script**: Devanagari ? Ol Chiki

### TTS DATA
- **Name**: N/A (No Santali TTS exists).

---

## PART 3 — SANTALI MODEL INVENTORY

### ASR MODEL
- **Name**: santhali_asr_final_5k
- **Architecture**: Wav2Vec2ForCTC (Large)
- **Method**: Fine-tuning

### NMT MODEL
- **Name**: IndicTrans2
- **Architecture**: Transformer Seq2Seq
- **Method**: Pre-trained API / Ngrok endpoint

---

## PART 4 — CURRENT HO ASR

- **Model**: Wav2Vec2ForCTC
- **Checkpoint**: models/ho_asr/ (~377MB).
- **Latency**: 5.0s - 7.5s (sub-optimal).
- **Android compatibility**: Yes (via REST API).
- **Verdict**: **RETRAIN**. The current base model has high latency and likely requires compression (ONNX) or an upgraded acoustic model to meet the = 3.0s target latency.

---

## PART 5 — PROJECT-BOLI/HO

- **Number of samples**: < 1,000.
- **Speakers**: 1 (Poonam Biruly).
- **License**: CC-BY-NC-SA-4.0.
- **Suitability for ASR**: Poor (Requires 50+ hours, currently < 1 hour).
- **Suitability for NMT**: None (Speech-only).
- **Suitability for TTS**: Moderate (Single speaker is ideal for TTS, but < 1K samples is insufficient for robust prosody).

---

## PART 6 — HO TRANSLATION

- **Current Architecture**: ExperimentalHindiToHoTranslator using Groq LLM API.
- **Method**: RAG-style lookup from HO_LEXICON_V4.json and grammar rules injected into an LLM prompt.
- **Failure Cases**: Hallucinations, extreme latency, dependent on external API.
- **Verdict**: **REPLACE**. RAG+LLM is too slow and fragile for real-time classroom routing. We must train/fine-tune a dedicated NMT model.

---

## PART 7 — HO TTS

- **Current Attempt**: acebook/mms-tts-hoc.
- **Failure Reason**: Model expects **Odia script**, ignoring genuine Ho (Latin/Devanagari) text.
- **Alternatives**: None exist on HuggingFace.
- **Verdict**: **TRAIN**. We must build a Ho TTS model from scratch or fine-tune a VITS base model using a clean, single-speaker dataset aligned with our chosen orthography (Latin/Devanagari).

---

## PART 8 — NEW HO DATASET REQUIREMENTS

### HO ASR DATA
- **Target Size**: 50+ hours.
- **Quality**: Mobile microphone classroom environment.
- **Method**: Crowdsourced recording.

### HO-HINDI TRANSLATION DATA
- **Target Size**: 50,000+ parallel sentence pairs.
- **Quality**: Verified orthography (strict Latin or strict Devanagari).
- **Method**: Translation of existing primary education textbooks.

### HO TTS DATA
- **Target Size**: 5-10 hours.
- **Quality**: Studio-quality, single female voice (teacher persona).
- **Method**: Professional recording of curriculum text.

---

## PART 9 — MODEL SELECTION

### HO ASR
- **Candidate**: wav2vec2-large-xlsr-53 or Whisper (via forced byte-level alignment).
- **Status**: FINE-TUNING REQUIRED.

### HINDI ? HO / HO ? HINDI
- **Candidate**: NLLB-200 or IndicTrans2 (Extending vocab).
- **Status**: FINE-TUNING REQUIRED.

### HO TTS
- **Candidate**: VITS or FastSpeech2.
- **Status**: TRAINING REQUIRED.

---

## PART 10 — GOOGLE COLAB PLAN

1. **Hardware**: A100 (40GB) recommended.
2. **Pipeline**: 
   Dataset Prep ? Tokenizer Training ? Fine-tuning ? Validation ? ONNX Export ? FastAPI integration.
3. **Storage**: Mount Google Drive for checkpointing.

---

## PART 11 — FINAL HO ARCHITECTURE

### PIPELINE A: Hindi ? Ho
Hindi Speech ? Whisper ASR ? Hindi Text ? Fine-Tuned IndicTrans2 ? Ho Text ? Trained VITS TTS ? Android

### PIPELINE B: Ho ? Hindi
Ho Speech ? Fine-Tuned Wav2Vec2 ASR ? Ho Text ? Fine-Tuned IndicTrans2 ? Hindi Text ? Sarvam TTS ? Android

*(Note: Santali continues using the existing hub architecture).*

---

## PART 12 — FINAL DECISION

- **HO ASR**: RETRAIN
- **HINDI ? HO**: REPLACE
- **HO ? HINDI**: REPLACE
- **HO TTS**: TRAIN
- **PROJECT-BOLI/HO**: SUPPLEMENT

---

## PART 13 — IMPLEMENTATION ORDER

- **PHASE HO-0**: Dataset Standardization (Collect 50h ASR, 50k NMT, 10h TTS data; lock orthography script).
- **PHASE HO-1**: NMT Fine-Tuning (Train Hindi?Ho NMT on A100; replace Groq LLM in backend).
- **PHASE HO-2**: ASR Retraining (Fine-tune Wav2Vec2 on Ho speech; export to ONNX for latency).
- **PHASE HO-3**: TTS Training (Train VITS on new Ho voice data; integrate into /tts endpoint).
- **PHASE HO-4**: Backend API Update (Wire ASR, NMT, and TTS models to FastAPI routes).
- **PHASE HO-5**: Android Integration (Enable Ho buttons in UI, route requests, offline DB sync).
- **PHASE HO-6**: E2E Latency Optimization & Deployment (Target = 3.0s).
