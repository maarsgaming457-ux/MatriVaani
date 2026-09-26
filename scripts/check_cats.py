import json
import os

res_path = os.path.join("PHASE_34_TEST_SUITE_RESULTS.json")
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

print("7. CHECK KNOWN 5")
for i, item in enumerate(results["category_a_known_base"]):
    print(f"ID: Known {i+1}")
    print(f"Input: {item['input']}")
    print(f"Expected: {item['expected_intent']}")
    print(f"Actual: {item['translation']}")
    print(f"Tier: {item['method']}")
    print(f"PASS/FAIL: {'PASS' if item['method'] == 'resource_supported_exact_retrieval' else 'FAIL'}")
    print("-")

print("8. CHECK GRAMMAR 5")
for i, item in enumerate(results["category_b_grammar_variants"]):
    print(f"ID: Grammar {i+1}")
    print(f"Input: {item['input']}")
    print(f"Expected: {item['expected_intent']}")
    print(f"Actual: {item['translation']}")
    print(f"Tier: {item['method']}")
    print(f"PASS/FAIL: {'PASS' if 'grammar_rule' in item['method'] else 'FAIL'}")
    print("-")
