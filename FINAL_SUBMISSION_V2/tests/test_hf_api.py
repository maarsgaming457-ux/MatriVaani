import urllib.request
import json
url = "https://huggingface.co/api/datasets/ai4bharat/IndicVoices/tree/main/santali"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print([d['path'] for d in data])
except Exception as e:
    print("Error:", e)
