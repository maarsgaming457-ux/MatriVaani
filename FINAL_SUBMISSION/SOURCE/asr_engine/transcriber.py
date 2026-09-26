import os
import torch
import numpy as np
import soundfile as sf
import librosa
import time
from dotenv import load_dotenv

load_dotenv()

def _resolve_path(env_var, default):
    p = os.environ.get(env_var, default)
    if p and p.startswith("./"):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.normpath(os.path.join(root, p[2:]))
    return p

MODEL_PATH = _resolve_path("ASR_MODEL_PATH", "")
PROCESSOR_PATH = _resolve_path("ASR_PROCESSOR_PATH", "")

class SantaliASR:
    def __init__(self):
        self.model = None
        self.processor = None
        self.placeholder_mode = True
        self.device = torch.device("cpu")

        if MODEL_PATH and os.path.exists(MODEL_PATH) and PROCESSOR_PATH and os.path.exists(PROCESSOR_PATH):
            if os.path.exists(os.path.join(MODEL_PATH, "model.safetensors")):
                try:
                    from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
                    print(f"Loading processor from {PROCESSOR_PATH}...")
                    self.processor = Wav2Vec2Processor.from_pretrained(PROCESSOR_PATH)
                    print(f"Loading model from {MODEL_PATH}...")
                    self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)
                    self.model.to(self.device)
                    self.model.eval()
                    self.placeholder_mode = False
                    print("ASR Engine initialized on CPU with trained model.")
                except Exception as e:
                    print(f"Warning: Could not load model: {e}. Running in placeholder mode.")
            else:
                print(f"Warning: model.safetensors missing in {MODEL_PATH}. Running in placeholder mode.")
        else:
            print("No model paths found. Running in PLACEHOLDER mode (demo responses).")
            print("Set ASR_MODEL_PATH and ASR_PROCESSOR_PATH environment variables to use trained model.")
        
    def transcribe(self, audio_array, sampling_rate=16000):
        t0 = time.time()

        if self.placeholder_mode:
            # Placeholder mode - return demo response
            duration = len(audio_array) / float(sampling_rate)
            inference_time = time.time() - t0
            return {
                "transcription": "[Placeholder] जोहार! आम मातृभाषा एपेसँग काम कराव आहां। (Connect trained model for real transcription)",
                "inference_time": inference_time,
                "audio_duration": duration,
                "rtf": inference_time / duration if duration > 0 else 0
            }

        if sampling_rate != 16000:
            audio_array = librosa.resample(audio_array, orig_sr=sampling_rate, target_sr=16000)

        if len(audio_array.shape) > 1:
            audio_array = audio_array.mean(axis=1)

        audio_array = audio_array.astype(np.float32)

        inputs = self.processor(audio_array, sampling_rate=16000, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        inference_time = time.time() - t0
        duration = len(audio_array) / 16000.0
        rtf = inference_time / duration if duration > 0 else 0

        return {
            "transcription": transcription,
            "inference_time": inference_time,
            "audio_duration": duration,
            "rtf": rtf
        }
