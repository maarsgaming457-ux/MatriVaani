import requests
import sys

url = "http://127.0.0.1:8000/translate/hindi-to-mundari"

cases = [
    "मेरा नाम सुमित है",
    "मेरा नाम सुमित है।",
    "क्या तुम ठीक हो?",
    "बहुत अच्छा!"
]

sys.stdout.reconfigure(encoding='utf-8')

for c in cases:
    try:
        resp = requests.post(url, json={"text": c}).json()
        print(f"Input: {c} -> Output: {resp.get('translation')}")
    except Exception as e:
        print(f"Error: {e}")
