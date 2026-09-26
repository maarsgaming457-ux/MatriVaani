import sys
import os
import soundfile as sf
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.services.asr_service import ASRService
from app.core.config import settings

def create_dummy_wav(path):
    # 1 second of silence/noise
    data = np.random.uniform(-0.1, 0.1, 16000).astype(np.float32)
    sf.write(path, data, 16000)

def main():
    dummy_wav = "test_dummy.wav"
    create_dummy_wav(dummy_wav)
    
    print("Testing ASRService initialization...")
    asr = ASRService()
    
    print("\nTest A (Santali routing):")
    try:
        # Should attempt to load Santali model
        # If it fails because the santali model is missing locally, that's fine, we catch it.
        # But we want to see it try.
        asr.transcribe(dummy_wav, "santali")
    except Exception as e:
        print(f"Santali Error: {e}")
        
    print("\nTest F (Ho missing path error):")
    settings.HO_ASR_MODEL_PATH = "invalid/path/ho"
    settings.HO_ASR_PROCESSOR_PATH = "invalid/path/ho"
    try:
        asr.transcribe(dummy_wav, "ho")
        print("FAIL: Ho should have thrown an error.")
    except Exception as e:
        print(f"EXPECTED Ho Error: {e}")
        
    if os.path.exists(dummy_wav):
        os.remove(dummy_wav)
        
if __name__ == '__main__':
    main()
