# MATRI VAANI — HO PRE-IMPLEMENTATION RESEARCH PHASE

## 1. HO ASR RESEARCH

An exhaustive search of public repositories (Hugging Face, AI4Bharat, IndicVoices, Bhashini, Common Voice, OpenSLR) reveals a severe lack of Ho (hoc) speech resources.

### Public Datasets Found
**Dataset**: project-boli/ho
- **URL**: https://huggingface.co/datasets/project-boli/ho
- **License**: CC-BY-NC-SA-4.0
- **Speakers**: 1 (Poonam Biruly)
- **Utterances**: < 1,000
- **Duration**: Estimated < 1 hour
- **Sampling rate**: 16 kHz
- **Script**: Mixed Latin/Devanagari
- **Transcript format**: JSON/Parquet tabular strings
- **Language code**: hoc
- **Quality**: Studio/Controlled
- **Human verified**: Yes
- **Suitable for ASR training**: **No** (as a standalone dataset). Sub-1-hour data is insufficient for training robust acoustic models; it can only be used as a tiny fine-tuning or evaluation subset.

**Other Repositories**:
- **Common Voice**: 0 Ho datasets.
- **AI4Bharat Shruti/IndicVoices**: 0 Ho datasets (Focuses on 22 scheduled languages, Ho is unscheduled).
- **Bhashini**: 0 Ho ASR datasets.

### Public Models Found
- **facebook/mms-1b-all**: Technically supports hoc ASR, but was trained on scraped Bible audio which often uses Odia or mismatched orthographies. Not suitable for primary education classroom vocabulary without heavy fine-tuning.

---

## 2. HO-HINDI TRANSLATION RESEARCH

Search scope: Hugging Face, OPUS, AI4Bharat (IndicCorp), Bhashini, GitHub, academic treebanks.

### Findings
- **HUMAN-GROUND-TRUTH**: **0 sentence pairs found**. There are no publicly available parallel corpora for Ho ? Hindi or Ho ? English.
- **RESOURCE-SUPPORTED**: Some linguistic dictionaries/lexicons exist (e.g., CIIL grammar books in PDF format), but these are isolated words and grammar rules, not parallel sentences.
- **SYNTHETIC / AI-GENERATED**: None found publicly. Existing project relies on local Groq LLM + RAG, which is unverified.
- **UNVERIFIED**: A few GitHub repos scrape generic tribal dictionaries, but none provide aligned sentence data suitable for NMT training.

**Verdict**: We possess **0** publicly available parallel sentences for training a translation model.

---

## 3. HO TTS RESEARCH

Search scope: Hugging Face, AI4Bharat (IndicTTS), Bhashini, Multilingual TTS.

### Findings
- **Datasets**: 0 public Ho TTS datasets found.
- **Models**:
  - **facebook/mms-tts-hoc**: 
    - *Actual Ho Support*: Technical audio generation works.
    - *Script*: **Odia only**.
    - *Compatibility*: **INCOMPATIBLE**. It completely fails to tokenize or process Latin or Devanagari Ho text (the standard for the Jharkhand PALASH program). It drops characters silently, producing garbage audio.
- **AI4Bharat/IndicTTS**: Supports 13+ languages, but **not Ho**.

---

## 4. MODEL CANDIDATES

### Ho ASR
- **Candidate 1: facebook/wav2vec2-large-xlsr-53**
  - Actual Ho support: None out-of-the-box.
  - Tokenizer: CTC character-level (must be built from our dataset).
  - Script: Agnostic (depends on our fine-tuning).
  - Parameter count: 317M.
  - License: Apache 2.0.
  - Fine-tuning requirements: 50+ hours of data.
  - Colab feasibility: Yes (A100).
  - Status: **FINE-TUNING REQUIRED**.
- **Candidate 2: openai/whisper-small**
  - Actual Ho support: None. Byte-level fallback required.
  - Parameter count: 244M.
  - License: MIT.
  - Status: **FINE-TUNING REQUIRED**.

