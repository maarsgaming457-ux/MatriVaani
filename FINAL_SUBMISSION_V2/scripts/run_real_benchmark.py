import os
import sys
import numpy as np
import soundfile as sf
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai.asr.benchmark import run_benchmarks

def generate_dummy_audio(path: str, duration_sec: int = 3, sample_rate: int = 16000):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    # 440 Hz sine wave
    samples = 0.5 * np.sin(2 * np.pi * 440 * t)
    sf.write(path, samples.astype(np.float32), sample_rate)

if __name__ == "__main__":
    audio_path = "test_audio.wav"
    generate_dummy_audio(audio_path)
    
    # We will test whisper-tiny and mms-1b-all
    models = ["openai/whisper-tiny", "facebook/mms-1b-all"]
    true_transcript = "नमस्ते दुनिया" # Hello world
    
    print("Starting rigorous benchmark on generated audio...")
    project_root = str(Path(__file__).parent.parent)
    
    # Note: Downloading models might take a few minutes.
    run_benchmarks(models, audio_path, true_transcript, language="hi", project_root=project_root)
    
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    print("Rigorous benchmark completed.")
