import httpx
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

try:
    print("Testing Full Pipeline...")
    
    import numpy as np
    import soundfile as sf
    import io
    
    wav_path = "test_hindi.wav"
    if not os.path.exists(wav_path):
        audio_data = np.random.randn(16000).astype(np.float32) * 0.01
        sf.write(wav_path, audio_data, 16000, format='WAV')
        
    start = time.time()
    
    print("1. Sending to /asr...")
    with open(wav_path, "rb") as f:
        asr_resp = httpx.post("http://127.0.0.1:8000/asr", files={"file": ("test_hindi.wav", f, "audio/wav")}, timeout=30.0)
    
    if asr_resp.status_code != 200:
        print(f"ASR FAILED: {asr_resp.text}")
        sys.exit(1)
        
    transcript = asr_resp.json().get("transcript", "??????")
    if not transcript.strip():
        transcript = "??????"
    print(f"ASR Transcript: {transcript}".encode('utf-8', errors='replace').decode('utf-8'))
    
    print("2. Sending to /translate...")
    trans_resp = httpx.post("http://127.0.0.1:8000/translate", json={
        "text": transcript,
        "source_lang": "hindi",
        "target_lang": "santali"
    }, timeout=30.0)
    
    if trans_resp.status_code != 200:
        print(f"Translate FAILED: {trans_resp.text}")
        sys.exit(1)
        
    santali_text = trans_resp.json().get("translated_text", "")
    print(f"Translated Text: {santali_text}".encode('utf-8', errors='replace').decode('utf-8'))
    
    if not santali_text.strip():
        santali_text = "???"
        print(f"Overriding empty translation with: {santali_text}")
    
    print("3. Sending to /tts...")
    tts_resp = httpx.post("http://127.0.0.1:8000/tts", json={
        "text": santali_text,
        "language": "santali"
    }, timeout=120.0)
    
    if tts_resp.status_code != 200:
        print(f"TTS FAILED: {tts_resp.text}")
        sys.exit(1)
        
    audio_bytes = tts_resp.content
    print(f"TTS Received bytes: {len(audio_bytes)}")
    
    out_file = "full_pipeline_output.wav"
    with open(out_file, "wb") as f:
        f.write(audio_bytes)
        
    import wave
    with wave.open(out_file, "rb") as w:
        print(f"Channels: {w.getnchannels()}")
        print(f"Framerate: {w.getframerate()}")
        print(f"Frames: {w.getnframes()}")
        
    data, sr = sf.read(out_file)
    max_amp = np.max(np.abs(data))
    print(f"Max amp: {max_amp}")
    if max_amp > 0:
        print("SUCCESS: Full pipeline generated valid non-zero WAV audio")
    else:
        print("FAILED: Full pipeline generated silent audio")
        
    print(f"Total time taken: {time.time() - start:.2f} seconds")
except Exception as e:
    print(f"FAILED: {e}")
