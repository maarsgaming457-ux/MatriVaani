import torch
import soundfile as sf
import numpy as np
from ai.asr.model_loader import get_asr_model
import time

def chunked_transcribe(model_name: str, audio_path: str, chunk_duration_sec: int = 3, language: str = "hi", quantize_int8: bool = True):
    """
    Transcribes audio by breaking it into smaller chunks to limit memory footprint.
    """
    model = get_asr_model(model_name)
    model.load_model(language=language, quantize_int8=quantize_int8)
    
    waveform, sample_rate = sf.read(audio_path, dtype='float32')
    
    chunk_samples = chunk_duration_sec * sample_rate
    total_samples = len(waveform)
    
    transcriptions = []
    start_time = time.time()
    
    import psutil, os
    mem_peaks = []
    
    for i in range(0, total_samples, chunk_samples):
        chunk = waveform[i:i+chunk_samples]
        
        # Save temporary chunk
        chunk_path = f"temp_chunk_{i}.wav"
        sf.write(chunk_path, chunk, sample_rate)
        
        mem_peaks.append(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024))
        
        # Transcribe chunk
        text = model.transcribe(chunk_path, language=language)
        transcriptions.append(text)
        
        os.remove(chunk_path)
        
    total_time = time.time() - start_time
    peak_ram = max(mem_peaks) if mem_peaks else 0
    
    return {
        "transcription": " ".join(transcriptions),
        "total_time_s": round(total_time, 2),
        "peak_chunking_ram_mb": round(peak_ram, 2)
    }
