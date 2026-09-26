import json
import os

OUTPUT_DIR = 'data/ho_hindi/experimental/phase36c_resource_expansion'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_v3_resources():
    ipil_path = 'data/ho_hindi/experimental/ipil_discovered_entries.json'
    ipil_data = {}
    if os.path.exists(ipil_path):
        with open(ipil_path, 'r', encoding='utf-8') as f:
            ipil_data = json.load(f)
            
    with open('data/ho_hindi/experimental/phase36b_hindi_to_ho/HINDI_TO_HO_LEXICON_V2.json', 'r', encoding='utf-8') as f:
        v2_lexicon = json.load(f)
        
    ho_lexicon = {}
    hindi_lexicon = {}
    
    # 1. Expand from IPIL
    for ho_w, entry in ipil_data.items():
        hi_w = entry.get('hindi', '').strip()
        en_w = entry.get('english', '').strip()
        pos = entry.get('pos', 'OTHER')
        
        if not ho_w: continue
        
        meanings_hi = []
        derived = False
        if hi_w:
            meanings_hi.append(hi_w)
        if en_w and not hi_w:
            en_to_hi = {
                "school": "स्कूल", "teacher": "शिक्षक", "student": "छात्र", "book": "किताब",
                "water": "पानी", "food": "खाना", "house": "घर", "village": "गाँव"
            }
            if en_w.lower() in en_to_hi:
                meanings_hi.append(en_to_hi[en_w.lower()])
                derived = True

        ho_lexicon[ho_w] = {
            "ho": ho_w,
            "meanings_hindi": meanings_hi,
            "meanings_english": [en_w] if en_w else [],
            "category": pos,
            "source": "ipil_dictionary",
            "source_type": "derived_from_English" if derived else "direct",
            "machine_generated": derived,
            "human_verified": not derived
        }
        
        for mh in meanings_hi:
            if mh not in hindi_lexicon:
                hindi_lexicon[mh] = []
            hindi_lexicon[mh].append({
                "ho": ho_w,
                "category": pos,
                "source": "ipil_dictionary",
                "machine_generated": derived
            })

    # 2. Add classroom vocab
    classroom_words = [
        ("school", "स्कूल", "इतु ओआः"), ("teacher", "शिक्षक", "मास्टर"), ("student", "छात्र", "पढवन्नी"),
        ("book", "किताब", "पोथी"), ("read", "पढ़ना", "पढव"), ("write", "लिखना", "ओल्"),
        ("water", "पानी", "दाः"), ("food", "खाना", "मंडी"), ("house", "घर", "ओआः"),
        ("village", "गाँव", "हातु"), ("mother", "माँ", "एंगा"), ("father", "पिता", "अपु"),
        ("friend", "दोस्त", "गाते"), ("today", "आज", "तिसिंग"), ("tomorrow", "कल", "गपा"),
        ("yesterday", "बीता कल", "होला"), ("here", "यहाँ", "नेन्ता"), ("there", "वहाँ", "एन्ता"),
        ("who", "कौन", "ओकोए"), ("what", "क्या", "चिकना"), ("where", "कहाँ", "ओकोरे"),
        ("yes", "हाँ", "हेँ"), ("no", "नहीं", "का"), ("one", "एक", "मिद"),
        ("two", "दो", "बार"), ("three", "तीन", "अपी")
    ]
    
    for en, hi, ho in classroom_words:
        ho_lexicon[ho] = {
            "ho": ho,
            "meanings_hindi": [hi],
            "meanings_english": [en],
            "category": "CLASSROOM",
            "source": "john_deeney_grammar",
            "source_type": "direct",
            "machine_generated": False,
            "human_verified": True
        }
        if hi not in hindi_lexicon:
            hindi_lexicon[hi] = []
        hindi_lexicon[hi].append({
            "ho": ho,
            "category": "CLASSROOM",
            "source": "john_deeney_grammar",
            "machine_generated": False
        })
        
    for hi, data in v2_lexicon.items():
        ho = data["ho"]
        if hi not in hindi_lexicon:
            hindi_lexicon[hi] = []
        if not any(h['ho'] == ho for h in hindi_lexicon[hi]):
             hindi_lexicon[hi].append({
                "ho": ho,
                "category": data.get("category", "OTHER"),
                "source": data.get("source", "legacy"),
                "machine_generated": data.get("machine_generated", False)
             })

    with open(f'{OUTPUT_DIR}/HO_LEXICON_V3.json', 'w', encoding='utf-8') as f:
        json.dump(ho_lexicon, f, ensure_ascii=False, indent=2)
    with open(f'{OUTPUT_DIR}/HINDI_TO_HO_LEXICON_V3.json', 'w', encoding='utf-8') as f:
        json.dump(hindi_lexicon, f, ensure_ascii=False, indent=2)
        
    grammar_rules = [
        {"rule_id": "GR001", "description": "Subject + Location + एते + Subject_Clitic + Verb (Past)", "source": "john_deeney"},
        {"rule_id": "GR002", "description": "Subject + Noun + ताना + Subject_Clitic", "source": "john_deeney"},
        {"rule_id": "GR003", "description": "Prohibitive: आलो + Clitic + Verb", "source": "ho_translation_map"}
    ]
    with open(f'{OUTPUT_DIR}/HO_GRAMMAR_RULES_V3.json', 'w', encoding='utf-8') as f:
        json.dump(grammar_rules, f, ensure_ascii=False, indent=2)

    morph_rules = [
        {"marker": "एते", "type": "ablative", "meaning": "from (से)", "attested": True},
        {"marker": "रे", "type": "locative", "meaning": "in/on (में/पर)", "attested": True},
        {"marker": "को", "type": "plural", "meaning": "plural marker", "attested": True},
        {"marker": "ताना", "type": "copula", "meaning": "is/are/am", "attested": True}
    ]
    with open(f'{OUTPUT_DIR}/HO_MORPHOLOGY_RULES.json', 'w', encoding='utf-8') as f:
        json.dump(morph_rules, f, ensure_ascii=False, indent=2)

    templates = [
        {"template_id": "T_V3_001", "semantic_pattern": "{SUBJECT} {LOCATION} से आया था।", "ho_pattern": "{SUBJECT} {LOCATION}एते{SUBJECT_CLITIC} हुजु लेना"},
        {"template_id": "T_V3_002", "semantic_pattern": "{SUBJECT} {NOUN} है।", "ho_pattern": "{SUBJECT} {NOUN} ताना{SUBJECT_CLITIC}"},
        {"template_id": "T_V3_003", "semantic_pattern": "{SUBJECT} {LOCATION} में है।", "ho_pattern": "{SUBJECT} {LOCATION}रे मेना{SUBJECT_CLITIC}"}
    ]
    with open(f'{OUTPUT_DIR}/HO_TEMPLATES_V3.json', 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)

    print(f"Ho Lexicon: {len(ho_lexicon)} entries")
    print(f"Hindi Lexicon: {len(hindi_lexicon)} entries")

if __name__ == '__main__':
    build_v3_resources()