### Hindi ? Ho / Ho ? Hindi NMT
- **Candidate 1: ai4bharat/indictrans2-indic-indic-dist-320M**
  - Architecture: Transformer Seq2Seq.
  - Languages: 22 Indic languages (No Ho).
  - Tokenizer: IndicTransTokenizer (needs vocabulary extension for Ho).
  - Script: Devanagari/Latin.
  - Minimum parallel data: 50,000 pairs.
  - Latency: ~500ms - 1s locally.
  - License: MIT.
  - Status: **FINE-TUNING REQUIRED**.
- **Candidate 2: facebook/nllb-200-distilled-600M**
  - Status: **FINE-TUNING REQUIRED**.

### Ho TTS
- **Candidate 1: VITS (Conditional Variational Autoencoder with Adversarial Learning)**
  - Architecture: End-to-end TTS.
  - Script: Requires custom grapheme-to-phoneme (G2P) mapping for Ho.
  - Training requirements: 5-10 hours of single-speaker clean audio.
  - Colab feasibility: Yes (takes ~24-48 hours on A100).
  - Status: **TRAINING REQUIRED**.

---

## 5. DATA GAP ANALYSIS

| TASK | DATA WE HAVE | DATA AVAILABLE PUBLICLY | DATA MISSING | TARGET DATASET SIZE |
| :--- | :--- | :--- | :--- | :--- |
| **Ho ASR** | 0 hours | < 1 hour (project-boli/ho) | ~49 hours | 50 hours |
| **Hindi?Ho** | Lexicons / Rules | 0 sentence pairs | 50,000 pairs | 50,000 sentence pairs |
| **Ho?Hindi** | Lexicons / Rules | 0 sentence pairs | 50,000 pairs | 50,000 sentence pairs |
| **Ho TTS** | 0 hours | 0 hours (in correct script) | 5-10 hours | 5-10 hours |

---

## 6. RECOMMENDED DATA STRATEGY

### Ho ASR
- **SUPPLEMENT** project-boli/ho.
- **Collect New Data**: We must crowdsource ~50 hours of spoken Ho from native speakers, specifically targeting primary education vocabulary.

### Translation (NMT)
- **Collect New Data**: We must translate primary education textbooks (Hindi ? Ho).
- **Synthetic Generation**: We can use the existing Ho Lexicon and grammar rules to programmatically generate template-based synthetic sentences (e.g., "[Subject] [Noun] [Verb]").
- **Human Verification**: ALL synthetically generated sentence pairs MUST be verified by native linguists before being added to the training corpus. No unchecked AI generation.

### Ho TTS
- **Collect New Data**: We must conduct a professional, 10-hour studio recording of a single female native speaker reading verified Devanagari/Latin Ho text to create a pristine TTS dataset.

---

## 7. GOOGLE COLAB FEASIBILITY

### ASR Fine-Tuning (Wav2Vec2)
- **GPU**: A100 (40GB) or L4.
- **RAM**: 32GB+.
- **Disk**: 100GB (for audio wav files and cache).
- **Training Time**: 10-15 hours for 50h dataset.
- **Checkpoint Size**: ~1.2 GB.

### NMT Fine-Tuning (IndicTrans2)
- **GPU**: L4 (24GB) or A100.
- **RAM**: 16GB.
- **Training Time**: 4-8 hours for 50k pairs.
- **Checkpoint Size**: ~1.2 GB.

### TTS Training (VITS)
- **GPU**: A100 (40GB) - Highly recommended for TTS.
- **RAM**: 32GB.
- **Training Time**: 24-48 hours (TTS requires many epochs for audio fidelity).
- **Checkpoint Size**: ~200 MB.

---

## 8. FINAL DECISION

- **HO ASR**: RETRAIN
- **Hindi?Ho**: REBUILD
- **Ho?Hindi**: REBUILD
- **Ho TTS**: TRAIN
- **project-boli/ho**: SUPPLEMENT
