import httpx
import sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    with open("test_hindi_voice.wav", "rb") as f:
        asr_resp = httpx.post("http://127.0.0.1:8000/asr", files={"file": ("test_hindi_voice.wav", f, "audio/wav")}, data={"language": "hi"}, timeout=30.0)
    print(asr_resp.text.encode('utf-8', errors='replace').decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
