from huggingface_hub import hf_hub_download
import os
import sys
import time

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

print("Starting robust download loop...")
success = False
attempts = 0

while not success and attempts < 20:
    attempts += 1
    try:
        print(f"Attempt {attempts}...")
        path = hf_hub_download(repo_id="ai4bharat/indic-parler-tts", filename="model.safetensors", resume_download=True)
        print("\nDownload complete:", path)
        success = True
    except Exception as e:
        print(f"\nFAILED attempt {attempts}: {e}")
        time.sleep(5)
