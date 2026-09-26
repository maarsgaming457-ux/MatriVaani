import requests
import time

BASE_URL = "http://127.0.0.1:8000"
now = int(time.time())

payload = {
    "client_changes": [
        {
            "id": "sync1", 
            "content_type": "flashcard",
            "topic": "numbers", 
            "language": "sat",
            "data": "{}",
            "created_at": now,
            "updated_at": now,
            "deleted": 0
        }
    ]
}

resp = requests.post(f"{BASE_URL}/sync", json=payload)
print(f"Sync status: {resp.status_code}")
if resp.status_code == 200:
    print(resp.json())
else:
    print(resp.text)
