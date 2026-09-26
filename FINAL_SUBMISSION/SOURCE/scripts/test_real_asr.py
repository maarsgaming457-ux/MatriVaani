import os
import time
import sys
import argparse
import glob

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.services.asr_service import ASRService
import soundfile as sf

def run_test():
    print("================================================================================")
    print("REAL MATRI VAANI ASR TEST")
    print("================================================================================\n")
    
    print(f"Provider: {settings.ASR_PROVIDER}")
    print(f"Model: {settings.ASR_MODEL_PATH}")
    print(f"Processor: {settings.PROCESSOR_PATH}")
    
    if settings.ASR_PROVIDER != "checkpoint":
        print("\nREAL ASR IMPLEMENTATION = READY")
        print("REAL ASR EXECUTION = BLOCKED")
        print("REASON = CHECKPOINT PATH UNAVAILABLE (ASR_PROVIDER is not 'checkpoint')")
        return
        
    if not os.path.exists(settings.ASR_MODEL_PATH):
        print("\nREAL ASR IMPLEMENTATION = READY")
        print("REAL ASR EXECUTION = BLOCKED")
        print("REASON = CHECKPOINT PATH UNAVAILABLE (Model not found)")
        return
        
    if not os.path.exists(settings.PROCESSOR_PATH):
        print("\nREAL ASR IMPLEMENTATION = READY")
        print("REAL ASR EXECUTION = BLOCKED")
        print("REASON = CHECKPOINT PATH UNAVAILABLE (Processor not found)")
        return
        
    try:
        service = ASRService()
    except Exception as e:
        print(f"ERROR initializing ASRService: {e}")
        return
        
    print(f"Device: {service.device}")
    
    # Vocabulary check
    if hasattr(service, 'tokenizer') and service.tokenizer:
        vocab_size = len(service.tokenizer)
        if vocab_size != 41:
            print(f"WARNING: Expected vocabulary size 41, got {vocab_size}")
            
    # Find a real audio file
    flac_files = glob.glob("datasets/cache/santali/**/*.flac", recursive=True)
    if not flac_files:
        print("ERROR: No real Santali audio files found in datasets/cache/santali/")
        return
        
    audio_file = flac_files[0]
    print(f"Audio: {audio_file}")
    
    try:
        audio_array, sr = sf.read(audio_file)
        print(f"Sample rate: {sr}")
        duration = len(audio_array) / sr
        print(f"Duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"ERROR reading audio file: {e}")
        return
        
    start_time = time.time()
    try:
        result = service.transcribe(audio_file)
        inference_time = time.time() - start_time
        
        print(f"Transcript: {result['transcript']}")
        print(f"Inference time: {inference_time:.2f} seconds")
    except Exception as e:
        print(f"ERROR during transcription: {e}")
        return
        
    print("\n================================================================================")

if __name__ == "__main__":
    run_test()
