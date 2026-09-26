import json
import os

cp_vocab = json.load(open('models/checkpoint-1500/vocab.json', 'r', encoding='utf-8'))
proc_vocab = json.load(open('models/santhali_wav2vec2_processor/vocab.json', 'r', encoding='utf-8'))

print('CP vocab count:', len(cp_vocab))
print('Proc vocab count:', len(proc_vocab))

cp_tokens = set(cp_vocab.keys())
proc_tokens = set(proc_vocab.keys())

print('\nIn CP but not Proc:', cp_tokens - proc_tokens)
print('In Proc but not CP:', proc_tokens - cp_tokens)

cp_total = len(cp_vocab)
if os.path.exists('models/checkpoint-1500/added_tokens.json'):
    added = json.load(open('models/checkpoint-1500/added_tokens.json', 'r', encoding='utf-8'))
    print('\nCP added tokens count:', len(added))
    cp_total += len(added)

print('CP total vocab:', cp_total)
