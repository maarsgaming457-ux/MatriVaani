from huggingface_hub import HfApi
api = HfApi()
info = api.dataset_info("ai4bharat/IndicVoices")
print([f.rfilename for f in info.siblings if 'santali' in f.rfilename or 'sat' in f.rfilename or 'data/' in f.rfilename])
