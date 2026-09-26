import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

import time
import pandas as pd
import jiwer
import gc
import re
import string
import httpx

from app.services.asr_service import ASRService
import librosa

def normalize_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation + '?|'))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("Initializing ASR Service...")
asr = ASRService()

df_data = pd.read_csv("dev.tsv", sep="\t", header=None, names=["id", "file", "text", "text_normalized", "audio_path", "unknown1", "unknown2"])

results = []
valid_samples = 0
excluded_samples = 0
successful_asr = 0
failed_asr = 0
silent_samples = 0
empty_predictions = 0
timeout_count = 0
api_error_count = 0

for idx, row in df_data.iterrows():
    wav_file = os.path.join("fleurs_hi", "dev", row['file'])
    
    if not os.path.exists(wav_file):
        excluded_samples += 1
        continue
        
    try:
        duration = librosa.get_duration(path=wav_file)
        valid_samples += 1
    except Exception as e:
        excluded_samples += 1
        continue
        
    sample_id = f"FLEURS_{row['file']}"
    reference = str(row['text'])
    
    print(f"[{valid_samples}] Processing {sample_id} ({duration:.2f}s)")
    
    start_time = time.time()
    try:
        asr_res = asr.transcribe(wav_file, language="hi")
        asr_time = time.time() - start_time
        pred = asr_res.get("transcript", "").strip()
        status = "SUCCESS"
        error = ""
        
        if "[SILENCE DETECTED]" in pred:
            status = "SILENT"
            silent_samples += 1
            pred = ""
        elif "[FAILED HINDI ASR]" in pred:
            status = "FAILED"
            failed_asr += 1
        elif not pred:
            status = "EMPTY"
            empty_predictions += 1
        else:
            successful_asr += 1
            
    except Exception as e:
        asr_time = time.time() - start_time
        pred = ""
        error = str(e)
        if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 429:
            print("Rate limit hit, sleeping for 60s...")
            time.sleep(60)
            try:
                start_time = time.time()
                asr_res = asr.transcribe(wav_file, language="hi")
                asr_time = time.time() - start_time
                pred = asr_res.get("transcript", "").strip()
                status = "SUCCESS"
                if "[SILENCE DETECTED]" in pred:
                    status = "SILENT"
                    silent_samples += 1
                    pred = ""
                elif "[FAILED HINDI ASR]" in pred:
                    status = "FAILED"
                    failed_asr += 1
                elif not pred:
                    status = "EMPTY"
                    empty_predictions += 1
                else:
                    successful_asr += 1
            except Exception as e2:
                status = "API_ERROR"
                api_error_count += 1
                error = str(e2)
        elif "timeout" in error.lower():
            status = "TIMEOUT"
            timeout_count += 1
        else:
            status = "API_ERROR"
            api_error_count += 1
            
    wer = 1.0
    cer = 1.0
    error_cat = ""
    
    if status == "SUCCESS" and pred:
        ref_norm = normalize_text(reference)
        pred_norm = normalize_text(pred)
        if ref_norm and pred_norm:
            try:
                wer = jiwer.wer(ref_norm, pred_norm)
                cer = jiwer.cer(ref_norm, pred_norm)
            except:
                pass
        
        if wer > 0.0:
            if re.search(r'[a-zA-Z]', pred):
                error_cat = "English/Hinglish"
            elif len(pred_norm.split()) < len(ref_norm.split()):
                error_cat = "Missing words"
            elif len(pred_norm.split()) > len(ref_norm.split()):
                error_cat = "Extra words"
            else:
                error_cat = "Word substitution"
                
    elif status != "SUCCESS":
        error_cat = status
        
    res = {
        "sample_id": sample_id,
        "reference_hindi": reference,
        "prediction_hindi": pred,
        "audio_duration": duration,
        "asr_latency": asr_time,
        "status": status,
        "WER": wer,
        "CER": cer,
        "error_category": error_cat,
        "error": error
    }
            
    results.append(res)
    gc.collect()
    
    time.sleep(1.0) 

df = pd.DataFrame(results)
df.to_csv("ASR_5000_RESULTS.csv", index=False)
print("Benchmark CSV saved.")

md = []
md.append("# MatriVaani Final Hindi ASR Benchmark Report\n")
md.append("## DATASET\n---------")
md.append(f"Available: {len(df_data)}")
md.append(f"Tested: {valid_samples}")
md.append(f"Excluded: {excluded_samples}\n")

md.append("## ASR\n---------")
md.append(f"Successful: {successful_asr}")
md.append(f"Failed: {failed_asr}")
md.append(f"Silent: {silent_samples}")
md.append(f"Empty: {empty_predictions}")
md.append(f"Timeout: {timeout_count}")
md.append(f"API errors: {api_error_count}\n")

if successful_asr > 0:
    success_df = df[df['status'] == 'SUCCESS']
    overall_wer = success_df['WER'].mean()
    overall_cer = success_df['CER'].mean()
    exact_match = len(success_df[success_df['WER'] == 0.0]) / len(success_df) * 100
    usable = len(success_df[success_df['WER'] <= 0.4]) / len(success_df) * 100
    
    avg_latency = success_df['asr_latency'].mean()
    med_latency = success_df['asr_latency'].median()
    p95_latency = success_df['asr_latency'].quantile(0.95)
    max_latency = success_df['asr_latency'].max()
    
    md.append("## ACCURACY\n---------")
    md.append(f"WER: {overall_wer:.4f}")
    md.append(f"CER: {overall_cer:.4f}")
    md.append(f"Exact match: {exact_match:.2f}%")
    md.append(f"Usable recognition: {usable:.2f}%\n")
    
    md.append("## LATENCY\n---------")
    md.append(f"Average: {avg_latency:.4f}s")
    md.append(f"Median: {med_latency:.4f}s")
    md.append(f"P95: {p95_latency:.4f}s")
    md.append(f"Maximum: {max_latency:.4f}s\n")
    
    md.append("## ERROR ANALYSIS\n---------")
    md.append("Top 5 failure categories:")
    counts = success_df[success_df['error_category'] != '']['error_category'].value_counts().head(5)
    for cat, count in counts.items():
        md.append(f"- {cat}: {count}")
    md.append("\n")
    
    verdict = "YES" if usable > 80.0 else "NEEDS IMPROVEMENT"
    md.append("## FINAL ASSESSMENT\n---------")
    md.append(f"Is Hindi ASR reliable enough for MatriVaani?\n{verdict}\n")
    md.append(f"Explanation: Out of {valid_samples} samples, the system successfully recognized {usable:.2f}% of them with a WER <= 0.40. The average WER was {overall_wer:.4f}.")
else:
    md.append("## FINAL ASSESSMENT\n---------")
    md.append("Is Hindi ASR reliable enough for MatriVaani?\nNO\n")
    md.append("Explanation: 0 successful transcriptions.")

with open("ASR_5000_FINAL_REPORT.md", "w", encoding='utf-8') as f:
    f.write("\n".join(md))

print("Report saved.")
