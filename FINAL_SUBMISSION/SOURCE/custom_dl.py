import os
import time
import requests
from huggingface_hub import get_token

token = get_token()
if not token:
    print("NO TOKEN")
    exit(1)

repo_id = "ai4bharat/indic-parler-tts"
filename = "model.safetensors"
url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
headers = {"Authorization": f"Bearer {token}"}

out_file = filename
mode = "ab"
if os.path.exists(out_file):
    downloaded_size = os.path.getsize(out_file)
else:
    downloaded_size = 0

print(f"Resuming from {downloaded_size}")

try:
    with requests.get(url, headers=headers, stream=True, timeout=10) as r:
        total_size = int(r.headers.get("content-length", 0))
        if total_size > 0 and downloaded_size == total_size:
            print("Already fully downloaded!")
            exit(0)
            
        print(f"Total size: {total_size}")
        
        if downloaded_size > 0:
            headers["Range"] = f"bytes={downloaded_size}-"
            
    # Re-request with Range
    with requests.get(url, headers=headers, stream=True, timeout=10) as r:
        r.raise_for_status()
        with open(out_file, mode) as f:
            for chunk in r.iter_content(chunk_size=8192*4):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if downloaded_size % (1024*1024*100) < 32768:
                        print(f"Downloaded: {downloaded_size / (1024*1024):.2f} MB")
                        
    print("Download finished successfully.")
except Exception as e:
    print(f"Download failed/interrupted: {e}")
