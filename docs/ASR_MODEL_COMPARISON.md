# ASR Model Comparison (Phase 2 Detailed Research)

## Candidates Evaluated

### 1. OpenAI Whisper (Tiny/Base)
1. **Model name**: `openai/whisper-tiny`
2. **Model version**: Tiny (v1)
3. **Architecture**: Transformer Encoder-Decoder
4. **Parameter count**: ~39M
5. **Supported languages**: 99+
6. **Hindi support**: Excellent, native support with punctuation and casing.
7. **Santhali support**: **NONE** (Requires massive tokenizer extension/retraining).
8. **Low-resource suitability**: Good structure, but encoder-decoder is heavy for pure acoustic modeling.
9. **Fine-tuning capability**: High (via Hugging Face PEFT/LoRA).
10. **License**: MIT
11. **Model size**: ~150 MB (Tiny)
12. **Expected RAM requirement**: ~1-1.5 GB
13. **CPU requirements**: Moderate (can run on modern mobile CPUs via whisper.cpp).
14. **GPU requirements**: Low for inference, High for training.
15. **Offline inference capability**: Yes.
16. **ONNX/TFLite/mobile feasibility**: Extremely high (whisper.cpp, TFLite supported).
17. **Quantization support**: High (int8, int4).
18. **Streaming capability**: Poor natively (designed for 30s chunks), requires chunking wrappers.
19. **Maintenance/community status**: Highly active.
20. **Python 3.14 compatibility**: Yes (via transformers).
21. **Hugging Face or official repository**: Hugging Face (`openai/whisper-tiny`).
22. **Known limitations**: Hallucinations on silence, poor streaming, zero tribal language support.

### 2. Meta MMS (Massively Multilingual Speech) `mms-300m`
1. **Model name**: `facebook/mms-300m`
2. **Model version**: 300M parameter variant
3. **Architecture**: wav2vec 2.0 (CTC)
4. **Parameter count**: ~300M
5. **Supported languages**: 1,100+
6. **Hindi support**: Good.
7. **Santhali support**: **EXPLICITLY SUPPORTED** (`sat` language code natively built-in).
8. **Low-resource suitability**: Excellent (uses efficient language-specific adapter layers).
9. **Fine-tuning capability**: High (CTC fine-tuning is lightweight).
10. **License**: CC-BY-NC 4.0
11. **Model size**: ~1.2 GB
12. **Expected RAM requirement**: ~2-2.5 GB
13. **CPU requirements**: Moderate.
14. **GPU requirements**: Low for inference, Moderate for fine-tuning.
15. **Offline inference capability**: Yes.
16. **ONNX/TFLite/mobile feasibility**: High (can be exported to TorchScript/ONNX).
17. **Quantization support**: Moderate (dynamic quantization works well).
18. **Streaming capability**: Good (CTC naturally supports streaming better than seq2seq).
19. **Maintenance/community status**: Active via fairseq/transformers.
20. **Python 3.14 compatibility**: Yes.
21. **Hugging Face or official repository**: Hugging Face (`facebook/mms-300m`).
22. **Known limitations**: CTC models emit raw text without punctuation or casing; license restricts some commercial use.

### 3. IndicConformer (AI4Bharat)
1. **Model name**: `ai4bharat/indicconformer`
2. **Model version**: v1
3. **Architecture**: Conformer / wav2vec 2.0
4. **Parameter count**: ~100M - 300M
5. **Supported languages**: 22 Indic Languages.
6. **Hindi support**: State-of-the-art.
7. **Santhali support**: **NONE**.
8. **Low-resource suitability**: Designed for Indian languages, but not tribal ones initially.
9. **Fine-tuning capability**: High.
10. **License**: MIT
11. **Model size**: ~1 GB
12. **Expected RAM requirement**: ~1.5 GB
13. **CPU requirements**: Low-Moderate.
14. **GPU requirements**: Low.
15. **Offline inference capability**: Very capable (designed for edge deployment in India).
16. **ONNX/TFLite/mobile feasibility**: High.
17. **Quantization support**: Yes.
18. **Streaming capability**: Moderate.
19. **Maintenance/community status**: Active.
20. **Python 3.14 compatibility**: Yes.
21. **Hugging Face or official repository**: Hugging Face.
22. **Known limitations**: Geared only toward scheduled languages, leaving out Santhali entirely.
