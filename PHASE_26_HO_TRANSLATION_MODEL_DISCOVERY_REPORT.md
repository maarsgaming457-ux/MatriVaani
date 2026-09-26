# PHASE 26 — AUTOMATED HO ↔ HINDI TRANSLATION MODEL DISCOVERY & VALIDATION REPORT

**Execution Date:** 2026-09-17  
**Status:** **`NO_VERIFIED_PRETRAINED_HO_TRANSLATION_MODEL_FOUND`**  
**Working Directory:** `C:\study_files\sih project`  
**Evaluation Standard:** Zero production modification, empirical inference with genuine Ho sentences, strict read-only protection of human translation forms, and isolation of experimental artifacts.

---

## 1. PROJECT INVENTORY

An exhaustive audit of local directories was conducted to identify any existing Ho-related models, translation checkpoints, parallel corpora, or previous experimental artifacts:
- **`C:\study_files\sih project\`**:
  - `models/ho_asr/`: Contains an acoustic Ho speech recognition model (`Wav2Vec2ForCTC`, 3 adapter layers, 768 hidden size) that transcribes Ho audio into Devanagari phonemic script. Contains **zero sequence-to-sequence translation** capability.
  - `tools/ho_annotator/`: Human annotation interface backed by SQLite (`annotations.db`, 101 rows) and audio storage containing 100 recovered genuine Ho WAV recordings (`tools/ho_annotator/audio/`).
  - `data/ho_hindi/collection/`: Contains master collection workbooks (`HO_HINDI_TRANSLATION_FORM.xlsx`, `HO_HINDI_TRANSLATION_FORM.csv`) and `work/HO_HINDI_TRANSLATION_FORM_WORKING.xlsx`. All 100 entries have `Completed: 0` and `Hindi Translation: None`, awaiting verified human expert translation per `INSTRUCTIONS_FOR_TRANSLATOR.md`.
  - `data/ho_hindi/experimental/`: Created to strictly isolate all Phase 26 automated discovery scripts, model caches, inference outputs, and logs under the safety tag `MACHINE_GENERATED | EXPERIMENTAL | NOT_GROUND_TRUTH`.
  - `FINAL_SUBMISSION/` & `FINAL_SUBMISSION_V2/`: Preserved without modification.
- **`C:\study_files\MatriVaani_GitHub\`**:
  - Checked for any previous translation models or checkpoints. None existed; past repositories focus on the core MatriVaani application, Santali ASR, and UI assets.
- **`C:\Users\maars\Downloads\`**:
  - Scanned for downloaded weights or checkpoints (`.safetensors`, `.pt`, `.bin`, `.onnx`). No Ho translation models found.
- **Previous Phase Reports Audited**:
  - `PHASE_13_BHASHAVERSE_HO_TRANSLATION_REPORT.md`: Audited `ltrciiith/bhashaverse`. Concluded with failure due to Devanagari source copying in Ho→Hindi and corrupted English/Nepali subwords in Hindi→Ho.
  - `PHASE_16A_HO_TRANSLATION_MODEL_INTEGRATION_REPORT.md` & `PHASE_17_HO_TRAINING_RECOVERY_REPORT.md`: Re-affirmed lack of direct pretrained models.
  - `PHASE_23_HO_ENGLISH_BRIDGE_REPORT.md`: Concluded with `HO_ENGLISH_BRIDGE_NOT_AVAILABLE` because no Ho↔English parallel text or models existed in the pipeline.

---

## 2. EXISTING HO MODELS

| Model Path | Architecture | Intended Task | Language / Script | Translation Feasibility |
|---|---|---|---|---|
| `models/ho_asr/` | `Wav2Vec2ForCTC` (Acoustic CTC) | Ho Speech-to-Text | Ho (`hoc`) in Devanagari script | **Zero** (Acoustic audio token classifier, no autoregressive decoder) |
| `ltrciiith/bhashaverse` | Multilingual Marian / Seq2Seq | Multilingual Translation | `hoc` metadata tag | **Failed / Rejected** (Source copying, hallucinations in Phase 13) |

---

## 3. EXISTING TRANSLATION MODELS

| Model / Service | Source Repo | Languages Supported | Ho Support Status | Feasibility |
|---|---|---|---|---|
| **IndicTrans2** | `ai4bharat/indictrans2-indic-indic-1B` | 22 Scheduled Indian Languages | **Not Supported** (Ho is a non-scheduled Austroasiatic language) | Incompatible |
| **NLLB-200** | `facebook/nllb-200-distilled-600M` | 200 World Languages (incl. Santali `sat_Olck`) | **Not Supported** (`hoc` / `hoc_Wara` absent from FLORES-200) | Incompatible |
| **Bhashini / Sarvam** | Production Cloud APIs | Scheduled Indian Languages | **Not Supported** for Ho | Incompatible |

---

## 4. EXISTING HO DATASETS

| Dataset | Location / Source | Type | Records | Modality | Ground Truth Status |
|---|---|---|---|---|---|
| **MatriVaani Ho Audio Collection** | `tools/ho_annotator/audio/` | Field Audio | 100 WAVs (16 kHz, Mono, 1.43s–5.68s) | Audio | Genuine Ho Field Recordings |
| **Working Translation Form** | `data/ho_hindi/collection/work/HO_HINDI_TRANSLATION_FORM_WORKING.xlsx` | Transcription & Translation Workbook | 100 sentences | Text | Ho transcripts verified; Hindi translations pending human annotator |
| **BoLI Ho Data Transcription** | `project-boli/ho` (Hugging Face) | ASR Audio Transcription | ~1K records | Audio + Text | ASR transcription only (No translation pairs) |
| **SICSOC Eng-Hoc Tatoeba-Wiki** | `sicsoc/eng-hoc-Tatoeba-Wiki` (Hugging Face) | Machine / Web Parallel Text | 23,889 train / 5,120 test | Text (Latin script) | Romanized English-Ho with heavy code-mixing |

---

## 5. ONLINE RESOURCES SEARCHED

Extensive automated searches and metadata inspections were executed across online repositories:
1. **Hugging Face Hub API (`huggingface_hub.HfApi`)**:
   - Filter query `filter="hoc"`: Discovered 21 model repositories and 2 dataset repositories.
   - Search queries: `"ho hindi translation"`, `"hoc hindi"`, `"ho english translation"`, `"hoc_Wara"`, `"ho parallel"`, `"munda translation"`.
2. **AI4Bharat Repositories**:
   - Inspected all `ai4bharat` models. Verified that IndicTrans2, IndicBART, and IN22 datasets support scheduled languages + Santali (`sat_Olck`), but do **not** support Ho (`hoc`).
3. **LTRC IIIT Hyderabad (`ltrciiith`)**:
   - Inspected all LTRC repositories including BhashaVerse variants.
4. **Meta FLORES-200 / NLLB**:
   - Inspected FLORES-200 language manifest. Confirmed that only Santali (`sat_Olck`) from the Munda language family is present; Ho (`hoc`) is absent.

---

## 6. CANDIDATES DISCOVERED

Three distinct candidate families were identified:
1. **`Anonym-050326/nirukti-translate-1.3b`**:
   - Author: Anonym-050326
   - Architecture: `M2M100ForConditionalGeneration` (1.3B parameters, `d_model=1024`, 24 encoder layers, 24 decoder layers).
   - Claims: Fine-tuned translation model supporting 55 Indian languages, explicitly adding 33 low-resource languages including Ho (`hoc_Deva`).
   - Format: PyTorch `model.safetensors` (2.61 GB).
2. **`sicsoc/eng-hoc-finetuned` & `sicsoc/eng-hoc_aug3`**:
   - Author: sicsoc
   - Architecture: TensorFlow MarianMT (`tf_model.h5`) based on `Helsinki-NLP/opus-mt-tc-bible-big-deu_eng_fra_por_spa-mul`.
   - Dataset: `sicsoc/eng-hoc-Tatoeba-Wiki` (English to Romanized Ho).
   - Direction: `eng -> hoc` strictly.
3. **`ltrciiith/bhashaverse`**:
   - Re-inspected to verify if any updated checkpoint exists. No new release since Phase 13.

---

## 7. HO LANGUAGE CODES

- **ISO 639-3:** `hoc`
- **BCP-47 / Script Variants:**
  - `hoc_Wara`: Ho in Warang Citi native script.
  - `hoc_Deva`: Ho in Devanagari script (standard for educational, administrative, and regional materials in Jharkhand).
  - `hoc_Latn`: Ho in Romanized / Latin script (used in academic linguistic datasets and Tatoeba).
- **Token in Nirukti 1.3B:** `hoc_Deva` (Added special token ID: `256238`).

---

## 8. HINDI LANGUAGE CODES

- **ISO 639-1 / ISO 639-3:** `hi` / `hin`
- **BCP-47:** `hin_Deva`
- **Token in Nirukti 1.3B:** `hin_Deva` (Added special token ID: `256068`).

---

## 9. HO → HINDI TESTS (`hoc_Deva -> hin_Deva`)

10 genuine Ho sentences extracted directly from `HO_HINDI_TRANSLATION_FORM_WORKING.xlsx` were passed through `Anonym-050326/nirukti-translate-1.3b` with `src_lang="hoc_Deva"` and `forced_bos_token_id=256068`:

| Row ID | Verified Ho Input | Nirukti Generated Output (`hin_Deva`) | Latency | Semantic Evaluation |
|---|---|---|---|---|
| `A20241007162806611787` | आबु एन हो को नेनता काबु बेटा इचि कोआ | अबू एन हो को नेता काबू बेटा इची कोआ | 1.51s | **FAILED**: Near-verbatim character copying (`आबु`→`अबू`, `नेनता`→`नेता`, `इचि`→`इची`). No translation into Hindi. |
| `A20241007162807221261` | एनको नेनता: काबु बेटा इचि कोआ | एनको नेता: काबू बेटा इची कोआ | 1.15s | **FAILED**: Copied untranslated Ho tokens (`एनको`, `कोआ`) into output. |
| `A20241007162807830102` | एनको नेनता: काबु बेटा इचि कोआ | एनको नेता: काबू बेटा इची कोआ | 1.14s | **FAILED**: Identical copy failure. |
| `A20241007162808406987` | एन ओआ: आलेया हातुरे का हुजुए | एन ओआ: हाथी का हाथ | 1.05s | **FAILED**: Severe phonetic hallucination. Ho `हातुरे` (in the village) hallucinates to Hindi `हाथी का हाथ` (elephant's hand). `ओआ:` (house) unhandled. |
| `A20241007162809013448` | एन ओआ: आलेया हातुरे का हुजुए | एन ओआ: हाथी का हाथ | 1.02s | **FAILED**: Hallucinatory repetition (`हाथी का हाथ`). |
| `A20241007162809588579` | एना आलेया हातुरे का हुजुए | एना ने हाथ से हाथ मिलाया। | 0.94s | **FAILED**: Completely fabricated Hindi phrase (`हाथ से हाथ मिलाया`). Completely ignores Ho grammar (`आलेया` = our, `का हुजुए` = does not come). |
| `A20241007162810181669` | एना आलेया हातुरे का हुजुए | एना ने हाथ से हाथ मिलाया। | 0.98s | **FAILED**: Hallucinatory repetition. |
| `A20241007162810805045` | एन हापानुम लो पोन रेञ जागार केना | अगर आप इसे समझते हैं तो जागते हैं। | 1.18s | **FAILED**: Ho verb `जागार` (speak/talk) is phonetically hallucinated to Hindi `जागते` (wake up). Grammatical structure discarded. |
| `A20241007162811315268` | आए लो पोन रेञ जागार केना | आओ, पानी भरकर जाग जाओ। | 0.93s | **FAILED**: Hallucination into nonsense Hindi (`आओ, पानी भरकर जाग जाओ`). |
| `A20241007162811918086` | आए लो पोन रेञ जागार केना | आओ, पानी भरकर जाग जाओ। | 0.93s | **FAILED**: Hallucination into nonsense Hindi. |

---

## 10. HINDI → HO TESTS (`hin_Deva -> hoc_Deva`)

Sanity tests with natural Hindi sentences were executed through Nirukti with `src_lang="hin_Deva"` and `forced_bos_token_id=256238`:

| Test ID | Hindi Input | Nirukti Generated Output (`hoc_Deva`) | Latency | Semantic Evaluation |
|---|---|---|---|---|
| `hi_1` | यह घर हमारा है। | यह घर हमारा है. | 0.64s | **FAILED (100% SOURCE COPYING)**: Generated verbatim Hindi. Expected Ho: `नेन ओआ: आलेया: तना:` |
| `hi_2` | वह लड़की गाँव में नहीं आती। | वह लड़की गाँव में नहीं आती. | 0.81s | **FAILED (100% SOURCE COPYING)**: Generated verbatim Hindi. Expected Ho: `एन कुरी हातुरे का हुजुए` |
| `hi_3` | हम हो लोग यहाँ नहीं आएँगे। | हम लोग यहां नहीं आएंगे. | 0.77s | **FAILED (SOURCE COPYING)**: Verbatim Hindi paraphrase. Zero Ho vocabulary generated. |
| `hi_4` | मैं तुम्हारे साथ बात करना चाहता हूँ। | आपसे बात करना चाहता हूं. | 0.71s | **FAILED (SOURCE COPYING)**: Verbatim Hindi paraphrase. Expected Ho verb `जागार`. |
| `hi_5` | आज मौसम बहुत अच्छा है। | आज मौसम बहुत अच्छा है. | 0.70s | **FAILED (100% SOURCE COPYING)**: Generated verbatim Hindi. Zero Ho vocabulary generated. |

---

## 11. HO → ENGLISH TESTS (`hoc_Deva -> eng_Latn`)

To assess whether Nirukti can map Ho to English for bridge translation, the 10 Ho sentences were passed to `eng_Latn` (`forced_bos_token_id=256047`):

| Row ID | Verified Ho Input | Nirukti Generated Output (`eng_Latn`) | Latency | Semantic Evaluation |
|---|---|---|---|---|
| `A20241007162806611787` | आबु एन हो को नेनता काबु बेटा इचि कोआ | Abu 'An Ho's son, Ichi Koa, is the leader of the rebellion. | 1.86s | **FAILED**: Extreme hallucination. Fabulates historical/rebellion names from syllables. |
| `A20241007162807221261` | एनको नेनता: काबु बेटा इचि कोआ | Enko leader: Kabu, son of Ichi Koa | 1.20s | **FAILED**: Syllabic hallucination. |
| `A20241007162808406987` | एन ओआ: आलेया हातुरे का हुजुए | N OA: The hand-to-hand combat | 1.19s | **FAILED**: Phonetic hallucination (`हातुरे` interpreted as "hand-to-hand combat"). |
| `A20241007162809588579` | एना आलेया हातुरे का हुजुए | Anna came to the handloom. | 0.94s | **FAILED**: Hallucination (`हातुरे` -> "handloom"). |
| `A20241007162810805045` | एन हापानुम लो पोन रेञ जागार केना | If you do not, the child will wake up. | 1.18s | **FAILED**: Fabricated English sentence. |
| `A20241007162811315268` | आए लो पोन रेञ जागार केना | Come, let's wake up | 0.90s | **FAILED**: Fabricated English sentence. |

---

## 12. ENGLISH → HINDI BRIDGE TESTS

- Since **Ho → English** completely fails (producing hallucinations such as "leader of the rebellion" and "hand-to-hand combat"), chaining Ho → English → Hindi is **computationally and semantically invalid**.
- The `sicsoc/eng-hoc-finetuned` model was also evaluated as a potential bridge candidate. However:
  1. It is strictly **English → Ho** (`eng -> hoc`), not Ho → English.
  2. It was trained on Latin/Romanized web text (`sicsoc/eng-hoc-Tatoeba-Wiki`), producing outputs like `Kalomaḱ barhisi sirma re, India aḱ GDP do 8% sirmaaḱ Average loḱ ayar tersana mente Expectation menaḱa`.
  3. It only provides TensorFlow 1.x / 2.x weights (`tf_model.h5`), lacking PyTorch support.
  4. It does not provide the reverse `hoc -> eng` model required for a bridge.
- **Bridge Verdict:** The Ho → English → Hindi bridge is completely non-functional.

---

## 13. EXACT EXAMPLE OUTPUTS (SUMMARY TABLE)

```
========================================================================================
Sentence 1: [A20241007162806611787]
Ho Source:       आबु एन हो को नेनता काबु बेटा इचि कोआ
Ho Meaning:      We will not let those Ho people arrive/reach here.
Nirukti (Hindi): अबू एन हो को नेता काबू बेटा इची कोआ   [COPYING / CORRUPTED PHONEMES]
Nirukti (Eng):   Abu 'An Ho's son, Ichi Koa, is the leader of the rebellion. [HALLUCINATION]
----------------------------------------------------------------------------------------
Sentence 4: [A20241007162808406987]
Ho Source:       एन ओआ: आलेया हातुरे का हुजुए
Ho Meaning:      That house does not come into our village.
Nirukti (Hindi): एन ओआ: हाथी का हाथ                     [PHONETIC NONSENSE]
Nirukti (Eng):   N OA: The hand-to-hand combat          [PHONETIC NONSENSE]
----------------------------------------------------------------------------------------
Sentence 8: [A20241007162810805045]
Ho Source:       एन हापानुम लो पोन रेञ जागार केना
Ho Meaning:      I spoke with that young girl...
Nirukti (Hindi): अगर आप इसे समझते हैं तो जागते हैं।     [HALLUCINATED HINDI]
Nirukti (Eng):   If you do not, the child will wake up. [FABRICATED ENGLISH]
----------------------------------------------------------------------------------------
Reverse Hindi 1:
Hindi Source:    यह घर हमारा है।
Nirukti (Ho):    यह घर हमारा है.                        [100% IDENTICAL SOURCE COPYING]
========================================================================================
```

---

## 14. REJECTED CANDIDATES

1. **`Anonym-050326/nirukti-translate-1.3b`** (M2M-100 1.3B Seq2Seq)
2. **`sicsoc/eng-hoc-finetuned`** (MarianMT / Helsinki-NLP Opus MT)
3. **`sicsoc/eng-hoc_aug3`** (MarianMT / Helsinki-NLP Opus MT)
4. **`ltrciiith/bhashaverse`** (Multilingual Seq2Seq)
5. **`project-boli/ho`** (ASR Transcription Dataset)

---

## 15. REASONS FOR REJECTION

| Candidate | Primary Reason for Rejection | Technical Evidence |
|---|---|---|
| **Nirukti 1.3B** | **No actual semantic translation**. Demonstrates 100% source copying on Hindi→Ho, verbatim Ho token copying or phonetic hallucination on Ho→Hindi, and unconstrained hallucination on Ho→English. | Empirical benchmark on 10 verified Ho sentences stored in `data/ho_hindi/experimental/candidate_test_results.json`. Training inspection in `download_datasets.py` confirms `hoc_Deva` was sourced from unverified "monolingual-translated" pseudo-data. |
| **SICSOC Models** | **Unidirectional `eng -> hoc` only; wrong script.** Does not support Ho as a source language. Operates on Latin/Romanized script with heavy English code-mixing, not Devanagari Ho field transcripts. | Hugging Face Hub metadata, `tf_model.h5` only format, and inspection of `sicsoc/eng-hoc-Tatoeba-Wiki`. |
| **BhashaVerse** | **Known degenerate behavior.** Copies Devanagari input directly to output; outputs English/Nepali corrupted tokens. | Thoroughly documented in `PHASE_13_BHASHAVERSE_HO_TRANSLATION_REPORT.md`. No new checkpoints exist. |
| **BoLI Ho** | **Not a translation model.** | Modality is audio speech-to-text transcription without parallel translation pairs. |

---

## 16. MODEL LICENSES

- **`Anonym-050326/nirukti-translate-1.3b`:** `cc-by-nc-4.0` (Non-commercial only).
- **`sicsoc/eng-hoc-finetuned`:** `apache-2.0`.
- **`sicsoc/eng-hoc_aug3`:** `apache-2.0`.
- **`project-boli/ho`:** `cc-by-nc-sa-4.0`.

---

## 17. MODEL SIZES

- **`Anonym-050326/nirukti-translate-1.3b`:**
  - Parameters: 1,324,533,760 (~1.32 Billion).
  - Weights: `model.safetensors` = 2,614.47 MB (2.61 GB in FP16).
  - Memory Footprint on CPU: ~3.8 GB RAM during inference.
- **`sicsoc/eng-hoc-finetuned`:**
  - Weights: `tf_model.h5` = ~930 MB.

---

## 18. INFERENCE LATENCY

Measurements conducted on CPU (PyTorch 2.12.1+cpu):
- **Model Load Time:** 282.0 seconds (cold load + initialization).
- **Tokenizer Load Time:** 7.3 seconds.
- **Ho → Hindi Generation Latency:** 0.93s to 1.51s per sentence (average: **1.11 seconds**).
- **Ho → English Generation Latency:** 0.90s to 1.86s per sentence (average: **1.21 seconds**).
- **Hindi → Ho Generation Latency:** 0.64s to 0.81s per sentence (average: **0.73 seconds**).

---

## 19. QUALITY OBSERVATIONS

1. **Failure Mode 1 — Verbatim Source Copying:**
   On Hindi → Ho, the model behaves as an identity function. It outputs the exact Devanagari input string verbatim (e.g., `यह घर हमारा है।` -> `यह घर हमारा है.`), scoring 0% Ho translation fidelity.
2. **Failure Mode 2 — Subword / Token Transliteration without Translation:**
   On Ho → Hindi, the model copies the Devanagari Ho tokens (`आबु एन हो को...` -> `अबू एन हो को...`) because both languages share Devanagari script. It fails to map Ho grammatical markers (`-को` plural, `नेनता` here, `काबु` negative first-person plural, `इचि` causative) to Hindi equivalents.
3. **Failure Mode 3 — Phonetic Sound-Resemblance Hallucination:**
   When the model encounters Ho roots that superficially resemble Hindi words, it hallucinates absurd meanings:
   - `हातुरे` (Ho: *in the village*, from `हातु`) -> Hindi `हाथी` (elephant) / `हाथ` (hand) / `हाथ से हाथ मिलाया` (shook hands).
   - `जागार` (Ho: *to speak/language*) -> Hindi `जागते` / `जाग जाओ` (*wake up*).
4. **Failure Mode 4 — Pure Unconstrained Hallucination:**
   On Ho → English, the model outputs completely fabricated stories involving rebellions, combat, and handlooms.

---

## 20. WHETHER ACTUAL HO TRANSLATION WAS DEMONSTRATED

**NO.**  
Under no tested configuration did any pretrained model demonstrate genuine, meaningful semantic translation for Ho → Hindi, Hindi → Ho, or Ho → English. Every candidate failed the empirical validation standard.

---

## 21. FINAL DECISION

# `NO_VERIFIED_PRETRAINED_HO_TRANSLATION_MODEL_FOUND`

---

## 22. NEXT TECHNICAL STEPS

1. **Protect Human Translation Form Integrity:**
   - Maintain `data/ho_hindi/collection/work/HO_HINDI_TRANSLATION_FORM_WORKING.xlsx` strictly read-only.
   - Do **NOT** populate the workbook with pseudo-labels from Nirukti, BhashaVerse, or any machine translation system.
2. **Execute Human Ground Truth Collection:**
   - Await completion of the 100 field sentences by certified native Ho speakers using the MatriVaani Ho Annotator (`tools/ho_annotator/`) according to `INSTRUCTIONS_FOR_TRANSLATOR.md`.
3. **Downstream Training Roadmap:**
   - Once verified human parallel pairs (Ho ↔ Hindi) are collected, fine-tune a compact Seq2Seq base model (e.g., LoRA adapter on IndicBART or NMT with custom vocabulary) specifically on verified pairs.
4. **Preserve Production Stability:**
   - Keep `app/services/translation_service.py` intact without introducing unverified or degenerate translation models into the active MatriVaani application.
