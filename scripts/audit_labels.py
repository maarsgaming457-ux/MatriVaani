import os
import json
from transformers import AutoFeatureExtractor
from training.asr.santali.tokenizer import get_santali_tokenizer
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_label_audit():
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    
    loader = IndicVoicesLoader()
    train_stream = loader.stream_train()
    
    count = 0
    results = []
    
    for item in train_stream:
        if count >= 50:
            break
            
        waveform = item["waveform"]
        sample_rate = item["sample_rate"]
        ref_text = item["normalized_text"]
        
        audio_duration = len(waveform) / sample_rate
        audio_frames = int(audio_duration * sample_rate / feature_extractor.hop_length) if hasattr(feature_extractor, "hop_length") else int(len(waveform) / 320)
        
        encoded = tokenizer(ref_text).input_ids
        
        results.append({
            "audio_duration_sec": audio_duration,
            "transcript_char_count": len(ref_text),
            "encoded_label_length": len(encoded),
            "audio_frames_approx": audio_frames,
            "possible": audio_frames >= len(encoded)
        })
        
        count += 1
        
    print(json.dumps(results[:5], indent=2))
    
    impossible = sum(1 for r in results if not r["possible"])
    print(f"\nImpossible alignments (frames < labels): {impossible} / 50")

if __name__ == "__main__":
    run_label_audit()
