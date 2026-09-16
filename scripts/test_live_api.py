import requests
import glob
import os

API_URL = "http://localhost:8000"

def test_live_api():
    print("================================================================================")
    print("MATRIVAANI LIVE API TEST")
    print("================================================================================\n")
    
    print(f"Testing API at: {API_URL}\n")
    
    # 1. Health Endpoint
    print("1. Testing GET /health...")
    try:
        r = requests.get(f"{API_URL}/health")
        if r.status_code == 200:
            print("SUCCESS")
            data = r.json()
            print(f"ASR Provider: {data.get('asr', {}).get('provider')}")
            print(f"Translation Provider: {data.get('translation', {}).get('provider')}")
        else:
            print(f"FAILED: {r.status_code}")
    except Exception as e:
        print(f"ERROR: Cannot connect to API. Is FastAPI running? {e}")
        return
        
    print("\n--------------------------------------------------------------------------------\n")
    
    # Locate audio
    flac_files = glob.glob("datasets/cache/santali/**/*.flac", recursive=True)
    if not flac_files:
        print("ERROR: No real Santali audio files found in datasets/cache/santali/")
        return
        
    audio_file = flac_files[0]
    
    # 2. ASR Endpoint
    print(f"2. Testing POST /api/v1/asr with {os.path.basename(audio_file)}...")
    try:
        with open(audio_file, "rb") as f:
            files = {"audio": (os.path.basename(audio_file), f, "audio/flac")}
            r = requests.post(f"{API_URL}/api/v1/asr", files=files)
            if r.status_code == 200:
                print("SUCCESS")
                data = r.json()
                print(f"Status: {data.get('status')}")
                print(f"Transcript: {data.get('transcript')}")
            else:
                print(f"FAILED: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"ERROR: {e}")
        
    print("\n--------------------------------------------------------------------------------\n")
    
    # 3. Process Endpoint
    print(f"3. Testing POST /api/v1/process with {os.path.basename(audio_file)}...")
    try:
        with open(audio_file, "rb") as f:
            files = {"audio": (os.path.basename(audio_file), f, "audio/flac")}
            data = {"target_language": "hi"}
            r = requests.post(f"{API_URL}/api/v1/process", files=files, data=data)
            if r.status_code == 200:
                print("SUCCESS")
                data = r.json()
                print(f"Pipeline Status: {data.get('status')}")
                print(f"Cleaned Transcript: {data.get('cleaned_transcript')}")
                print(f"Translation: {data.get('translation')}")
                script = data.get('script')
                print(f"Script Generated: {'Yes' if script else 'No'}")
            else:
                print(f"FAILED: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"ERROR: {e}")
        
    print("\n================================================================================")

if __name__ == "__main__":
    test_live_api()
