import os
import sys
import json
import time
import torch
import jiwer
import numpy as np

# Prevent shadowing
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from data_modules.santali.indicvoices_loader import IndicVoicesLoader
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def evaluate():
    model_path = "models/checkpoint-1500"
    progress_file = "evaluation/asr/santali/baseline_2169_progress.json"
    results_file = "evaluation/asr/santali/baseline_2169_results.json"
    
    os.makedirs(os.path.dirname(progress_file), exist_ok=True)
    
    print(f"Loading processor and model from {model_path}...")
    processor = Wav2Vec2Processor.from_pretrained(model_path)
    model = Wav2Vec2ForCTC.from_pretrained(model_path)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    loader = IndicVoicesLoader()
    print("Streaming valid dataset...")
    
    progress_data = []
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            progress_data = json.load(f)
            print(f"Resuming from {len(progress_data)} completed samples.")
    
    completed_ids = {item["sample_id"] for item in progress_data}
    
    # IndicVoices valid split should have 2169 samples for Santali
    try:
        stream = loader.stream_valid()
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    sample_idx = 0
    
    for item in stream:
        sample_id = f"valid_{sample_idx}"
        
        if sample_id in completed_ids:
            sample_idx += 1
            continue
            
        reference = item["normalized_text"]
        waveform = item["waveform"]
        sr = item["sample_rate"]
        
        start_time = time.time()
        
        try:
            inputs = processor(waveform, sampling_rate=sr, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                logits = model(**inputs).logits
                
            predicted_ids = torch.argmax(logits, dim=-1)
            prediction = processor.batch_decode(predicted_ids)[0]
            
            status = "SUCCESS"
            error_msg = ""
        except Exception as e:
            prediction = ""
            status = "FAILED"
            error_msg = str(e)
            
        inference_time = time.time() - start_time
        
        wer = 1.0
        cer = 1.0
        
        if status == "SUCCESS" and prediction:
            # simple normalization for evaluation
            ref_eval = reference.strip()
            pred_eval = prediction.strip()
            if ref_eval and pred_eval:
                try:
                    wer = jiwer.wer(ref_eval, pred_eval)
                    cer = jiwer.cer(ref_eval, pred_eval)
                except:
                    pass
                    
        res = {
            "sample_id": sample_id,
            "reference_text": reference,
            "predicted_text": prediction,
            "WER": wer,
            "CER": cer,
            "status": status,
            "error": error_msg,
            "inference_time": inference_time
        }
        
        progress_data.append(res)
        
        if sample_idx % 10 == 0:
            print(f"Processed {sample_idx+1} samples. Current WER: {wer:.4f}")
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
                
        sample_idx += 1
        
    # Final save
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
        
    print(f"Evaluation finished. Total samples processed: {len(progress_data)}")
    
    # Calculate metrics
    successful = [x for x in progress_data if x["status"] == "SUCCESS"]
    failed = [x for x in progress_data if x["status"] == "FAILED"]
    
    total_samples = len(progress_data)
    
    wers = [x["WER"] for x in successful if x["predicted_text"]]
    cers = [x["CER"] for x in successful if x["predicted_text"]]
    times = [x["inference_time"] for x in progress_data]
    
    final_wer = sum(wers)/len(wers) if wers else 1.0
    final_cer = sum(cers)/len(cers) if cers else 1.0
    avg_time = sum(times)/len(times) if times else 0
    median_time = float(np.median(times)) if times else 0
    
    report = {
        "total_samples": total_samples,
        "successful_samples": len(successful),
        "failed_samples": len(failed),
        "average_wer": final_wer,
        "average_cer": final_cer,
        "average_inference_time": avg_time,
        "median_inference_time": median_time,
        "total_evaluation_time": sum(times)
    }
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    print("Report saved to", results_file)
    print("Final WER:", final_wer)
    print("Final CER:", final_cer)

if __name__ == "__main__":
    evaluate()
