import json
import random

# Load the data
warang_pairs = []
with open('ho_nmt_data_audit/seed_warang_hindi_ho.jsonl', 'r', encoding='utf-8') as f:
    warang_pairs = [json.loads(line) for line in f]

latin_pairs = []
with open('ho_nmt_data_audit/seed_latin_hindi_ho.jsonl', 'r', encoding='utf-8') as f:
    latin_pairs = [json.loads(line) for line in f]

all_pairs = warang_pairs + latin_pairs
print(f'Total initial pairs: {len(all_pairs)}')

# Analyze duplicates
hindi_ho_map = {}
ho_hindi_map = {}
for p in all_pairs:
    h = p['source_text']
    ho = p['target_text']
    hindi_ho_map.setdefault(h, []).append(ho)
    ho_hindi_map.setdefault(ho, []).append(h)

dup_hindi_diff_ho = {h: hos for h, hos in hindi_ho_map.items() if len(set(hos)) > 1}
dup_ho_diff_hindi = {ho: hs for ho, hs in ho_hindi_map.items() if len(set(hs)) > 1}

print(f'Duplicate Hindi with diff Ho: {len(dup_hindi_diff_ho)}')
print(f'Duplicate Ho with diff Hindi: {len(dup_ho_diff_hindi)}')

# We will keep them as they might be legitimate variations, but ensure they don't leak across splits.
# To prevent leakage, we group by exact matches on either side (connected components).
from collections import defaultdict

def build_components(pairs):
    adj = defaultdict(list)
    for i, p in enumerate(pairs):
        adj['H_'+p['source_text']].append(i)
        adj['O_'+p['target_text']].append(i)
        
    visited_nodes = set()
    visited_edges = set()
    components = []
    
    for i, p in enumerate(pairs):
        if i in visited_edges: continue
        comp_edges = set()
        queue = [i]
        while queue:
            curr_edge = queue.pop(0)
            if curr_edge in visited_edges: continue
            visited_edges.add(curr_edge)
            comp_edges.add(curr_edge)
            
            p_curr = pairs[curr_edge]
            # add all edges connected to source
            for e in adj['H_'+p_curr['source_text']]:
                if e not in visited_edges:
                    queue.append(e)
            # add all edges connected to target
            for e in adj['O_'+p_curr['target_text']]:
                if e not in visited_edges:
                    queue.append(e)
        components.append(list(comp_edges))
    return components

comps = build_components(all_pairs)
print(f'Total independent components: {len(comps)}')

# Shuffle components and split
random.seed(42)
random.shuffle(comps)

train = []
val = []
test = []

# Because the corpus is small (330 pairs), let's reserve ~20 for val and ~30 for test.
# But we need to ensure test/val have some Warang Citi.
# Let's segregate components by whether they contain Warang Citi.
wc_comps = []
latin_comps = []

for c in comps:
    has_wc = any(all_pairs[i]['script_class'] == 'WARANG_CITI' for i in c)
    if has_wc:
        wc_comps.append(c)
    else:
        latin_comps.append(c)

# We have 59 WC pairs. Let's put ~10 in test, ~5 in val, rest in train.
wc_test = wc_comps[:10]
wc_val = wc_comps[10:15]
wc_train = wc_comps[15:]

# Remaining Latin
latin_test = latin_comps[:20]
latin_val = latin_comps[20:35]
latin_train = latin_comps[35:]

for c in wc_train + latin_train:
    for i in c: train.append(all_pairs[i])
for c in wc_val + latin_val:
    for i in c: val.append(all_pairs[i])
for c in wc_test + latin_test:
    for i in c: test.append(all_pairs[i])

print(f'Train: {len(train)}')
print(f'Val: {len(val)}')
print(f'Test: {len(test)}')

def write_jsonl(path, dataset):
    with open(path, 'w', encoding='utf-8') as f:
        for r in dataset:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

write_jsonl('ho_nmt_data_audit/train.jsonl', train)
write_jsonl('ho_nmt_data_audit/validation.jsonl', val)
write_jsonl('ho_nmt_data_audit/test.jsonl', test)

def create_manifest(dataset, path):
    manifest = []
    for r in dataset:
        manifest.append({
            'source': r['source_text'],
            'target': r['target_text'],
            'direction': f"{r['source_language']}2{r['target_language']}",
            'script_class': r.get('script_class', 'UNKNOWN')
        })
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

create_manifest(train, 'ho_nmt_data_audit/train_manifest.json')
create_manifest(val, 'ho_nmt_data_audit/validation_manifest.json')
create_manifest(test, 'ho_nmt_data_audit/test_manifest.json')

# Write quality report
with open('ho_nmt_data_audit/dataset_quality_report.csv', 'w', encoding='utf-8') as f:
    f.write('Metric,Value\n')
    f.write(f'Total Valid Pairs,{len(all_pairs)}\n')
    f.write(f'Warang Citi,{len(warang_pairs)}\n')
    f.write(f'Latin,{len(latin_pairs)}\n')
    f.write(f'Duplicate Hindi diff Ho,{len(dup_hindi_diff_ho)}\n')
    f.write(f'Duplicate Ho diff Hindi,{len(dup_ho_diff_hindi)}\n')
    f.write(f'Independent semantic components,{len(comps)}\n')
    f.write(f'Train Pairs,{len(train)}\n')
    f.write(f'Validation Pairs,{len(val)}\n')
    f.write(f'Test Pairs,{len(test)}\n')

print('Data split complete.')
