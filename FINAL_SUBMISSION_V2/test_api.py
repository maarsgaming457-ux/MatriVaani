import requests
import time

def test_asr(lang, file_path):
    print(f"Testing {lang} ASR with {file_path}")
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"language": lang}
        
        t0 = time.time()
        response = requests.post("http://127.0.0.1:8000/asr", files=files, data=data)
        t1 = time.time()
        
    print(f"Status Code: {response.status_code}")
    print(f"Time: {t1 - t0:.2f}s")
    if response.status_code == 200:
        try:
            print(f"Response: {response.json()}")
        except Exception:
            print(f"Response text: {response.text.encode('unicode_escape').decode('utf-8')}")
    else:
        print(f"Response: {response.text}")
    print("-" * 50)

if __name__ == '__main__':
    test_asr('ho', 'fleurs_hi/dev/14584887621258891555.wav')
    test_asr('ho', 'fleurs_hi/dev/10691214664103820058.wav')
    test_asr('ho', 'fleurs_hi/dev/2790069619537345490.wav')
    
    # Test existing Santali
    test_asr('santali', 'fleurs_hi/dev/14584887621258891555.wav')
    
    # Test translate
    print("Testing Translation (santali to hi)")
    t0 = time.time()
    response = requests.post("http://127.0.0.1:8000/translate", json={
        "text": "This is a test",
        "source_lang": "santali",
        "target_lang": "hi"
    })
    t1 = time.time()
    print(f"Status: {response.status_code}")
    print(f"Time: {t1 - t0:.2f}s")
    print(f"Response: {response.text}")
