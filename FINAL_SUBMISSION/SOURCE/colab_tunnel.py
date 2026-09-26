import threading
import time
from pyngrok import ngrok
import uvicorn
import requests
from colab_matrivaani_api import app

# Assuming NGROK_AUTHTOKEN is set in the environment or Colab secrets
def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# Start FastAPI in a background thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(3) # wait for server to start

# Open a secure tunnel via ngrok
public_url = ngrok.connect(8000).public_url
print(f"Public URL: {public_url}")

# Local Colab test
try:
    res = requests.get("http://127.0.0.1:8000/health")
    print("Local Health:", res.json())
except Exception as e:
    print("Local Health Failed:", e)

# Public Tunnel test
try:
    res = requests.get(f"{public_url}/health")
    print("Public Health:", res.json())
except Exception as e:
    print("Public Health Failed:", e)

