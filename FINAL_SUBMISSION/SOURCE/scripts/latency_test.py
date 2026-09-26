import os
import sys
import time
import json
import librosa

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()

def test_multiple():
    results = []
    audio_path = 'test_audio.wav'
    if not os.path.exists(audio_path):
        print("Audio found: NO")
        return

    from app.services.asr_service import ASRService
    from app.services.translation_service import TranslationService
    
    asr = ASRService()
    translator = TranslationService()
    
    for i in range(3):
        print(f"--- RUN {i+1} ---")
        res = {'asr': 0, 'trans': 0, 'total': 0}
        
        t_asr_start = time.time()
        transcript = asr.transcribe(audio_path)
        t_asr_end = time.time()
        
        transcript_str = transcript['transcript'] if isinstance(transcript, dict) else transcript
        res['asr'] = t_asr_end - t_asr_start
        
        t_trans_start = time.time()
        hindi_translation = translator.translate(transcript_str, source_lang="santali", target_lang="hi")
        t_trans_end = time.time()
        
        res['trans'] = t_trans_end - t_trans_start
        res['total'] = res['asr'] + res['trans']
        
        results.append(res)
        print(f"ASR: {res['asr']:.3f}s")
        print(f"Trans: {res['trans']:.3f}s")
        print(f"Total: {res['total']:.3f}s")
        time.sleep(1) # prevent rate limit
        
    asr_times = [r['asr'] for r in results]
    trans_times = [r['trans'] for r in results]
    total_times = [r['total'] for r in results]
    
    print("\n--- SUMMARY ---")
    print(f"ASR - Min: {min(asr_times):.3f}, Avg: {sum(asr_times)/3:.3f}, Max: {max(asr_times):.3f}")
    print(f"Trans - Min: {min(trans_times):.3f}, Avg: {sum(trans_times)/3:.3f}, Max: {max(trans_times):.3f}")
    print(f"Total - Min: {min(total_times):.3f}, Avg: {sum(total_times)/3:.3f}, Max: {max(total_times):.3f}")

if __name__ == '__main__':
    test_multiple()
