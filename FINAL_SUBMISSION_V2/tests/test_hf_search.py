import requests
import json

def search_hf(query):
    url = f'https://huggingface.co/api/models?search={query}'
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json()
        print(f'Results for {query}:')
        for m in models[:5]:
            print(f"- {m['id']}")
    else:
        print(f'Failed to search {query}: {response.status_code}')

search_hf('santali tts')
search_hf('sat tts')
search_hf('vexyl')
