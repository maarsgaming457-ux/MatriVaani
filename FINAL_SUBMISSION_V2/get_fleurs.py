import os
import urllib.request
import tarfile

URL = "https://huggingface.co/datasets/google/fleurs/resolve/main/data/hi_in/audio/dev.tar.gz"
print(f"Downloading {URL}...")
urllib.request.urlretrieve(URL, "dev.tar.gz")

print("Extracting...")
with tarfile.open("dev.tar.gz", "r:gz") as tar:
    tar.extractall(path="fleurs_hi")
    
print("Done!")
