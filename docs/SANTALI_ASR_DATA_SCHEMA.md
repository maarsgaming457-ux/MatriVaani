# SANTALI ASR DATA SCHEMA (IndicVoices)

Based on the empirical verification of the `ai4bharat/IndicVoices` dataset (`santali` configuration), the following schema represents the actual data structure observed in the `train` and `valid` splits.

## 1. Field Documentation

### `audio_filepath` (Required)
- **Type:** `dict` (from `datasets.Audio`)
- **Structure:**
  - `path`: `str` or `None` (The virtual filename, usually `None` when streaming from parquet)
  - `bytes`: `bytes` (The raw encoded audio payload)
- **Format:** Verified as FLAC (binary signature `fLaC`).
- **Sample Rate:** Natively 16000 Hz.
- **Constraints:** The `bytes` payload must not be `None` and must be decodable by standard FLAC decoders (e.g., `soundfile`).

### `text` (Required)
- **Type:** `str`
- **Description:** The human-transcribed text corresponding to the audio.
- **Script:** Primarily Ol Chiki (Unicode U+1C50 - U+1C7F), though exact Unicode verification must be done per-sample.
- **Constraints:** Must not be empty. Must contain valid UTF-8/Unicode characters.

### `duration` (Required)
- **Type:** `float`
- **Description:** The duration of the audio sample in seconds.
- **Constraints:** This metadata duration should closely match the dynamically decoded `num_samples / sample_rate` duration.

### `lang` (Required)
- **Type:** `str`
- **Description:** The language code identifier.
- **Observed Value:** `"sat"` (Santali).

### `speaker_id` (Optional/Contextual)
- **Type:** `str` (Usually observed if speaker metadata is preserved in IndicVoices).

## 2. Pipeline Ingestion Schema

When ingested by the `MatriVaani` pipeline, the raw Hugging Face dictionary is transformed into the following normalized dictionary format before being sent to the feature extractor:

```json
{
  "waveform": "<numpy.ndarray> (mono, float32, finite)",
  "sample_rate": 16000,
  "original_text": "...",
  "normalized_text": "...",
  "duration": 5.23,
  "language": "sat",
  "script_identified": "ol_chiki",
  "decode_status": "SUCCESS"
}
```

Records that fail any of the strict validation checks (empty audio, empty text, script mismatch, etc.) are explicitly dropped by the pipeline with a logged rejection reason.
