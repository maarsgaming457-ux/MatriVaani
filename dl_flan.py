from huggingface_hub import snapshot_download
import os

print("Downloading flan-t5-large tokenizer...")
try:
    path = snapshot_download(repo_id="google/flan-t5-large", allow_patterns=["*.json", "*.model", "*.txt"])
    print("Download complete:", path)
except Exception as e:
    print(f"FAILED: {e}")
