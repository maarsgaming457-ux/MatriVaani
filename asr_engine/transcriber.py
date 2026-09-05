import os
import torch
import numpy as np
import soundfile as sf
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import time

MODEL_PATH = os.environ.get("ASR_MODEL_PATH", "/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500/")
PROCESSOR_PATH = os.environ.get("ASR_PROCESSOR_PATH", "/content/drive/MyDrive/MatriVaani_ASR/processor/")

class SantaliASR:
    def __init__(self):
        print(f"Loading processor from {PROCESSOR_PATH}...")
        self.processor = Wav2Vec2Processor.from_pretrained(PROCESSOR_PATH)
        print(f"Loading model from {MODEL_PATH}...")
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)
        
        # CPU Inference
        self.device = torch.device("cpu")
        self.model.to(self.device)
        self.model.eval()
        print("ASR Engine initialized on CPU.")
        
    def transcribe(self, audio_array, sampling_rate=16000):
        t0 = time.time()
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
