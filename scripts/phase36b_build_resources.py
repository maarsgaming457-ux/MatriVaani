import json
import os
import re

OUTPUT_DIR = 'data/ho_hindi/experimental/phase36b_hindi_to_ho'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_v2_resources():
    # Load old resources
    with open('data/ho_hindi/experimental/phase36a_hindi_to_ho/HINDI_TO_HO_LEXICON.json', 'r', encoding='utf-8') as f:
        lexicon_v1 = json.load(f)
    with open('data/ho_hindi/experimental/phase36a_hindi_to_ho/HO_TEMPLATES.json', 'r', encoding='utf-8') as f:
        templates_v1 = json.load(f)
    with open('data/ho_hindi/experimental/phase36a_hindi_to_ho/HO_GRAMMAR_RULES.json', 'r', encoding='utf-8') as f:
        grammar_v1 = json.load(f)
        
    # --- 1. LEXICON V2 ---
    # We will expand the lexicon slightly and categorize words.
    lexicon_v2 = {}
    for hi, data in lexicon_v1.items():
        # Heuristics for categories
        category = "OTHER"
        ho_w = data['ho']
        if hi in ['मैं', 'तुम', 'हम', 'वह', 'वे']:
            category = "PRONOUN"
        elif hi.endswith('ना') and len(hi) > 2:
            category = "VERB"
        elif hi in ['यहाँ', 'वहाँ', 'कहाँ']:
            category = "LOCATION"
        else:
            category = "NOUN"
            
        lexicon_v2[hi] = {
            "hindi": hi,
            "ho": ho_w,
            "category": category,
            "source": data['source'],
            "source_type": data['source_type'],
            "confidence": data['confidence'],
            "machine_generated": data['machine_generated'],
            "human_verified": data['human_verified'],
            "ground_truth": data['ground_truth'],
            "notes": "Inherited from V1"
        }
    
    # --- 2. TEMPLATES V2 ---
    # Convert rigid templates into slot-based templates
    templates_v2 = []
    
    # Examples of generalizations
    # 1. "मैं गंगटोक से आया था।" -> "मैं {LOCATION} से {VERB} था।"
    # 2. "आम लो पोन रेञ जागार केना" (I talked on phone with you)
    
    # We'll just define some generic templates manually based on the grammar rules
    templates_v2 = [
        {
            "template_id": "T_V2_001",
            "semantic_pattern": "{SUBJECT} {LOCATION} से आया था।",
            "ho_pattern": "{SUBJECT} {LOCATION}एते{SUBJECT_CLITIC} हुजु लेना",
            "variables": ["SUBJECT", "LOCATION", "SUBJECT_CLITIC"],
            "source_examples": ["मैं गंगटोक से आया था। -> आइंग गेंगटोकेतेइंग हुजु लेना"],
            "confidence": "HIGH",
            "limitations": "Works primarily with 1st person singular 'मैं' (आइंग / -इंग)."
        },
        {
            "template_id": "T_V2_002",
            "semantic_pattern": "तुम कुछ मत करो।",
            "ho_pattern": "अम जाना आलोम चिकेया",
            "variables": [],
            "source_examples": ["तुम कुछ मत करो। -> अम जाना आलोम चिकेया"],
            "confidence": "HIGH",
            "limitations": "Fixed prohibitive phrase."
        },
        {
            "template_id": "T_V2_003",
            "semantic_pattern": "{SUBJECT} एक {NOUN} है।",
            "ho_pattern": "{SUBJECT} {NOUN} ताना{SUBJECT_CLITIC}",
            "variables": ["SUBJECT", "NOUN", "SUBJECT_CLITIC"],
            "source_examples": ["मैं एक किसान हूँ। -> आइंग चास हो तानाइंग"],
            "confidence": "HIGH",
            "limitations": "Predicative equational noun clause."
        }
    ]
    
    # Retain the rest as rigid
    for t in templates_v1:
        if t["hindi_example"] not in ["मैं गंगटोक से आया था।", "तुम कुछ मत करो।", "मैं एक किसान हूँ।"]:
            templates_v2.append({
                "template_id": "V2_" + t["template_id"],
                "semantic_pattern": t["hindi_example"],
                "ho_pattern": t["ho_example"],
                "variables": [],
                "source_examples": [f'{t["hindi_example"]} -> {t["ho_example"]}'],
                "confidence": "HIGH",
                "limitations": "Rigid exact match."
            })
            
    # --- 3. GRAMMAR RULES V2 ---
    grammar_v2 = []
    for g in grammar_v1:
        grammar_v2.append({
            "rule_id": "V2_" + g["rule_id"],
            "pattern": "UNKNOWN",
            "description": g["description"],
            "source": g["source"],
            "example": g["example_ho"],
            "confidence": g["confidence"],
            "supported_variables": [],
            "limitations": "Derived from 100-sentence corpus"
        })

    # Save
    with open(os.path.join(OUTPUT_DIR, 'HINDI_TO_HO_LEXICON_V2.json'), 'w', encoding='utf-8') as f:
        json.dump(lexicon_v2, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTPUT_DIR, 'HO_TEMPLATES_V2.json'), 'w', encoding='utf-8') as f:
        json.dump(templates_v2, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTPUT_DIR, 'HO_GRAMMAR_RULES_V2.json'), 'w', encoding='utf-8') as f:
        json.dump(grammar_v2, f, ensure_ascii=False, indent=2)

    print(f"Lexicon V2: {len(lexicon_v2)} entries")
    print(f"Templates V2: {len(templates_v2)} entries")
    print(f"Grammar V2: {len(grammar_v2)} entries")

if __name__ == '__main__':
    build_v2_resources()
