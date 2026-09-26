import requests
text = 'ᱟᱢ ᱫᱚ ᱪᱮᱫ ᱮᱢ ᱪᱮᱠᱟᱭ ᱮᱫᱟ'
res = requests.post('http://127.0.0.1:8000/tts', json={'text': text, 'language': 'sat'})
print(f'Status: {res.status_code}')
print(f'Content-Type: {res.headers.get("content-type")}')
print(f'Size: {len(res.content)} bytes')
if res.status_code == 200:
    with open('test_santali_tts.wav', 'wb') as f:
        f.write(res.content)
