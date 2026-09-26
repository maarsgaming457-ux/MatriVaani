from IndicTransToolkit import IndicProcessor

ip = IndicProcessor(inference=True)
text = "मेरा नाम सुमित है।"
try:
    batch = ip.preprocess_batch([text], src_lang="hin_Deva", tgt_lang="unr_Deva")
    print("Preprocess output:", batch)
except Exception as e:
    print("Error:", e)
