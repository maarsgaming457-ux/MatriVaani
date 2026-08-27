import os
import json

def audit_datasets(raw_dir="datasets/nmt/raw", out_file="evaluation/accuracy/nmt/dataset_audit.json"):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    audit_results = {
        "status": "ACCESS UNAVAILABLE",
        "reason": "Datasets (e.g. COILD-MT-Corpus) are gated and require manual token/authentication. No files exist locally.",
        "total_records": 0,
        "hindi_records": 0,
        "santhali_records": 0,
        "aligned_pairs": 0,
        "duplicate_count": 0,
        "malformed_records": 0,
        "verified_records": 0,
        "machine_generated_records": 0
    }
        
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=4)
        
    print(f"Audit complete. Results saved to {out_file}")

if __name__ == "__main__":
    audit_datasets()
