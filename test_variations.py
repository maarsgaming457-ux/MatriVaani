import requests
import sys

url = "http://127.0.0.1:8000/translate/hindi-to-mundari"

variations = [
    "मेरा नाम सुमित है",
    "मेरा नाम सुमित है।",
    "मेरा नाम सुमित है.",
    "मेरा नाम सुमीत है",
    "मेरा नाम सुमित हे",
    "मेरे नाम सुमित है",
    "मेरा नाम सुमित है ",
    "मैरा नाम सुमित है",
    "मेरा नाम सुमित हैं",
    "मेरा नाम सुमित है!",
    "मैं सुमित हूँ"
]

sys.stdout.reconfigure(encoding='utf-8')

for v in variations:
    try:
        resp = requests.post(url, json={"text": v}).json()
        print(f"Input: {v} -> Output: {resp.get('translation')}")
    except Exception as e:
        print(f"Input: {v} -> Error: {e}")
