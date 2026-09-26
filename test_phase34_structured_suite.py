import os
import sys
import json
import time
import logging

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from dotenv import load_dotenv
load_dotenv()

from app.services.experimental_ho_translation.translator import experimental_ho_translator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("phase34_suite")

def run_structured_tests():
    logger.info("Starting Phase 34 Structured Test Suite & Edge Case Validation...")

    # Category A: Known Base Sentences (from authentic 196 dataset)
    cat_a = [
        {"input": "आबु एन हो को नेनता काबु बेटा इचि कोआ", "expected_intent": "हम उन लोगों को यहाँ पहुँचने नहीं देंगे।", "note": "Authentic base record 1"},
        {"input": "एन ओआ: आलेया हातुरे का हुजुए", "expected_intent": "वह घर हमारे गाँव में नहीं आएगा।", "note": "Authentic base record 4"},
        {"input": "एना आलेया हातुरे का हुजुए", "expected_intent": "वह हमारे गाँव में नहीं आता है।", "note": "Authentic base record 6"},
        {"input": "एन हापानुम लो पोन रेञ जागार केना", "expected_intent": "मैंने उस युवती के साथ फोन पर बात की थी।", "note": "Authentic base record 8"},
        {"input": "आए लो पोन रेञ जागार केना", "expected_intent": "मैंने फोन पर उससे बात की थी।", "note": "Authentic base record 9"}
    ]

    # Category B: Known Grammar Variants (from synthetic augmented / concord rules)
    cat_b = [
        {"input": "आबु एन हो किन नेनता काबु बेटा इचि कोआ", "expected_intent": "हम उन दोनों को यहाँ पहुँचने नहीं देंगे।", "note": "Dual marker substitution (-kin)"},
        {"input": "एन हातु आलेया हातुरे का हुजुए", "expected_intent": "वह गाँव हमारे गाँव में नहीं आएगा।", "note": "Locative noun substitution (घर -> गाँव)"},
        {"input": "साबिन हातु रे मियड सेता मेनाइए", "expected_intent": "हर गाँव में एक कुत्ता है।", "note": "Existential locative substitution"},
        {"input": "आइंग जोका मान्डि एमाइंगपे", "expected_intent": "मुझे थोड़ा भात दीजिए।", "note": "Mass noun substitution (दा: -> मान्डि)"},
        {"input": "आए एन पुतिको हातु रे बागे ताडा", "expected_intent": "उसने वे किताबें गाँव में छोड़ रखी हैं।", "note": "Plural object locative substitution"}
    ]

    # Category C: Unseen Authentic Ho Sentences (Authentic Deeney constructions not in 196 base)
    cat_c = [
        {"input": "अले ओआ:रे मेना:लेया।", "expected_intent": "हम लोग घर में हैं। (Deeney 1978: exclusive plural in house)"},
        {"input": "हो को हातु रे मेना:कोआ।", "expected_intent": "हो लोग गाँव में हैं। (Plural human existential)"},
        {"input": "आइंग दाः नुः ताना।", "expected_intent": "मैं पानी पी रहा हूँ। (Drinking water present continuous)"},
        {"input": "सोमा मंडी जोम ताना।", "expected_intent": "सोमा खाना खा रहा है। (Eating food continuous)"},
        {"input": "ने ओआ: रे ओकोए मेनाइए?", "expected_intent": "इस घर में कौन है? (Interrogative locative existential)"},
        {"input": "आबु गपा सेनोःआबु।", "expected_intent": "हम कल चलेंगे / जाएँगे। (Future temporal adverbial)"}
    ]

    # Edge Cases & Negative Constraints (Task 13 & 14)
    edge_cases = [
        {"input": "", "type": "empty_string", "desc": "Empty input string"},
        {"input": "   ", "type": "whitespace_only", "desc": "Whitespace only"},
        {"input": "Hello how are you today?", "type": "english_latin", "desc": "Latin script English sentence"},
        {"input": "नमस्ते, आप कैसे हैं और क्या कर रहे हैं?", "type": "hindi_input", "desc": "Hindi mistakenly passed as Ho"},
        {"input": "सेनोः", "type": "single_word", "desc": "Single Ho lexical verb"},
        {"input": "ओआ:", "type": "single_noun", "desc": "Single Ho noun with glottal stop"},
        {"input": "asdfghjkl qwertyuiop zxcvbnm", "type": "gibberish", "desc": "Random non-lexical string"},
        {"input": "अम " * 40, "type": "long_input", "desc": "Repetitive extremely long string"}
    ]

    suite_results = {
        "category_a_known_base": [],
        "category_b_grammar_variants": [],
        "category_c_unseen_authentic": [],
        "edge_cases": []
    }

    # Run Category A
    logger.info("Evaluating Category A: Known Base Sentences...")
    for item in cat_a:
        t0 = time.time()
        res = experimental_ho_translator.translate(item["input"])
        lat = time.time() - t0
        suite_results["category_a_known_base"].append({
            "input": item["input"],
            "expected_intent": item["expected_intent"],
            "translation": res["translation"],
            "method": res["method"],
            "confidence": res["confidence"],
            "ground_truth": res.get("ground_truth", False),
            "human_verified": res.get("human_verified", False),
            "latency_sec": round(lat, 3)
        })

    # Run Category B
    logger.info("Evaluating Category B: Known Grammar Variants...")
    for item in cat_b:
        t0 = time.time()
        res = experimental_ho_translator.translate(item["input"])
        lat = time.time() - t0
        suite_results["category_b_grammar_variants"].append({
            "input": item["input"],
            "expected_intent": item["expected_intent"],
            "translation": res["translation"],
            "method": res["method"],
            "confidence": res["confidence"],
            "ground_truth": res.get("ground_truth", False),
            "human_verified": res.get("human_verified", False),
            "latency_sec": round(lat, 3)
        })

    # Run Category C
    logger.info("Evaluating Category C: Unseen Authentic Ho...")
    for item in cat_c:
        t0 = time.time()
        res = experimental_ho_translator.translate(item["input"])
        lat = time.time() - t0
        suite_results["category_c_unseen_authentic"].append({
            "input": item["input"],
            "expected_intent": item["expected_intent"],
            "translation": res["translation"],
            "method": res["method"],
            "confidence": res["confidence"],
            "ground_truth": res.get("ground_truth", False),
            "human_verified": res.get("human_verified", False),
            "latency_sec": round(lat, 3)
        })

    # Run Edge Cases
    logger.info("Evaluating Edge Cases & Negative Constraints...")
    for item in edge_cases:
        t0 = time.time()
        res = experimental_ho_translator.translate(item["input"])
        lat = time.time() - t0
        suite_results["edge_cases"].append({
            "input": item["input"][:50] + ("..." if len(item["input"]) > 50 else ""),
            "type": item["type"],
            "desc": item["desc"],
            "translation": res["translation"],
            "method": res["method"],
            "confidence": res["confidence"],
            "ground_truth": res.get("ground_truth", False),
            "human_verified": res.get("human_verified", False),
            "latency_sec": round(lat, 3)
        })

    with open("PHASE_34_TEST_SUITE_RESULTS.json", "w", encoding="utf-8") as f:
        json.dump(suite_results, f, ensure_ascii=False, indent=2)

    logger.info("Structured Test Suite complete. Saved to PHASE_34_TEST_SUITE_RESULTS.json")

if __name__ == "__main__":
    run_structured_tests()
