import requests
url = "https://huggingface.co/api/models/ai4bharat/indic-parler-tts/tree/main"
res = requests.get(url)
print(res.json())
