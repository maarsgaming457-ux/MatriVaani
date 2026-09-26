import time
import urllib.request
import json
import urllib.error
import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    url = "http://127.0.0.1:8000/translate"
    payload = {
        "text": "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
        "source_lang": "Hindi",
        "target_lang": "Santali"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    print("Sending live request to Windows FastAPI:8000...", flush=True)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45) as res:
            t1 = time.time()
            if res.status != 200:
                print(f"Error HTTP {res.status}")
                return
            response_data = json.loads(res.read().decode('utf-8'))
            print(f"Latency: {t1-t0:.2f}s", flush=True)
            print(f"Result: {response_data}", flush=True)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    main()
