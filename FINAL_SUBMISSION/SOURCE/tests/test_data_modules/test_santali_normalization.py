import os
import sys

# Prevent shadowing the pip datasets module in tests
sys.path = [p for p in sys.path if p != '' and p != os.getcwd()]
# Add project root back to path for imports to work
sys.path.insert(0, os.getcwd())

import pytest
from data_modules.santali.text_normalizer import SantaliNormalizer

def test_normalization():
    normalizer = SantaliNormalizer()
    
    # Test basic normalization
    assert normalizer.normalize("  \u1c50\u1c51   \u1c52 ")["normalized_text"] == "\u1c50\u1c51 \u1c52"
    
    # Test invisible char removal
    assert normalizer.normalize("\u1c50\u200b\u1c51")["normalized_text"] == "\u1c50\u1c51"
    
    # Test original text preservation
    assert normalizer.normalize("  \u1c50 ")["original_text"] == "  \u1c50 "
    
def test_ol_chiki_detection():
    normalizer = SantaliNormalizer()
    
    # Pure Ol Chiki
    assert normalizer.is_predominantly_ol_chiki("\u1c50\u1c51\u1c52") == True
    
    # Mixed with spaces
    assert normalizer.is_predominantly_ol_chiki("\u1c50 \u1c51 \u1c52") == True
    
    # Not Ol Chiki
    assert normalizer.is_predominantly_ol_chiki("Hello World") == False
    
def test_script_identification():
    normalizer = SantaliNormalizer()
    assert normalizer.identify_script("\u1c50\u1c51\u1c52") == "ol_chiki"
    assert normalizer.identify_script("नमस्ते") == "devanagari"
    assert normalizer.identify_script("Hello") == "latin"
    assert normalizer.identify_script("\u1c50 H") == "mixed"
    assert normalizer.identify_script("") == "empty"
