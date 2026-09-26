import requests
import time
import json
import subprocess
import threading
import sys

BASE_URL = 'http://127.0.0.1:8000'

def start_server():
    print('Starting backend server...')
    process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.api.main:app', '--host', '0.0.0.0', '--port', '8000'])
    time.sleep(5)
    return process

def run_tests():
    print('=== HEALTH TEST ===')
    try:
        r = requests.get(f'{BASE_URL}/health')
        print(f'Status: {r.status_code}, Body: {r.text}')
    except Exception as e:
        print(f'Health error: {e}')

    print('\n=== TRANSLATION TEST: EMPTY TEXT ===')
    r = requests.post(f'{BASE_URL}/translate', json={'text': '', 'source_lang': 'hi', 'target_lang': 'sat'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== TRANSLATION TEST: VALID HINDI -> SANTALI ===')
    r = requests.post(f'{BASE_URL}/translate', json={'text': 'नमस्ते', 'source_lang': 'hi', 'target_lang': 'sat'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== TRANSLATION TEST: INVALID JSON ===')
    r = requests.post(f'{BASE_URL}/translate', data='invalid json', headers={'Content-Type': 'application/json'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== TTS TEST: NONE PROVIDER ===')
    r = requests.post(f'{BASE_URL}/tts', json={'text': 'Hello', 'language': 'en'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== FILE UPLOAD (ASR) TEST: TEXT AS AUDIO ===')
    with open('dummy.txt', 'w') as f:
        f.write('This is a text file.')
    with open('dummy.txt', 'rb') as f:
        r = requests.post(f'{BASE_URL}/asr', files={'file': ('dummy.txt', f, 'text/plain')}, data={'language': 'sat'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== FILE UPLOAD (ASR) TEST: EMPTY FILE ===')
    with open('empty.wav', 'wb') as f:
        pass
    with open('empty.wav', 'rb') as f:
        r = requests.post(f'{BASE_URL}/asr', files={'file': ('empty.wav', f, 'audio/wav')}, data={'language': 'sat'})
    print(f'Status: {r.status_code}, Body: {r.text}')

    print('\n=== FILE UPLOAD (ASR) TEST: MISSING FILE ===')
    r = requests.post(f'{BASE_URL}/asr', data={'language': 'sat'})
    print(f'Status: {r.status_code}, Body: {r.text}')

if __name__ == '__main__':
    server = start_server()
    try:
        run_tests()
    finally:
        server.terminate()
        server.wait()
