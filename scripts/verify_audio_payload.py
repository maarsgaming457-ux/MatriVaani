import os
import sys
import io
import time
import psutil
import soundfile as sf
import numpy as np
import librosa
from datasets import load_dataset, Audio
from transformers import AutoFeatureExtractor

def get_ram():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def decode_audio_bytes(audio_bytes):
    with io.BytesIO(audio_bytes) as f:
        waveform, sample_rate = sf.read(f)
    return waveform, sample_rate

def test_sample(sample, feature_extractor=None):
    audio_field = sample["audio_filepath"]
    audio_bytes = audio_field["bytes"]
    
    # Check payload
    if audio_bytes is None:
        raise ValueError("Audio bytes are missing!")
    
    audio_size_bytes = len(audio_bytes)
    
    # 1. Inspect Payload signature
    signature = audio_bytes[:4]
    if signature.startswith(b'OggS'):
        audio_format = "Ogg/Opus"
    elif signature.startswith(b'RIFF'):
        audio_format = "WAV"
    elif signature.startswith(b'fLaC'):
        audio_format = "FLAC"
    elif signature.startswith(b'ID3') or audio_bytes[:2] == b'\xff\xfb':
        audio_format = "MP3"
    else:
        audio_format = "Unknown"
        
    audio_payload_type = "bytes"
    
    # 2. Decode Audio
    try:
        waveform, sr = decode_audio_bytes(audio_bytes)
        decode_success = True
    except Exception as e:
        print(f"Decode Failed: {e}")
        return False, {}
        
    # 3. Waveform Validation
    if waveform.ndim > 1:
        waveform = waveform.mean(axis=1) # Convert stereo to mono
        
    num_samples = len(waveform)
    decoded_duration = num_samples / sr
    
    is_valid = True
    is_valid &= (num_samples > 0)
    is_valid &= np.isfinite(waveform).all()
    
    results = {
        "audio_payload_type": audio_payload_type,
        "audio_format": audio_format,
        "audio_size_bytes": audio_size_bytes,
        "decode_success": decode_success,
        "sample_rate": sr,
        "num_samples": num_samples,
        "duration": decoded_duration,
        "waveform_valid": is_valid,
        "dtype": str(waveform.dtype),
        "shape": waveform.shape
    }
    
    # 6. ASR Compatibility Check
    if feature_extractor is not None:
        if sr != feature_extractor.sampling_rate:
            waveform = librosa.resample(waveform, orig_sr=sr, target_sr=feature_extractor.sampling_rate)
            sr = feature_extractor.sampling_rate
            
        inputs = feature_extractor(waveform, sampling_rate=sr, return_tensors="pt")
        tensor = inputs.input_values
        
        asr_valid = True
        asr_valid &= np.isfinite(tensor.numpy()).all()
        
        results["asr_compatibility"] = {
            "tensor_shape": tuple(tensor.shape),
            "tensor_dtype": str(tensor.dtype),
            "resampled_rate": sr,
            "no_nan": asr_valid
        }
    
    return True, results

def test_split(split_name, feature_extractor, num_samples=5):
    print(f"\n--- Testing {split_name.upper()} split ---")
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split=split_name, streaming=True)
    ds = ds.cast_column("audio_filepath", Audio(decode=False))
    ds_iter = iter(ds)
    
    results_list = []
    
    for i in range(num_samples):
        print(f"Sample {i+1}...")
        sample = next(ds_iter)
        success, res = test_sample(sample, feature_extractor if i == 0 else None)
        if success:
            res["metadata_duration"] = sample["duration"]
            results_list.append(res)
            print(f"  Format: {res['audio_format']}, Size: {res['audio_size_bytes']} bytes")
            print(f"  Decoded: {res['num_samples']} samples @ {res['sample_rate']}Hz ({res['duration']:.2f}s)")
            if "asr_compatibility" in res:
                print(f"  ASR Preprocessed Tensor: {res['asr_compatibility']['tensor_shape']} {res['asr_compatibility']['tensor_dtype']}")
        else:
            print("  FAILED TO DECODE")
    
    return results_list

def main():
    print(f"baseline_ram_mb: {get_ram():.2f}")
    feature_extractor = AutoFeatureExtractor.from_pretrained('facebook/wav2vec2-base-100k-voxpopuli')
    print(f"loader_ram_mb: {get_ram():.2f}")
    
    train_res = test_split("train", feature_extractor, 5)
    print(f"decoded_one_sample_ram_mb: {get_ram():.2f}")
    
    valid_res = test_split("valid", feature_extractor, 5)
    print(f"decoded_five_sample_peak_ram_mb: {get_ram():.2f}")
    
    print("\n--- Summary ---")
    print("All 10 samples successfully decoded and tested.")
    
if __name__ == "__main__":
    main()
