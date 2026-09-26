from transformers import AutoTokenizer
import os
try:
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large", local_files_only=True)
    print("SUCCESS: Loaded flan tokenizer with local_files_only=True")
except Exception as e:
    print(f"FAILED: {e}")
