import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from app.core.config import settings

def test():
    print("PROCESSOR_PATH:", settings.PROCESSOR_PATH)
    print("ASR_MODEL_PATH:", settings.ASR_MODEL_PATH)
    
    try:
        processor = Wav2Vec2Processor.from_pretrained(settings.PROCESSOR_PATH)
        print("Processor loaded: YES")
        proc_vocab = len(processor.tokenizer)
        print("Processor vocabulary:", proc_vocab)
    except Exception as e:
        print("Processor loaded: NO", e)
        proc_vocab = -1
        
    try:
        model = Wav2Vec2ForCTC.from_pretrained(settings.ASR_MODEL_PATH)
        print("Checkpoint loaded: YES")
        model.eval()
        print("Model initialized: YES")
        model_vocab = model.config.vocab_size
        print("Model vocabulary:", model_vocab)
    except Exception as e:
        print("Checkpoint loaded: NO", e)
        model_vocab = -1
        
    if proc_vocab == 41 and model_vocab == 41:
        print("Vocabulary compatible: YES")
    else:
        print("Vocabulary compatible: NO")
        
    # Optional Real Load Test
    try:
        from app.services.asr_service import ASRService
        asr = ASRService()
        result = asr.transcribe("test_audio.wav")
        print("Real ASR test: PASS")
    except Exception as e:
        print("Real ASR test: FAILED", e)

if __name__ == "__main__":
    test()
