import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from dotenv import load_dotenv
load_dotenv()

import time
import pandas as pd
import soundfile as sf
import io
import jiwer
import gc
import wave
import numpy as np
import librosa

from app.services.asr_service import ASRService
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService

MAX_ASR_SAMPLES = 25
MAX_TTS_SAMPLES = 2
MAX_DURATION = 5.0 # Max 5 seconds audio to speed up TTS

print("Initializing models...")
asr = ASRService()
trans = TranslationService()
tts = TTSService()

df_data = pd.read_csv("dev.tsv", sep="\t", header=None, names=["id", "file", "text", "text_normalized", "audio_path", "unknown1", "unknown2"])

results = []
tts_tested = 0
asr_count = 0

for idx, row in df_data.iterrows():
    if asr_count >= MAX_ASR_SAMPLES:
        break
        
    wav_file = os.path.join("fleurs_hi", "dev", row['file'])
    
    if not os.path.exists(wav_file):
        continue
        
    try:
        duration = librosa.get_duration(path=wav_file)
    except Exception as e:
        duration = 999
        
    if duration > MAX_DURATION:
        continue
        
    sample_id = f"FLEURS_{row['file']}"
    reference = str(row['text'])
    
    print(f"\n--- [{asr_count+1}/{MAX_ASR_SAMPLES}] {row['file']} ({duration:.2f}s) ---")
    
    start_time = time.time()
    try:
        asr_res = asr.transcribe(wav_file, language="hi")
        asr_time = time.time() - start_time
        pred = asr_res.get("transcript", "")
        if "[SILENCE DETECTED]" in pred or "[FAILED HINDI ASR]" in pred:
            status = "FAILED"
        else:
            status = "SUCCESS"
    except Exception as e:
        asr_time = time.time() - start_time
        pred = str(e)
        status = "ERROR"
        
    wer = 1.0
    cer = 1.0
    if status == "SUCCESS" and pred.strip():
        try:
            wer = jiwer.wer(reference, pred)
            cer = jiwer.cer(reference, pred)
        except:
            pass
            
    print(f"Ref:  {reference}")
    print(f"Pred: {pred} (WER: {wer:.2f})")
            
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
    
    if status == "SUCCESS" and wer < 0.6: 
        t_start = time.time()
        try:
            translation = trans.translate(pred, source_lang="hi", target_lang="santali")
            res["translation_time"] = time.time() - t_start
            res["translation"] = translation
            print(f"Translation: {translation}")
        except Exception as e:
            res["error"] = str(e)
            
        if res["translation"] and tts_tested < MAX_TTS_SAMPLES:
            print(f"Running TTS...")
            tts_start = time.time()
            try:
                audio_bytes = tts.synthesize(res["translation"], language="santali")
                res["tts_time"] = time.time() - tts_start
                if len(audio_bytes) > 0:
                    res["tts_status"] = "SUCCESS"
                    try:
                        with wave.open(io.BytesIO(audio_bytes), 'rb') as w:
                            res["tts_sample_rate"] = w.getframerate()
                            res["tts_channels"] = w.getnchannels()
                            res["tts_frames"] = w.getnframes()
                            res["tts_duration"] = res["tts_frames"] / res["tts_sample_rate"]
                        
                        arr, _ = sf.read(io.BytesIO(audio_bytes))
                        res["tts_nonzero_samples"] = np.count_nonzero(arr)
                        res["tts_max_amplitude"] = np.max(np.abs(arr)) if len(arr) > 0 else 0.0
                        print(f"TTS SUCCESS: Duration {res['tts_duration']:.2f}s, Max Amp {res['tts_max_amplitude']:.4f}")
                    except Exception as e:
                        res["error"] = f"WAV parse error: {e}"
                else:
                    res["tts_status"] = "FAILED"
                    res["error"] = "Empty TTS bytes"
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
