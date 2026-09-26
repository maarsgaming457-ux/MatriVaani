from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

@app.post("/translate")
def translate(req: TranslateRequest):
    if req.source_lang == "hi" and req.target_lang == "sat":
        return {"translation": "Mocked Santali translation"}
    if req.source_lang == "sat" and req.target_lang == "hi":
        return {"translation": "Mocked Hindi translation"}
    return {"translation": "Mocked translation"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
