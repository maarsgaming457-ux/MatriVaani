import time
import requests
import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

# Ensure we're in the project root to import services if needed
sys.path.insert(0, os.path.abspath('.'))
from app.services.translation_service import TranslationService

FASTAPI_URL = "http://127.0.0.1:8000"

def test_health():
    print("--- FastAPI Health ---")
    try:
        t0 = time.time()
        res = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        t1 = time.time()
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
        print(f"Latency: {t1-t0:.4f}s")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_translation(text, src, tgt, test_name):
    print(f"\n--- Translation: {test_name} ---")
    payload = {
        "text": text,
        "source_lang": src,
        "target_lang": tgt
    }
    try:
        t0 = time.time()
        res = requests.post(f"{FASTAPI_URL}/translate", json=payload, timeout=45)
        t1 = time.time()
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print(f"Result: {res.json().get('translation', '')}")
        else:
            print(f"Error Result: {res.text}")
        print(f"Latency: {t1-t0:.4f}s")
        return t1 - t0
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

def test_sarvam():
    print("\n--- Sarvam TTS ---")
    payload = {
        "text": "नमस्ते",
        "language": "hi",
        "provider": "sarvam"
    }
    try:
        t0 = time.time()
        res = requests.post(f"{FASTAPI_URL}/tts", json=payload, timeout=10)
        t1 = time.time()
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            audio_bytes = res.content
            print(f"Audio received: {len(audio_bytes)} bytes")
            print(f"Content-Type: {res.headers.get('content-type')}")
        else:
            print(f"Error Result: {res.text}")
        print(f"Latency: {t1-t0:.4f}s")
    except Exception as e:
        print(f"Sarvam TTS failed: {e}")

def test_bhashini():
    print("\n--- Bhashini Translation (Direct) ---")
    try:
        ts = TranslationService()
        ts.provider = "bhashini"
        t0 = time.time()
        # Bhashini requires valid user/API key in .env, if they are blank, it will fail gracefully
        res = ts.translate("नमस्ते", "Hindi", "Santali")
        t1 = time.time()
        print(f"Result: {res}")
        print(f"Latency: {t1-t0:.4f}s")
    except Exception as e:
        print(f"Bhashini failed: {e}")

def test_asr():
    print("\n--- ASR ---")
    audio_path = "data_modules/raw/audio/synthetic_santhali_000.wav"
    if not os.path.exists(audio_path):
        print(f"ASR: NOT EVALUATED (File {audio_path} missing)")
        return
        
    try:
        t0 = time.time()
        with open(audio_path, 'rb') as f:
            files = {'file': (audio_path, f, 'audio/wav')}
            data = {'language': 'santali'}
            res = requests.post(f"{FASTAPI_URL}/asr", files=files, data=data, timeout=30)
        t1 = time.time()
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print(f"Result: {res.json().get('transcript', '')}")
        else:
            print(f"Error Result: {res.text}")
        print(f"Latency: {t1-t0:.4f}s")
    except Exception as e:
        print(f"ASR failed: {e}")

def main():
    test_health()
    
    l1 = test_translation("नमस्ते बच्चों, आज हम गिनती सीखेंगे।", "Hindi", "Santali", "Test 1")
    l2 = test_translation("एक, दो, तीन, चार और पाँच।", "Hindi", "Santali", "Test 2")
    l3 = test_translation("यह एक आम है।", "Hindi", "Santali", "Test 3")
    
    if l1 and l2 and l3:
        print(f"\nAverage Hindi -> Santali Latency: {(l1+l2+l3)/3:.4f}s")
        
    # Santali -> Hindi
    test_translation("ᱦᱚᱞᱮ ᱜᱤᱫᱽᱨᱟᱹᱠᱚ ᱾", "Santali", "Hindi", "Santali to Hindi")
    
    test_sarvam()
    test_bhashini()
    test_asr()
    
if __name__ == '__main__':
    main()
