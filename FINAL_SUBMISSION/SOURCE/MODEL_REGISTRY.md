# Model Registry

This registry tracks the versions, benchmarks, and performance metrics of the models used in the PALASH Language Engine.

## ASR Models
| Version | Base Model | Languages | WER | Latency (ms) | Size (MB) | RAM (MB) | Notes |
|---------|------------|-----------|-----|--------------|-----------|----------|-------|
| v0.1    | mms-300m   | hi, sat   | TBD | ~1200 (CPU)  | ~1200     | ~1800    | Baseline |

## NMT Models
| Version | Base Model | Direction | BLEU | Latency (ms) | Size (MB) | RAM (MB) | Notes |
|---------|------------|-----------|------|--------------|-----------|----------|-------|
| -       | -          | -         | -    | -            | -         | -        | -     |

## TTS
| Model | Version | Dataset | WER/CER/BLEU/chrF | RAM | Latency | Status |
|---|---|---|---|---|---|---|
| MatriVaani-ASR-Santhali-v1 | Wav2Vec2/SraVaani | None | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT READY |
| MatriVaani-NMT-HI-SAT-v1 | IndicTrans2 INT8 | None | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT READY |
| MatriVaani-TTS-Santhali-v1 | VITS | None | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT READY |

| Version | Base Model | Languages | MOS | Latency (ms) | Size (MB) | RAM (MB) | Notes |
|---------|------------|-----------|-----|--------------|-----------|----------|-------|
| v0.1 (Pending) | VITS (Pending) | sat       | INSUFFICIENT DATA | < 500 (CPU)  | ~150      | ~150     | Baseline Pending Dataset |
