import json
import os
import soundfile as sf
import re
import pandas as pd

def create_splits():
    metadata_path = "datasets/cache/santali/metadata/train.jsonl"
    
    with open(metadata_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    valid_samples = []
    seen_transcripts = set()
    ol_chiki_pattern = re.compile(r'^[\u1C50-\u1C7F\s\.,!?\'-]+$')
    
    total_duration = 0.0
    
    for i, line in enumerate(lines):
        item = json.loads(line)
        path = item.get("audio_path")
        transcript = item.get("transcript", "").strip()
        duration = item.get("duration", 0)
        
        if not path or not os.path.exists(path): continue
        if not transcript: continue
        if not ol_chiki_pattern.match(transcript): continue
        if transcript in seen_transcripts: continue
        seen_transcripts.add(transcript)
        if duration < 1.0 or duration > 20.0: continue
        
        try:
            info = sf.info(path)
            if info.samplerate != 16000 or info.channels != 1: continue
        except:
            continue
            
        valid_samples.append({
            "file_name": os.path.abspath(path),
            "transcription": transcript,
            "duration": duration
        })
        
        total_duration += duration
        
    print(f"Total valid samples available: {len(valid_samples)}")
    
    # Take first 5000 for train
    train_samples = valid_samples[:5000]
    
    # Take next 2949 for test
    test_samples = valid_samples[5000:5000+2949]
    
    os.makedirs("datasets/splits", exist_ok=True)
    
    train_df = pd.DataFrame(train_samples)
    train_df.to_csv("datasets/splits/train_5000.csv", index=False)
    
    test_df = pd.DataFrame(test_samples)
    test_df.to_csv("datasets/splits/test_2949.csv", index=False)
    
    train_duration = train_df['duration'].sum() / 3600
    test_duration = test_df['duration'].sum() / 3600
    
    print(f"TRAIN: {len(train_samples)} samples, {train_duration:.2f} hours")
    print(f"TEST: {len(test_samples)} samples, {test_duration:.2f} hours")
    
if __name__ == "__main__":
    create_splits()
