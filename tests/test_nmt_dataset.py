import pytest
from pydantic import ValidationError
from data_modules.nmt.schemas import NMTRecord, VerificationStatus, ScriptVariant, DomainCategory
from data_modules.nmt.pipeline import normalize_text, detect_duplicates, validate_and_ingest, generate_splits

def test_normalize_text():
    # Test whitespace normalization
    assert normalize_text("  hello   world  ") == "hello world"
    # Test Ol Chiki preservation
    assert normalize_text(" ᱥᱟᱱᱛᱟᱲᱤ  ") == "ᱥᱟᱱᱛᱟᱲᱤ"
    # Test Devanagari preservation
    assert normalize_text("  नमस्ते  ") == "नमस्ते"

def test_nmt_record_validation():
    # Valid record
    valid_data = {
        "id": "123",
        "source_language": "hi",
        "target_language": "sat",
        "source_script": "Devanagari",
        "target_script": "Ol_Chiki",
        "source_text": "नमस्ते",
        "target_text": "ᱡᱚᱦᱟᱨ",
        "domain": "GENERAL",
        "verification_status": "VERIFIED_HUMAN",
        "source": "EnSanCorp",
        "synthetic": False
    }
    record = NMTRecord(**valid_data)
    assert record.id == "123"

    # Invalid: Synthetic data cannot be VERIFIED_HUMAN
    invalid_data = valid_data.copy()
    invalid_data["synthetic"] = True
    with pytest.raises(ValidationError):
        NMTRecord(**invalid_data)

    # Invalid: TEST split must be verified human and non-synthetic
    invalid_split_data = valid_data.copy()
    invalid_split_data["verification_status"] = "UNVERIFIED"
    invalid_split_data["split"] = "test"
    with pytest.raises(ValidationError):
        NMTRecord(**invalid_split_data)

def test_detect_duplicates():
    records = [
        NMTRecord(id="1", source_text="hello", target_text="world", source="test"),
        NMTRecord(id="2", source_text="hello", target_text="world", source="test"), # Exact duplicate
        NMTRecord(id="3", source_text="hello", target_text="earth", source="test"), # Same source, different target
        NMTRecord(id="4", source_text="hi", target_text="there", source="test"), # Unique
    ]
    
    unique, flagged = detect_duplicates(records)
    
    assert len(unique) == 3 # 1, 3, 4
    assert len(flagged) == 2
    assert flagged[0]["type"] == "exact_duplicate"
    assert flagged[1]["type"] == "conflicting_target"

def test_generate_splits():
    records = [
        NMTRecord(id=f"{i}", source_text=f"hi{i}", target_text=f"sat{i}", source="test", verification_status="VERIFIED_HUMAN")
        for i in range(10)
    ]
    records.append(NMTRecord(id="unverified", source_text="h", target_text="s", source="test", verification_status="UNVERIFIED"))
    records.append(NMTRecord(id="synthetic", source_text="h2", target_text="s2", source="test", synthetic=True, verification_status="MACHINE_GENERATED"))
    
    # 12 records total. 10 eligible for test.
    # 10% of 12 is 1 (for test), 1 (for val).
    splits = generate_splits(records, val_ratio=0.1, test_ratio=0.1)
    
    assert len(splits["test"]) == 1
    assert len(splits["validation"]) == 1
    assert len(splits["train"]) == 10
    
    # Test set must only contain verified human
    for r in splits["test"]:
        assert r.verification_status == VerificationStatus.VERIFIED_HUMAN
        assert not r.synthetic
