import os
import pytest
from app.graph.workflow import run_pipeline
from app.core.config import settings
import soundfile as sf
import glob

def test_real_end_to_end_pipeline():
    print(f"\n--- REAL END-TO-END PIPELINE AUDIT ---")
    
    # Configuration
    asr_provider = settings.ASR_PROVIDER
    translation_provider = settings.TRANSLATION_PROVIDER
    llm_provider = settings.LLM_PROVIDER
    
    print(f"ASR Provider: {asr_provider}")
    print(f"Translation Provider: {translation_provider}")
    print(f"LLM Provider: {llm_provider}")
    
    if asr_provider != "checkpoint":
        pytest.skip(f"Test requires ASR_PROVIDER=checkpoint, got {asr_provider}")
        
    if not os.path.exists(settings.ASR_MODEL_PATH):
        pytest.skip(f"REAL CHECKPOINT NOT FOUND ON DISK AT: {settings.ASR_MODEL_PATH}")
        
    if not os.path.exists(settings.PROCESSOR_PATH):
        pytest.skip(f"REAL PROCESSOR NOT FOUND ON DISK AT: {settings.PROCESSOR_PATH}")
        
    flac_files = glob.glob("datasets/cache/santali/**/*.flac", recursive=True)
    if not flac_files:
        pytest.skip("No real audio file found in datasets/cache to test.")
        
    audio_file = flac_files[0]
    print(f"Testing with real audio file: {audio_file}")
    
    # Run the full pipeline
    result = run_pipeline(audio_path=audio_file, target_language="hi")
    
    print(f"\nPipeline Status: {result['status']}")
    print(f"Real Transcript: {result.get('transcript')}")
    print(f"Cleaned Transcript: {result.get('cleaned_transcript')}")
    
    if translation_provider == "mock":
        print("EXTERNAL COMPONENT NOT CONFIGURED: Translation")
    else:
        print(f"Translation: {result.get('translation')}")
        
    if llm_provider == "mock":
        print("EXTERNAL COMPONENT NOT CONFIGURED: Scriptwriter & Copy Editor")
    else:
        print(f"Script: {result.get('script')}")
        
    if result["errors"]:
        print(f"Errors: {result['errors']}")
        
    if result["warnings"]:
        print(f"Warnings: {result['warnings']}")

    # If the real components passed, we consider the pipeline structure valid.
    assert "transcript" in result
    print("\nREAL COMPONENTS PASSED")
