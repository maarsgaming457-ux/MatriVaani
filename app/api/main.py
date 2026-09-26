from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form
from fastapi.responses import Response
from app.core.logging_config import logger
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
from app.services.experimental_ho_translation.translator import experimental_ho_translator
from app.services.mundari_translation_service import mundari_translation_service

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

class ExperimentalHoTranslatePayload(BaseModel):
    text: str

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
    from app.services.santali_tts_preprocessor import santali_to_tts_text
    
    try:
        text_to_synthesize = payload.text
        tts_lang = payload.language
        
        # Santali TTS Workaround: Use Hindi TTS engine via phonetic representation
        if tts_lang.lower().strip() in ["sat", "santali", "santhali"]:
            text_to_synthesize = santali_to_tts_text(payload.text)
            if not text_to_synthesize.strip():
                raise HTTPException(status_code=400, detail="Generated TTS text was empty.")
            tts_lang = "hi"
            logger.info(f"[TTS PREPROCESSOR] Original: {payload.text}")
            logger.info(f"[TTS PREPROCESSOR] Devanagari representation: {text_to_synthesize}")

        audio_bytes = tts_service.synthesize(text_to_synthesize, tts_lang, provider_override=payload.provider)
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

@app.post("/experimental/translate/ho-hi")
def experimental_ho_translate_endpoint(payload: ExperimentalHoTranslatePayload):
    try:
        result = experimental_ho_translator.translate(payload.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class HindiToMundariPayload(BaseModel):
    text: str

@app.post("/translate/hindi-to-mundari")
def translate_hindi_to_mundari_endpoint(payload: HindiToMundariPayload):
    try:
        logger.info(f"[NMT_REQUEST] Exact payload: {payload.model_dump()}")
        translation = mundari_translation_service.translate(payload.text)
        logger.info(f"[NMT_RESPONSE] Exact translation: {translation}")
        return {"translation": translation}
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
from app.services.experimental_ho_translation.hi_ho_translator import hi_ho_translator

@app.post("/experimental/translate/hi-ho")
def experimental_hi_ho_translate_endpoint(payload: ExperimentalHoTranslatePayload):
    try:
        result = hi_ho_translator.translate(payload.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
