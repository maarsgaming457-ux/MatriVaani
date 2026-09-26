import time
import json
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from ai.asr.streaming import chunked_transcribe
from scripts.run_real_benchmark import generate_dummy_audio

if __name__ == "__main__":
    audio_path = "test_audio_long.wav"
    # Generate 10 seconds of audio
    generate_dummy_audio(audio_path, duration_sec=10)
    
    results = []
    
    # 1. MMS FP32 Normal (No chunking)
    from ai.asr.memory_profiler import run_memory_profile
    print("Running Normal Inference FP32...")
    res_normal = run_memory_profile("facebook/mms-1b-all", audio_path, quantize_int8=False)
    results.append({"type": "Normal FP32", "data": res_normal})
    
    # 2. MMS FP32 Streaming
    print("Running Chunked Streaming FP32...")
    res_stream = chunked_transcribe("facebook/mms-1b-all", audio_path, chunk_duration_sec=2, quantize_int8=False)
    results.append({"type": "Chunked FP32 (2s)", "data": res_stream})
    
    out_dir = Path("evaluation/memory/asr")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "streaming.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("Streaming profiling complete.")
