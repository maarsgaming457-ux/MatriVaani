import requests
import time

url = "http://localhost:8000/tts"
payload = {
    "text": "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
    "provider": "sarvam"
}

try:
    print("Testing /tts with sarvam...")
    t0 = time.time()
    resp = requests.post(url, json=payload, timeout=10)
    t1 = time.time()
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('content-type')}")
    print(f"Latency: {t1-t0:.3f}s")
    if resp.status_code == 200:
        print(f"Success! Bytes: {len(resp.content)}")
    else:
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
