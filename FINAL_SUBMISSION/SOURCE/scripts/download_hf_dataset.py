import os
from datasets import load_dataset
import pandas as pd
import hashlib
from datetime import datetime

def download_and_inspect_dataset():
    # Load dataset from Hugging Face
    dataset_name = "ainlpml-iitp/COILD-MT-Corpus"
    print(f"Loading {dataset_name}...")
    try:
        ds = load_dataset(dataset_name)
        # Check what splits exist, we just want to grab the HIN-SAT subset if available
        # COILD-MT has multiple languages.
        print("Dataset loaded successfully.")
        print(ds)
        
        # It's likely a single train split with language pairs. Let's inspect the first row.
        if 'train' in ds:
            print("First row:", ds['train'][0])
            
            # Let's save the first 1000 rows locally as raw data
            raw_dir = "datasets/nmt/raw/COILD_MT_Corpus"
            os.makedirs(raw_dir, exist_ok=True)
            
            csv_path = os.path.join(raw_dir, "hin_sat_raw.csv")
            df = ds['train'].to_pandas()
            # Filter for hindi-santali if there's a language column, or if it's already just hin-sat
            print("Columns:", df.columns)
            
            # We will just take the first 100 for inspection to not blow up space right now
            df_sample = df.head(100)
            df_sample.to_csv(csv_path, index=False)
            print(f"Saved sample to {csv_path}")
            
            # Create README
            readme_path = os.path.join(raw_dir, "README.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# COILD-MT-Corpus\n")
                f.write(f"- Source: Hugging Face ({dataset_name})\n")
                f.write(f"- Download Date: {datetime.now().isoformat()}\n")
                f.write(f"- License: Check repo (assume academic/research)\n")
                
            # Create sha256
            hasher = hashlib.sha256()
            with open(csv_path, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            print(f"SHA256: {hasher.hexdigest()}")
            
    except Exception as e:
        print(f"Error loading dataset: {e}")

if __name__ == "__main__":
    download_and_inspect_dataset()
