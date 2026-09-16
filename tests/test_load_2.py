import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

print("Loading processor...")
processor = Wav2Vec2Processor.from_pretrained("models/checkpoint-1500")
print("Processor loaded. Loading model...")
model = Wav2Vec2ForCTC.from_pretrained("models/checkpoint-1500")
print("Model loaded. Moving to device...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print("Moved to device.")

for i in range(100):
    print("hello", i)
