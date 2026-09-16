import os
import sys
import glob

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.graph.workflow import run_pipeline

def run_real_pipeline():
    print("================================================")
    print("MATRIVAANI: FULL PIPELINE EXECUTION DEMO")
    print("================================================")
    
    # Configuration
    print(f"ASR Provider: {settings.ASR_PROVIDER}")
    print(f"Translation Provider: {settings.TRANSLATION_PROVIDER}")
    print(f"Scriptwriter Provider: {settings.LLM_PROVIDER}")
    print(f"Copy Editor Provider: {settings.LLM_PROVIDER}\n")
    
    # Verify ASR
    if settings.ASR_PROVIDER == "checkpoint":
        if not os.path.exists(settings.ASR_MODEL_PATH) or not os.path.exists(settings.PROCESSOR_PATH):
            print("ERROR: ASR_PROVIDER=checkpoint but checkpoint/processor not found locally.")
            print(f"Model Path: {settings.ASR_MODEL_PATH}")
            print(f"Processor Path: {settings.PROCESSOR_PATH}")
            return
            
    # Find audio file
    flac_files = glob.glob("datasets/cache/santali/**/*.flac", recursive=True)
    if not flac_files:
        print("ERROR: No demo audio file found in datasets/cache/santali/")
        return
        
    audio_file = flac_files[0]
    print(f"Using Audio File: {audio_file}\n")
    
    print("Executing Pipeline...")
    
    result = run_pipeline(audio_path=audio_file, target_language="hi")
    
    print("\n================================================")
    print("PIPELINE RESULTS")
    print("================================================")
    print(f"Status: {result.get('status')}")
    print(f"Santali Transcript:\n{result.get('transcript', '')}\n")
    print(f"Cleaned Transcript:\n{result.get('cleaned_transcript', '')}\n")
    
    if settings.TRANSLATION_PROVIDER != "mock":
        print("TRANSLATION (REAL):")
    else:
        print("TRANSLATION (MOCK):")
    print(f"{result.get('translation', '')}\n")
        
    if settings.LLM_PROVIDER != "mock":
        print("SCRIPTWRITER (REAL):")
    else:
        print("SCRIPTWRITER (MOCK):")
    script = result.get("script", "")
    print(f"{script}\n")
        
    if settings.LLM_PROVIDER != "mock":
        print("COPY EDITOR (REAL):")
    else:
        print("COPY EDITOR (MOCK):")
    print(f"{result.get('final_script', '')}\n")
    
    print("NODE STATUS:")
    for node, status in result.get('metadata', {}).get('node_status', {}).items():
        print(f" - {node}: {status}")
        
    if result.get("warnings"):
        print("\nWARNINGS:")
        for w in result["warnings"]:
            print(f" - {w}")
            
    if result.get("errors"):
        print("\nERRORS:")
        for e in result["errors"]:
            print(f" - {e}")
            
    print("================================================")

if __name__ == "__main__":
    run_real_pipeline()
