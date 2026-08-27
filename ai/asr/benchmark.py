import time
import json
import os
import jiwer
import numpy as np
from pathlib import Path
from typing import List
import soundfile as sf
from ai.asr.model_loader import get_asr_model

def benchmark_model(model_name: str, audio_path: str, true_transcript: str, language: str = "hi", num_runs: int = 5):
    """
    Runs a rigorous benchmark for a specific model on a given audio file.
    """
    model = get_asr_model(model_name)
    
    # Measure memory before loading
    mem_before = model.get_memory_usage()
    
    # Measure load time
    start_time = time.time()
    model.load_model()
    load_time_s = time.time() - start_time
    
    # Measure memory after loading
    mem_loaded = model.get_memory_usage()
    model_size_mb = mem_loaded - mem_before
    
    # Get audio duration for RTF
    try:
        audio_info = sf.info(audio_path)
        audio_duration = audio_info.duration
    except Exception:
        audio_duration = 1.0 # fallback
        
    # Measure cold start inference
    start_time = time.time()
    predicted_cold = model.transcribe(audio_path, language=language)
    cold_latency_s = time.time() - start_time
    
    # Measure warm inference (steady-state)
    warm_latencies = []
    mem_peaks = []
    
    predicted = predicted_cold
    
    for _ in range(num_runs):
        start_time = time.time()
        pred = model.transcribe(audio_path, language=language)
        warm_latencies.append(time.time() - start_time)
        mem_peaks.append(model.get_memory_usage())
        predicted = pred
        
    avg_warm_latency_s = np.mean(warm_latencies)
    p95_warm_latency_s = np.percentile(warm_latencies, 95)
    peak_ram_mb = max(mem_peaks)
    
    # Calculate RTF (Real-Time Factor)
    real_time_factor = avg_warm_latency_s / audio_duration if audio_duration > 0 else 0
    
    # Calculate WER and CER
    wer = jiwer.wer(true_transcript, predicted)
    cer = jiwer.cer(true_transcript, predicted)
    
    result = {
        "model": model.model_name,
        "version": model.version,
        "language": language,
        "dataset": "PATH A (Hindi Sample)",
        "dataset_version": "v1.0",
        "samples": 1,
        "wer": float(wer),
        "cer": float(cer),
        "latency_ms": round(avg_warm_latency_s * 1000, 2),
        "cold_start_latency_ms": round(cold_latency_s * 1000, 2),
        "p95_latency_ms": round(p95_warm_latency_s * 1000, 2),
        "load_time_ms": round(load_time_s * 1000, 2),
        "real_time_factor": round(real_time_factor, 2),
        "ram_mb": round(mem_loaded, 2),
        "peak_ram_mb": round(peak_ram_mb, 2),
        "model_size_mb": round(model_size_mb, 2)
    }
    return result

def save_result_to_dirs(res: dict, base_dir: str):
    root = Path(base_dir)
    acc_dir = root / "evaluation" / "accuracy" / "asr"
    lat_dir = root / "evaluation" / "latency" / "asr"
    mem_dir = root / "evaluation" / "memory" / "asr"
    
    for d in [acc_dir, lat_dir, mem_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    filename = f"{res['model'].replace('/', '_')}_benchmark.json"
    
    # Save full result to all for now (they act as logs)
    with open(acc_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    with open(lat_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    with open(mem_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)

def run_benchmarks(models: List[str], audio_path: str, true_transcript: str, language: str, project_root: str):
    results = []
    
    for m in models:
        try:
            print(f"Benchmarking {m}...")
            res = benchmark_model(m, audio_path, true_transcript, language)
            results.append(res)
            save_result_to_dirs(res, project_root)
            print(f"Completed {m}")
        except Exception as e:
            print(f"Error benchmarking {m}: {e}")
            
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--lang", required=True)
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    
    run_benchmarks(args.models, args.audio, args.transcript, args.lang, args.root)
