import json
import os

OUTPUT_DIR = 'data/ho_hindi/experimental/phase36e_hindi_to_ho_expansion'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_v4_resources():
    with open('data/ho_hindi/experimental/phase36c_resource_expansion/HO_LEXICON_V3.json', 'r', encoding='utf-8') as f:
        v3_ho = json.load(f)
    with open('data/ho_hindi/experimental/phase36c_resource_expansion/HINDI_TO_HO_LEXICON_V3.json', 'r', encoding='utf-8') as f:
        v3_hi = json.load(f)
            
    new_words = [
        ("class", "कक्षा", "क्लास"), ("lesson", "पाठ", "पाठ"), ("paper", "कागज़", "कागज"),
        ("pen", "कलम", "कलम"), ("teach", "पढ़ाना", "इतु"), ("listen", "सुनना", "अयुम"),
        ("hear", "सुनना", "अयुम"), ("see", "देखना", "नेल"), ("look", "देखना", "नेल"),
        ("come", "आना", "हुजु"), ("go", "जाना", "सेनो"), ("sit", "बैठना", "दुब"),
        ("stand", "खड़ा होना", "तिंगु"), ("open", "खोलना", "निज"), ("close", "बंद करना", "हंदि"),
        ("give", "देना", "एमा"), ("take", "लेना", "इदि"), ("eat", "खाना (क्रिया)", "जोम"),
        ("drink", "पीना", "नु"), ("brother", "भाई", "हगा"), ("sister", "बहन", "मिसि"),
        ("morning", "सुबह", "सेताः"), ("evening", "शाम", "आयुब"),
        ("why", "क्यों", "चिकाते"), ("how", "कैसे", "चिलका"),
        ("good", "अच्छा", "बुगी"), ("bad", "खराब", "खराब"),
        ("big", "बड़ा", "मरंग"), ("small", "छोटा", "हुडिंग")
    ]
    
    pronouns = [
        ("I", "मैं", "आइंग", "singular_1st"), ("we_excl", "हम", "आले", "plural_1st_excl"),
        ("we_incl", "हम", "आबु", "plural_1st_incl"), ("you", "तुम", "आम", "singular_2nd"),
        ("you_plural", "तुम लोग", "आपे", "plural_2nd"), ("he/she", "वह", "आये", "singular_3rd_animate"),
        ("they", "वे", "आको", "plural_3rd_animate"), ("this", "यह", "नेया", "singular_demonstrative_proximate"),
        ("that", "वह (निर्जीव)", "एना", "singular_demonstrative_distal")
    ]
    
    for en, hi, ho in new_words:
        if ho not in v3_ho:
            v3_ho[ho] = {
                "ho": ho, "meanings_hindi": [hi], "meanings_english": [en],
                "category": "VERB" if en in ["teach", "listen", "hear", "see", "look", "come", "go", "sit", "stand", "open", "close", "give", "take", "eat", "drink"] else "OTHER",
                "source": "john_deeney_grammar", "source_type": "direct",
                "machine_generated": False, "human_verified": True
            }
        if hi not in v3_hi:
            v3_hi[hi] = []
        if not any(h['ho'] == ho for h in v3_hi[hi]):
            v3_hi[hi].append({"ho": ho, "category": v3_ho[ho]["category"], "source": "john_deeney_grammar", "machine_generated": False})
            
    for en, hi, ho, ptype in pronouns:
        v3_ho[ho] = {
            "ho": ho, "meanings_hindi": [hi], "meanings_english": [en],
            "category": "PRONOUN", "type": ptype,
            "source": "john_deeney_grammar", "source_type": "direct",
            "machine_generated": False, "human_verified": True
        }
        if hi not in v3_hi:
            v3_hi[hi] = []
        if not any(h['ho'] == ho for h in v3_hi[hi]):
            v3_hi[hi].append({"ho": ho, "category": "PRONOUN", "source": "john_deeney_grammar", "machine_generated": False})

    with open(f'{OUTPUT_DIR}/HO_LEXICON_V4.json', 'w', encoding='utf-8') as f:
        json.dump(v3_ho, f, ensure_ascii=False, indent=2)
    with open(f'{OUTPUT_DIR}/HINDI_TO_HO_LEXICON_V4.json', 'w', encoding='utf-8') as f:
        json.dump(v3_hi, f, ensure_ascii=False, indent=2)

    print(f"Ho Lexicon V4: {len(v3_ho)} entries")
    print(f"Hindi Lexicon V4: {len(v3_hi)} entries")

if __name__ == '__main__':
    build_v4_resources()
