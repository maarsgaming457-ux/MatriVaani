import json
import os

res_path = os.path.join("data", "ho_hindi", "experimental", "phase35a_100_sentence_validation", "PHASE_35A_HO_100_SENTENCE_RESULTS.json")
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

with open('partial_75.txt', 'w', encoding='utf8') as f:
    for r in results:
        if r['asr_similarity'] < 1.0:
            f.write(f"{r['id']} | Ref: {r['reference_ho']} | ASR: {r['asr_ho']} | Sim: {r['asr_similarity']}\n")
