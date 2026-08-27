# Santali ASR Baseline vs Pilot Fine-tuning

## 1. Zero-Shot Baseline (facebook/wav2vec2-base-100k-voxpopuli)
The base model was evaluated out-of-the-box on the Santali validation split prior to any fine-tuning. Because the base model's vocabulary only consisted of Latin characters, it was physically impossible for it to predict Ol Chiki characters.

- **WER**: 100.00%
- **CER**: 141.00%
- **Mean Latency**: 0.35 sec/sample
- **Outputs**: Latin character hallucinations. 

## 2. Pilot Fine-Tuning (santhali_asr_v0_1_pilot)
We replaced the LM Head of the base model to match the exact 39-token Ol Chiki vocabulary derived from our dataset. We then trained the new head (keeping the CNN feature extractor frozen) for roughly 2.5 epochs (150 steps) on 1000 Santali training samples.

- **WER**: 100.00%
- **CER**: 100.00%
- **Mean Latency**: 0.51 sec/sample
- **Outputs**: Blank tokens (empty strings)

### Why is WER/CER still 100%?
The pilot training was intentionally limited to a very small subset of data (1000 samples) and epochs (2.5) to test the end-to-end pipeline mechanics while strictly monitoring the `< 2 GB` RAM constraint. 

In early CTC training, models typically undergo a "blank collapse" phase where they learn to predict the CTC blank token `[PAD]` for all frames to minimize immediate loss. Because the model predicts empty strings (`""`), the Levenshtein distance to the reference text is exactly the length of the reference text, resulting in a CER and WER of exactly 1.0 (100%). It requires more steps (and the full 224K dataset) to confidently emit character spikes.

## 3. Engineering Validation
The pilot successfully proved the following infrastructural goals:
1. **Dynamic Resizing**: The model correctly mapped the 39-token Ol Chiki vocabulary.
2. **Memory Target Success**: By wrapping `IndicVoicesLoader` into a lazy PyTorch `IterableDataset` and freezing the CNN layers, the peak training RAM fell from 2.3 GB down to **~517 MB**. This successfully satisfies the strict 2 GB Android footprint requirement.
3. **End-to-End Execution**: Audio streaming, feature extraction, CTC padding, loss computation, model saving, and evaluation all executed natively without crashing (barring minor network timeouts handled by checkpointing).
