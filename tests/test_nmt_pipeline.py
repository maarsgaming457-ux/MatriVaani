import pytest
from ai.nmt.inference import translate_text

def test_empty_input():
    assert translate_text("", "dummy_model") == ""
    assert translate_text("   ", "dummy_model") == ""

def test_model_not_found():
    result = translate_text("नमस्ते", "invalid_model_name")
    assert "Translation Error" in result

def test_unicode_handling():
    # Ensure it doesn't crash on Devanagari or Ol Chiki
    result = translate_text("नमस्ते", "invalid_model")
    assert isinstance(result, str)
