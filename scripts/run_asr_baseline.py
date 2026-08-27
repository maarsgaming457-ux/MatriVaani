import os
import json
import time
import psutil
import torch
import jiwer
import numpy as np
from data_modules.santali.indicvoices_loader import IndicVoicesLoader
from transformers import AutoFeatureExtractor, AutoModelForCTC, Wav2Vec2Processor

def get_ram():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def run_baseline(max_samples=200):
    os.makedirs("evaluation/asr/santali", exist_ok=True)
    
    baseline_ram = get_ram()
    print(f"Baseline RAM: {baseline_ram:.2f} MB")
    
    model_id = "facebook/wav2vec2-base-100k-voxpopuli"
    print(f"Loading {model_id}...")
    
    # We load feature extractor and tokenizer (processor) + model
    # Wait, voxpopuli base might not have a tokenizer attached if it wasn't fine-tuned, or it might just be the base model.
    # Voxpopuli 100k is a PRETRAINED base model, NOT fine-tuned on Santali!
    # A pretrained wav2vec2 model doesn't have a CTC head initialized for text, but let's check if it has a vocab.
    # Wait! If it's `wav2vec2-base-100k-voxpopuli`, it is just the base encoder, it doesn't have `lm_head`.
    # Let me use `AutoModelForCTC`. It will probably warn about randomly initialized weights for the LM head, 
    # which is expected for a zero-shot baseline of a base model.
    
    # Actually, to get text out, we need a tokenizer. Let's see if there's a processor.
    try:
        processor = Wav2Vec2Processor.from_pretrained(model_id)
        model = AutoModelForCTC.from_pretrained(model_id)
    except Exception as e:
        print(f"Model doesn't have a processor/head attached for direct text generation. We will just use it as a CTC model.")
        print(e)
        
        # If it's purely a base model, we can't do text generation without a vocabulary!
        # The prompt says: "Use the existing candidate: facebook/wav2vec2-base-100k-voxpopuli. Do NOT fine-tune yet. First run inference..."
        # If the model has no tokenizer, it cannot produce text.
        # However, let's load it and see if we can get a character sequence out.
        # If we can't, we will log 100% WER and explain why in the error analysis.
        processor = AutoFeatureExtractor.from_pretrained(model_id)
        model = AutoModelForCTC.from_pretrained(model_id) # Randomly initializes LM head to its default vocab size
    
    model_load_ram = get_ram()
    print(f"Model Load RAM: {model_load_ram:.2f} MB")
    
    loader = IndicVoicesLoader()
    valid_stream = loader.stream_valid()
    
    results = []
    latencies = {
        "preprocessing": [],
        "inference": [],
        "total": []
    }
    
    count = 0
    peak_ram = model_load_ram
    
    for item in valid_stream:
        if count >= max_samples:
            break
            
        waveform = item["waveform"]
        sr = item["sample_rate"]
        ref_text = item["normalized_text"]
        
        t0 = time.time()
        
        # 1. Preprocessing
        if hasattr(processor, "feature_extractor"):
            fe = processor.feature_extractor
        else:
            fe = processor
            
        inputs = fe(waveform, sampling_rate=sr, return_tensors="pt")
        
        t1 = time.time()
        
        # 2. Inference
        with torch.no_grad():
            logits = model(inputs.input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            
        t2 = time.time()
        
        # 3. Decode
        if hasattr(processor, "batch_decode"):
            pred_text = processor.batch_decode(predicted_ids)[0]
        else:
            # Random string if no tokenizer
            pred_text = ""
            
        t3 = time.time()
        
        lat_prep = t1 - t0
        lat_inf = t2 - t1
        lat_total = t3 - t0
        
        latencies["preprocessing"].append(lat_prep)
        latencies["inference"].append(lat_inf)
        latencies["total"].append(lat_total)
        
        # We need something for jiwer, jiwer fails on empty reference or prediction usually.
        # If text is empty, replace with [EMPTY]
        pred_clean = pred_text if pred_text.strip() else "[EMPTY]"
        ref_clean = ref_text if ref_text.strip() else "[EMPTY]"
        
        try:
            wer = jiwer.wer(ref_clean, pred_clean)
            cer = jiwer.cer(ref_clean, pred_clean)
        except:
            wer = 1.0
            cer = 1.0
            
        results.append({
            "original_text": item["original_text"],
            "normalized_text": ref_clean,
            "predicted_text": pred_clean,
            "duration": item["duration"],
            "wer": wer,
            "cer": cer
        })
        
        peak_ram = max(peak_ram, get_ram())
        count += 1
        
        if count % 10 == 0:
            print(f"Processed {count}/{max_samples}...")
            
    final_ram = get_ram()
    
    # Calculate Latency Stats
    def get_stats(arr):
        return {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "p95": float(np.percentile(arr, 95))
        }
        
    metrics = {
        "model_id": model_id,
        "samples_tested": count,
        "average_wer": float(np.mean([r["wer"] for r in results])),
        "average_cer": float(np.mean([r["cer"] for r in results])),
        "latency_seconds": {
            "preprocessing": get_stats(latencies["preprocessing"]),
            "inference": get_stats(latencies["inference"]),
            "total": get_stats(latencies["total"])
        },
        "memory_mb": {
            "baseline": baseline_ram,
            "model_load": model_load_ram,
            "peak_during_inference": peak_ram,
            "final_after_inference": final_ram
        }
    }
    
    with open("evaluation/asr/santali/baseline_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    with open("evaluation/asr/santali/baseline_error_analysis.md", "w", encoding="utf-8") as f:
        f.write(f"# Baseline Error Analysis: {model_id}\n\n")
        f.write(f"**Average WER:** {metrics['average_wer']:.2f}\n")
        f.write(f"**Average CER:** {metrics['average_cer']:.2f}\n\n")
        f.write("## Observations\n")
        if metrics['average_wer'] >= 1.0:
            f.write("The model outputs empty or garbage predictions because it is a PRETRAINED base encoder with a randomly initialized LM head. It has zero knowledge of Ol Chiki characters, thus resulting in 100% WER/CER.\n\n")
            
        f.write("## Sample Errors\n\n")
        for i, r in enumerate(results[:20]):
            f.write(f"### Sample {i+1} (Duration: {r['duration']:.2f}s)\n")
            f.write(f"- **Reference:** {r['normalized_text']}\n")
            f.write(f"- **Predicted:** {r['predicted_text']}\n")
            f.write(f"- **WER:** {r['wer']:.2f} | **CER:** {r['cer']:.2f}\n\n")
            
    print("Baseline execution complete!")
    print(f"Average WER: {metrics['average_wer']:.2f}")
    print(f"Average CER: {metrics['average_cer']:.2f}")
    print(f"Total Mean Latency: {metrics['latency_seconds']['total']['mean']:.2f}s")
    print(f"Peak RAM: {peak_ram:.2f} MB")

if __name__ == "__main__":
    run_baseline(200)
