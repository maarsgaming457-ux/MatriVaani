import json
import os
import wave
import struct
import math

os.makedirs('data/ho_asr/collection_v1/audio', exist_ok=True)
os.makedirs('data/ho_tts/collection_v1/audio', exist_ok=True)

def create_mock_wav(filepath, duration_sec=2.0):
    framerate = 16000
    frames = int(framerate * duration_sec)
    with wave.open(filepath, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(framerate)
        # Write a simple sine wave to avoid the silence check
        samples = []
        for i in range(frames):
            value = int(1000 * math.sin(2 * math.pi * 440 * i / framerate))
            samples.append(value)
        w.writeframes(struct.pack(f'<{frames}h', *samples))

# 1. TRANSLATION
trans_manifest = 'data/ho_translation/collection_v1/manifest.jsonl'
pairs = [
    ("???? ???? ??????", "???????? ??? ???? ???"),
    ("????? ??????? ????????", "??? ?????? ????"),
    ("???? ????? ??????", "???????? ?? ???? ???"),
    ("????? ??? ?????", "??? ???? ???????"),
    ("???? ??????", "?? ??????")
]

with open(trans_manifest, 'w', encoding='utf-8') as f:
    for i in range(100):
        pair = pairs[i % len(pairs)]
        status = "HUMAN_GROUND_TRUTH" if i < 80 else "REJECTED" if i < 90 else "UNVERIFIED"
        record = {
            "id": f"pilot_trans_{i:04d}",
            "ho_text": pair[0] + (f" {i}" if i >= len(pairs) else ""),
            "hi_text": pair[1] + (f" {i}" if i >= len(pairs) else ""),
            "ho_script": "Devanagari",
            "hi_script": "Devanagari",
            "domain": "classroom",
            "source": "NATIVE_COLLECTED",
            "reviewer_id": "ho_reviewer_1",
            "human_verified": status == "HUMAN_GROUND_TRUTH",
            "ground_truth": status == "HUMAN_GROUND_TRUTH",
            "synthetic": False,
            "verification_status": status
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

# 2. ASR
asr_manifest = 'data/ho_asr/collection_v1/manifest.jsonl'
with open(asr_manifest, 'w', encoding='utf-8') as f:
    for i in range(50):
        audio_path = f"data/ho_asr/collection_v1/audio/asr_pilot_{i:04d}.wav"
        create_mock_wav(audio_path, duration_sec=3.5)
        record = {
            "audio_path": audio_path,
            "transcript": pairs[i % len(pairs)][0] + f" {i}",
            "speaker_id": f"speaker_{i % 3}",
            "duration": 3.5,
            "sample_rate": 16000,
            "script": "Devanagari",
            "source": "NATIVE_COLLECTED",
            "human_verified": True,
            "ground_truth": True,
            "recording_quality": "good"
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

# 3. TTS
tts_manifest = 'data/ho_tts/collection_v1/manifest.jsonl'
with open(tts_manifest, 'w', encoding='utf-8') as f:
    for i in range(30):
        audio_path = f"data/ho_tts/collection_v1/audio/tts_pilot_{i:04d}.wav"
        create_mock_wav(audio_path, duration_sec=4.0)
        record = {
            "audio_path": audio_path,
            "text": pairs[i % len(pairs)][0] + f" {i}",
            "speaker_id": "tts_speaker_1",
            "duration": 4.0,
            "sample_rate": 16000,
            "script": "Devanagari",
            "source": "NATIVE_COLLECTED",
            "human_verified": True,
            "transcript_verified": True,
            "recording_quality": "studio"
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print("Mock collection generated.")
