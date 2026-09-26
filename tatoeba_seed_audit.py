import json
import re

warang = []
latin = []
unverified = []

# Regex for scripts
WC_RANGE = re.compile(r'[\U000118A0-\U000118FF]')
DEVA_RANGE = re.compile(r'[\u0900-\u097F]')
LATIN_RANGE = re.compile(r'[a-zA-Z]')

with open('ho_nmt_data_audit/tatoeba_hindi_ho.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        src = data['source_text']
        tgt = data['target_text']
        sl = data['source_language']
        tl = data['target_language']
        
        # Ensure Hindi is source, Ho is target for standard structure
        if sl == 'hoc':
            src, tgt = tgt, src
            sl, tl = tl, sl
        
        has_wc = bool(WC_RANGE.search(tgt))
        has_deva = bool(DEVA_RANGE.search(tgt))
        has_latin = bool(LATIN_RANGE.search(tgt))
        
        record = {
            'source_text': src,
            'target_text': tgt,
            'source_language': 'hin_Deva',
            'target_language': 'hoc_Wara' if has_wc else 'hoc_Latn',
            'source_dataset': 'Tatoeba',
            'original_id': data['source_id'],
            'quality_status': 'VERIFIED'
        }
        
        if len(src.strip()) == 0 or len(tgt.strip()) == 0:
            record['quality_status'] = 'UNVERIFIED'
            record['reason'] = 'Empty text'
            unverified.append(record)
            continue
            
        if src.strip() == tgt.strip():
            record['quality_status'] = 'UNVERIFIED'
            record['reason'] = 'Identical source and target'
            unverified.append(record)
            continue
            
        # Classify by script
        if has_wc and not has_deva and not has_latin:
            record['script_class'] = 'WARANG_CITI'
            warang.append(record)
        elif has_latin and not has_wc and not has_deva:
            record['script_class'] = 'LATIN'
            latin.append(record)
        else:
            record['script_class'] = 'MIXED_OR_OTHER'
            record['quality_status'] = 'UNVERIFIED'
            record['reason'] = 'Mixed script or transliteration artifacts'
            unverified.append(record)

# Remove exact duplicates (source, target)
def deduplicate(dataset):
    seen = set()
    res = []
    for r in dataset:
        sig = (r['source_text'], r['target_text'])
        if sig not in seen:
            seen.add(sig)
            res.append(r)
    return res

warang = deduplicate(warang)
latin = deduplicate(latin)

def write_jsonl(path, dataset):
    with open(path, 'w', encoding='utf-8') as f:
        for r in dataset:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

write_jsonl('ho_nmt_data_audit/seed_warang_hindi_ho.jsonl', warang)
write_jsonl('ho_nmt_data_audit/seed_latin_hindi_ho.jsonl', latin)
write_jsonl('ho_nmt_data_audit/seed_unverified.jsonl', unverified)

print(f'Warang Citi verified pairs: {len(warang)}')
print(f'Latin Ho verified pairs: {len(latin)}')
print(f'Unverified/Mixed pairs: {len(unverified)}')
