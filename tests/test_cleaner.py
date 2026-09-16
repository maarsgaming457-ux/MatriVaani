import pytest
from app.graph.state import initialize_state
from app.graph.nodes.cleaner import cleaner_node

def test_cleaner_node():
    # Test cases:
    # 1. Normal Santali text with <unintelligible>
    state1 = initialize_state()
    state1["santali_transcript"] = "ᱚᱞ ᱪᱤᱠᱤ <unintelligible>  ᱚᱞ ᱪᱤᱠᱤ "
    state1 = cleaner_node(state1)
    assert state1["cleaned_santali"] == "ᱚᱞ ᱪᱤᱠᱤ ᱚᱞ ᱪᱤᱠᱤ"
    
    # 2. Only unintelligible (should be empty and set warning)
    state2 = initialize_state()
    state2["santali_transcript"] = "<unintelligible>"
    state2 = cleaner_node(state2)
    assert state2["cleaned_santali"] == ""
    assert "Transcript became empty after cleaning." in state2["warnings"]
    
    # 3. Multiple spaces and invisible control characters
    state3 = initialize_state()
    state3["santali_transcript"] = "ᱟᱵᱚ\u200b   ᱫᱚ\u200c"
    state3 = cleaner_node(state3)
    assert state3["cleaned_santali"] == "ᱟᱵᱚ ᱫᱚ"
    
    # 4. English code-switching
    state4 = initialize_state()
    state4["santali_transcript"] = "school ᱨᱮ"
    state4 = cleaner_node(state4)
    assert state4["cleaned_santali"] == "school ᱨᱮ"
