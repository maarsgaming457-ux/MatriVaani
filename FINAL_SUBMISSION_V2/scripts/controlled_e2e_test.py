import os
import sys
import time
import json
import librosa

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.config import settings

def test():
    results = {
        'audio_found': False,
        'asr': {'status': 'FAILED', 'time': 0, 'transcript': None},
        'translation': {'status': 'FAILED', 'time': 0, 'output': None},
        'scriptwriter': {'status': 'FAILED', 'time': 0, 'output': None},
        'copy_editor': {'status': 'FAILED', 'time': 0, 'output': None}
    }
    
    audio_path = 'test_audio.wav'
    if os.path.exists(audio_path):
        results['audio_found'] = True
        duration = librosa.get_duration(path=audio_path)
        print(f"Audio found: YES\nAudio path: {audio_path}\nDuration: {duration:.3f}")
    else:
        print("Audio found: NO")
        return results

    try:
        from app.services.asr_service import ASRService
        asr = ASRService()
        
        t0 = time.time()
        transcript = asr.transcribe(audio_path)
        t1 = time.time()
        
        results['asr']['status'] = 'SUCCESS'
        results['asr']['time'] = t1 - t0
        results['asr']['transcript'] = transcript
        print(f"ASR Transcript: {transcript}")
        
    except Exception as e:
        print(f"ASR FAILED: {e}")
        return results
        
    try:
        from app.services.translation_service import TranslationService
        translator = TranslationService()
        
        t0 = time.time()
        hindi_translation = translator.translate(transcript)
        t1 = time.time()
        
        results['translation']['status'] = 'SUCCESS'
        results['translation']['time'] = t1 - t0
        results['translation']['output'] = hindi_translation
        
    except Exception as e:
        print(f"Translation FAILED: {e}")
        return results
        
    try:
        from app.ai.agents.scriptwriter import ScriptwriterAgent
        scriptwriter = ScriptwriterAgent()
        
        t0 = time.time()
        # Scriptwriter typically returns a JSON or dict
        script = scriptwriter.generate(hindi_translation)
        t1 = time.time()
        
        results['scriptwriter']['status'] = 'SUCCESS'
        results['scriptwriter']['time'] = t1 - t0
        results['scriptwriter']['output'] = script
        
    except Exception as e:
        print(f"Scriptwriter FAILED: {e}")
        return results
        
    try:
        from app.ai.agents.copy_editor import CopyEditorAgent
        copy_editor = CopyEditorAgent()
        
        t0 = time.time()
        edited = copy_editor.edit(str(script))
        t1 = time.time()
        
        results['copy_editor']['status'] = 'SUCCESS'
        results['copy_editor']['time'] = t1 - t0
        results['copy_editor']['output'] = edited
        
    except Exception as e:
        print(f"Copy Editor FAILED: {e}")
        return results
        
    return results

if __name__ == '__main__':
    r = test()
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(r, f, ensure_ascii=False, indent=2)

