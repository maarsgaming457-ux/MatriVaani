import requests
import time

for _ in range(30):
    try:
        resp = requests.post("http://127.0.0.1:8001/translate", json={"text": "test", "source_lang": "hi", "target_lang": "sat"})
        if resp.status_code == 200:
            print("IndicTrans2 is UP!")
            break
        print(f"Status: {resp.status_code}")
    except Exception as e:
        print("Waiting...")
    time.sleep(2)
