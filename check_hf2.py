from huggingface_hub import HfApi
api = HfApi()
info = api.dataset_info("ai4bharat/IndicVoices")
for f in info.siblings:
    if 'santali' in f.rfilename or 'sat' in f.rfilename:
        print(f.rfilename)
