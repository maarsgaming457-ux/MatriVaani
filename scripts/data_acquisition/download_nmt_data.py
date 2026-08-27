import os
import sys

def download_nmt():
    print("--- MatriVaani NMT Download Engine ---")
    print("Target: MatriVaani Manual Curation Database")
    
    data_dir = "datasets/nmt/raw"
    if not os.path.exists(data_dir):
        print(f"[FAIL] Local curation directory {data_dir} missing.")
        sys.exit(1)
        
    files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    
    if len(files) == 0:
        print("[FAIL] 0 manually curated pairs found.")
        print("Human contributors must execute scripts/nmt_manual_curation_tool.py to populate data.")
        print("Status: DATA_BLOCKED (Human Curation Required)")
        sys.exit(1)
        
    print(f"[PASS] {len(files)} pairs discovered.")
    
if __name__ == "__main__":
    download_nmt()
