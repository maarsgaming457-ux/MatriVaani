# Low-RAM ASR Model Candidates

Based on the failure of `facebook/mms-1b-all` (1B params, ~4.1GB Peak RAM) to meet the 2.0GB hardware constraint, we have pivoted to compact foundational architectures `< 300M` parameters. 

**Note on Santhali**: Because dedicated open-source Santhali ASR models below 300M parameters do not currently exist on non-gated repositories, Santhali support is evaluated as **ADAPTABLE** (meaning the base architecture supports tokenizer expansion and CTC/Decoder head fine-tuning).

## Candidate List

| Model | Params Size | Hindi | Santhali | License | Runtime RAM | Quantization | ONNX | Fine-tuning | Android Status |
|-------|-------------|-------|----------|---------|-------------|--------------|------|-------------|----------------|
| `openai/whisper-tiny` | 39M | YES | ADAPTABLE | MIT | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| `openai/whisper-base` | 74M | YES | ADAPTABLE | MIT | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| `facebook/wav2vec2-base-100k-voxpopuli` | 90M | ADAPTABLE | ADAPTABLE | Apache 2.0 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Selection Methodology
1. Evaluate RAM limits and baseline FP32 footprint.
2. Evaluate dynamic INT8 conversion RAM spikes (must fit within 2GB).
3. Confirm basic offline operability.
4. If successful, select the strongest base architecture for Phase 3 Santhali fine-tuning.
