import json
import os
import soundfile as sf
import re

def audit_dataset():
    metadata_path = "datasets/cache/santali/metadata/train.jsonl"
    
    with open(metadata_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    total_raw = len(lines)
    
    missing_audio = 0
    missing_transcript = 0
    short_audio = 0
    long_audio = 0
    duplicate_transcript = 0
    invalid_script = 0
    corrupt_audio = 0
    wrong_sr_channel = 0
    
    valid_samples = []
    seen_transcripts = set()
    
    # Ol Chiki Unicode range is 1C50-1C7F. We also allow spaces and basic punctuation.
    ol_chiki_pattern = re.compile(r'^[\u1C50-\u1C7F\s\.,!?\'-]+$')
    
    for i, line in enumerate(lines):
        item = json.loads(line)
        path = item.get("audio_path")
        transcript = item.get("transcript", "").strip()
        duration = item.get("duration", 0)
        
        # 1. Missing audio file
        if not path or not os.path.exists(path):
            missing_audio += 1
            continue
            
        # 2. Missing/Empty transcript
        if not transcript:
            missing_transcript += 1
            continue
            
        # 3. Invalid characters/script (must be Ol Chiki)
        if not ol_chiki_pattern.match(transcript):
            invalid_script += 1
            continue
            
        # 4. Duplicate transcript
        if transcript in seen_transcripts:
            duplicate_transcript += 1
            continue
        seen_transcripts.add(transcript)
        
        # 5. Short audio
        if duration < 1.0:
            short_audio += 1
            continue
            
        # 6. Long audio
        if duration > 20.0:
            long_audio += 1
            continue
            
        # 7. Corrupt audio / sample rate / channel
        try:
            info = sf.info(path)
            if info.samplerate != 16000 or info.channels != 1:
                wrong_sr_channel += 1
                continue
        except Exception as e:
            corrupt_audio += 1
            continue
            
        valid_samples.append(item)
        
        if (i+1) % 1000 == 0:
            print(f"Processed {i+1}/{total_raw}")
            
    print("\n--- AUDIT REPORT ---")
    print(f"Total Raw Samples: {total_raw}")
    print(f"Missing Audio: {missing_audio}")
    print(f"Missing/Empty Transcript: {missing_transcript}")
    print(f"Invalid Script/Characters: {invalid_script}")
    print(f"Duplicate Transcript: {duplicate_transcript}")
    print(f"Short Audio (<1s): {short_audio}")
    print(f"Long Audio (>20s): {long_audio}")
    print(f"Corrupt Audio: {corrupt_audio}")
    print(f"Wrong SR/Channels: {wrong_sr_channel}")
    print(f"Total Valid Samples: {len(valid_samples)}")

if __name__ == "__main__":
    audit_dataset()
