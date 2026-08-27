import unicodedata
import re

class SantaliNormalizer:
    def __init__(self):
        # We preserve legitimate Ol Chiki characters, whitespace, and basic punctuation.
        # Ol Chiki Unicode range is U+1C50 - U+1C7F
        self.ol_chiki_pattern = re.compile(r'[\u1c50-\u1c7f]')

    def normalize(self, text: str) -> dict:
        if not text:
            return {"original_text": text, "normalized_text": ""}
        
        # 1. Unicode Normalization (NFC)
        normalized = unicodedata.normalize('NFC', text)
        
        # 2. Whitespace normalization (replace multiple spaces with single space)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # 3. Strip leading/trailing whitespace
        normalized = normalized.strip()
        
        # 4. Remove invisible control characters (except legitimate whitespace like space)
        normalized = re.sub(r'[\u200b\u200c\u200d\uFEFF]', '', normalized)
        
        return {
            "original_text": text,
            "normalized_text": normalized
        }

    def is_predominantly_ol_chiki(self, text: str, threshold: float = 0.5) -> bool:
        if not text:
            return False
            
        # Count Ol Chiki characters vs total non-whitespace characters
        chars = [c for c in text if not c.isspace()]
        if not chars:
            return False
            
        ol_chiki_count = sum(1 for c in chars if self.ol_chiki_pattern.match(c))
        return (ol_chiki_count / len(chars)) >= threshold

    def identify_script(self, text: str) -> str:
        if not text:
            return "empty"
            
        chars = [c for c in text if not c.isspace()]
        if not chars:
            return "empty"
            
        ol_chiki_count = sum(1 for c in chars if self.ol_chiki_pattern.match(c))
        devanagari_count = sum(1 for c in chars if '\u0900' <= c <= '\u097f')
        latin_count = sum(1 for c in chars if ('a' <= c.lower() <= 'z'))
        
        total = len(chars)
        
        if ol_chiki_count / total >= 0.8:
            return "ol_chiki"
        elif devanagari_count / total >= 0.8:
            return "devanagari"
        elif latin_count / total >= 0.8:
            return "latin"
        else:
            return "mixed"
