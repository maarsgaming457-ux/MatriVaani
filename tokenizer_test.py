import json
from transformers import AutoTokenizer

models = [
    'google/byt5-small',
    'facebook/nllb-200-distilled-600M',
    'google/mt5-small',
    'facebook/mbart-large-50-many-to-many-mmt'
]

test_hindi = ['पुलिस!', 'शुक्रिया।', 'मेरे पास एक गाड़ी है।']
test_wc = ['𑢸𑣉𑣚𑣂𑣞!', '𑢷𑣂𑣕𑣂𑣈𑣖.', '𑢩𑣓𑣑𑣉𑣄 𑣖𑣂𑣞𑣈!']
test_latin = ['Ań taḱ Car menaḱa.', 'London remea chi?', 'Hokaê me!']

results = {}

for m in models:
    try:
        if 'mbart' in m:
            tokenizer = AutoTokenizer.from_pretrained(m, src_lang="hi_IN")
        elif 'nllb' in m:
            tokenizer = AutoTokenizer.from_pretrained(m, src_lang="hin_Deva")
        else:
            tokenizer = AutoTokenizer.from_pretrained(m)
            
        m_results = {'hindi': [], 'warang_citi': [], 'latin': []}
        
        for text in test_hindi:
            toks = tokenizer.encode(text)
            dec = tokenizer.decode(toks, skip_special_tokens=True)
            m_results['hindi'].append({'text': text, 'tokens': len(toks), 'decoded': dec, 'unknown': tokenizer.unk_token_id in toks})
            
        for text in test_wc:
            toks = tokenizer.encode(text)
            dec = tokenizer.decode(toks, skip_special_tokens=True)
            m_results['warang_citi'].append({'text': text, 'tokens': len(toks), 'decoded': dec, 'unknown': tokenizer.unk_token_id in toks})
            
        for text in test_latin:
            toks = tokenizer.encode(text)
            dec = tokenizer.decode(toks, skip_special_tokens=True)
            m_results['latin'].append({'text': text, 'tokens': len(toks), 'decoded': dec, 'unknown': tokenizer.unk_token_id in toks})
            
        results[m] = m_results
    except Exception as e:
        results[m] = {'error': str(e)}

with open('ho_nmt_data_audit/tokenizer_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print('Tokenizer test complete.')
