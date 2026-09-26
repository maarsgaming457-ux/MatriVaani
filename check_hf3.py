from huggingface_hub import HfApi
api = HfApi()
info = api.dataset_info("ai4bharat/IndicVoices")
print(info.cardData)
