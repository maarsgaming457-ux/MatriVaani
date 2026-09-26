import requests

url = "https://huggingface.co/api/datasets?search=hindi%20audio&limit=5"
response = requests.get(url)
print(response.json())
