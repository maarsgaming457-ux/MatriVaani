import httpx
import time

try:
    print("Testing /tts endpoint...")
    
    start = time.time()
    response = httpx.post("http://127.0.0.1:8000/tts", json={
        "text": "???",
        "language": "santali"
    }, timeout=120.0)
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        audio_bytes = response.content
        print(f"Received bytes: {len(audio_bytes)}")
        
        with open("fastapi_test_output.wav", "wb") as f:
            f.write(audio_bytes)
            
        import wave
        with wave.open("fastapi_test_output.wav", "rb") as w:
            print(f"Channels: {w.getnchannels()}")
            print(f"Framerate: {w.getframerate()}")
            print(f"Frames: {w.getnframes()}")
            
        import soundfile as sf
        import numpy as np
        data, sr = sf.read("fastapi_test_output.wav")
        max_amp = np.max(np.abs(data))
        print(f"Max amp: {max_amp}")
        if max_amp > 0:
            print("SUCCESS: Endpoint returned valid non-zero WAV audio")
        else:
            print("FAILED: Endpoint returned silent audio")
    else:
        print(f"FAILED: Endpoint returned error {response.text}")
        
    print(f"Time taken: {time.time() - start:.2f} seconds")
except Exception as e:
    print(f"FAILED: {e}")
