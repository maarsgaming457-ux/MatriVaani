from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import subprocess
import soundfile as sf
import time
from .transcriber import SantaliASR, MODEL_PATH, PROCESSOR_PATH

app = FastAPI(title="MatriVaani Santali ASR API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

asr_engine = None

@app.on_event("startup")
def startup_event():
    global asr_engine
    try:
        asr_engine = SantaliASR()
    except Exception as e:
        print(f"Error initializing ASR Engine: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": asr_engine is not None}

@app.get("/model-info")
def model_info():
    return {
        "model_path": MODEL_PATH,
        "processor_path": PROCESSOR_PATH,
        "device": "cpu",
        "language": "Santali (Ol Chiki)"
    }

MAX_FILE_SIZE = 50 * 1024 * 1024 # 50 MB

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not asr_engine:
        raise HTTPException(status_code=503, detail="ASR engine not loaded")
        
    if not file.filename.endswith(('.wav', '.mp3', '.m4a', '.ogg', '.flac', '.mp4')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
        
    try:
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large (limit 50MB)")
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_input:
            temp_input.write(content)
            temp_input_path = temp_input.name
            
        temp_output_path = temp_input_path + "_converted.wav"
        
        # FFmpeg conversion to 16kHz mono WAV
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-i', temp_input_path,
            '-ar', '16000', '-ac', '1',
            temp_output_path
        ]
        
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        audio_array, sr = sf.read(temp_output_path)
        
        result = asr_engine.transcribe(audio_array, sampling_rate=sr)
        
        # Cleanup
        os.remove(temp_input_path)
        os.remove(temp_output_path)
        
        return {
            "success": True,
            "transcription": result["transcription"],
            "metrics": {
                "inference_time": round(result["inference_time"], 3),
                "audio_duration": round(result["audio_duration"], 3),
                "rtf": round(result["rtf"], 3)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
