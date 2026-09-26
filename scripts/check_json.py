import json
import os

res_path = os.path.join("data", "ho_hindi", "experimental", "phase35a_100_sentence_validation", "PHASE_35A_HO_100_SENTENCE_RESULTS.json")
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

print(json.dumps(results[0], indent=2, ensure_ascii=False))
