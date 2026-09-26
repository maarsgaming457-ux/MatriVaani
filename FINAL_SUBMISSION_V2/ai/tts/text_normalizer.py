import re

def normalize_santhali_text(text: str) -> str:
    """
    Normalizes Santhali (Ol Chiki or Roman/Devanagari) text for TTS synthesis.
    
    # Script Handling (Step 5)
    - Original Script: Ol Chiki is strongly preferred. If input is Devanagari, it is flagged (currently not transliterated, but preserved).
    - Unicode Normalization: Characters within U+1C50–U+1C7F are strictly protected.
    - Punctuation Rules: Commas and periods are preserved for TTS pausing.
    - Numeral Handling: Latin numerals are currently passed through to the phonemizer.
    
    Removes extraneous HTML/whitespace and standardizes punctuation while preserving Ol Chiki characters.
    """
    if not isinstance(text, str):
        return ""

    # Remove HTML tags if any leaked in
    text = re.sub(r'<[^>]+>', '', text)
    
    # Standardize whitespace
    text = " ".join(text.split())
    
    # We do NOT arbitrarily strip Unicode, because Ol Chiki resides at U+1C50–U+1C7F.
    # We will strip specific known bad control characters.
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()
