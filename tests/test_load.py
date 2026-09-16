from transformers import Wav2Vec2ForCTC
try:
    model = Wav2Vec2ForCTC.from_pretrained("models/santhali_asr_5k/checkpoint-1000")
    print("LOADABLE: TRUE")
except Exception as e:
    print("LOADABLE: FALSE")
    print(e)
