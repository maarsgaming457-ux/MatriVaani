import httpx

try:
    print("Testing health...")
    resp = httpx.get("http://127.0.0.1:8000/health")
    print(resp.status_code)
except Exception as e:
    print(e)
