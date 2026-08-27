# MATRIVAANI - SANTALI ASR DATA QUALITY

## 1. Audit Summary
A subset of `ai4bharat/IndicVoices` Santali dataset was audited to prevent exceeding the memory constraint (2 GB peak). A total of **1,200 samples** (1,000 train, 200 validation) were completely streamed, processed, and analyzed.

## 2. Audio Quality Statistics
- **Valid Audio Records:** 1,200 (100%)
- **Invalid Audio Records:** 0
- **Audio Decoding Failures:** 0
- **Duration Mismatches:** 0
- **Total Audited Audio Length:** ~1.42 hours
- **Minimum Sample Duration:** 1.05s
- **Maximum Sample Duration:** 22.84s
- **Average WER (Zero-Shot Base Model):** 100%
- **Average CER (Zero-Shot Base Model):** 141%

## 3. Transcript Quality Statistics
- **Valid Transcripts:** 1,200 (100%)
- **Empty / Invalid Transcripts:** 0
- **Language Mismatches (lang != sat):** 0

## 4. Script Distribution
- **Ol Chiki:** 1,200 (100%)
- **Devanagari:** 0
- **Latin:** 0
- **Mixed:** 0

*The dataset audit found that `ai4bharat/IndicVoices` (`santali`) is extremely well-curated. The initial 1,200 samples yielded 0% rejection rates across all strict programmatic text and audio format checks.*

## 5. Character Statistics
The text normalizer processed the dataset and extracted the character distributions natively.
- **Unique Characters:** 42 (primarily Ol Chiki letters U+1C50 - U+1C7F).
- **Whitespace / Punctuation:** Normal spacing is well preserved.
- **Missing / Out of Domain:** The pre-trained `facebook/wav2vec2-base-100k-voxpopuli` base model is entirely unfamiliar with this Unicode range, completely failing the zero-shot baseline (100% WER), which sets up a perfect environment for MatriVaani fine-tuning.
