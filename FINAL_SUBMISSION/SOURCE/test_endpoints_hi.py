import requests
import time

url = "http://localhost:8000/tts"
payload = {
    "text": "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
    "language": "hi",
    "provider": "sarvam"
}

t0 = time.time()
resp = requests.post(url, json=payload, timeout=10)
t1 = time.time()
print(f"Status: {resp.status_code}, Latency: {t1-t0:.3f}s")
