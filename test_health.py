import requests
import time
import base64
import os

print("--- Testing FastAPI ---")
try:
    resp = requests.get('http://127.0.0.1:8000/health')
    print(f"Health check status: {resp.status_code}")
    print(f"Response: {resp.json()}")
except Exception as e:
    print(f"FastAPI not running or error: {e}")

