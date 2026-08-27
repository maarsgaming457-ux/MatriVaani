# TTS Final Decision

## Selected Model: VITS
Due to Android latency and RAM limits, transformer-based TTS models like Parler-TTS (>800MB) are rejected. VITS (~150MB) is officially selected as the baseline TTS architecture. 

## Dataset Needs
VITS requires exactly 22050Hz Mono PCM WAV files aligned perfectly to Santhali transcripts normalized with our Ol Chiki text_normalizer.

## Baseline Metrics
- **RAM**: ~150 MB
- **Latency (Time-to-First-Audio)**: NOT MEASURED.
- **Naturalness (MOS)**: NOT MEASURED.

With this decision documented, Phase 6 is marked as **Complete** pending dataset availability.
