import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor
import nest_asyncio
import uvicorn
from pyngrok import ngrok

# Initialize FastAPI
app = FastAPI(title="IndicTrans2 API")

# Setup device
device = "cuda" if torch.cuda.is_available() else "cpu"

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

# Reusable model state
class ModelManager:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.ip = None

    def load(self):
        if self.model is not None:
            return
            
        model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
        
        # We assume the user has configured HF_TOKEN in Colab Secrets
        # e.g., from google.colab import userdata; HF_TOKEN = userdata.get('HF_TOKEN')
        # Here we rely on Hugging Face hub having access to the token automatically via huggingface-cli login
        # or the token being passed in the environment as HF_TOKEN.

        print(f"Loading tokenizer {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        print(f"Loading model {model_name} on {device}...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
        self.model.eval()
        print("Loading IndicProcessor...")
        self.ip = IndicProcessor(inference=True)

manager = ModelManager()

@app.on_event("startup")
def startup_event():
    # Load model once on startup
    manager.load()

@app.get("/health")
def health():
    return {"status": "ok", "device": device}

@app.post("/translate")
def translate(req: TranslateRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided.")
        
    lang_map = {
        "hi": "hin_Deva",
        "hindi": "hin_Deva",
        "sat": "sat_Olck",
        "santali": "sat_Olck",
        "santhali": "sat_Olck"
    }
    
    src = lang_map.get(req.source_lang.lower())
    tgt = lang_map.get(req.target_lang.lower())
    
    if not src or not tgt:
        raise HTTPException(status_code=400, detail=f"Unsupported language pair: {req.source_lang} -> {req.target_lang}")
        
    if src == tgt:
        raise HTTPException(status_code=400, detail="Source and target languages must be different.")
        
    try:
        sentences = [req.text]
        batch = manager.ip.preprocess_batch(sentences, src_lang=src, tgt_lang=tgt)
        
        inputs = manager.tokenizer(
            batch, 
            padding="longest", 
            truncation=True, 
            max_length=256, 
            return_tensors="pt"
        ).to(device)
        
        with torch.no_grad():
            outputs = manager.model.generate(
                **inputs, 
                max_length=256,
                num_beams=5
            )
            
        decoded = manager.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        postprocessed = manager.ip.postprocess_batch(decoded, lang=tgt)
        
        return {"translation": postprocessed[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Apply nest_asyncio to allow uvicorn to run in Colab notebook
    nest_asyncio.apply()
    
    # Check for ngrok token
    ngrok_token = os.getenv("NGROK_AUTHTOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
        
    public_url = ngrok.connect(8000).public_url
    print(f"\\n\\n>>> Public Colab API URL: {public_url} <<<\\n\\n")
    print(f"Set INDICTRANS2_ENDPOINT='{public_url}/translate' in your MatriVaani .env file.\\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
