import requests
import json
import wave
import numpy as np
import soundfile as sf
import time

BASE_URL = "http://127.0.0.1:8000"

def create_dummy_wav(filename="dummy_test.wav"):
    sr = 16000
    duration = 2
    t = np.linspace(0, duration, int(sr * duration), False)
    audio = np.sin(2 * np.pi * 440 * t)
    sf.write(filename, audio, sr, subtype='PCM_16')
    return filename

try:
    print("Health check:", requests.get(f"{BASE_URL}/health").json())

    wav_file = create_dummy_wav()
    with open(wav_file, 'rb') as f:
        res_asr = requests.post(f"{BASE_URL}/asr", files={'file': (wav_file, f, 'audio/wav')}, data={'language': 'hi'})
    transcript = res_asr.json().get("transcript", "मेरा नाम सुमित है।")
    print("ASR output:", transcript)

    t0 = time.time()
    res_nmt = requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": "मेरा नाम सुमित है।"})
    translation = res_nmt.json().get("translation")
    t1 = time.time()
    print("NMT output:", translation, f"(Latency: {t1-t0:.2f}s)")

    t0 = time.time()
    res_tts = requests.post(f"{BASE_URL}/tts", json={"text": translation, "language": "hi"})
    t1 = time.time()
    print(f"TTS output: {res_tts.status_code}, length={len(res_tts.content)} bytes (Latency: {t1-t0:.2f}s)")

except Exception as e:
    print(f"Error: {e}")
