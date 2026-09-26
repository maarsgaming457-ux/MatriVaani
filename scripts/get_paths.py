import json
import os
import sys

# Windows cp1252 print fix
sys.stdout.reconfigure(encoding='utf-8')

res_path = os.path.join('data', 'ho_hindi', 'experimental', 'phase35a_100_sentence_validation', 'PHASE_35A_HO_100_SENTENCE_RESULTS.json')
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

for r in results:
    if r['translation_tier'] == 'resource_supported_exact_retrieval':
        print(f"EXACT: {r['audio_filename']}")
        break
for r in results:
    if r['translation_tier'] == 'resource_assisted_ai':
        print(f"AI: {r['audio_filename']}")
        break
for r in results:
    if r['translation_tier'] == 'controlled_fallback':
        print(f"CONTROLLED: {r['audio_filename']}")
        break
