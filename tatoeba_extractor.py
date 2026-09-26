import urllib.request
import json
import os
import time

def get_tatoeba_pairs(from_lang, to_lang):
    pairs = []
    page = 1
    total_pages = 1
    
    while page <= total_pages:
        url = f'https://tatoeba.org/en/api_v0/search?from={from_lang}&to={to_lang}&page={page}'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'MatriVaani-Research/1.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if page == 1:
                    total_pages = data.get('paging', {}).get('Sentences', {}).get('pageCount', 1)
                    print(f'Total {from_lang}-{to_lang} pairs expected: {data.get("paging", {}).get("Sentences", {}).get("count")}')
                
                for result in data.get('results', []):
                    source_id = result.get('id')
                    source_text = result.get('text')
                    source_lang = result.get('lang')
                    
                    for tl_group in result.get('translations', []):
                        for tl in tl_group:
                            if tl.get('lang') == to_lang:
                                pairs.append({
                                    'source_language': source_lang,
                                    'target_language': tl.get('lang'),
                                    'source_text': source_text,
                                    'target_text': tl.get('text'),
                                    'source_id': source_id,
                                    'target_id': tl.get('id')
                                })
                page += 1
                time.sleep(1) # Be nice to the API
        except Exception as e:
            print(f'Error on page {page}: {e}')
            break
            
    return pairs

os.makedirs('ho_nmt_data_audit', exist_ok=True)
pairs = get_tatoeba_pairs('hin', 'hoc')

# Remove exact duplicates
unique_pairs = []
seen = set()
for p in pairs:
    sig = (p['source_text'], p['target_text'])
    if sig not in seen:
        seen.add(sig)
        unique_pairs.append(p)

with open('ho_nmt_data_audit/tatoeba_hindi_ho.jsonl', 'w', encoding='utf-8') as f:
    for p in unique_pairs:
        f.write(json.dumps(p, ensure_ascii=False) + '\n')

print(f'Extracted {len(unique_pairs)} unique pairs.')

# Calculate script statistics
warang_citi = 0
devanagari = 0
latin = 0
mixed = 0

for p in unique_pairs:
    ho_text = p['target_text']
    has_wc = any(0x118A0 <= ord(c) <= 0x118FF for c in ho_text)
    has_deva = any(0x0900 <= ord(c) <= 0x097F for c in ho_text)
    has_latin = any(c.isascii() and c.isalpha() for c in ho_text)
    
    if has_wc and not has_deva and not has_latin:
        warang_citi += 1
    elif has_deva and not has_wc and not has_latin:
        devanagari += 1
    elif has_latin and not has_wc and not has_deva:
        latin += 1
    else:
        mixed += 1

print(f'Warang Citi: {warang_citi}')
print(f'Devanagari: {devanagari}')
print(f'Latin: {latin}')
print(f'Mixed: {mixed}')
