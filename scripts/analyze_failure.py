import os
import json
import torch
import jiwer
import numpy as np
from transformers import AutoFeatureExtractor, Wav2Vec2ForCTC
from training.asr.santali.tokenizer import get_santali_tokenizer
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_analysis():
    model_dir = "models/santhali_asr_v0_1_pilot/checkpoint-150"
    
    print("Loading model and tokenizer...")
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    model = Wav2Vec2ForCTC.from_pretrained(model_dir)
    model.eval()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    loader = IndicVoicesLoader()
    valid_stream = loader.stream_valid()
    
    results = []
    predictions = []
    references = []
    empty_count = 0
    
    count = 0
    print("Running inference on 20 validation samples...")
    for item in valid_stream:
        if count >= 20:
            break
            
        waveform = item["waveform"]
        sample_rate = item["sample_rate"]
        ref_text = item["normalized_text"]
        
        if not ref_text.strip():
            continue
            
        inputs = feature_extractor(waveform, sampling_rate=sample_rate, return_tensors="pt")
        input_values = inputs.input_values.to(device)
        
        with torch.no_grad():
            logits = model(input_values).logits
            
        pred_ids = torch.argmax(logits, dim=-1)
        pred_text = tokenizer.batch_decode(pred_ids)[0]
        
        predictions.append(pred_text)
        references.append(ref_text)
        
        if not pred_text.strip():
            empty_count += 1
            
        results.append({
            "reference": ref_text,
            "prediction": pred_text,
            "reference_length": len(ref_text),
            "prediction_length": len(pred_text)
        })
        
        count += 1
        
    wer = jiwer.wer(references, predictions)
    cer = jiwer.cer(references, predictions)
    
    avg_pred_len = sum(r["prediction_length"] for r in results) / len(results)
    avg_ref_len = sum(r["reference_length"] for r in results) / len(results)
    empty_rate = empty_count / len(results)
    
    final_analysis = {
        "wer": wer,
        "cer": cer,
        "empty_prediction_rate": empty_rate,
        "average_predicted_character_count": avg_pred_len,
        "average_reference_character_count": avg_ref_len,
        "samples": results
    }
    
    os.makedirs("evaluation/asr/santali", exist_ok=True)
    with open("evaluation/asr/santali/phase37_failure_analysis.json", "w", encoding="utf-8") as f:
        json.dump(final_analysis, f, indent=4, ensure_ascii=False)
        
    print("Analysis saved to evaluation/asr/santali/phase37_failure_analysis.json")

if __name__ == "__main__":
    run_analysis()
