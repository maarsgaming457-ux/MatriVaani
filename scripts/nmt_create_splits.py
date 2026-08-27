import os
import json

def create_splits(normalized_dir="datasets/nmt/normalized"):
    """
    Creates train/validation/test splits from normalized records.
    Currently halts due to INSUFFICIENT DATA.
    """
    if not os.path.exists(normalized_dir) or not os.listdir(normalized_dir):
        print(f"Error: No normalized datasets found in {normalized_dir}. Cannot create splits.")
        return
        
    print("Splitting datasets...")

if __name__ == "__main__":
    create_splits()
