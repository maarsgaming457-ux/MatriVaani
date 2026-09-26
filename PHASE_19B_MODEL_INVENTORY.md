# PHASE 19B MODEL INVENTORY

## CANDIDATE 1
* **PATH:** models/ho_asr
* **MODEL:** Wav2Vec2ForCTC
* **TASK:** Automatic Speech Recognition (ASR)
* **SOURCE:** Ho Audio
* **TARGET:** Ho Text (Devanagari script)
* **LANGUAGE CODES:** N/A (custom vocabulary)
* **TRAINING DATA:** Local Pilot Dataset (100 records)
* **LICENSE:** Unknown/Custom
* **USABLE FOR HO→HINDI:** No
* **USABLE FOR HINDI→HO:** No
* **EVIDENCE:** config.json confirms architecture is Wav2Vec2ForCTC. Testing in Phase 17 confirms it does not translate.

## CANDIDATE 2
* **PATH:** Hugging Face acebook/mms-tts-hoc
* **MODEL:** VITS (Massively Multilingual Speech)
* **TASK:** Text-to-Speech (TTS)
* **SOURCE:** Ho Text (Odia script)
* **TARGET:** Ho Audio (16kHz)
* **LANGUAGE CODES:** hoc
* **TRAINING DATA:** MMS dataset
* **LICENSE:** CC-BY-NC 4.0
* **USABLE FOR HO→HINDI:** No
* **USABLE FOR HINDI→HO:** No (It is for TTS)
* **EVIDENCE:** Successfully downloaded and verified locally via 	est_mms_tts.py. Model generated valid 16kHz WAV audio from Odia-scripted Ho text.

## CANDIDATE 3
* **PATH:** Hugging Face ltrciiith/bhashik-parallel-corpora-generic (Associated BhashaVerse Models)
* **MODEL:** mT5 / M2M100 based (BhashaVerse)
* **TASK:** Machine Translation
* **SOURCE:** hoc_Wara
* **TARGET:** hin_Deva
* **LANGUAGE CODES:** hoc, hin
* **TRAINING DATA:** Bhashik Parallel Corpora
* **LICENSE:** CC-BY-NC 4.0
* **USABLE FOR HO→HINDI:** No
* **USABLE FOR HINDI→HO:** No
* **EVIDENCE:** Phase 13 zero-shot tests explicitly failed, demonstrating that the model hallucinates or transliterates instead of translating.
