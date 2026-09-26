# HO-NMT-TRAIN-2 — BYT5 COLAB GPU EXPERIMENT RESULTS

## 1. Hardware
- **GPU Model:** `[To be populated after Colab run]`
- **GPU VRAM:** `[To be populated after Colab run]`

## 2. Software Versions
- **PyTorch:** `[To be populated]`
- **Transformers:** `[To be populated]`
- **Datasets:** `[To be populated]`

## 3. Dataset
The verified MatriVaani direct Hindi ↔ Ho dataset.

## 4. Unique Parallel Pairs
- **330** total unique verified pairs.

## 5. Directional Training Examples
- **346** effective directional pairs for training.

## 6. Train/Validation/Test Counts
- **Train:** 173 pairs (346 directional examples)
- **Validation:** 46 pairs (92 directional examples)
- **Test:** 111 pairs (222 directional examples)

## 7. Leakage Verification
- Exact pair duplication: **0**
- Source/Target crossover: **0**
- Normalized pair leakage: **0**

## 8. Warang Citi Distribution
- **Train:** 39 Warang Citi / 134 Latin Ho
- **Validation:** 6 Warang Citi / 40 Latin Ho
- **Test:** 14 Warang Citi / 97 Latin Ho

## 9. Training Configuration
See `training_config.json` for exact dumped values.
- **Model:** `google/byt5-small`
- **Optimizer:** `AdamW`
- **Learning Rate:** `2e-5`
- **Epochs:** `30` (maximum)
- **Early Stopping:** `Enabled (Patience 3)`
- **Weight Decay:** `0.01`
- **Warmup Ratio:** `0.05`
- **Seed:** `42`

## 10. Training Duration
- `[To be populated after Colab run]`

## 11. Training Loss
- `[To be populated after Colab run]`

## 12. Validation Loss
- `[To be populated after Colab run]`

## 13. Best Epoch
- `[To be populated after Colab run]`

---

## 14. Hindi → Ho BLEU
- **BLEU:** `[To be populated]`

## 15. Hindi → Ho chrF
- **chrF:** `[To be populated]`

## 16. Hindi → Ho Exact Match
- **Exact Match %:** `[To be populated]`

## 17. Ho → Hindi BLEU
- **BLEU:** `[To be populated]`

## 18. Ho → Hindi chrF
- **chrF:** `[To be populated]`

## 19. Ho → Hindi Exact Match
- **Exact Match %:** `[To be populated]`

---

## 20. Warang Citi-Specific Results
- **Non-empty prediction:** `[To be populated]`
- **Warang Citi character preservation:** `[To be populated]`
- **Replacement-character rate:** `[To be populated]`
- **Punctuation-only outputs:** `[To be populated]`
- **Hindi-copy outputs:** `[To be populated]`
- **Latin-only outputs:** `[To be populated]`

## 21. Latin Ho-Specific Results
- `[To be populated]`

---

## 22. Qualitative Examples
*Please extract 20 Hindi→Ho and 20 Ho→Hindi examples from predictions_*.jsonl*

### Hindi → Ho
`[Examples]`

### Ho → Hindi
`[Examples]`

## 23. Failure Patterns
- `[To be populated based on observation: e.g., Hallucinations, Script-switching, Repetition]`

## 24. Overfitting Observations
- `[To be populated based on train vs validation loss curves]`

## 25. Checkpoint Path
- `ho_nmt_models/byt5_small_hindi_ho_v1/`

## 26. Exact Files Created
- `train_byt5_colab.py`
- `HO-NMT-TRAIN-2-COLAB.ipynb`
- `training_config.json` (generated during run)
- `metrics.json` (generated during run)
- `predictions_hindi_to_ho.jsonl` (generated during run)
- `predictions_ho_to_hindi.jsonl` (generated during run)
- `HO-NMT-TRAIN-2-BYT5-COLAB-RESULTS.md`
