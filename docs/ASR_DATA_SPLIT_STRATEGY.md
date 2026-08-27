# ASR Data Split Strategy

## Principle: Strict Speaker Disjointness
When MatriVaani eventually acquires physical audio (e.g., from Common Voice or IndicVoices), the training, validation, and test splits **must** be entirely speaker-disjoint. 

### Why?
Santhali dataset sizes are small. If a speaker's utterances are randomly split across the train and test sets, the ASR model will overfit to that individual's specific acoustic characteristics rather than generalizing to the Santhali language. This creates "Speaker Leakage" and artificially inflates the WER performance on the test set.

### Execution Policy
1. **Metadata Hashing**: Extract the `speaker_id` (or client ID) for every utterance.
2. **Speaker-Level Grouping**: Group all utterances by `speaker_id`.
3. **Partitioning**: 
    - 80% of unique speakers assigned exclusively to `train`.
    - 10% of unique speakers assigned exclusively to `validation`.
    - 10% of unique speakers assigned exclusively to `test`.
4. **Leakage Check**: The dataset pipeline must assert that `intersection(train_speakers, test_speakers) == 0`.
