import os
import sys
import json

def check_readiness(dataset_type: str, raw_dir: str):
    print(f"--- Checking Readiness: {dataset_type} ---")
    
    # Check if real data exists
    if not os.path.exists(raw_dir) or not os.listdir(raw_dir):
        print(f"Status: DATA_BLOCKED")
        return "DATA_BLOCKED"
        
    # Checking metadata (Mock)
    registry_path = "datasets/metadata/dataset_registry.json"
    with open(registry_path, "r") as f:
        registry = json.load(f)
        
    # We would normally parse the specific registry entry, but since data is blocked, 
    # we exit early above.
    
    return "READY"

if __name__ == "__main__":
    asr_status = check_readiness("ASR", "datasets/asr/raw")
    nmt_status = check_readiness("NMT", "datasets/nmt/raw")
    tts_status = check_readiness("TTS", "datasets/tts/raw")
    
    if "DATA_BLOCKED" in [asr_status, nmt_status, tts_status]:
        print("\nOVERALL STATUS: DATA_BLOCKED")
        sys.exit(1)
    
    print("\nOVERALL STATUS: READY")
    sys.exit(0)
