import io
import soundfile as sf
import numpy as np

def decode_audio_bytes(audio_bytes: bytes, target_sr: int = 16000):
    """
    Deterministically decodes audio bytes (e.g. FLAC payload) into a mono, float32 numpy array.
    """
    if not audio_bytes:
        raise ValueError("Audio bytes are empty")
        
    try:
        with io.BytesIO(audio_bytes) as f:
            waveform, sr = sf.read(f)
    except Exception as e:
        raise ValueError(f"Failed to decode audio bytes: {e}")
        
    # Validation checks
    if len(waveform) == 0:
        raise ValueError("Decoded waveform is empty")
        
    if not np.isfinite(waveform).all():
        raise ValueError("Waveform contains NaN or Inf values")
        
    # Ensure float32
    if waveform.dtype != np.float32:
        waveform = waveform.astype(np.float32)
        
    # Ensure Mono
    if waveform.ndim == 2:
        waveform = waveform.mean(axis=1)
    elif waveform.ndim > 2:
        raise ValueError(f"Unsupported number of audio channels: {waveform.ndim}")
        
    # Check sample rate (we don't resample here to keep it simple and deterministic; 
    # we expect IndicVoices to be 16kHz native).
    if sr != target_sr:
        # If resampling is absolutely required, it should be done carefully via librosa,
        # but IndicVoices is 16kHz, so we enforce it here.
        raise ValueError(f"Expected sample rate {target_sr}, got {sr}")
        
    return waveform, sr
