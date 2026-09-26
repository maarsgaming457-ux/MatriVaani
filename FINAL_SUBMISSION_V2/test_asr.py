
import requests, time, json
out = {}
def test(f):
    t0 = time.time()
    r = requests.post('http://127.0.0.1:8000/asr', files={'file': open(f, 'rb')}, data={'language': 'ho'})
    t1 = time.time()
    out[f] = {'status': r.status_code, 'json': r.json(), 'latency': f'{t1-t0:.2f}s'}

test('ho_test_audio/ho1.wav')
test('ho_test_audio/ho2.wav')
open('asr_test_out.txt', 'w', encoding='utf-8').write(json.dumps(out))

