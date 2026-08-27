# ASR Model Decision Matrix

## Evaluated Candidates
1. OpenAI Whisper (`openai/whisper-tiny`)
2. Meta MMS (`facebook/mms-300m`)
3. AI4Bharat IndicConformer

## Weighted Decision Matrix

| Metric | Weight | Whisper | MMS | IndicConformer |
|--------|--------|---------|-----|----------------|
| **Language Suitability** | HIGH | Low (No `sat`) | **High (Native `sat`)** | Low (No `sat`) |
| **Accuracy (Hindi)** | HIGH | High | Medium | **High** |
| **Offline Feasibility** | HIGH | **High** | High | High |
| **Latency** | HIGH | Medium | **High (CTC)** | Medium |
| **RAM Requirement** | HIGH | **High (<1GB)** | Medium (~2GB) | High (~1GB) |
| **Model Size** | MEDIUM | **High (150MB)** | Low (1.2GB) | Medium |
| **Fine-Tuning** | HIGH | Medium | **High (Adapters)** | High |
| **Mobile Feasibility**| HIGH | **High (whisper.cpp)**| Medium | Medium |
| **License** | MANDATORY | **Pass (MIT)** | Pass (CC-BY-NC) | **Pass (MIT)** |

## Selected Baseline
**PALASH-ASR-Baseline-v0.1**: `facebook/mms-300m`

### Justification
The explicit constraint of PALASH is **Mother Tongue-Based Primary Education** with **Santhali** as the initial target. Whisper and IndicConformer score incredibly well on RAM, Size, and Hindi accuracy, but fundamentally fail the "Language Suitability" constraint for Santhali. We cannot pick a model purely for Hindi performance. Meta MMS is the only model with zero-shot acoustic foundations for Santhali (`sat`), meaning fine-tuning will require orders of magnitude less data than training a new tokenizer and acoustic mapping from scratch in Whisper.

### Risks
1. **RAM Limits**: `mms-300m` consumes near 2GB of RAM in PyTorch, which pushes the limit of the target low-cost Android tablet. We must prioritize ONNX/TFLite dynamic quantization in later phases.
2. **Punctuation**: CTC models lack punctuation. A subsequent LM step or simple heuristic pass is required.
3. **License Constraints**: CC-BY-NC 4.0 may prohibit for-profit resale, though it is usually perfectly viable for SIH prototypes and open-source government deployments.

### What must be tested after fine-tuning
1. Santhali WER/CER on the golden `PALASH-DATA-v0.1`.
2. ONNX dynamic quantization memory footprint on a 2GB RAM profile.
3. Real-time factor (RTF) on ARM CPUs.
