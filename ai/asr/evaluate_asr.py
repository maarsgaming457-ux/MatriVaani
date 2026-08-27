import torch
import pandas as pd
import soundfile as sf
from jiwer import wer, cer
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def evaluate_model():
    print("Loading Fine-Tuned Model and Processor...")
    processor = Wav2Vec2Processor.from_pretrained("models/santhali_asr_final")
    model = Wav2Vec2ForCTC.from_pretrained("models/santhali_asr_final")
    model.eval()
    
    df = pd.read_csv("datasets/raw/metadata.csv")
    
    predictions = []
    references = []
    
    print("Evaluating...")
    for idx, row in df.iterrows():
        audio_path = f"datasets/raw/{row['file_name']}"
        speech, _ = sf.read(audio_path)
        
        inputs = processor(speech, sampling_rate=16000, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            logits = model(inputs.input_values).logits
            
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        
        predictions.append(transcription)
        references.append(row["transcription"])
        
    calc_wer = wer(references, predictions)
    calc_cer = cer(references, predictions)
    
    print(f"Validation WER: {calc_wer:.4f}")
    print(f"Validation CER: {calc_cer:.4f}")

if __name__ == "__main__":
    evaluate_model()
