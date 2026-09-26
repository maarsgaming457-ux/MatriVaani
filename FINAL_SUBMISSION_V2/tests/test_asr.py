import pytest
import os
import sys
import numpy as np
import soundfile as sf
from pathlib import Path
from unittest.mock import patch

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai.asr.base import ASRModel
from ai.asr.benchmark import benchmark_model
from ai.asr.model_loader import get_asr_model

class MockASR(ASRModel):
    def __init__(self, should_fail_load=False):
        super().__init__("mock/asr", "1.0")
        self.should_fail_load = should_fail_load
        
    def load_model(self):
        if self.should_fail_load:
            raise RuntimeError("Model missing")
        self.is_loaded = True
        
    def transcribe(self, audio_path: str, language: str) -> str:
        if not Path(audio_path).exists():
            raise FileNotFoundError("Audio file invalid")
        return "नमस्ते दुनिया"

def create_dummy_audio(path: str):
    samples = np.zeros(16000, dtype=np.float32)
    sf.write(path, samples, 16000)

def test_missing_model():
    model = MockASR(should_fail_load=True)
    with pytest.raises(RuntimeError):
        model.load_model()

def test_invalid_audio(tmp_path):
    model = MockASR()
    model.load_model()
    with pytest.raises(FileNotFoundError):
        model.transcribe(str(tmp_path / "does_not_exist.wav"), "hi")

@patch('ai.asr.benchmark.get_asr_model')
def test_benchmark_output_schema(mock_get_model, tmp_path):
    mock_model = MockASR()
    mock_get_model.return_value = mock_model
    
    audio_file = tmp_path / "test.wav"
    create_dummy_audio(str(audio_file))
    
    res = benchmark_model("mock/asr", str(audio_file), "नमस्ते दुनिया", "hi", num_runs=1)
    
    # Test strict output format
    required_keys = ["model", "version", "language", "dataset", "dataset_version", 
                     "samples", "wer", "cer", "latency_ms", "real_time_factor", 
                     "ram_mb", "model_size_mb", "cold_start_latency_ms", "p95_latency_ms", "peak_ram_mb"]
    for k in required_keys:
        assert k in res
