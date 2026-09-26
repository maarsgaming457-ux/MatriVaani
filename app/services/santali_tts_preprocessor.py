def santali_to_tts_text(text: str) -> str:
    """
    Converts Santali Ol Chiki text into a phonetic Devanagari representation 
    specifically optimized for the Sarvam Bulbul v3 Hindi TTS engine.
    """
    if not text:
        return ""
        
    # 1. Phonetic normalizations for Ol Chiki aspirated clusters
    text = text.replace('ᱠᱷ', 'ख').replace('ᱜᱷ', 'घ').replace('ᱪᱷ', 'छ').replace('ᱡᱷ', 'झ')
    text = text.replace('ᱴᱷ', 'ठ').replace('ᱰᱷ', 'ढ').replace('ᱛᱷ', 'थ').replace('ᱫᱷ', 'ध')
    text = text.replace('ᱯᱷ', 'फ').replace('ᱵᱷ', 'भ').replace('ᱲᱷ', 'ढ़')
    
    # 2. Modifiers (GAAHLAA TTUDDAAG)
    text = text.replace('ᱟᱹ', 'অ').replace('ᱚᱹ', 'অ').replace('ᱮᱹ', 'ऐ').replace('ᱳᱹ', 'औ')
    
    VOWEL_IND = {
        'ᱚ': 'ओ', 'ᱟ': 'आ', 'ᱤ': 'इ', 'ᱩ': 'उ', 'ᱮ': 'ए', 'ᱳ': 'ओ',
        'অ': 'अ', 'ऐ': 'ऐ', 'औ': 'औ'
    }
    VOWEL_DEP = {
        'ᱚ': 'ो', 'ᱟ': 'ा', 'ᱤ': 'ि', 'ᱩ': 'ु', 'ᱮ': 'े', 'ᱳ': 'ो',
        'অ': '', 'ऐ': 'ै', 'औ': 'ौ'
    }
    CONSONANTS = {
        'ᱛ': 'त', 'ᱜ': 'ग', 'ᱝ': 'ंग', 'ᱞ': 'ल', 'ᱠ': 'क', 'ᱡ': 'ज',
        'ᱢ': 'म', 'ᱣ': 'व', 'ᱥ': 'स', 'ᱦ': 'ह', 'ᱧ': 'न्य', 'ᱨ': 'र',
        'ᱪ': 'च', 'ᱫ': 'द', 'ᱬ': 'ण', 'ᱭ': 'य', 'ᱯ': 'प', 'ᱰ': 'ड',
        'ᱱ': 'न', 'ᱲ': 'ड़', 'ᱴ': 'ट', 'ᱵ': 'ब', 'ᱶ': 'ंव', 'ᱷ': 'ह',
        'ख':'ख', 'घ':'घ', 'छ':'छ', 'झ':'झ', 'ठ':'ठ', 'ढ':'ढ', 'थ':'थ', 'ध':'ध', 'फ':'फ', 'भ':'भ', 'ढ़':'ढ़'
    }
    NUMERALS = {
        '᱐': '0', '᱑': '1', '᱒': '2', '᱓': '3', '᱔': '4',
        '᱕': '5', '᱖': '6', '᱗': '7', '᱘': '8', '᱙': '9'
    }
    
    out = []
    prev_was_cons = False
    
    for c in text:
        if c in CONSONANTS:
            if prev_was_cons:
                out.append('्')
            out.append(CONSONANTS[c])
            prev_was_cons = True
        elif c in VOWEL_IND:
            if prev_was_cons:
                out.append(VOWEL_DEP[c])
            else:
                out.append(VOWEL_IND[c])
            prev_was_cons = False
        elif c == 'ᱸ':
            out.append('ं')
            # prev_was_cons unchanged
        elif c in NUMERALS:
            out.append(NUMERALS[c])
            prev_was_cons = False
        else:
            out.append(c)
            prev_was_cons = False
            
    res = ''.join(out)
    # Map Ol Chiki punctuation to standard Hindi TTS-friendly punctuation
    res = res.replace('᱾', '.').replace('᱿', '.')
    return res
