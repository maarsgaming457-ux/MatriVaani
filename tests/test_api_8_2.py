import requests
import json
import time

url = "http://127.0.0.1:8000"

try:
    res = requests.post(f"{url}/translate", json={"text": "मेरा नाम सुमित है।", "source_lang": "hi", "target_lang": "sat"})
    print(f"Translate HI->SAT: {res.status_code} - {res.text.encode('utf-8')}")
except Exception as e:
    print(f"Translate check failed: {e}")

try:
    res = requests.post(f"{url}/translate", json={"text": "ᱤᱧᱟᱹᱜ ᱧᱩᱛᱩᱢ ᱥᱩᱢᱤᱛ ᱾", "source_lang": "sat", "target_lang": "hi"})
    print(f"Translate SAT->HI: {res.status_code} - {res.text.encode('utf-8')}")
except Exception as e:
    print(f"Translate check failed: {e}")

