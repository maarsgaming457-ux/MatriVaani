import urllib.request
import urllib.parse
import json
import time

queries = [
    '"Hindi Ho" corpus',
    '"Hindi-Ho" corpus',
    '"hin hoc"',
    '"hin_Deva hoc_Wara"',
    '"Warang Citi Hindi" dataset',
]

headers = {'User-Agent': 'MatriVaani-Research/1.0', 'Accept': 'application/vnd.github.v3+json'}

for q in queries:
    url = 'https://api.github.com/search/repositories?q=' + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f'Query: {q} -> {data["total_count"]} repos')
            for item in data.get('items', []):
                print(f'  - {item["full_name"]}: {item["description"]}')
    except Exception as e:
        print(f'Error for query {q}: {e}')
    time.sleep(2)
