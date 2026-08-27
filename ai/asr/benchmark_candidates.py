import os
import sys
import time
import psutil
import json
import threading
from pathlib import Path
import torch
import torchaudio

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def get_process_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def profile_model(model_id: str, audio_path: str, quantize_int8: bool = False):
    print(f"--- Profiling {model_id} (INT8={quantize_int8}) ---")
    
    # 1. Base Memory
    mem_base = get_process_memory_mb()
    
    # 2. Load Model
    start_load = time.time()
    
    if "whisper" in model_id.lower():
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        processor = WhisperProcessor.from_pretrained(model_id)
        model = WhisperForConditionalGeneration.from_pretrained(model_id)
    else:
        # Wav2Vec2 Base (No CTC head for raw base model, so use base model class)
        from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
        processor = Wav2Vec2FeatureExtractor.from_pretrained(model_id)
        model = Wav2Vec2Model.from_pretrained(model_id)

    model.eval()
    
    mem_after_load = get_process_memory_mb()
    load_time = time.time() - start_load
    
    # 3. Quantization
    mem_peak_during_quant = mem_after_load
    if quantize_int8:
        print("  Applying INT8 Dynamic Quantization...")
        
        # Track memory specifically during quantization
        peak_q_mem = [mem_after_load]
        stop_thread = False
        def monitor_mem():
            while not stop_thread:
                peak_q_mem[0] = max(peak_q_mem[0], get_process_memory_mb())
                time.sleep(0.01)
        
        t = threading.Thread(target=monitor_mem)
        t.start()
        
        # In PyTorch, linear layers are standard for dynamic quantization
        model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        
        stop_thread = True
        t.join()
        mem_peak_during_quant = peak_q_mem[0]

    mem_after_quant = get_process_memory_mb()
    
    # 4. Inference
    import soundfile as sf
    waveform, sample_rate = sf.read(audio_path)
    if waveform.ndim > 1:
        waveform = waveform[:, 0]
    
    if sample_rate != 16000:
        import librosa
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)
    
    audio_input = waveform
    
    if "whisper" in model_id.lower():
        inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt")
    else:
        inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt")
        
    start_infer = time.time()
    
    # Monitor peak RAM during inference
    peak_inf_mem = [mem_after_quant]
    stop_inf_thread = False
    def monitor_inf_mem():
        while not stop_inf_thread:
            peak_inf_mem[0] = max(peak_inf_mem[0], get_process_memory_mb())
            time.sleep(0.01)
            
    t_inf = threading.Thread(target=monitor_inf_mem)
    t_inf.start()
    
    with torch.no_grad():
        if "whisper" in model_id.lower():
            # For conditional generation, we just generate
            _ = model.generate(inputs["input_features"])
        else:
            # Wav2vec2 base forward
            _ = model(**inputs)
            
    stop_inf_thread = True
    t_inf.join()
    
    infer_time = time.time() - start_infer
    mem_after_infer = get_process_memory_mb()
    
    result = {
        "model": model_id,
        "quantize_int8": quantize_int8,
        "base_python_ram_mb": round(mem_base, 2),
        "post_load_ram_mb": round(mem_after_load, 2),
        "peak_quantization_ram_mb": round(mem_peak_during_quant, 2),
        "post_quantization_ram_mb": round(mem_after_quant, 2),
        "peak_inference_ram_mb": round(peak_inf_mem[0], 2),
        "post_inference_ram_mb": round(mem_after_infer, 2),
        "load_time_s": round(load_time, 2),
        "inference_time_s": round(infer_time, 2)
    }
    
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    audio_test = "test_audio.wav"
    # Create dummy audio if it doesn't exist
    if not os.path.exists(audio_test):
        import numpy as np
        import soundfile as sf
        print(f"Creating dummy {audio_test}...")
        sf.write(audio_test, np.zeros(16000 * 5), 16000)  # 5 seconds of silence
        
    model_id = sys.argv[1]
    quantize_int8 = sys.argv[2] == "True" if len(sys.argv) > 2 else False
    
    out_dir = Path("evaluation/memory/asr/candidate_results")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    result = profile_model(model_id, audio_test, quantize_int8=quantize_int8)
    
    out_file = out_dir / f"{model_id.replace('/', '_')}_int8_{quantize_int8}.json"
    with open(out_file, "w") as f:
        json.dump(result, f, indent=4)
