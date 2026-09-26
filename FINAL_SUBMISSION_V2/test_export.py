import requests

# Post complete data with human_verified = True
payload = {
    "ho": "Test Ho",
    "hindi": "Test Hindi",
    "category": "other",
    "human_verified": True,
    "review_status": "APPROVED",
    "notes": ""
}
r = requests.post("http://127.0.0.1:8080/api/records/HOH_A20241007162810805045", json=payload)
print("Post complete:", r.json())

# Export VERIFIED
r = requests.post("http://127.0.0.1:8080/api/export/VERIFIED")
print("Export:", r.json())
