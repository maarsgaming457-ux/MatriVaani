import json
import os
from collections import Counter
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_audit(max_train=1000, max_valid=200):
    loader = IndicVoicesLoader()
    
    report = {
        "records_inspected": 0,
        "valid_audio": 0,
        "invalid_audio": 0,
        "valid_transcripts": 0,
        "invalid_transcripts": 0,
        "language_mismatch": 0,
        "script_distribution": Counter(),
        "duration_statistics": {
            "total_hours": 0.0,
            "min_seconds": float('inf'),
            "max_seconds": 0.0
        },
        "rejection_reasons": Counter()
    }
    
    char_stats = {
        "unique_characters": set(),
        "character_frequencies": Counter(),
        "whitespace_frequency": 0,
        "digits_frequency": 0
    }
    
    subset = {
        "train": [],
        "valid": []
    }
    
    # We will use the underlying _stream_split to get BOTH valid and rejected items
    # Wait, the loader currently yields ONLY valid items and drops rejected ones. 
    # Let's bypass the loader's _process_record to do our own audit logic so we can count rejections.
    
    def audit_split(split_name, max_samples):
        print(f"Auditing {split_name} split (max {max_samples})...")
        ds = loader._stream_split.__self__._stream_split(split_name) # Call the raw dataset stream?
        # Actually _stream_split is on IndicVoicesLoader but wait, _stream_split returns PROCESSED items in my rewritten version!
        pass
        
    # Redefine audit logic directly on raw HF dataset for accurate failure counting
    import datasets
    
    def process_raw_split(split_name, max_samples):
        ds = datasets.load_dataset(
            loader.dataset_name, 
            loader.config, 
            split=split_name, 
            streaming=True, 
            token=loader.token,
            cache_dir=loader.cache_dir,
            trust_remote_code=True
        )
        ds = ds.cast_column("audio_filepath", datasets.Audio(decode=False))
        
        count = 0
        for item in ds:
            if count >= max_samples:
                break
            
            report["records_inspected"] += 1
            
            # Text validation
            raw_text = item.get("text", "")
            if not raw_text or not raw_text.strip():
                report["invalid_transcripts"] += 1
                report["rejection_reasons"]["empty_text"] += 1
                continue
                
            lang = item.get("lang", "")
            if lang != "sat":
                report["language_mismatch"] += 1
                report["rejection_reasons"]["language_mismatch"] += 1
                continue
                
            script = loader.normalizer.identify_script(raw_text)
            report["script_distribution"][script] += 1
            
            if script not in ["ol_chiki", "mixed", "latin", "devanagari"]:
                report["invalid_transcripts"] += 1
                report["rejection_reasons"][f"invalid_script_{script}"] += 1
                continue
                
            # Audio validation
            audio_data = item.get("audio_filepath", {})
            if not audio_data or not audio_data.get("bytes"):
                report["invalid_audio"] += 1
                report["rejection_reasons"]["missing_audio"] += 1
                continue
                
            metadata_duration = item.get("duration", 0.0)
            
            # Since we just want to verify it CAN decode without spending an hour decoding 1200 files,
            # we will just trust the bytes exist for the quick audit, or decode them if requested.
            # To be thorough and prove 0 RAM leakage, we WILL decode them all.
            from data_modules.santali.audio import decode_audio_bytes
            try:
                waveform, sr = decode_audio_bytes(audio_data["bytes"])
                decoded_duration = len(waveform) / sr
                
                if metadata_duration > 0 and abs(metadata_duration - decoded_duration) > 0.5:
                    report["invalid_audio"] += 1
                    report["rejection_reasons"]["duration_mismatch"] += 1
                    continue
                    
                report["valid_audio"] += 1
                report["valid_transcripts"] += 1
                
                # Update duration stats
                report["duration_statistics"]["total_hours"] += (decoded_duration / 3600.0)
                report["duration_statistics"]["min_seconds"] = min(report["duration_statistics"]["min_seconds"], decoded_duration)
                report["duration_statistics"]["max_seconds"] = max(report["duration_statistics"]["max_seconds"], decoded_duration)
                
                # Update Character stats
                normalized_text = loader.normalizer.normalize(raw_text)["normalized_text"]
                for char in normalized_text:
                    char_stats["unique_characters"].add(char)
                    char_stats["character_frequencies"][char] += 1
                    if char.isspace():
                        char_stats["whitespace_frequency"] += 1
                    if char.isdigit():
                        char_stats["digits_frequency"] += 1
                        
                # Add to subset
                subset[split_name].append({
                    "original_text": raw_text,
                    "normalized_text": normalized_text,
                    "duration": decoded_duration,
                    "script": script
                })
                
                count += 1
                if count % 100 == 0:
                    print(f"{split_name}: {count}/{max_samples} processed...")
                    
            except Exception as e:
                report["invalid_audio"] += 1
                report["rejection_reasons"]["decode_error"] += 1
                continue
                
    process_raw_split("train", max_train)
    process_raw_split("valid", max_valid)
    
    # Serialize outputs
    os.makedirs("evaluation/datasets/santali", exist_ok=True)
    
    # Clean up non-serializable sets/counters
    report["script_distribution"] = dict(report["script_distribution"])
    report["rejection_reasons"] = dict(report["rejection_reasons"])
    char_stats["unique_characters"] = sorted(list(char_stats["unique_characters"]))
    char_stats["character_frequencies"] = dict(char_stats["character_frequencies"].most_common())
    
    with open("evaluation/datasets/santali/data_quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    with open("evaluation/datasets/santali/character_statistics.json", "w", encoding="utf-8") as f:
        json.dump(char_stats, f, indent=4, ensure_ascii=False)
        
    with open("evaluation/datasets/santali/development_subset.json", "w", encoding="utf-8") as f:
        json.dump(subset, f, indent=4, ensure_ascii=False)
        
    print("\nAudit Complete!")
    print(f"Total Records Inspected: {report['records_inspected']}")
    print(f"Valid Samples Added to Subset: Train={len(subset['train'])}, Valid={len(subset['valid'])}")

if __name__ == "__main__":
    run_audit(max_train=1000, max_valid=200)
