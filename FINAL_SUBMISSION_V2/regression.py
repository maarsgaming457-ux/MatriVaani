import requests
import time
import base64
import os
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

results = {}

def test_asr(lang, file_path, name):
    print(f"Testing ASR ({lang}) - {name}...")
    if not os.path.exists(file_path):
        results[name] = "File not found"
        return
    t0 = time.time()
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/asr", 
            files={"file": (os.path.basename(file_path), f, "audio/wav")},
            data={"language": lang}
        )
    latency = time.time() - t0
    if resp.status_code == 200:
        results[name] = {"status": resp.status_code, "latency": latency, "output": resp.json().get('transcript')}
    else:
        results[name] = {"status": resp.status_code, "latency": latency, "error": resp.text}

def test_translate(text, src, tgt, name):
    print(f"Testing Translate ({src} -> {tgt}) - {name}...")
    t0 = time.time()
    resp = requests.post(f"{BASE_URL}/translate", json={
        "text": text,
        "source_lang": src,
        "target_lang": tgt
    })
    latency = time.time() - t0
    if resp.status_code == 200:
        results[name] = {"status": resp.status_code, "latency": latency, "output": resp.json().get('translation')}
        return resp.json().get('translation')
    else:
        results[name] = {"status": resp.status_code, "latency": latency, "error": resp.text}
        return None

def test_tts(text, lang, name):
    print(f"Testing TTS ({lang}) - {name}...")
    t0 = time.time()
    resp = requests.post(f"{BASE_URL}/tts", json={
        "text": text,
        "language": lang
    })
    latency = time.time() - t0
    if resp.status_code == 200:
        results[name] = {"status": resp.status_code, "latency": latency, "output": "[Audio Data Received]"}
    else:
        results[name] = {"status": resp.status_code, "latency": latency, "error": resp.text}

test_asr("hi", "test_hindi_voice.wav", "ASR_Hindi")
test_asr("ho", "ho_test_audio/ho1.wav", "ASR_Ho1")
test_asr("ho", "ho_test_audio/ho2.wav", "ASR_Ho2")

hindi_sentences = [
    "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
    "यह एक किताब है।",
    "यह लाल गेंद है।",
    "हम आज गिनती सीखेंगे।",
    "बच्चे स्कूल जा रहे हैं।"
]

for i, sentence in enumerate(hindi_sentences):
    santali_res = test_translate(sentence, "hi", "santali", f"Trans_Hi_Sat_{i}")
    if santali_res:
        test_translate(santali_res, "santali", "hi", f"Trans_Sat_Hi_{i}")

test_translate("Testing Ho", "ho", "hi", "Trans_Ho_Hi_Blocked")
test_translate("Testing Ho", "hi", "ho", "Trans_Hi_Ho_Blocked")

test_tts("नमस्ते बच्चों, आज हम गिनती सीखेंगे।", "hi", "TTS_Hindi")

with open('regression_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Done.")
