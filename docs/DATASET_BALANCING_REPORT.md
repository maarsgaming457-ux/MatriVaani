# Dataset Balancing Report

## Overview
Because physical data is scarce for Santhali, there is a severe risk of domain and speaker imbalance.

### 1. Speaker Imbalance (ASR/TTS)
- **Problem**: A single fluent contributor might provide 80% of the audio, causing the model to overfit to their specific voice/accent.
- **Strategy**: Implement hard sampling caps per `speaker_id` during dataloader generation (e.g., no speaker can constitute more than 15% of an epoch). 

### 2. Domain Imbalance (NMT)
- **Problem**: We might acquire 10,000 sentences of generic Wikipedia text, but only 500 sentences of Foundation Literacy & Numeracy (FLN) classroom text.
- **Strategy**: Up-sample the FLN text during training. Assign a domain weight `w_fln = 5.0` to classroom vocabulary to ensure the NMT model learns the pedagogical domain properly.

### 3. Script Imbalance
- **Problem**: Santhali exists in Ol Chiki, Devanagari, and Latin.
- **Strategy**: As established in `SANTHALI_SCRIPT_ANALYSIS.md`, we will forcefully normalize all incoming text into Ol Chiki *before* training to prevent the model's vocabulary from splitting across three scripts.

## Data Augmentation Strategy (ASR)
To artificially increase robustness without fabricating new vocabulary:
- **Speed Perturbation**: Alter audio speed by 0.9x and 1.1x.
- **Background Noise Injection**: Add generic classroom background noise (children talking, desk shuffling) at 10-15dB SNR.
- **Tracking Rule**: Augmented data will be tagged in metadata (`is_augmented: true`) and will **never** be counted towards the "total real hours" metric.
