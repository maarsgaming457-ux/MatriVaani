import requests
import time

def test_asr(filepath, lang):
    start = time.time()
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            data = {'language': lang}
            res = requests.post("http://127.0.0.1:8000/asr", files=files, data=data)
            dur = time.time() - start
            print(f"{filepath} ({lang}): {res.status_code} - {res.json()} - Latency: {dur:.3f}s")
    except Exception as e:
        print(f"Error testing {filepath}: {e}")

test_asr("ho_test_audio/ho1.wav", "ho")
test_asr("ho_test_audio/ho2.wav", "ho")
