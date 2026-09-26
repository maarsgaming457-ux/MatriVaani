import requests
import pandas as pd
import io
import json

url = "https://huggingface.co/api/datasets/PYD4320/audio-text-pair_train-test-dataset-hindi/parquet/default/test"
resp = requests.get(url)
print(resp.json())
