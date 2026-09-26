from huggingface_hub import hf_hub_download
import os
import sys

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

print("Downloading model.safetensors...")
try:
    path = hf_hub_download(repo_id="ai4bharat/indic-parler-tts", filename="model.safetensors")
    print("\nDownload complete:", path)
except Exception as e:
    print(f"\nFAILED: {e}")
