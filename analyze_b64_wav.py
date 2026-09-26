import base64
import wave
import numpy as np

with open('test_mic2_base64.txt', 'r', encoding='utf-16') as f:
    b64_data = f.read()

# Strip any unexpected characters
b64_data = ''.join(c for c in b64_data if c.isalnum() or c in '+/=')

wav_data = base64.b64decode(b64_data)
with open('test_mic_decoded.wav', 'wb') as f:
    f.write(wav_data)

with wave.open('test_mic_decoded.wav', 'rb') as f:
    frames = f.readframes(f.getnframes())
    audio = np.frombuffer(frames, dtype=np.int16)
    
    print(f"Channels: {f.getnchannels()}")
    print(f"Sample Width: {f.getsampwidth()}")
    print(f"Frame Rate: {f.getframerate()}")
    print(f"Total Frames: {f.getnframes()}")
    
    if len(audio) > 0:
        rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
        max_val = np.max(np.abs(audio))
        print(f"RMS: {rms:.2f}")
        print(f"Max Amplitude: {max_val}")
    else:
        print("RMS: N/A (Empty)")
