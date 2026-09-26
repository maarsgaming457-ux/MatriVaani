import json
import re
import os

count = 0
out_data = []

files_to_check = [
    'data/ho_hindi/corpus_v3/ho_grammar_examples.jsonl',
    'data/ho_hindi/corpus_v3/ho_english_parallel.jsonl',
    'data/ho_hindi/corpus_v3/ho_authentic_only.jsonl'
]

for file_path in files_to_check:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
                ho = d.get('ho', '').strip()
                ho = re.sub(r'^\d+[a-z]?\.\s*', '', ho)
                
                # Check if purely Latin alphabet, spaces, hyphens
                if 10 < len(ho) < 150 and re.match(r'^[a-zA-Z\s\-]+$', ho):
                    out_data.append(d)
                    count += 1
            except:
                pass

# Select 3 short, 3 medium, 3 long
out_data.sort(key=lambda x: len(x.get('ho', '')))

selected = []
if len(out_data) >= 9:
    selected.extend(out_data[:3])
    mid = len(out_data) // 2
    selected.extend(out_data[mid-1:mid+2])
    selected.extend(out_data[-3:])
else:
    selected = out_data

with open('selected_ho.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, indent=2, ensure_ascii=False)
    
print(f'Found {len(out_data)} clean candidates. Saved {len(selected)} to selected_ho.json.')
