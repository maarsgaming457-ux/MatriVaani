import requests
import time
import os
import subprocess
import json

url = "http://localhost:8000/tts"

sentences = [
    "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
    "बच्चों, अपने सामने रखी वस्तुओं को गिनिए।",
    "अब बताइए कि पाँच के बाद कौन-सी संख्या आती है?"
]

print("Running TTS verification tests...\n")

for i, text in enumerate(sentences):
    payload = {
        "text": text,
        "language": "hi",
        "provider": "sarvam"
    }
    
    print(f"--- TEST {i+1} ---")
    print(f"Text: {text.encode('utf-8')}")
    
    t0 = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=15)
        t1 = time.time()
        
        status = resp.status_code
        size = len(resp.content)
        ctype = resp.headers.get("content-type")
        latency = t1 - t0
        
        print(f"Status: {status}")
        print(f"Latency: {latency:.3f}s")
        print(f"Content-Type: {ctype}")
        print(f"Size: {size} bytes")
        
        if status == 200:
            filename = f"test_{i+1}.wav"
            with open(filename, "wb") as f:
                f.write(resp.content)
            
            # Use ffprobe to validate audio
            try:
                cmd = [
                    "ffprobe", "-v", "error", "-show_format", "-show_streams",
                    "-of", "json", filename
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                info = json.loads(res.stdout)
                
                stream = info.get("streams", [{}])[0]
                format_info = info.get("format", {})
                
                print(f"Codec: {stream.get('codec_name')}")
                print(f"Sample Rate: {stream.get('sample_rate')}")
                print(f"Channels: {stream.get('channels')}")
                print(f"Duration: {format_info.get('duration')}s")
                print("Audio: VALID")
            except Exception as e:
                print(f"Audio validation error: {e}")
                print("Audio: UNVERIFIED")
        else:
            print(f"Error: {resp.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")
    print()

