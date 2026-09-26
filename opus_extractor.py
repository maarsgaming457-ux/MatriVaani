import urllib.request
import urllib.parse
import os
import zipfile
import tempfile
import ssl
from collections import defaultdict
import glob

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_moses = 'https://object.pouta.csc.fi/OPUS-translatewiki/v2025-01-01/moses/hi-hoc.txt.zip'
try:
    print('Downloading translatewiki hi-hoc...')
    req = urllib.request.Request(url_moses)
    with urllib.request.urlopen(req, context=ctx) as response:
        with open('hi-hoc.zip', 'wb') as f:
            f.write(response.read())
            
    with zipfile.ZipFile('hi-hoc.zip', 'r') as zip_ref:
        zip_ref.extractall('opus_hi_hoc')
        
    print('Extracted files:', os.listdir('opus_hi_hoc'))
    hi_file = glob.glob('opus_hi_hoc/*.hi')[0]
    hoc_file = glob.glob('opus_hi_hoc/*.hoc')[0]
    
    with open(hi_file, 'r', encoding='utf-8') as fh, open(hoc_file, 'r', encoding='utf-8') as fho:
        hi_lines = fh.readlines()
        hoc_lines = fho.readlines()
        
    print(f'Total OPUS pairs: {len(hi_lines)}')
    print('Sample OPUS pairs:')
    for i in range(10):
        print(f"HI: {hi_lines[i].strip()}")
        print(f"HOC: {hoc_lines[i].strip()}")
        print()
except Exception as e:
    print('Error:', e)
