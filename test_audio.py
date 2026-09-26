
import scipy.io.wavfile as wav
import numpy as np
import os

def stats(f):
    fs, data = wav.read(f)
    data_f = data / np.iinfo(data.dtype).max if data.dtype.kind == 'i' else data
    print(f'File: {f}')
    print(f'Duration: {len(data)/fs:.2f}s')
    print(f'Sample rate: {fs} Hz')
    print(f'Channels: {1 if data.ndim==1 else data.shape[1]}')
    print(f'Size: {os.path.getsize(f)} bytes')
    print(f'Peak: {np.max(np.abs(data_f)):.4f}')
    print(f'RMS: {np.sqrt(np.mean(data_f**2)):.4f}')
    print()

stats('ho_test_audio/ho1.wav')
stats('ho_test_audio/ho2.wav')

