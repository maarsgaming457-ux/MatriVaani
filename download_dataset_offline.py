import os
import datasets
datasets.load_dataset("ai4bharat/IndicVoices", "santali", split="valid", streaming=False, trust_remote_code=True, cache_dir="datasets/cache")
