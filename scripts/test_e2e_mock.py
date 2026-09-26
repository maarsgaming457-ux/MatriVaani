import time
import requests
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:8000'

def test_pipeline(name, audio_filename, reference):
    audio_path = os.path.join('tools', 'ho_annotator', 'audio', audio_filename)
    
    print(f"\\n--- TEST: {name} ---")
    print(f"Recording: {audio_filename}")
    print(f"Reference Ho: {reference}")
    
    start_asr = time.time()
    with open(audio_path, 'rb') as f:
        res_asr = requests.post(f"{BASE_URL}/asr", files={'file': f}, data={'language': 'ho'})
    asr_latency = time.time() - start_asr
    
    if res_asr.status_code != 200:
        print(f"ASR FAILED: {res_asr.text}")
        return
        
    asr_text = res_asr.json().get('transcript', '')
    print(f"Actual ASR: {asr_text}")
    print(f"Translator input: {asr_text}")
    
    start_trans = time.time()
    res_trans = requests.post(
        f"{BASE_URL}/experimental/translate/ho-hi",
        json={'text': asr_text}
    )
    trans_latency = time.time() - start_trans
    
    if res_trans.status_code != 200:
        print(f"TRANSLATION FAILED: {res_trans.text}")
        return
        
    trans_data = res_trans.json()
    hindi = trans_data.get('translation') or trans_data.get('hindi_text')
    tier = trans_data.get('method')
    conf = trans_data.get('confidence')
    
    print(f"Hindi: {hindi}")
    print(f"Tier: {tier}")
    print(f"Confidence: {conf}")
    
    start_tts = time.time()
    res_tts = requests.post(
        f"{BASE_URL}/tts",
        json={'text': hindi, 'language': 'hi', 'provider': 'sarvam'}
    )
    tts_latency = time.time() - start_tts
    
    if res_tts.status_code == 200:
        print("TTS: SUCCESS")
        print("Playback: EXECUTED / NOT INDEPENDENTLY AUDIBLE-VERIFIED")
        print("Result: PASS")
    else:
        print(f"TTS: FAILED {res_tts.text}")
        print("Result: FAIL")
        
    total_latency = asr_latency + trans_latency + tts_latency
    print(f"ASR Latency: {asr_latency:.3f}s")
    print(f"Trans Latency: {trans_latency:.3f}s")
    print(f"TTS Latency: {tts_latency:.3f}s")
    print(f"Total Latency: {total_latency:.3f}s")

if __name__ == '__main__':
    test_pipeline('Exact Retrieval', '281474976799629_0019800406.wav', 'आम लो पोन रेञ जागार केना')
    test_pipeline('AI Fallback', '281474976799624_0016800560.wav', 'आबु एन हो को नेनता काबु बेटा इचि कोआ')
    test_pipeline('Controlled Fallback', '281474976799643_0012300691.wav', 'आपुञ ओआ:ते सेनो:आञ')
