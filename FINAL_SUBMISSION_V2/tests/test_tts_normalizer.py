import pytest
from ai.tts.text_normalizer import normalize_santhali_text

def test_normalize_santhali_text():
    # Test whitespace
    assert normalize_santhali_text("  Ol   Chiki  ") == "Ol Chiki"
    
    # Test HTML removal
    assert normalize_santhali_text("<b>Santhali</b>") == "Santhali"
    
    # Test keeping Ol Chiki characters (mock example Unicode range)
    # ᱚ is U+1C5A
    assert normalize_santhali_text("ᱚ ᱛ ᱜ ᱝ") == "ᱚ ᱛ ᱜ ᱝ"
    
    # Test control char stripping
    assert normalize_santhali_text("bad\x00char") == "badchar"
