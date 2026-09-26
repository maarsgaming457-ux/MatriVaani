import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.services.asr_service import ASRService
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService

asr = ASRService()
trans = TranslationService()
tts = TTSService()

print("\n--- ASR Test ---")
asr_res = asr.transcribe("test_hindi_voice.wav", language="hi")
print(f"ASR Result: {asr_res}")

print("\n--- ASR Silence Test ---")
asr_silence = asr.transcribe("silent_test.wav", language="hi")
print(f"Silence Result: {asr_silence}")

print("\n--- TTS Test ---")
audio_bytes = tts.synthesize("???", language="santali")
print(f"Generated TTS bytes: {len(audio_bytes)}")

import soundfile as sf
import io
info = sf.info(io.BytesIO(audio_bytes))
print(f"WAV Format: {info.format}")
print(f"WAV Subtype: {info.subtype}")
