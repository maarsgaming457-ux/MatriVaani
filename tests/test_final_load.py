from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
try:
    processor = Wav2Vec2Processor.from_pretrained("models/santhali_asr_final_5k")
    model = Wav2Vec2ForCTC.from_pretrained("models/santhali_asr_final_5k")
    print("LOADABLE: TRUE")
except Exception as e:
    print("LOADABLE: FALSE")
    print(e)
