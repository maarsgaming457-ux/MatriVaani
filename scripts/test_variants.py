import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.experimental_ho_translation.translator import experimental_ho_translator

cat_b = [
    {"input": "आबु एन हो किन नेनता काबु बेटा इचि कोआ", "expected_intent": "हम उन दोनों को यहाँ पहुँचने नहीं देंगे।", "note": "Dual marker substitution (-kin)"},
    {"input": "एन हातु आलेया हातुरे का हुजुए", "expected_intent": "वह गाँव हमारे गाँव में नहीं आएगा।", "note": "Locative noun substitution (घर -> गाँव)"},
    {"input": "साबिन हातु रे मियड सेता मेनाइए", "expected_intent": "हर गाँव में एक कुत्ता है।", "note": "Existential locative substitution"},
    {"input": "आइंग जोका मान्डि एमाइंगपे", "expected_intent": "मुझे थोड़ा भात दीजिए।", "note": "Mass noun substitution (दा: -> मान्डि)"},
    {"input": "आए एन पुतिको हातु रे बागे ताडा", "expected_intent": "उसने वे किताबें गाँव में छोड़ रखी हैं।", "note": "Plural object locative substitution"}
]

with open('variant_results.txt', 'w', encoding='utf8') as f:
    for i, item in enumerate(cat_b):
        res = experimental_ho_translator.translate(item["input"])
        f.write(f"ID: Variant {i+1}\n")
        f.write(f"INPUT: {item['input']}\n")
        f.write(f"EXPECTED: {item['expected_intent']}\n")
        f.write(f"ACTUAL: {res['translation']}\n")
        f.write(f"TIER: {res['method']}\n")
        f.write(f"CONFIDENCE: {res['confidence']}\n")
        if res['method'] == 'grammar_substitution' or res['method'] == 'grammar_rule':
            f.write("PASS/FAIL: PASS\n")
        else:
            f.write(f"PASS/FAIL: FAIL (Reason: Method was {res['method']}, expected grammar_substitution/grammar_rule)\n")
        f.write("-" * 40 + "\n")
