import json
import os

odia_map = {
    'a': '?', 'A': '?', 'b': '?', 'c': '?', 'd': '?', 'e': '?', 'g': '?',
    'h': '?', 'i': '?', 'I': '?', 'j': '?', 'k': '?', 'l': '?', 'm': '?',
    'n': '?', 'o': '?', 'p': '?', 'r': '?', 's': '?', 't': '?', 'u': '?',
    'U': '?', 'w': '?', 'y': '?', '-': '-', ' ': ' '
}
# very naive transliteration just to see if the tokenizer doesn't drop tokens

with open('data/ho_hindi/experimental/master_task2/ho_tts_test_sentences.json', 'r', encoding='utf-8') as f:
    sentences = json.load(f)

for s in sentences:
    odia_text = ""
    for char in s['ho_text'].lower():
        odia_text += odia_map.get(char, char)
    s['odia_text'] = odia_text

with open('data/ho_hindi/experimental/master_task2/ho_tts_test_sentences_odia.json', 'w', encoding='utf-8') as f:
    json.dump(sentences, f, indent=2, ensure_ascii=False)
