import os
import torch
import torch.nn.functional as F
import json
from transformers import AutoFeatureExtractor, Wav2Vec2ForCTC
from training.asr.santali.tokenizer import get_santali_tokenizer
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_diagnostics():
    model_dir = "models/santhali_asr_v0_1_pilot/checkpoint-150"
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    model = Wav2Vec2ForCTC.from_pretrained(model_dir)
    model.eval()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    loader = IndicVoicesLoader()
    valid_stream = loader.stream_valid()
    
    # Just take 1 sample
    item = next(valid_stream)
    waveform = item["waveform"]
    sample_rate = item["sample_rate"]
    ref_text = item["normalized_text"]
    
    inputs = feature_extractor(waveform, sampling_rate=sample_rate, return_tensors="pt")
    input_values = inputs.input_values.to(device)
    
    with torch.no_grad():
        logits = model(input_values).logits
        
    probs = F.softmax(logits, dim=-1) # shape: (1, seq_len, vocab_size)
    probs = probs[0] # (seq_len, vocab_size)
    
    blank_idx = tokenizer.pad_token_id
    
    blank_probs = probs[:, blank_idx].tolist()
    non_blank_probs = (1.0 - probs[:, blank_idx]).tolist()
    
    max_tokens = torch.argmax(probs, dim=-1)
    
    unique_tokens, counts = torch.unique(max_tokens, return_counts=True)
    dominant_tokens = dict(zip(unique_tokens.tolist(), counts.tolist()))
    
    # Calculate entropy
    entropy = -(probs * torch.log(probs + 1e-9)).sum(dim=-1).mean().item()
    
    results = {
        "sequence_length": probs.shape[0],
        "vocab_size": probs.shape[1],
        "mean_blank_probability": sum(blank_probs) / len(blank_probs),
        "mean_non_blank_probability": sum(non_blank_probs) / len(non_blank_probs),
        "mean_entropy": entropy,
        "dominant_tokens_counts": dominant_tokens,
        "max_token_ids": max_tokens.tolist(),
        "reference_text": ref_text,
        "reference_length": len(ref_text)
    }
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_diagnostics()
