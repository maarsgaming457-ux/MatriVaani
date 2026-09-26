import os
import pytest
from data_modules.santali.local_cache_loader import LocalSantaliDataset
import json

@pytest.fixture
def mock_cache(tmp_path):
    meta_dir = tmp_path / "metadata"
    meta_dir.mkdir()
    train_file = meta_dir / "train.jsonl"
    
    import soundfile as sf
    import numpy as np
    
    # Create fake audio
    audio_path = str(tmp_path / "test.flac")
    sf.write(audio_path, np.zeros(16000), 16000, format='FLAC', subtype='PCM_16')
    
    with open(train_file, "w") as f:
        f.write(json.dumps({
            "sample_id": "test_1",
            "audio_path": audio_path,
            "transcript": "ᱚᱞ ᱪᱤᱠᱤ",
            "duration": 1.0,
            "language_code": "sat",
            "split": "train"
        }) + "\n")
        
    return str(train_file)

def test_local_cache_loader(mock_cache):
    dataset = LocalSantaliDataset(mock_cache)
    assert len(dataset) == 1
    
    item = dataset[0]
    assert item["sample_id"] == "test_1"
    assert item["normalized_text"] == "ᱚᱞ ᱪᱤᱠᱤ"
    assert item["sample_rate"] == 16000
    assert item["waveform"].shape == (16000,)
