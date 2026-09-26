import json
import os

in_files = [
    'data/ho_hindi/experimental/v3_dataset/test.jsonl',
    'data/ho_hindi/experimental/v3_dataset/train.jsonl',
    'data/ho_hindi/experimental/v3_dataset/val.jsonl'
]
out_trans = 'data/ho_translation/ho_translation_v1_manifest.jsonl'
count_trans = 0

with open(out_trans, 'w', encoding='utf-8') as fo:
    for fpath in in_files:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fi:
                for line in fi:
                    try:
                        row = json.loads(line)
                        ho_text = row.get('ho_text') or row.get('ho')
                        hi_text = row.get('hi_text') or row.get('hi') or row.get('hindi')
                        if not ho_text or not hi_text:
                            continue
                        
                        v_status = row.get('verification_status', 'UNVERIFIED')
                        if v_status == 'RESOURCE_SUPPORTED_AI':
                            v_status = 'RESOURCE_SUPPORTED'
                            
                        new_row = {
                            'id': f'trans_v1_{count_trans}',
                            'ho_text': ho_text,
                            'hi_text': hi_text,
                            'ho_script': 'Warang Citi/Odia',
                            'hi_script': 'Devanagari',
                            'source': row.get('source', 'experimental_v3_dataset'),
                            'domain': 'general',
                            'human_verified': row.get('human_verified', False),
                            'ground_truth': row.get('ground_truth', False),
                            'synthetic': row.get('machine_generated', True),
                            'verification_status': v_status if v_status in ['HUMAN_GROUND_TRUTH', 'RESOURCE_SUPPORTED', 'SYNTHETIC', 'AI_GENERATED', 'UNVERIFIED'] else 'UNVERIFIED'
                        }
                        fo.write(json.dumps(new_row, ensure_ascii=False) + '\n')
                        count_trans += 1
                    except Exception as e:
                        pass

print('Trans rows written:', count_trans)
