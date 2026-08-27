# Santhali TTS Dataset Specification

## 1. Identified Dataset Candidates

1. **Mozilla Common Voice (sat)**
   - **Source**: `mozilla/common_voice_17_0` (or later)
   - **License**: CC0 (Public Domain)
   - **Script**: Ol Chiki
   - **Status**: AVAILABLE (Requires HF token for gated programmatic access, but openly available on the web).

2. **Rasa (AI4Bharat)**
   - **Source**: `ai4bharat/Rasa`
   - **License**: Gated / Research
   - **Script**: Ol Chiki
   - **Status**: ACCESS UNAVAILABLE (Without verified token).

3. **Nirantar & Vaani**
   - **Source**: Hugging Face / ARTPARK
   - **License**: Gated / Custom
   - **Script**: Ol Chiki / Mixed
   - **Status**: ACCESS UNAVAILABLE.

## 2. TTS Training Data Requirements
The chosen architecture (VITS) requires a dataset comprising:
- A directory of `.wav` files.
- A `metadata.csv` (or `.txt`) file containing `audio_id|transcript|speaker_id`.
- **Sample Rate**: 22050 Hz (Standard for VITS/HiFi-GAN).
- **Format**: Mono 16-bit PCM WAV.

## 3. MatriVaani Dataset Pipeline
- **Raw Files**: Placed manually into `datasets/tts/raw/<dataset_name>/`.
- **Normalization**: Downsampled to 22050Hz Mono using `librosa` or `ffmpeg`. Text normalized via `ai/tts/text_normalizer.py`.
- **Splits**: `datasets/tts/splits/` containing `train.txt` and `val.txt`.

## 4. Current Availability
**INSUFFICIENT DATA**. No physical `.wav` files currently exist in the MatriVaani environment. Training scripts will gracefully report missing data.
