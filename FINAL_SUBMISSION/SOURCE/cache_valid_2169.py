import os
import json
import io
import soundfile as sf
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def cache_split(split_name, max_samples):
    print(f"Caching {split_name} split ({max_samples} samples)...")
    
    loader = IndicVoicesLoader()
    stream = loader.stream_train() if split_name == "train" else loader.stream_valid()
    
    audio_dir = f"datasets/cache/santali/{split_name}"
    meta_dir = "datasets/cache/santali/metadata"
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)
    
    meta_file = os.path.join(meta_dir, f"{split_name}.jsonl")
    
    count = 0
    # Read existing meta
    existing = set()
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                existing.add(d["sample_id"])
        print(f"Found {len(existing)} existing cached samples.")
    
    with open(meta_file, "a", encoding="utf-8") as f:
        for item in stream:
            if count >= max_samples:
                break
                
            sample_id = f"{split_name}_{count}"
            
            if sample_id in existing:
                count += 1
                continue
                
            waveform = item["waveform"]
            sample_rate = item["sample_rate"]
            
            audio_path = os.path.join(audio_dir, f"{sample_id}.flac")
            
            # Save as FLAC
            sf.write(audio_path, waveform, sample_rate, format='FLAC', subtype='PCM_16')
            
            duration = len(waveform) / sample_rate
            
            meta = {
                "sample_id": sample_id,
                "audio_path": audio_path,
                "transcript": item["normalized_text"],
                "duration": duration,
                "language_code": "sat",
                "split": split_name
            }
            
            f.write(json.dumps(meta) + "\n")
            f.flush()
            
            count += 1
            if count % 100 == 0:
                print(f"Cached {count}/{max_samples} samples...")

    print(f"Finished caching {count} samples for {split_name}.")

if __name__ == "__main__":
    cache_split("validation", 2169)
