import urllib.request, json
urls = [
    'https://huggingface.co/api/models/ltrciiith/bhashaverse',
    'https://huggingface.co/api/models/VIzzxy/Bhashaverse_base_updt_WMT2026'
]
for url in urls:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print('Model:', data.get('modelId'))
            print('Gated:', data.get('gated'))
            print('Siblings:', [s['rfilename'] for s in data.get('siblings', [])])
            print('-'*40)
    except Exception as e:
        print('Error for', url, ':', e)
