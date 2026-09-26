from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dotenv import load_dotenv
load_dotenv()

from app.services.asr_service import ASRService
from app.services.translation_service import TranslationService
from app.services.llm_service import LLMService
from app.services.offline_service import OfflineService
from app.services.tts_service import TTSService

app = FastAPI(title="MatriVaani Shared API")

asr_service = ASRService()
translation_service = TranslationService()
llm_service = LLMService()
offline_service = OfflineService()
tts_service = TTSService()

class SyncPayload(BaseModel):
    client_changes: List[Dict[str, Any]]

class TTSPayload(BaseModel):
    text: str
    language: str = "santali"
    provider: Optional[str] = None

class TranslatePayload(BaseModel):
    text: str
    source_lang: str = "santali"
    target_lang: str = "hi"

class ContentPayload(BaseModel):
    content_type: str
    topic: str
    language: str
    data: Dict[str, Any]
    id: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Shared API is running."}

@app.post("/asr")
async def asr_endpoint(file: UploadFile = File(...), language: str = Form("santali")):
    file_bytes = await file.read()
    

        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    try:
        result = asr_service.transcribe(tmp_path, language=language)
        transcript = result["transcript"] if isinstance(result, dict) else result
        return {"transcript": transcript}
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/tts")
def tts_endpoint(payload: TTSPayload):
    from app.services.tts_service import TTSUnavailableError
    try:
        audio_bytes = tts_service.synthesize(payload.text, payload.language, provider_override=payload.provider)
        return Response(content=audio_bytes, media_type="audio/wav")
    except TTSUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
def translate_endpoint(payload: TranslatePayload):
    try:
        trans = translation_service.translate(payload.text, payload.source_lang, payload.target_lang)
        return {"translation": trans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync")
def sync_endpoint(payload: SyncPayload):
    try:
        server_state = offline_service.sync(payload.client_changes)
        return {"server_state": server_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content")
def get_content(content_type: Optional[str] = None):
    return {"content": offline_service.get_content(content_type)}

@app.post("/content")
def save_content(payload: ContentPayload):
    item_id = offline_service.save_content(
        payload.content_type, payload.topic, payload.language, payload.data, payload.id
    )
    return {"id": item_id, "status": "saved"}

@app.delete("/content/{item_id}")
def delete_content(item_id: str):
    offline_service.delete_content(item_id)
    return {"status": "deleted"}
