import urllib.request
import json
import time

url = 'http://127.0.0.1:8000/translate'
def trans(text, sl, tl):
    data = json.dumps({'text': text, 'source_lang': sl, 'target_lang': tl}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode('utf-8'))['translation']
    except Exception as e:
        return str(e)

A_tests = [
    'मैं घर जा रहा हूँ।',
    'मेरा नाम राहुल है।',
    'आज मौसम बहुत अच्छा है।',
    'मैं पानी पी रहा हूँ।',
    'बच्चे स्कूल जा रहे हैं।',
    'कृपया दरवाज़ा बंद करें।',
    'मुझे संथाली भाषा सीखनी है।',
    'कल हम बाजार जाएंगे।',
    'यह मेरी किताब है।',
    'आप कैसे हैं?'
]

B_tests = [
    'ᱤᱧ ᱫᱚ ᱦᱟᱛᱟᱣ ᱠᱟᱱᱟ।',
    'ᱤᱧ ᱫᱚ ᱦᱚᱲ ᱠᱟᱱᱟ।',
    'ᱱᱤᱛ ᱚᱱᱟ ᱢᱟᱥᱤᱛ ᱢᱮᱱᱟ।',
    'ᱟᱢ ᱫᱚ ᱠᱟᱹᱛᱮ ᱠᱚ ᱛᱟᱦᱮᱱᱟ?',
    'ᱤᱧ ᱫᱚ ᱥᱟᱠᱟᱢ ᱡᱚᱢ ᱠᱟᱱᱟ।',
    'ᱟᱢ ᱫᱚ ᱵᱟᱝ ᱢᱮᱱᱟ?',
    'ᱤᱧ ᱫᱚ ᱵᱟᱡᱟᱨ ᱥᱮᱱᱚᱜ ᱠᱟᱱᱟ।',
    'ᱱᱤᱭᱟ ᱫᱚ ᱤᱧᱟᱜ ᱯᱩᱛᱷᱤ ᱠᱟᱱᱟ।',
    'ᱟᱢ ᱫᱚ ᱡᱟᱦᱟᱸ ᱢᱮᱱᱟ?',
    'ᱥᱮᱛᱟᱜ ᱫᱚ ᱵᱟᱹᱲᱤ ᱢᱮᱱᱟ।'
]

C_tests = [
    'मेरा मोबाइल नंबर 9876543210 है।',
    'आज 25 विद्यार्थी कक्षा में हैं।',
    'रवि दिल्ली जा रहा है।',
    'नमस्ते!',
    'धन्यवाद।'
]

out = []
out.append('--- TEST A: HI -> SAT ---')
a_results = []
for i, t in enumerate(A_tests):
    res = trans(t, 'hi', 'sat')
    a_results.append(res)
    out.append(f'A{i+1}: {t} -> {res}')

out.append('\n--- TEST B: SAT -> HI ---')
for i, t in enumerate(B_tests):
    res = trans(t, 'sat', 'hi')
    out.append(f'B{i+1}: {t} -> {res}')

out.append('\n--- TEST C: SPECIAL ---')
for i, t in enumerate(C_tests):
    res = trans(t, 'hi', 'sat')
    out.append(f'C{i+1}: {t} -> {res}')

out.append('\n--- TEST D: REVERSE CONSISTENCY ---')
for i in range(3):
    t_hi = A_tests[i]
    t_sat = a_results[i]
    if t_sat.startswith('HTTP Error'):
        t_rev = 'Error'
    else:
        t_rev = trans(t_sat, 'sat', 'hi')
    out.append(f'D{i+1}: {t_hi} -> {t_sat} -> {t_rev}')

out.append('\n--- TEST H: UNSUPPORTED ---')
out.append(f'H1: {trans("Hello", "en", "fr")}')

open('test_results.txt', 'w', encoding='utf-8').write('\n'.join(out))
