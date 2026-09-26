import numpy as np
import soundfile as sf
import io

audio_arr = np.random.randn(16000).astype(np.float32)
buffer = io.BytesIO()
sf.write(buffer, audio_arr, 16000, format='WAV')
buffer.seek(0)
info = sf.info(buffer)
print(f"Format: {info.format}")
print(f"Subtype: {info.subtype}")
