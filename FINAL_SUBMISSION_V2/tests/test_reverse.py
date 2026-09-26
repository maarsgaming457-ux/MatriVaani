import requests
import json
import time
import subprocess
import os

print("Starting FastAPI server...")
server = subprocess.Popen([".\\\\venv\\\\Scripts\\\\python", "-m", "uvicorn", "app.api.main:app", "--port", "8000"])

time.sleep(5) # Wait for server to start

try:
    print("Testing Health...")
    r = requests.get("http://localhost:8000/health")
    print(r.json())

    # Create dummy wav file
    print("Creating dummy wav file...")
    import soundfile as sf
    import numpy as np
    sf.write("dummy_hi.wav", np.zeros(16000, dtype=np.float32), 16000)

    print("Testing ASR (Hindi)...")
    with open("dummy_hi.wav", "rb") as f:
        r = requests.post("http://localhost:8000/asr", files={"file": f}, data={"language": "hi"})
    transcript = r.json().get("transcript", "")
    print(transcript.encode('utf-8'))

    print("Testing Translate (Hindi -> Santali)...")
    r = requests.post("http://localhost:8000/translate", json={"text": transcript, "source_lang": "hi", "target_lang": "santali"})
    translation = r.json().get("translation", "")
    print(translation.encode('utf-8'))

    print("Testing TTS (Santali)...")
    r = requests.post("http://localhost:8000/tts", json={"text": translation, "language": "santali"})
    print(f"TTS Status Code: {r.status_code}")
    print(f"TTS Content Length: {len(r.content)} bytes")
    
    if len(r.content) > 100:
        print("TTS returned playable audio bytes successfully!")
        
finally:
    print("Terminating server...")
    server.terminate()
    if os.path.exists("dummy_hi.wav"):
        os.remove("dummy_hi.wav")
