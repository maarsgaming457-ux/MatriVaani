import time
import json
import torch
import jiwer
import io
import soundfile as sf
import numpy as np
import pickle
import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from multiprocessing import freeze_support

def main():
    print("Loading processor and model...")
    processor = Wav2Vec2Processor.from_pretrained("models/santhali_asr_final_5k")
    model = Wav2Vec2ForCTC.from_pretrained("models/santhali_asr_final_5k")
    print("Moving to device...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    print("Loading data...")
    with open("valid_2169.pkl", "rb") as f:
        data = pickle.load(f)

    results = []
    print("Evaluating...")
    for i, item in enumerate(data):
        start_time = time.time()
        sample_id = item["sample_id"]
        reference = item["reference_text"]
        
        try:
            audio_bytes = item["audio_bytes"]
            with io.BytesIO(audio_bytes) as f:
                waveform, sr = sf.read(f)
            
            # Ensure mono float32
            if len(waveform.shape) > 1:
                waveform = waveform.mean(axis=1)
            waveform = waveform.astype(np.float32)
            
            if sr != 16000:
                raise ValueError("Expected 16kHz audio")
                
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
        
        if (i+1) % 50 == 0:
            print(f"Evaluated {i+1}/2169...")

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

    os.makedirs("evaluation/asr/santali", exist_ok=True)
    with open("evaluation/asr/santali/5k_2169_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    with open("evaluation/asr/santali/5k_2169_predictions.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("Final WER:", final_wer)
    print("Final CER:", final_cer)

if __name__ == '__main__':
    freeze_support()
    main()

