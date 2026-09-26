import re

with open('app/api/main.py', 'r') as f:
    content = f.read()

content = content.replace(
    'from fastapi import FastAPI, HTTPException, Body, File, UploadFile',
    'from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form\nfrom fastapi.responses import Response'
)

content = content.replace(
    'from app.services.offline_service import OfflineService',
    'from app.services.offline_service import OfflineService\nfrom app.services.tts_service import TTSService'
)

content = content.replace(
    'offline_service = OfflineService()',
    'offline_service = OfflineService()\ntts_service = TTSService()'
)

tts_payload = '''class TTSPayload(BaseModel):
    text: str
    language: str = "santali"
'''
content = content.replace(
    'class TranslatePayload(BaseModel):',
    tts_payload + '\nclass TranslatePayload(BaseModel):'
)

asr_old = '''@app.post("/asr")
async def asr_endpoint(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    try:
        result = asr_service.transcribe(tmp_path)'''

asr_new = '''@app.post("/asr")
async def asr_endpoint(file: UploadFile = File(...), language: str = Form("santali")):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    try:
        result = asr_service.transcribe(tmp_path, language=language)'''

content = content.replace(asr_old, asr_new)

tts_endpoint = '''
@app.post("/tts")
def tts_endpoint(payload: TTSPayload):
    try:
        audio_bytes = tts_service.synthesize(payload.text, payload.language)
        return Response(content=audio_bytes, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''

content = content.replace(
    '@app.post("/translate")',
    tts_endpoint + '\n@app.post("/translate")'
)

with open('app/api/main.py', 'w') as f:
    f.write(content)
