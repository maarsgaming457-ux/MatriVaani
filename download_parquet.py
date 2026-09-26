import urllib.request
import os

token_path = os.path.expanduser("~/.cache/huggingface/token")
with open(token_path, "r") as f:
    token = f.read().strip()

url = "https://huggingface.co/datasets/ai4bharat/IndicVoices/resolve/main/santali/valid-00000-of-00001.parquet"
out_path = "datasets/cache/santali/valid.parquet"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

print(f"Downloading {url} to {out_path}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Authorization': f'Bearer {token}'})
try:
    with urllib.request.urlopen(req) as response, open(out_path, 'wb') as out_file:
        chunk_size = 1024 * 1024
        downloaded = 0
        while True:
            data = response.read(chunk_size)
            if not data:
                break
            out_file.write(data)
            downloaded += len(data)
            if downloaded % (10 * 1024 * 1024) == 0:
                print(f"Downloaded {downloaded / (1024*1024)} MB")
    print("Downloaded successfully.")
except Exception as e:
    print("Error:", e)
