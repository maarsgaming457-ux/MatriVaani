from huggingface_hub import hf_hub_download
import os

print("Starting download of model.safetensors...")
try:
    path = hf_hub_download(repo_id="ai4bharat/indic-parler-tts", filename="model.safetensors", resume_download=True)
    print("Download complete at:", path)
except Exception as e:
    print(f"FAILED: {e}")
