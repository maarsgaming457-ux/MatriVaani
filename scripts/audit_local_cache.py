import os
import json
import soundfile as sf
import collections
import re

def is_ol_chiki(char):
    return '\u1C50' <= char <= '\u1C7F'

def is_devanagari(char):
    return '\u0900' <= char <= '\u097F'

def is_latin(char):
    return char.isalpha() and char.isascii()

def audit():
    meta_dir = "datasets/cache/santali/metadata"
    
    # Audit train
    train_meta = []
    with open(os.path.join(meta_dir, "train.jsonl"), "r", encoding="utf-8") as f:
        for line in f:
            train_meta.append(json.loads(line))
            
    valid_meta = []
    try:
        with open(os.path.join(meta_dir, "validation.jsonl"), "r", encoding="utf-8") as f:
            for line in f:
                valid_meta.append(json.loads(line))
    except FileNotFoundError:
        pass
            
    all_meta = train_meta + valid_meta
    
    stats = {
        "num_samples": len(all_meta),
        "num_train": len(train_meta),
        "num_valid": len(valid_meta),
        "total_duration_hrs": sum(m["duration"] for m in all_meta) / 3600.0 if all_meta else 0,
        "min_duration": min(m["duration"] for m in all_meta) if all_meta else 0,
        "max_duration": max(m["duration"] for m in all_meta) if all_meta else 0,
        "mean_duration": (sum(m["duration"] for m in all_meta) / len(all_meta)) if all_meta else 0,
        "median_duration": sorted(m["duration"] for m in all_meta)[len(all_meta)//2] if all_meta else 0,
        "empty_transcript_count": sum(1 for m in all_meta if not m["transcript"].strip()),
        "invalid_language_code_count": sum(1 for m in all_meta if m["language_code"] != "sat"),
    }
    
    # Check script contamination
    ol_chiki_count = 0
    devanagari_count = 0
    latin_count = 0
    mixed_script_count = 0
    
    for m in all_meta:
        t = m["transcript"]
        has_ol = any(is_ol_chiki(c) for c in t)
        has_dev = any(is_devanagari(c) for c in t)
        has_lat = any(is_latin(c) for c in t)
        
        if has_ol: ol_chiki_count += 1
        if has_dev: devanagari_count += 1
        if has_lat: latin_count += 1
        
        if sum([has_ol, has_dev, has_lat]) > 1:
            mixed_script_count += 1
            
    stats["script_distribution"] = {
        "ol_chiki": ol_chiki_count,
        "devanagari": devanagari_count,
        "latin": latin_count,
        "mixed": mixed_script_count
    }
    
    # verify audio files
    invalid_audio_count = 0
    for m in all_meta:
        if not os.path.exists(m["audio_path"]):
            invalid_audio_count += 1
            
    stats["invalid_audio_count"] = invalid_audio_count
    
    os.makedirs("evaluation/datasets/santali", exist_ok=True)
    with open("evaluation/datasets/santali/local_cache_audit.json", "w") as f:
        json.dump(stats, f, indent=2)
        
    # Split integrity
    train_ids = set(m["sample_id"] for m in train_meta)
    valid_ids = set(m["sample_id"] for m in valid_meta)
    
    intersection = train_ids.intersection(valid_ids)
    
    integrity = {
        "train_unique_ids": len(train_ids),
        "valid_unique_ids": len(valid_ids),
        "intersection_count": len(intersection),
        "is_disjoint": len(intersection) == 0
    }
    
    with open("evaluation/datasets/santali/split_integrity.json", "w") as f:
        json.dump(integrity, f, indent=2)
        
    print(json.dumps(stats, indent=2))
    print(json.dumps(integrity, indent=2))
    
    # Doc
    doc = f"""# Santali Local Dataset Cache Audit

## Summary
- **Total Samples**: {stats['num_samples']} (Train: {stats['num_train']}, Valid: {stats['num_valid']})
- **Total Duration**: {stats['total_duration_hrs']:.2f} hours
- **Mean Duration**: {stats['mean_duration']:.2f} seconds
- **Invalid Audio Files**: {stats['invalid_audio_count']}
- **Empty Transcripts**: {stats['empty_transcript_count']}

## Split Integrity
- **Is Disjoint**: {integrity['is_disjoint']} (Overlap: {integrity['intersection_count']})

## Script Analysis
- Ol Chiki: {stats['script_distribution']['ol_chiki']}
- Devanagari: {stats['script_distribution']['devanagari']}
- Latin: {stats['script_distribution']['latin']}
- Mixed: {stats['script_distribution']['mixed']}
"""
    with open("docs/SANTALI_LOCAL_DATASET_CACHE.md", "w", encoding="utf-8") as f:
        f.write(doc)
        
if __name__ == "__main__":
    audit()
