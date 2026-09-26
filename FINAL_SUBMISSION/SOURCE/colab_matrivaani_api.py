from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import torch

# Assuming model, 	okenizer, and ip are already loaded in the global scope from previous Colab cells.
# For example:
# model = AutoModelForSeq2SeqLM.from_pretrained(...)
# tokenizer = AutoTokenizer.from_pretrained(...)
# ip = IndicProcessor(inference=True)

app = FastAPI(title="MatriVaani Local Colab Translation API")

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty or whitespace")
        return v

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/translate")
def translate(req: TranslateRequest):
    # Map external codes to internal codes
    lang_map = {
        "hi": "hin_Deva",
        "sat": "sat_Olck",
        "hindi": "hin_Deva",
        "santali": "sat_Olck"
    }

    src = lang_map.get(req.source_lang.lower())
    tgt = lang_map.get(req.target_lang.lower())

    if not src or not tgt:
        raise HTTPException(status_code=400, detail="Unsupported language combination. Supported: hi, sat")

    if src == tgt:
        raise HTTPException(status_code=400, detail="Source and target languages must be different.")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        # Preprocess
        batch = ip.preprocess_batch([req.text], src_lang=src, tgt_lang=tgt)
        
        # Tokenize
        inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
        
        # Generate with use_cache=False as mandated
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_length=256, 
                num_beams=5, 
                num_return_sequences=1,
                use_cache=False
            )
            
        # Decode and Postprocess
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translation = ip.postprocess_batch(decoded, lang=tgt)[0]

        return {"translation": translation}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
