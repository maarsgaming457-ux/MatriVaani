import pytest
import numpy as np
import io
import soundfile as sf
from data_modules.santali.audio import decode_audio_bytes

def generate_dummy_flac(sr=16000, duration=1.0, channels=1):
    num_samples = int(sr * duration)
    # Generate 440Hz sine wave
    t = np.linspace(0, duration, num_samples, endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    if channels == 2:
        waveform = np.column_stack((waveform, waveform))
        
    with io.BytesIO() as f:
        sf.write(f, waveform, sr, format='FLAC')
        return f.getvalue()

def test_decode_valid_audio():
    audio_bytes = generate_dummy_flac(sr=16000)
    waveform, sr = decode_audio_bytes(audio_bytes)
    
    assert sr == 16000
    assert waveform.dtype == np.float32
    assert waveform.ndim == 1
    assert len(waveform) == 16000
    assert np.isfinite(waveform).all()

def test_decode_stereo_audio():
    audio_bytes = generate_dummy_flac(sr=16000, channels=2)
    waveform, sr = decode_audio_bytes(audio_bytes)
    
    # Decoder should convert to mono
    assert sr == 16000
    assert waveform.dtype == np.float32
    assert waveform.ndim == 1

def test_decode_empty_bytes():
    with pytest.raises(ValueError, match="Audio bytes are empty"):
        decode_audio_bytes(b"")

def test_decode_invalid_format():
    with pytest.raises(ValueError, match="Failed to decode audio bytes"):
        decode_audio_bytes(b"this is not an audio file")
