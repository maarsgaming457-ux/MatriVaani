import os
import json
import numpy as np
import scipy.io.wavfile as wavfile

AUDIO_DIR = 'data/ho_hindi/experimental/master_task2/audio'
RESULTS_FILE = 'data/ho_hindi/experimental/master_task2/audio_validation.json'

validation_results = []

for fn in sorted(os.listdir(AUDIO_DIR)):
    if not fn.endswith('.wav'): continue
    filepath = os.path.join(AUDIO_DIR, fn)
    
    try:
        sr, data = wavfile.read(filepath)
        size = os.path.getsize(filepath)
        
        # normalize to float for stats
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
            
        sample_count = len(data)
        duration = sample_count / sr
        
        rms = float(np.sqrt(np.mean(data**2)))
        peak = float(np.max(np.abs(data)))
        has_nan = bool(np.isnan(data).any())
        has_inf = bool(np.isinf(data).any())
        
        # Silence check
        silence_ratio = float(np.sum(np.abs(data) < 0.001) / sample_count)
        
        validation_results.append({
            'file': fn,
            'exists': True,
            'file_size_bytes': size,
            'valid_wav_header': True,
            'pcm': True,
            'channels': 1 if len(data.shape) == 1 else data.shape[1],
            'sample_rate': sr,
            'duration_sec': duration,
            'sample_count': sample_count,
            'rms': rms,
            'peak': peak,
            'finite_samples': not (has_nan or has_inf),
            'nan_count': int(np.isnan(data).sum()),
            'inf_count': int(np.isinf(data).sum()),
            'silence_ratio': silence_ratio
        })
    except Exception as e:
        validation_results.append({
            'file': fn,
            'exists': True,
            'error': str(e)
        })

with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(validation_results, f, indent=2)
print("Audio validation complete.")
