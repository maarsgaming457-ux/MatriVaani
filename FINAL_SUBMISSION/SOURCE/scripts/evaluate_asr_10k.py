import os
import gc
import time
import json
import psutil
import torch
from transformers import AutoFeatureExtractor, Wav2Vec2ForCTC
from training.asr.santali.tokenizer import get_santali_tokenizer
import jiwer

from data_modules.santali.local_cache_loader import LocalSantaliDataset

def get_ram_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def evaluate_10k():
    print("=== PHASE 3.9: 10K MODEL EVALUATION ===")
    
    baseline_ram = get_ram_mb()
    print(f"Baseline RAM: {baseline_ram:.2f} MB")
    
    model_dir = "models/santhali_asr_v0_1_10k/checkpoint-50"
    
    # Measure loading RAM
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    
    processor_ram = get_ram_mb()
    print(f"Tokenizer/Processor RAM: {processor_ram - baseline_ram:.2f} MB")
    
    model = Wav2Vec2ForCTC.from_pretrained(model_dir)
    model.eval()
    
    model_ram = get_ram_mb()
    print(f"Model Loading RAM: {model_ram - processor_ram:.2f} MB")
    print(f"Total Loading RAM: {model_ram - baseline_ram:.2f} MB")
    
    # Load validation data
    valid_data = LocalSantaliDataset("datasets/cache/santali/metadata/validation.jsonl")
    
    refs = []
    preds = []
    latencies = []
    
    peak_inference_ram = model_ram
    
    print("Evaluating Validation Set...")
    with torch.no_grad():
        for item in valid_data:
            start_time = time.time()
            
            # Preprocessing
            inputs = feature_extractor(item["waveform"], sampling_rate=item["sample_rate"], return_tensors="pt")
            
            # Inference
            logits = model(inputs.input_values).logits
            pred_ids = torch.argmax(logits, dim=-1)
            
            # Decoding
            pred_str = tokenizer.batch_decode(pred_ids)[0]
            
            latency = time.time() - start_time
            latencies.append(latency)
            
            current_ram = get_ram_mb()
            if current_ram > peak_inference_ram:
                peak_inference_ram = current_ram
                
            refs.append(item["normalized_text"])
            preds.append(pred_str)
            
    # Metrics
    valid_refs = []
    valid_preds = []
    
    for r, p in zip(refs, preds):
        if r.strip():
            valid_refs.append(r)
            valid_preds.append(p)
            
    wer = jiwer.wer(valid_refs, valid_preds) if valid_refs else 1.0
    cer = jiwer.cer(valid_refs, valid_preds) if valid_refs else 1.0
    
    empty_count = sum(1 for p in valid_preds if not p.strip())
    empty_rate = empty_count / len(valid_preds) if valid_preds else 1.0
    
    mean_latency = sum(latencies) / len(latencies) if latencies else 0
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
    median_latency = sorted(latencies)[int(len(latencies) * 0.5)] if latencies else 0
    
    results = {
        "wer": wer,
        "cer": cer,
        "empty_rate": empty_rate,
        "mean_latency": mean_latency,
        "median_latency": median_latency,
        "p95_latency": p95_latency,
        "baseline_ram_mb": baseline_ram,
        "model_ram_mb": model_ram - processor_ram,
        "peak_inference_ram_mb": peak_inference_ram,
        "total_inference_ram_mb": peak_inference_ram - baseline_ram
    }
    
    os.makedirs("evaluation/asr/santali", exist_ok=True)
    with open("evaluation/asr/santali/10k_evaluation.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(json.dumps(results, indent=2))
    
    # Save a few examples for error analysis
    examples = []
    for i in range(10):
        examples.append({
            "ref": valid_refs[i] if i < len(valid_refs) else "",
            "pred": valid_preds[i] if i < len(valid_preds) else ""
        })
        
    with open("evaluation/asr/santali/10k_examples.json", "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    evaluate_10k()
