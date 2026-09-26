import requests
import json

url = "http://127.0.0.1:8000/translate/hindi-to-mundari"
payload = {"text": "मेरा नाम सुमित है"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", str(e))
