import os
import time
import requests
import wave
import numpy as np
import soundfile as sf
import json

BASE_URL = "http://127.0.0.1:8000"

def create_dummy_wav(filename="dummy_test.wav"):
    sr = 16000
    duration = 2
    t = np.linspace(0, duration, int(sr * duration), False)
    audio = np.sin(2 * np.pi * 440 * t)
    sf.write(filename, audio, sr, subtype='PCM_16')
    return filename

def test_nmt(sentences):
    results = []
    for s in sentences:
        start = time.time()
        res = requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": s})
        lat = time.time() - start
        if res.status_code == 200:
            results.append({"hindi": s, "mundari": res.json().get("translation"), "latency": lat})
        else:
            results.append({"hindi": s, "error": res.text, "latency": lat})
    return results

if __name__ == "__main__":
    print("--- 9. Direct NMT testing ---")
    sentences = [
        "मेरा नाम सुमित है।", # simple
        "क्या आप मुझे सुन सकते हैं?", # question
        "यह एक बहुत ही लंबा वाक्य है जिसका उपयोग हम मशीन अनुवाद प्रणाली की जांच करने के लिए कर रहे हैं।", # longer
        "हाँ, मैं सहमत हूँ!", # punctuation
        "मेरे पास 100 रुपये हैं।", # numbers
        "नमस्ते", # Hindi Unicode
        "आप कैसे हैं?", # conversational
        "हम स्कूल में विज्ञान और गणित पढ़ते हैं।", # educational
        "राम और श्याम बाजार गए हैं।", # names
        "आज बहुत तेज बारिश हो रही है और मौसम ठंडा है।" # multiple words
    ]
    nmt_results = test_nmt(sentences)
    for r in nmt_results:
        print(f"Hindi: {r.get('hindi')}")
        print(f"Mundari: {r.get('mundari')}")
        print(f"Latency: {r.get('latency'):.4f}s")
        print()
    
    print("--- 11. Verify FastAPI endpoint ---")
    print(requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": ""}).json())
    print(requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": "   "}).json())
    print(requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": "नमस्ते"}).json())
    print(requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": "यह " * 50}).json())
    print(requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"invalid": "field"}).status_code)
    
    print("--- 12. Verify existing ASR ---")
    wav_file = create_dummy_wav()
    with open(wav_file, 'rb') as f:
        res = requests.post(f"{BASE_URL}/asr", files={'file': (wav_file, f, 'audio/wav')}, data={'language': 'hi'})
    print(f"ASR Output: {res.json()}")
    
    print("--- 13. Verify ASR -> NMT ---")
    asr_out = res.json().get('transcript', 'नमस्ते')
    res_nmt = requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": asr_out})
    print(f"ASR->NMT Output: {res_nmt.json()}")
    
    print("--- 14. Verify NMT -> TTS ---")
    mundari_text = res_nmt.json().get('translation', 'नमस्ते')
    res_tts = requests.post(f"{BASE_URL}/tts", json={"text": mundari_text, "language": "hi"})
    print(f"TTS Status: {res_tts.status_code}, length: {len(res_tts.content)}")
