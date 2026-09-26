import urllib.request
import pandas as pd

URL = "https://huggingface.co/datasets/google/fleurs/resolve/main/data/hi_in/dev.tsv"
print(f"Downloading {URL}...")
urllib.request.urlretrieve(URL, "dev.tsv")

df = pd.read_csv("dev.tsv", sep="\t", header=None, names=["id", "file", "text", "text_normalized", "audio_path", "unknown1", "unknown2"])
print(df.head())
