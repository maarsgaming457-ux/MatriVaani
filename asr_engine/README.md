# MatriVaani Santali ASR Engine

This directory contains the production-ready Automatic Speech Recognition (ASR) engine for the Santali language (Ol Chiki script). It is designed to run efficiently on CPU environments using the `Wav2Vec2ForCTC` architecture.

## Model and Processor Locations

**IMPORTANT: The model and dataset files are NOT committed to GitHub due to their large size.**

The definitive models are stored on Google Drive under the following paths:
- **Trained ASR Model:** `/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500/`
- **Processor:** `/content/drive/MyDrive/MatriVaani_ASR/processor/`
- **Dataset:** `/content/drive/MyDrive/MatriVaani_ASR/datasets/`

By default, `transcriber.py` will attempt to load the model and processor from those Google Drive paths. You can override these paths using environment variables if running locally:
```bash
export ASR_MODEL_PATH="./models/checkpoint-1500"
export ASR_PROCESSOR_PATH="./models/processor"
```

## Running the API

The ASR engine exposes a FastAPI backend for easy integration with frontend applications (like the Flutter Classroom app).

To run the API locally:
```bash
uvicorn asr_engine.api:app --host 0.0.0.0 --port 8000
```

### API Endpoints

- `GET /health` : Returns API health status and whether the model is loaded in memory.
- `GET /model-info` : Returns model path, processor path, inference device (CPU), and language target.
- `POST /transcribe` : Uploads an audio file and returns the Santali transcription.
  - Automatically converts audio to 16 kHz mono using FFmpeg.
  - Supports `.wav`, `.mp3`, `.m4a`, `.ogg`, `.flac`, `.mp4`.
  - Max upload size is 50MB.

### Example Request
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_sample.wav"
```

### Expected Response Format
```json
{
  "success": true,
  "transcription": "ᱡᱚᱦᱟᱨ ᱜᱮ, ᱪᱮᱫ ᱞᱮᱠᱟ ᱢᱮᱱᱟᱢᱟ?",
  "metrics": {
    "inference_time": 2.15,
    "audio_duration": 4.5,
    "rtf": 0.477
  }
}
```

## Evaluation and Benchmarks

The current production model (`checkpoint-1500`) has been evaluated on robust, real-world datasets:

**Offline 2.9K Sample Evaluation:**
- Test samples: 2,949
- Successful transcriptions: 2,949/2,949
- WER: 59.17%
- CER: 22.37%
- Exact matches: 286/2,949 (9.70%)
- Total audio: approximately 5.39 hours
- Average CPU inference time: 3.39 seconds
- CPU Real-Time Factor (RTF): 0.515

**Live API Stress Test:**
- Tested with short `.wav` files and a 165.58-second external Santali recording.
- Stable short-file API RTF: ~0.81.
- Chunked processing (17 chunks) of the long external recording completed successfully.
- Chunked API RTF: ~0.52.
