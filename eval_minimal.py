import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import json
import torch
import pandas as pd
import io
import soundfile as sf
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

print("Loading processor and model...")
processor = Wav2Vec2Processor.from_pretrained("models/checkpoint-1500")
model = Wav2Vec2ForCTC.from_pretrained("models/checkpoint-1500")
print("Moving to device...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

print("Loading dataset...")
df = pd.read_parquet("datasets/cache/santali/valid.parquet")

results = []
count = 0
for idx, row in df.iterrows():
    if count >= 2169: break
    
    text = str(row.get("text", ""))
    if not text.strip() or row.get("lang") != "sat": continue
    
    audio_bytes = row.get("audio_filepath", {}).get("bytes")
    if not audio_bytes: continue
    
    try:
        with io.BytesIO(audio_bytes) as f:
            waveform, sr = sf.read(f)
        if len(waveform.shape) > 1:
            waveform = waveform.mean(axis=1)
        if sr != 16000:
            waveform = librosa.resample(waveform, orig_sr=sr, target_sr=16000)
            sr = 16000
            
        inputs = processor(waveform, sampling_rate=sr, return_tensors="pt").to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
        pred = processor.batch_decode(torch.argmax(logits, dim=-1))[0]
        results.append({"idx": idx, "ref": text, "pred": pred})
        count += 1
        if count % 100 == 0: print(f"Done {count}")
    except Exception as e:
        print("Error:", e)

with open("raw_preds.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False)
print("Finished.")
