# Phase 1: 2,169-Sample Santali ASR Baseline Evaluation

## 1. Previous Work Found
We performed an extensive audit of the existing `models/` directory and Google Drive/Colab artifacts.

- **2K Model (`checkpoint-1500`)**
  - TRAINED? YES
  - CHECKPOINT EXISTS? YES (`models/checkpoint-1500`)
  - LOADABLE? YES
  - EVALUATED? YES (currently running)

- **5K Model**
  - TRAINED? NO (No valid 5K checkpoint exists locally or in Colab artifacts)
  - CHECKPOINT EXISTS? NO
  - LOADABLE? NO
  - EVALUATED? NO

- **7K Model**
  - TRAINED? NO
  - CHECKPOINT EXISTS? NO
  - LOADABLE? NO
  - EVALUATED? NO

- **Other Checkpoints**
  - `santhali_asr_final` (377MB, missing full optimizer states but loadable for inference)
  - Various recovery checkpoints (`santhali_asr_v0_1_recovery_a`, `_b`, `_c`) and a 10K test (`santhali_asr_v0_1_10k/checkpoint-50`).

## 2. Evaluation Process
- **Dataset**: `ai4bharat/IndicVoices` Santali validation split.
- **Methodology**: The dataset was downloaded locally via parquet to bypass HuggingFace streaming/DNS hangs on Windows. We then dumped the filtered 2,169 raw audio samples to a `.pkl` file to avoid severe Windows OpenMP/MKL deadlocks caused by concurrent `pandas`, `soundfile`, and PyTorch imports.
- **Evaluation Script**: A pure PyTorch evaluation script (`pure_eval.py`) is now iterating over all 2,169 samples sequentially.
- **Resumed or Restarted**: Restarted safely from the beginning, as no existing `progress.json` with recoverable progress was found.
- **Status**: **RUNNING** (~1.5s per sample on CPU, estimated total time: ~55 minutes).

## 3. Results (2K Baseline)
- **Total Samples**: 2,169
- **Successful Samples**: [EVALUATING...]
- **Failed Samples**: [EVALUATING...]
- **Final WER**: [EVALUATING...]
- **Final CER**: [EVALUATING...]
- **Average Inference Latency**: [EVALUATING...]
- **Median Inference Latency**: [EVALUATING...]

## 4. Files Generated / Changed
- `dump_dataset.py` & `valid_2169.pkl` (Safely dumped the dataset offline)
- `pure_eval.py` (Stable evaluation script)
- `evaluation/asr/santali/baseline_2169_results.json` (Pending)
- `evaluation/asr/santali/baseline_2169_predictions.json` (Pending)
- `PHASE_1_BASELINE_REPORT.md` (This report)
