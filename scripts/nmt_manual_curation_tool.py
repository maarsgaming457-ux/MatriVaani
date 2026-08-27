import os
import json
import time

DATA_DIR = "datasets/nmt/raw"

def initialize():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
def get_next_id():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    return len(files) + 1

def curate():
    print("--- MatriVaani Manual NMT Curation Engine ---")
    print("Status: Pending human data entry.")
    print("Type 'exit' to quit.\n")
    
    while True:
        hindi_text = input("Enter Hindi sentence (FLN/Primary Education context): ")
        if hindi_text.lower() == 'exit':
            break
            
        santhali_text = input("Enter Santhali translation (Ol Chiki preferred): ")
        if santhali_text.lower() == 'exit':
            break
            
        translator_id = input("Enter your Translator ID (e.g., JD01): ")
        
        # State machine initialized at RAW -> TRANSLATED
        
        data_id = get_next_id()
        data = {
            "id": f"SAT-NMT-{data_id:05d}",
            "hindi": hindi_text,
            "santhali": santhali_text,
            "script": "Ol Chiki",
            "domain": "primary_education",
            "translator_id": translator_id,
            "reviewer_id": None,
            "status": "TRANSLATED", # Status flow: TRANSLATED -> REVIEW -> VERIFIED -> APPROVED
            "timestamp": time.time()
        }
        
        file_path = os.path.join(DATA_DIR, f"{data['id']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"[+] Saved to {file_path}. Awaiting reviewer verification.\n")

if __name__ == "__main__":
    initialize()
    curate()
