import pytest
import os
import sys
from pathlib import Path

from data_modules.validation.validator import DatasetValidator
from data_modules.schemas.schemas import QualityStatus

def test_nmt_schema_validation():
    validator = DatasetValidator("nmt")
    
    valid_record = {
        "sample_id": "NMT-001",
        "source_language": "hi",
        "target_language": "sat",
        "source_text": "नमस्ते",
        "target_text": "Johar",
        "domain": "greeting",
        "dataset_version": "v0.1"
    }
    
    invalid_record = {
        "sample_id": "NMT-002",
        "source_language": "en", # invalid language choice
        "target_language": "sat",
        "source_text": "Hello",
        "target_text": "Johar",
        "domain": "greeting",
        "dataset_version": "v0.1"
    }
    
    report = validator.validate_records([valid_record, invalid_record])
    
    assert report["total_records"] == 2
    assert report["valid_records"] == 1
    assert report["invalid_records"] == 1
    assert "source_language" in report["errors"][0]["error"]

def test_duplicate_detection():
    validator = DatasetValidator("nmt")
    
    record = {
        "sample_id": "NMT-001",
        "source_language": "hi",
        "target_language": "sat",
        "source_text": "नमस्ते",
        "target_text": "Johar",
        "domain": "greeting",
        "dataset_version": "v0.1"
    }
    
    # Pass the same record twice
    report = validator.validate_records([record, record])
    
    assert len(report["duplicate_ids"]) == 1
    assert report["duplicate_ids"][0] == "NMT-001"
    assert len(report["duplicate_content"]) == 1

def test_missing_audio_file(tmp_path):
    validator = DatasetValidator("asr")
    
    record = {
        "sample_id": "ASR-001",
        "language": "hi",
        "speaker_id": "SPK01",
        "audio_path": "non_existent.wav",
        "transcript": "नमस्ते",
        "domain": "greeting",
        "duration_seconds": 2.5,
        "sample_rate": 16000,
        "dataset_version": "v0.1"
    }
    
    report = validator.validate_records([record], root_dir=str(tmp_path))
    assert report["invalid_records"] == 1
    assert "Audio file not found" in report["errors"][0]["error"]

def test_valid_audio_file(tmp_path):
    # Create a dummy audio file
    audio_file = tmp_path / "existent.wav"
    audio_file.write_text("dummy audio content")
    
    validator = DatasetValidator("asr")
    
    record = {
        "sample_id": "ASR-001",
        "language": "hi",
        "speaker_id": "SPK01",
        "audio_path": "existent.wav",
        "transcript": "नमस्ते",
        "domain": "greeting",
        "duration_seconds": 2.5,
        "sample_rate": 16000,
        "dataset_version": "v0.1"
    }
    
    report = validator.validate_records([record], root_dir=str(tmp_path))
    assert report["valid_records"] == 1
