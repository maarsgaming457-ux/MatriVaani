import time
import psutil
import os
import gc
import json
import numpy as np
import soundfile as sf
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ai.asr.model_loader import get_asr_model

def get_ram_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def run_memory_profile(model_name: str, audio_path: str, quantize_int8: bool = False, language: str = "sat"):
    gc.collect()
    ram_base = get_ram_mb()
    
    print(f"Loading {model_name} (quantize={quantize_int8}, lang={language})...")
    
    try:
        model = get_asr_model(model_name)
        
        start_load = time.time()
        model.load_model(language=language, quantize_int8=quantize_int8)
        load_time = time.time() - start_load
        
        ram_loaded = get_ram_mb()
        model_ram_footprint = ram_loaded - ram_base
        
        print(f"Transcribing {audio_path}...")
        start_inf = time.time()
        predicted = model.transcribe(audio_path, language=language, quantize_int8=quantize_int8)
        inf_time = time.time() - start_inf
        
        ram_peak = get_ram_mb()
        inf_ram_spike = ram_peak - ram_loaded
        
        # Try to free memory
        del model
        gc.collect()
        ram_after = get_ram_mb()
        
        profile = {
            "model": model_name,
            "quantize_int8": quantize_int8,
            "language": language,
            "status": "VERIFIED",
            "base_python_ram_mb": round(ram_base, 2),
            "model_load_ram_mb": round(model_ram_footprint, 2),
            "inference_spike_ram_mb": round(inf_ram_spike, 2),
            "peak_total_ram_mb": round(ram_peak, 2),
            "post_inference_retention_ram_mb": round(ram_after, 2),
            "load_time_s": round(load_time, 2),
            "inference_time_s": round(inf_time, 2)
        }
    except Exception as e:
        print(f"Error during {model_name} quant={quantize_int8}: {e}")
        profile = {
            "model": model_name,
            "quantize_int8": quantize_int8,
            "language": language,
            "status": "FAILED",
            "error": str(e)
        }
        
    return profile

if __name__ == "__main__":
    audio_path = "test_audio.wav"
    from scripts.run_real_benchmark import generate_dummy_audio
    generate_dummy_audio(audio_path, 3)
    
    profiles = []
    
    # Test MMS 1B FP32 (Santhali)
    profiles.append(run_memory_profile("facebook/mms-1b-all", audio_path, False, language="sat"))
    # Test MMS 1B INT8 (Santhali)
    profiles.append(run_memory_profile("facebook/mms-1b-all", audio_path, True, language="sat"))

    
    out_dir = Path("evaluation/memory/asr")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "memory_profile.json", "w") as f:
        json.dump(profiles, f, indent=4)
        
    print("Memory profiling complete.")
