import os
import sys
import json

def check_model(name: str, checkpoint_dir: str, eval_file: str):
    print(f"--- Checking {name} ---")
    
    # 1. Check if checkpoint exists
    if not os.path.exists(checkpoint_dir) or not os.listdir(checkpoint_dir):
        print(f"[FAIL] Checkpoint not found in {checkpoint_dir}")
        return False
        
    # 2. Check evaluation
    if not os.path.exists(eval_file):
        print(f"[FAIL] Evaluation file {eval_file} not found")
        return False
        
    with open(eval_file, "r") as f:
        metrics = json.load(f)
        if metrics.get("status") == "TRAINING BLOCKED":
            print(f"[FAIL] Model evaluation flagged as blocked.")
            return False
            
    print(f"[PASS] {name} is READY.")
    return True

if __name__ == "__main__":
    asr_ready = check_model("ASR", "models/matrivaani_asr_santhali_v1", "evaluation/asr/asr_final_report.json")
    nmt_ready = check_model("NMT", "models/matrivaani_nmt_hi_sat_v1", "evaluation/nmt/nmt_final_report.json")
    tts_ready = check_model("TTS", "models/matrivaani_tts_santhali_v1", "evaluation/tts/tts_final_report.json")
    
    if not (asr_ready and nmt_ready and tts_ready):
        print("\nOVERALL STATUS: NOT READY")
        print("Integration Voice-to-Voice tests cannot proceed with mock models.")
        sys.exit(1)
    else:
        print("\nOVERALL STATUS: READY")
        sys.exit(0)
