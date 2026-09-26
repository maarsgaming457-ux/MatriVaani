import json
import os

res_path = os.path.join("data", "ho_hindi", "experimental", "phase35a_100_sentence_validation", "PHASE_35A_HO_100_SENTENCE_RESULTS.json")
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

ho2 = next((r for r in results if 'ho2.wav' in r['audio_filename'].lower()), None)
if ho2:
    print(f"Reference: {ho2['reference_ho']}")
    print(f"ASR: {ho2['asr_ho']}")
    print(f"Translator input: {ho2['asr_ho']}")
    print(f"Hindi: {ho2['hindi_translation']}")
    print(f"Tier: {ho2['translation_tier']}")
    print(f"Confidence: {ho2['confidence']}")
    print(f"ASR latency: {ho2['asr_latency_seconds']}")
    print(f"Translation latency: {ho2['translation_latency_seconds']}")
    print(f"Total latency: {ho2['total_latency_seconds']}")
else:
    print("ho2.wav NOT FOUND in audio_filename.")
