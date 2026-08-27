import os
import io
import pytest
import soundfile as sf
import numpy as np
from datasets import load_dataset, Audio
from transformers import AutoFeatureExtractor

@pytest.mark.integration
def test_real_santali_audio_decode_and_preprocess():
    """
    Integration test to verify that the Santali audio payload from IndicVoices
    can be successfully streamed, downloaded (bytes), decoded using soundfile (FLAC),
    and preprocessed by the wav2vec2 feature extractor.
    """
    # 1. Access dataset (1 sample only to preserve RAM)
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split="train", streaming=True)
    # Bypass torchcodec native load
    ds = ds.cast_column("audio_filepath", Audio(decode=False))
    
    sample = next(iter(ds))
    
    # 2. Extract payload
    audio_bytes = sample["audio_filepath"]["bytes"]
    assert audio_bytes is not None, "Audio bytes payload missing"
    assert audio_bytes[:4] == b'fLaC', "Audio is not in FLAC format"
    
    # 3. Decode
    with io.BytesIO(audio_bytes) as f:
        waveform, sr = sf.read(f)
    
    assert sr == 16000, f"Expected 16000Hz, got {sr}Hz"
    assert waveform.ndim in (1, 2), "Waveform must be mono or stereo"
    
    if waveform.ndim == 2:
        waveform = waveform.mean(axis=1)
        
    assert len(waveform) > 0, "Decoded waveform is empty"
    assert np.isfinite(waveform).all(), "Waveform contains NaN/Inf values"
    
    # 4. ASR Preprocessing
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    
    inputs = feature_extractor(waveform, sampling_rate=sr, return_tensors="pt")
    input_tensor = inputs.input_values
    
    assert input_tensor.shape[0] == 1, "Batch dimension mismatch"
    assert input_tensor.shape[1] == len(waveform), "Sequence length mismatch after preprocessing"
    assert np.isfinite(input_tensor.numpy()).all(), "ASR tensor contains NaN/Inf values"
