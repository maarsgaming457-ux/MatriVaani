import os
import pytest
from app.services.asr_service import ASRService
from app.core.config import settings
from app.core.exceptions import ASRError

def test_real_asr_initialization():
    print(f"\nMODEL PATH: {settings.ASR_MODEL_PATH}")
    print(f"PROCESSOR PATH: {settings.PROCESSOR_PATH}")
    print(f"ASR PROVIDER: {settings.ASR_PROVIDER}")
    
    # Check if the checkpoint actually exists locally
    if not os.path.exists(settings.ASR_MODEL_PATH):
        print(f"REAL CHECKPOINT NOT FOUND ON DISK AT: {settings.ASR_MODEL_PATH}")
        pytest.skip(f"Real checkpoint {settings.ASR_MODEL_PATH} not found. Ensure the Google Drive is mounted or the checkpoint is downloaded.")
        
    if not os.path.exists(settings.PROCESSOR_PATH):
        print(f"REAL PROCESSOR NOT FOUND ON DISK AT: {settings.PROCESSOR_PATH}")
        pytest.skip(f"Real processor {settings.PROCESSOR_PATH} not found.")

    try:
        service = ASRService()
        print(f"DEVICE: {service.device}")
        
        # Test with a real audio file if available
        # Find one in cache
        sample_audio = "datasets/cache/santali/train/train_0.flac"
        # Since I don't know the exact name of the file in cache, let's just search for any flac
        import glob
        flac_files = glob.glob("datasets/cache/santali/**/*.flac", recursive=True)
        if flac_files:
            audio_file = flac_files[0]
            print(f"AUDIO FILE: {audio_file}")
            
            # Read to get duration and sample rate
            import soundfile as sf
            audio_array, sr = sf.read(audio_file)
            print(f"AUDIO SAMPLE RATE: {sr}")
            print(f"AUDIO DURATION: {len(audio_array)/sr} seconds")
            
            result = service.transcribe(audio_file)
            print(f"TRANSCRIPT: {result['transcript']}")
            assert result['transcript']
        else:
            print("No real audio file found in datasets/cache to test.")
    except Exception as e:
        print(f"ASR inference failed: {e}")
        raise
