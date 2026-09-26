import urllib.request
import json
url = 'https://opus.nlpl.eu/opusapi/?source=hi&target=hoc'
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        corpora = data.get('corpora', [])
        alignments = [c for c in corpora if c.get('source') in ('hi','hoc') and c.get('target') in ('hi','hoc') and c.get('source') != c.get('target')]
        for a in alignments:
            print(a.get('preprocessing'), a.get('url'))
except Exception as e:
    print('OPUS Error hi-hoc:', e)
