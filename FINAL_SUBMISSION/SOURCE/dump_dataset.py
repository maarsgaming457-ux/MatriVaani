import pandas as pd
import pickle
from data_modules.santali.indicvoices_loader import IndicVoicesLoader
import sys

print("Loading dataset...")
df = pd.read_parquet("datasets/cache/santali/valid.parquet")
loader = IndicVoicesLoader()

data = []
count = 0
for idx, row in df.iterrows():
    if count >= 2169: break
    
    item = row.to_dict()
    if pd.isna(item.get("duration")):
        item["duration"] = 0.0
        
    processed = loader._process_record(item)
    if processed is None:
        continue
        
    count += 1
    # We will save the RAW audio bytes instead of the waveform so pickle isn't massive
    data.append({
        "sample_id": f"valid_{idx}",
        "audio_bytes": item.get("audio_filepath", {}).get("bytes"),
        "reference_text": processed["normalized_text"]
    })
    if count % 100 == 0:
        print(f"Dumped {count}")

print(f"Saving {len(data)} samples...")
with open("valid_2169.pkl", "wb") as f:
    pickle.dump(data, f)
print("Done.")
