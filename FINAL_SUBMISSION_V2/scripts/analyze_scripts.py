import sys
import json
import re
from datasets import load_dataset, Audio

def detect_script(text):
    has_ol_chiki = bool(re.search(r'[\u1C50-\u1C7F]', text))
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    has_latin = bool(re.search(r'[A-Za-z]', text))
    
    scripts = []
    if has_ol_chiki: scripts.append("Ol_Chiki")
    if has_devanagari: scripts.append("Devanagari")
    if has_latin: scripts.append("Latin")
    
    if not scripts:
        return "Unknown"
    elif len(scripts) > 1:
        return "Mixed"
    else:
        return scripts[0]

def analyze_split(split_name, num_samples=5):
    print(f"Loading {split_name} split for analysis...")
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split=split_name, streaming=True)
    ds = ds.cast_column("audio_filepath", Audio(decode=False))
    
    ds_iter = iter(ds)
    
    ol_chiki_samples = 0
    devanagari_samples = 0
    latin_samples = 0
    mixed_script_samples = 0
    
    for i in range(num_samples):
        sample = next(ds_iter)
        text = sample["text"]
        
        script = detect_script(text)
        if script == "Ol_Chiki": ol_chiki_samples += 1
        elif script == "Devanagari": devanagari_samples += 1
        elif script == "Latin": latin_samples += 1
        elif script == "Mixed": mixed_script_samples += 1
        
        print(f"Sample {i+1} Script: {script}")
        
    print(f"  Ol Chiki: {ol_chiki_samples}")
    print(f"  Devanagari: {devanagari_samples}")
    print(f"  Latin: {latin_samples}")
    print(f"  Mixed: {mixed_script_samples}")
    return ol_chiki_samples, devanagari_samples, latin_samples, mixed_script_samples

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    analyze_split("train", 5)
    analyze_split("valid", 5)

if __name__ == "__main__":
    main()
