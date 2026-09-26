import sqlite3
import pandas as pd
import sys
import os

db_path = 'tools/ho_annotator/annotations.db'
if not os.path.exists(db_path):
    print("Database not found")
    sys.exit(1)

conn = sqlite3.connect(db_path)
df = pd.read_sql_query('SELECT ho FROM annotations WHERE ho IS NOT NULL AND ho != "" LIMIT 5', conn)

if df.empty:
    df = pd.read_sql_query('SELECT raw_asr_text FROM annotations WHERE raw_asr_text IS NOT NULL AND raw_asr_text != "" LIMIT 5', conn)
    df.rename(columns={'raw_asr_text': 'ho'}, inplace=True)

ho_texts = df['ho'].tolist()
print("Genuine Ho transcripts to test:")
for text in ho_texts:
    print(f" - {text}")

print("\n--- IndicTrans2 Tokenizer Test ---\n")

try:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-indic-indic-dist-320M", trust_remote_code=True)
    
    for text in ho_texts:
        print(f"\nOriginal Ho: {text}")
        tokens = tokenizer.tokenize(text)
        print(f"Tokens: {tokens}")
        ids = tokenizer.encode(text)
        print(f"Token IDs: {ids}")
        decoded = tokenizer.decode(ids, skip_special_tokens=True)
        print(f"Decoded: {decoded}")
        
except Exception as e:
    print(f"Error testing tokenizer: {e}")
