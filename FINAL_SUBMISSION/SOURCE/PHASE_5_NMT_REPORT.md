# PHASE 5 NMT REPORT

## 1. MatriVaani Architecture
MatriVaani handles speech-to-text (ASR), translation (NMT), and text-to-speech (TTS). Phase 5 focuses specifically on establishing the Hindi->Santhali NMT baseline using `IndicTrans2` (1.1B parameters). Due to Android RAM limitations, distillation and sequential model loading will be utilized in deployment.

## 2. Data Sources
None. No `.csv` or `.jsonl` files were present in the `datasets/nmt/raw` directory at the time of execution.

## 3. Dataset Audit
`nmt_dataset_audit.py` successfully executed and produced `evaluation/accuracy/nmt/dataset_audit.json` with the status: **INSUFFICIENT DATA**.

## 4. Dataset Version
`MATRI-NMT-HI-SAT-v0.1` (Schema created, content empty).

## 5. Language Pair
Hindi (hi) -> Santhali (sat)

## 6. Script
Target: Ol Chiki (`sat_Olck`)

## 7. Training Pairs
0 (Insufficient Data)

## 8. Validation Pairs
0 (Insufficient Data)

## 9. GOLD Test Pairs
0 (Insufficient Data)

## 10. IndicTrans2 Baseline
`evaluator.py` executed, but failed gracefully due to the absence of the GOLD test set.

## 11. Baseline BLEU
NOT MEASURED

## 12. Baseline chrF
NOT MEASURED

## 13. Fine-Tuned BLEU
NOT MEASURED

## 14. Fine-Tuned chrF
NOT MEASURED

## 15. Human Evaluation
NOT MEASURED

## 16. RAM
NOT MEASURED (IndicTrans2 theoretical INT8 footprint: ~1.5 GB).

## 17. Latency
NOT MEASURED

## 18. Error Analysis
No NMT evaluation has occurred, so `docs/NMT_ERROR_ANALYSIS.md` contains 0 entries.

## 19. Educational-Domain Performance
NOT MEASURED

## 20. Limitations
The entire fine-tuning and evaluation stack is strictly **blocked** by the lack of verified human parallel data.

## 21. Deployment Feasibility
As currently architected (1.1B parameters), it is **infeasible** to run IndicTrans2 simultaneously with ASR on a 2GB Android device. It requires sequential lifecycle loading, which harms latency.

## 22. Distillation Recommendation
Highly recommended. Once data is acquired and the teacher model fine-tuned, a ~300M parameter student model should be distilled to restore real-time voice-to-voice functionality.

## 23. Phase 6 Recommendation
Proceed to Phase 6 (TTS Development) while data collection operations are carried out by human educators in the background. NMT fine-tuning can be resumed asynchronously when data arrives.
