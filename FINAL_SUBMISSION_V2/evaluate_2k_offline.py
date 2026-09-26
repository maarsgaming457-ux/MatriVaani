import os
import time
import json
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

print("Loading processor...")
processor = Wav2Vec2Processor.from_pretrained("models/checkpoint-1500")
print("Loading model...")
model = Wav2Vec2ForCTC.from_pretrained("models/checkpoint-1500")
print("Moving to device...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print("Model ready!")

import jiwer
import io
import soundfile as sf
import numpy as np
import pandas as pd
import sys
sys.path = [p for p in sys.path if p != '']
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

parquet_path = "datasets/cache/santali/valid.parquet"
results_file = "evaluation/asr/santali/baseline_2169_results.json"
os.makedirs(os.path.dirname(results_file), exist_ok=True)

print("Loading pandas dataframe...")
df = pd.read_parquet(parquet_path)
print(f"Loaded {len(df)} rows.")

loader = IndicVoicesLoader()
results = []
valid_count = 0

print("Starting evaluation loop...")
for idx, row in df.iterrows():
    if valid_count >= 2169:
        break
        
    item = row.to_dict()
    if pd.isna(item.get("duration")):
        item["duration"] = 0.0
        
    processed = loader._process_record(item)
    if processed is None:
        continue
        
    valid_count += 1
    sample_id = f"valid_{idx}"
    reference = processed["normalized_text"]
    
    start_time = time.time()
    
    try:
        waveform = processed["waveform"]
        sr = processed["sample_rate"]
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
        ref_eval = reference.strip()
        pred_eval = prediction.strip()
        if ref_eval and pred_eval:
            try:
                wer = jiwer.wer(ref_eval, pred_eval)
                cer = jiwer.cer(ref_eval, pred_eval)
            except:
                pass
                
    results.append({
        "sample_id": sample_id,
        "reference_text": reference,
        "predicted_text": prediction,
        "WER": wer,
        "CER": cer,
        "status": status,
        "error": error_msg,
        "inference_time": inference_time
    })
    
    if valid_count % 50 == 0:
        print(f"Evaluated {valid_count}/2169...")
        with open("evaluation/asr/santali/baseline_2169_progress.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
print(f"Evaluation finished. Total samples processed: {len(results)}")

successful = [x for x in results if x["status"] == "SUCCESS"]
failed = [x for x in results if x["status"] == "FAILED"]

wers = [x["WER"] for x in successful if x["predicted_text"]]
cers = [x["CER"] for x in successful if x["predicted_text"]]
times = [x["inference_time"] for x in results]

final_wer = sum(wers)/len(wers) if wers else 1.0
final_cer = sum(cers)/len(cers) if cers else 1.0
avg_time = sum(times)/len(times) if times else 0
median_time = float(np.median(times)) if times else 0

report = {
    "total_samples": len(results),
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
    
pred_file = "evaluation/asr/santali/baseline_2169_predictions.json"
with open(pred_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
    
print("Report saved to", results_file)
print("Final WER:", final_wer)
print("Final CER:", final_cer)

