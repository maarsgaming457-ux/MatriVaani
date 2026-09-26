import requests, os, json
from dotenv import load_dotenv
import codecs, sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
load_dotenv('.env')

url = 'https://api.sarvam.ai/translate'
payload = {
    'input': 'तुम क्या कर रहे हो?',
    'source_language_code': 'hi-IN',
    'target_language_code': 'sat-IN',
    'speaker_gender': 'Male',
    'mode': 'formal',
    'model': 'sarvam-translate:v1',
    'enable_preprocessing': True
}
headers = {
    'api-subscription-key': os.getenv('SARVAM_API_KEY').strip('"').strip("'"),
    'Content-Type': 'application/json'
}
try:
    res = requests.post(url, json=payload, headers=headers)
    print(f'Status: {res.status_code}')
    print(f'Response: {res.text}')
except Exception as e:
    print(e)
