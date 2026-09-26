# Model Runtime & Conversion Strategy

The frozen production models in MatriVaani are tracked via Git LFS and execute natively in Python/PyTorch via the FastAPI backend. To achieve true Android offline functionality, they must be converted for on-device runtimes.

## Strict Rules
- **Do not modify the original model weights.**
- **Never overwrite** `backend/best_model_main2/` or `models/santhali_asr_final_5k/`.
- Converted artifacts must be stored separately from the frozen originals.

## Feasible Android Runtimes
We are actively investigating the following runtimes for MatriVaani:
- **ONNX Runtime Mobile**
- **LiteRT (formerly TFLite)**
- **ExecuTorch** (Native PyTorch edge runtime)

## Conversion Audit Requirements
For every model converted to mobile, the following metrics must be recorded in this repository:
1. Original framework (e.g., PyTorch)
2. Model architecture (e.g., IndicTrans2, Wav2Vec2)
3. Input format (text/audio shapes)
4. Output format (logits/tokens)
5. Tokenizer/preprocessing pipeline portability
6. Postprocessing requirements
7. Conversion feasibility (errors encountered)
8. Selected Android runtime
9. Mobile Model size (MB)
10. RAM requirement on Android
11. CPU latency per inference
12. Output/accuracy comparison against the original frozen model

## Packaging Investigation
Mobile models are extremely large. We must investigate:
- Bundled models (inside APK, significantly increasing size)
- Android App Bundle (AAB) install-time assets
- First-run model package downloads
- Local device storage mounting
