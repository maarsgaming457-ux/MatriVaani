import urllib.request
import gzip
import xml.etree.ElementTree as ET
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_align = 'https://object.pouta.csc.fi/OPUS-translatewiki/v2025-01-01/xml/hi-hoc.xml.gz'
url_hi = 'https://object.pouta.csc.fi/OPUS-translatewiki/v2025-01-01/xml/hi.zip'
url_hoc = 'https://object.pouta.csc.fi/OPUS-translatewiki/v2025-01-01/xml/hoc.zip'

try:
    print('Downloading translatewiki alignments...')
    req = urllib.request.Request(url_align, headers={'User-Agent': 'Mozilla'})
    with urllib.request.urlopen(req, context=ctx) as resp, open('hi-hoc.xml.gz', 'wb') as f:
        f.write(resp.read())
        
    print('Downloading hi.zip...')
    req = urllib.request.Request(url_hi, headers={'User-Agent': 'Mozilla'})
    with urllib.request.urlopen(req, context=ctx) as resp, open('hi.zip', 'wb') as f:
        f.write(resp.read())
        
    print('Downloading hoc.zip...')
    req = urllib.request.Request(url_hoc, headers={'User-Agent': 'Mozilla'})
    with urllib.request.urlopen(req, context=ctx) as resp, open('hoc.zip', 'wb') as f:
        f.write(resp.read())
        
    import zipfile
    with zipfile.ZipFile('hi.zip', 'r') as zip_ref:
        zip_ref.extractall('opus_tw_hi')
    with zipfile.ZipFile('hoc.zip', 'r') as zip_ref:
        zip_ref.extractall('opus_tw_hoc')
        
    print('Files extracted successfully.')
except Exception as e:
    print('Error downloading OPUS files:', e)
