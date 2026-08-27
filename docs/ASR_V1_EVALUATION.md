# MatriVaani-ASR-Santhali-v1 Evaluation

## Dataset Strategy
- **Quality Gate Status**: `BLOCKED_NO_DATA`

## Model Selection
Wav2Vec2 / SraVaani architecture selected for balancing Santhali performance and `< 2 GB` RAM footprint constraint.

## Fine-Tuning Execution
- **Status**: TRAINING BLOCKED. 
- **Reason**: The dataset validation gate detected zero physical audio files in `datasets/asr/raw`. Per strict project instructions, we will not fabricate data or synthesize artificial checkpoints. 

## Evaluation Metrics
- **WER**: NOT MEASURED
- **CER**: NOT MEASURED
- **Speaker-Wise WER**: NOT MEASURED
- **Vocabulary Accuracy**: NOT MEASURED
- **Inference RAM**: NOT MEASURED
- **Latency (Cold)**: NOT MEASURED
- **Latency (Warm)**: NOT MEASURED

Because training is blocked, the model cannot be evaluated.
