import os
import time
import requests
from huggingface_hub import get_token

token = get_token()
repo_id = "ai4bharat/indic-parler-tts"
filename = "model.safetensors"
url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
headers = {"Authorization": f"Bearer {token}"} if token else {}

blob_dir = os.path.expanduser("~/.cache/huggingface/hub/models--ai4bharat--indic-parler-tts/blobs")
os.makedirs(blob_dir, exist_ok=True)
out_file = os.path.join(blob_dir, "c68daecb60f80c8f1faf0a6d2e6ddd6de8e224fb19750f3e9a33bca43c552c90")

total_size_expected = 3751321772

while True:
    downloaded_size = os.path.getsize(out_file) if os.path.exists(out_file) else 0
    if downloaded_size >= total_size_expected:
        print("Download complete!")
        break
        
    print(f"Resuming from {downloaded_size / (1024*1024):.2f} MB")
    current_headers = headers.copy()
    if downloaded_size > 0:
        current_headers["Range"] = f"bytes={downloaded_size}-"
        
    try:
        with requests.get(url, headers=current_headers, stream=True, timeout=15) as r:
            if r.status_code not in (200, 206):
                print(f"Bad status code: {r.status_code}")
                time.sleep(5)
                continue
                
            with open(out_file, "ab") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        print(f"\rDownloaded: {downloaded_size / (1024*1024):.2f} MB / {total_size_expected / (1024*1024):.2f} MB", end="")
    except Exception as e:
        print(f"\nError: {e}. Retrying in 2 seconds...")
        time.sleep(2)
