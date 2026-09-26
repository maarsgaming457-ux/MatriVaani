import json
import sys
import random
sys.stdout.reconfigure(encoding='utf-8')
print('Random Tatoeba samples:')
with open('ho_nmt_data_audit/tatoeba_hindi_ho.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    random.seed(42)
    random.shuffle(lines)
    for i, line in enumerate(lines[:10]):
        data = json.loads(line)
        print(f"{i+1}. {data['source_language']}->{data['target_language']}")
        print(f"   {data['source_text']}")
        print(f"   {data['target_text']}")
        print()
