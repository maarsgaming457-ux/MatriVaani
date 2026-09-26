from fastapi.testclient import TestClient
from app.api.main import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "asr" in response.json()

def test_process_audio(tmp_path):
    # Force mock providers
    from app.core.config import settings
    settings.ASR_PROVIDER = "mock"
    settings.TRANSLATION_PROVIDER = "mock"
    settings.LLM_PROVIDER = "mock"
    
    file_path = tmp_path / "test.flac"
    file_path.write_bytes(b"dummy audio data")
    
    with open(file_path, "rb") as f:
        # Should fail processing dummy bytes as audio, but test the endpoint wrapper
        # The endpoint uses soundfile which will throw an exception on dummy bytes
        response = client.post(
            "/api/v1/process",
            files={"audio": ("test.flac", f, "audio/flac")},
            data={"target_language": "hi"}
        )
    
    # The pipeline catches the error and returns a structured response with status="failed"
    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert "Audio processing failed" in str(response.json()["errors"])
