import os
import time
import requests
import pandas as pd
import soundfile as sf
import io
import jiwer
import gc
import wave
import numpy as np

MAX_ASR_SAMPLES = 50
MAX_TTS_SAMPLES = 10

API_BASE = "http://127.0.0.1:8000"

print("Loading dataset via pandas...")
df_data = pd.read_parquet("https://huggingface.co/api/datasets/PYD4320/audio-text-pair_train-test-dataset-hindi/parquet/default/test/0.parquet")
print(f"Loaded {len(df_data)} samples.")

results = []
tts_tested = 0
asr_count = 0

for idx, row in df_data.iterrows():
    if asr_count >= MAX_ASR_SAMPLES:
        break
        
    sample_id = f"PYD_{asr_count}"
    reference = row['text']
    
    audio_data = row['audio']
    audio_bytes = audio_data['bytes']
    
    # Save temp mp3/wav
    temp_file = f"temp_{asr_count}.mp3"
    with open(temp_file, "wb") as f:
        f.write(audio_bytes)
        
    file_size = os.path.getsize(temp_file)
    
    print(f"[{asr_count+1}/{MAX_ASR_SAMPLES}] Processing ASR...")
    
    start_time = time.time()
    try:
        with open(temp_file, "rb") as f:
            resp = requests.post(f"{API_BASE}/asr", files={"file": (temp_file, f, "audio/mpeg")}, data={"language": "hi"})
        asr_time = time.time() - start_time
        
        if resp.status_code == 200:
            pred = resp.json().get("transcript", "")
            if "[SILENCE DETECTED]" in pred or "[FAILED HINDI ASR]" in pred:
                status = "FAILED"
            else:
                status = "SUCCESS"
        else:
            pred = ""
            status = "API_ERROR"
    except Exception as e:
        asr_time = time.time() - start_time
        pred = str(e)
        status = "ERROR"
        
    os.remove(temp_file)
    
    wer = 1.0
    cer = 1.0
    if status == "SUCCESS" and pred.strip():
        try:
            wer = jiwer.wer(reference, pred)
            cer = jiwer.cer(reference, pred)
        except:
            pass
            
    res = {
        "sample_id": sample_id,
        "reference_hindi": reference,
        "asr_prediction": pred,
        "asr_status": status,
        "asr_time": asr_time,
        "wer": wer,
        "cer": cer,
        "translation": "",
        "translation_time": 0.0,
        "tts_status": "SKIPPED",
        "tts_time": 0.0,
        "tts_sample_rate": 0,
        "tts_channels": 0,
        "tts_frames": 0,
        "tts_duration": 0.0,
        "tts_nonzero_samples": 0,
        "tts_max_amplitude": 0.0,
        "error": ""
    }
    
    if status == "SUCCESS" and wer < 0.5: # only translate good transcriptions
        print(f"[{asr_count+1}] Translating...")
        t_start = time.time()
        try:
            t_resp = requests.post(f"{API_BASE}/translate", json={"text": pred, "source_lang": "hi", "target_lang": "santali"})
            res["translation_time"] = time.time() - t_start
            if t_resp.status_code == 200:
                res["translation"] = t_resp.json().get("translation", "")
            else:
                res["error"] = f"Translation API {t_resp.status_code}"
        except Exception as e:
            res["error"] = str(e)
            
        if res["translation"] and tts_tested < MAX_TTS_SAMPLES:
            print(f"[{asr_count+1}] Running TTS for translation '{res['translation']}'...")
            tts_start = time.time()
            try:
                tts_resp = requests.post(f"{API_BASE}/tts", json={"text": res["translation"], "language": "santali"})
                res["tts_time"] = time.time() - tts_start
                if tts_resp.status_code == 200:
                    audio_bytes = tts_resp.content
                    res["tts_status"] = "SUCCESS"
                    
                    try:
                        import io
                        with wave.open(io.BytesIO(audio_bytes), 'rb') as w:
                            res["tts_sample_rate"] = w.getframerate()
                            res["tts_channels"] = w.getnchannels()
                            res["tts_frames"] = w.getnframes()
                            res["tts_duration"] = res["tts_frames"] / res["tts_sample_rate"]
                        
                        arr, _ = sf.read(io.BytesIO(audio_bytes))
                        res["tts_nonzero_samples"] = np.count_nonzero(arr)
                        res["tts_max_amplitude"] = np.max(np.abs(arr)) if len(arr) > 0 else 0.0
                    except Exception as e:
                        res["error"] = f"WAV parse error: {e}"
                else:
                    res["tts_status"] = "FAILED"
                    res["error"] = f"TTS API {tts_resp.status_code}"
            except Exception as e:
                res["tts_status"] = "ERROR"
                res["error"] = str(e)
            tts_tested += 1
            
    results.append(res)
    asr_count += 1
    gc.collect()

df = pd.DataFrame(results)
df.to_csv("benchmark_results.csv", index=False)
print("Benchmark complete!")
