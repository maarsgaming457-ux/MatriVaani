import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
print('Tatoeba samples:')
with open('ho_nmt_data_audit/tatoeba_hindi_ho.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:5]):
        data = json.loads(line)
        print(f"{i+1}. {data['source_language']}->{data['target_language']}")
        print(f"   {data['source_text']}")
        print(f"   {data['target_text']}")
        print()
