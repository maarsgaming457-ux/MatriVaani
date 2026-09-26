import torch
from transformers import VitsModel, AutoTokenizer
import soundfile as sf
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    print("Loading model...")
    model_id = "facebook/mms-tts-hoc"
    model = VitsModel.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Use an Odia character since the tokenizer seems to use Odia script
    text = "\u0b15\u0b3e" # "ka" in Odia
    
    inputs = tokenizer(text, return_tensors="pt")
    
    print("Generating audio...")
    start_time = time.time()
    with torch.no_grad():
        output = model(**inputs).waveform
    latency = time.time() - start_time
    print(f"Inference Latency: {latency:.2f} seconds")

    audio_path = "ho_tts_output.wav"
    sf.write(audio_path, output.squeeze().cpu().numpy(), model.config.sampling_rate)
    
    print(f"Saved audio to {audio_path}")
    print(f"Sample Rate: {model.config.sampling_rate}")
    print(f"Duration: {output.shape[-1] / model.config.sampling_rate:.2f} seconds")
    
except Exception as e:
    print(f"Error: {e}")
