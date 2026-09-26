import os
import io
import wave
import requests
import librosa
import soundfile as sf
import numpy as np

BASE_URL = "http://127.0.0.1:8000"

def create_dummy_wav(filename="dummy.wav"):
    sr = 16000
    duration = 2
    t = np.linspace(0, duration, int(sr * duration), False)
    # Generate a simple sine wave
    audio = np.sin(2 * np.pi * 440 * t)
    sf.write(filename, audio, sr, subtype='PCM_16')
    return filename

def test_pipeline():
    print("Testing End-to-End Pipeline (ASR -> NMT -> TTS)")
    
    # 1. ASR
    wav_file = create_dummy_wav()
    print(f"\n1. Sending audio for ASR to {BASE_URL}/asr")
    with open(wav_file, 'rb') as f:
        files = {'file': (wav_file, f, 'audio/wav')}
        # ASR uses 'language' form data
        data = {'language': 'hi'}
        res = requests.post(f"{BASE_URL}/asr", files=files, data=data)
    
    if res.status_code != 200:
        print("ASR Failed:", res.text)
        return
        
    asr_output = res.json().get('transcript', '')
    print(f"ASR Output: {asr_output}")
    if not asr_output:
        asr_output = "मेरा नाम सुमित है।"
        print(f"Using mock ASR output for testing NMT: {asr_output}")
        
    # 2. NMT
    print(f"\n2. Sending text to NMT {BASE_URL}/translate/hindi-to-mundari")
    res = requests.post(f"{BASE_URL}/translate/hindi-to-mundari", json={"text": asr_output})
    if res.status_code != 200:
        print("NMT Failed:", res.text)
        return
        
    nmt_output = res.json().get('translation', '')
    print(f"NMT Output: {nmt_output}")
    
    # 3. TTS
    print(f"\n3. Sending translation to TTS {BASE_URL}/tts")
    # Note: Mundari TTS might not be fully supported by Sarvam, using target language parameter
    res = requests.post(f"{BASE_URL}/tts", json={"text": nmt_output, "language": "hi"})
    if res.status_code == 200:
        print(f"TTS Success: Received {len(res.content)} bytes of audio data")
    else:
        print("TTS Failed:", res.status_code, res.text)
        
if __name__ == "__main__":
    test_pipeline()
