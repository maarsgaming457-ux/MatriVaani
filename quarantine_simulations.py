import json
import os

real_trans_manifest = 'data/ho_translation/ho_translation_real_v1_manifest.jsonl'
real_trans_hgt = 0
real_trans_synthetic = 0

if os.path.exists('data/ho_translation/ho_translation_v1_manifest.jsonl'):
    with open('data/ho_translation/ho_translation_v1_manifest.jsonl', 'r', encoding='utf-8') as fin, open(real_trans_manifest, 'w', encoding='utf-8') as fout:
        for line in fin:
            try:
                row = json.loads(line)
                row['human_verified'] = False
                row['ground_truth'] = False
                row['synthetic'] = True
                row['verification_status'] = 'SYNTHETIC'
                fout.write(json.dumps(row, ensure_ascii=False) + '\n')
                real_trans_synthetic += 1
            except:
                pass

print(f"Real Trans HGT: {real_trans_hgt}, Synthetic: {real_trans_synthetic}")
