import os
import pytest
from app.graph.workflow import run_pipeline
from app.core.config import settings

@pytest.fixture
def mock_audio_file(tmp_path):
    # We create a dummy audio file using soundfile
    import soundfile as sf
    import numpy as np
    
    file_path = str(tmp_path / "test_audio.flac")
    # 1 second of silence at 16kHz
    audio_data = np.zeros(16000, dtype=np.float32)
    sf.write(file_path, audio_data, 16000)
    return file_path

def test_end_to_end_pipeline(mock_audio_file):
    # Force mock providers to avoid external API calls during testing
    from app.core.config import settings
    settings.ASR_PROVIDER = "mock"
    settings.TRANSLATION_PROVIDER = "mock"
    settings.LLM_PROVIDER = "mock"
    
    result = run_pipeline(audio_path=mock_audio_file, target_language="hi")
    
    assert result["status"] == "success"
    # ASR on zero-data with voxpopuli might return empty or weird tokens, but should not crash
    assert "transcript" in result
    assert "translation" in result
    assert "script" in result
    assert "final_script" in result
    
    assert "[MOCK TRANSLATION to hi]" in result["translation"]
    assert "MAIN CONTENT:" in result["script"]
    assert "[EDITED]" in result["final_script"]
