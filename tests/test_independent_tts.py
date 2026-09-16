import os
import io
import soundfile as sf
import numpy as np
import time

print('Testing TTSService independent instantiation...')
from app.services.tts_service import TTSService

tts = TTSService()
santali_text = '???' # Jal / Net

print('Calling synthesize()...')
start_time = time.time()
audio_bytes = tts.synthesize(santali_text, 'santali')
inference_time = time.time() - start_time
print(f'Inference completed in {inference_time:.2f} seconds.')

if not audio_bytes:
    print('ERROR: Audio bytes are empty!')
    exit(1)
    
print(f'Received {len(audio_bytes)} bytes.')

# Verify WAV Header (RIFF....WAVE)
if not audio_bytes.startswith(b'RIFF') or b'WAVE' not in audio_bytes[:16]:
    print('ERROR: Invalid WAV header!')
    exit(1)
else:
    print('WAV header verified.')

# Read bytes as WAV
try:
    buffer = io.BytesIO(audio_bytes)
    data, samplerate = sf.read(buffer)
    duration = len(data) / samplerate
    print(f'Successfully read WAV. Duration: {duration:.2f} seconds, Samplerate: {samplerate} Hz')
    
    if duration <= 0:
        print('ERROR: Duration is 0!')
        exit(1)
        
    if np.max(np.abs(data)) == 0.0:
        print('ERROR: Audio contains only silence (all zeros)!')
        exit(1)
    else:
        print(f'Audio contains non-zero samples. Max amplitude: {np.max(np.abs(data)):.4f}')
        
except Exception as e:
    print(f'ERROR parsing WAV file: {e}')
    exit(1)

print('Independent TTS test PASSED.')
