import requests

try:
    res = requests.post("http://127.0.0.1:8000/translate", json={
        "text": "Hello world",
        "source_lang": "hi",
        "target_lang": "ho"
    })
    print(f"HI -> HO: {res.json()}")
except Exception as e:
    print(f"Error: {e}")
