import os
import json

def audit_tts_datasets(raw_dir="datasets/tts/raw", out_file="evaluation/accuracy/tts/dataset_audit.json"):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    if not os.path.exists(raw_dir) or not os.listdir(raw_dir):
        print(f"Warning: No TTS datasets found in {raw_dir}")
        audit_results = {
            "status": "INSUFFICIENT DATA",
            "total_audio_files": 0,
            "total_duration_hours": 0.0,
            "santhali_hours": 0.0,
            "ol_chiki_transcripts": 0,
            "malformed_audio": 0,
            "missing_transcripts": 0,
            "speakers": 0
        }
    else:
        # Placeholder for actual audio processing/librosa checks
        audit_results = {}
        
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=4)
        
    print(f"TTS Audit complete. Results saved to {out_file}")

if __name__ == "__main__":
    audit_tts_datasets()
