import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

app = FastAPI()

model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
device = "cpu"
print(f"Loading IndicTrans2 on {device}...")

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
model.eval()
ip = IndicProcessor(inference=True)
print("Model loaded.")

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        batch = ip.preprocess_batch([req.text], src_lang=req.source_lang, tgt_lang=req.target_lang)
        inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
        
        with torch.no_grad():
            out = model.generate(**inputs, max_length=256, num_beams=5)
            
        res = ip.postprocess_batch(tokenizer.batch_decode(out, skip_special_tokens=True), lang=req.target_lang)
        return {"translation": res[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
