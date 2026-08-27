import os
import torch
import jiwer
import numpy as np
import time
from transformers import AutoFeatureExtractor, Wav2Vec2ForCTC
from training.asr.santali.tokenizer import get_santali_tokenizer
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_evaluation():
    model_dir = "models/santhali_asr_v0_1_pilot/checkpoint-150"
    if not os.path.exists(model_dir):
        print(f"Error: {model_dir} not found.")
        return
        
    print(f"Loading model from {model_dir}")
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    model = Wav2Vec2ForCTC.from_pretrained(model_dir)
    model.eval()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    loader = IndicVoicesLoader()
    print("Evaluating on 200 validation samples...")
    
    valid_stream = loader.stream_valid()
    
    predictions = []
    references = []
    
    start_time = time.time()
    count = 0
    
    for item in valid_stream:
        if count >= 200:
            break
            
        waveform = item["waveform"]
        sample_rate = item["sample_rate"]
        ref_text = item["normalized_text"]
        
        # Audio
        inputs = feature_extractor(waveform, sampling_rate=sample_rate, return_tensors="pt")
        input_values = inputs.input_values.to(device)
        
        with torch.no_grad():
            logits = model(input_values).logits
            
        pred_ids = torch.argmax(logits, dim=-1)
        pred_text = tokenizer.batch_decode(pred_ids)[0]
        
        # Only evaluate if reference is not empty
        if ref_text.strip():
            predictions.append(pred_text)
            references.append(ref_text)
            
        count += 1
        if count % 20 == 0:
            print(f"Processed {count}/200...")
            
    end_time = time.time()
    
    if len(references) == 0:
        print("No valid references found.")
        return
        
    wer = jiwer.wer(references, predictions)
    cer = jiwer.cer(references, predictions)
    latency = (end_time - start_time) / count
    
    print("\n=== EVALUATION RESULTS ===")
    print(f"Samples: {len(references)}")
    print(f"WER: {wer * 100:.2f}%")
    print(f"CER: {cer * 100:.2f}%")
    print(f"Mean Latency: {latency:.4f} sec/sample")
    
    # Save to json
    import json
    results = {
        "samples": len(references),
        "wer": wer,
        "cer": cer,
        "latency_sec_per_sample": latency
    }
    
    os.makedirs("evaluation/asr/santali", exist_ok=True)
    with open("evaluation/asr/santali/pilot_metrics.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nSaved metrics to evaluation/asr/santali/pilot_metrics.json")
    
    # Print a few examples
    print("\n=== EXAMPLES ===")
    for i in range(min(5, len(references))):
        print(f"Ref : {references[i]}")
        print(f"Pred: {predictions[i]}")
        print("-" * 30)

if __name__ == "__main__":
    run_evaluation()
