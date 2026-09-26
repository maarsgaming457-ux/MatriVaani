import os
import requests

repo_id = "google/flan-t5-large"
files = ["config.json", "generation_config.json", "spiece.model", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json"]

blob_dir = os.path.expanduser("~/.cache/huggingface/hub/models--google--flan-t5-large/snapshots/a178bb092025170d18bcff70125d19db2fb6e98b")
os.makedirs(blob_dir, exist_ok=True)

for filename in files:
    out_file = os.path.join(blob_dir, filename)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
        print(f"{filename} already downloaded.")
        continue
        
    url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
    print(f"Downloading {filename}...")
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(out_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
    except Exception as e:
        print(f"Failed {filename}: {e}")
print("Done.")
