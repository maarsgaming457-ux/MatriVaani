import os
import numpy as np
import soundfile as sf
import sys
from dotenv import load_dotenv
load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("No Groq API Key found in .env!")
    sys.exit(1)

import openai
client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

print("Testing Whisper on pure silence...")
silent_arr = np.zeros(32000, dtype=np.float32)
sf.write("silent_test.wav", silent_arr, 16000, format='WAV')
with open("silent_test.wav", "rb") as f:
    try:
        transcription = client.audio.transcriptions.create(
            file=("silent_test.wav", f.read()),
            model="whisper-large-v3",
            language="hi",
            temperature=0.0
        )
        print(f"Silence transcribed as: '{transcription.text}'")
    except Exception as e:
        print(f"Error: {e}")

print("Testing Whisper on pure static (noise)...")
noise_arr = np.random.randn(32000).astype(np.float32) * 0.05
sf.write("noise_test.wav", noise_arr, 16000, format='WAV')
with open("noise_test.wav", "rb") as f:
    try:
        transcription = client.audio.transcriptions.create(
            file=("noise_test.wav", f.read()),
            model="whisper-large-v3",
            language="hi",
            temperature=0.0
        )
        print(f"Noise transcribed as: '{transcription.text}'")
    except Exception as e:
        print(f"Error: {e}")
        
print("Testing Whisper on noise with prompt...")
with open("noise_test.wav", "rb") as f:
    try:
        transcription = client.audio.transcriptions.create(
            file=("noise_test.wav", f.read()),
            model="whisper-large-v3",
            language="hi",
            prompt="?? ?? ????? ????? ???",
            temperature=0.0
        )
        print(f"Noise + prompt transcribed as: '{transcription.text}'")
    except Exception as e:
        print(f"Error: {e}")
