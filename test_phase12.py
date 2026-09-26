import sys
import os

# Start the uvicorn server in a separate thread for testing
import threading
import uvicorn
import time
import requests

def run_server():
    os.chdir('tools/ho_annotator')
    uvicorn.run("app:app", host="127.0.0.1", port=8082, log_level="error")

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(2)

try:
    # 1. Fetch records
    r = requests.get("http://127.0.0.1:8082/api/records")
    records = r.json()
    print(f"Loaded {len(records)} records")
    
    # 2. Pick the first real record
    real_records = [x for x in records if x['demo_only'] == 0]
    first_id = real_records[0]['id']
    print(f"Testing on {first_id}")
    
    # 3. Post incomplete data with human_verified = True (should override to False)
    payload = {
        "ho": "Test Ho",
        "hindi": "",
        "category": "other",
        "human_verified": True,
        "review_status": "APPROVED",
        "notes": ""
    }
    r = requests.post(f"http://127.0.0.1:8082/api/records/{first_id}", json=payload)
    print("Post incomplete:", r.json())
    
    # 4. Post complete data with human_verified = True
    payload["hindi"] = "Test Hindi"
    r = requests.post(f"http://127.0.0.1:8082/api/records/{first_id}", json=payload)
    print("Post complete:", r.json())
    
    # 5. Export VERIFIED
    r = requests.post("http://127.0.0.1:8082/api/export/VERIFIED")
    print("Export:", r.json())
    
    # Revert record to empty
    payload["ho"] = ""
    payload["hindi"] = ""
    payload["human_verified"] = False
    payload["review_status"] = "NEW"
    requests.post(f"http://127.0.0.1:8082/api/records/{first_id}", json=payload)
    
except Exception as e:
    print("Error:", e)
