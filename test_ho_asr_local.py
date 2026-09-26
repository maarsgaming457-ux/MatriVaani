import os
import time
import json
import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2ForCTC

def preprocess_audio(audio_path):
    t0 = time.time()
    audio, sr = sf.read(audio_path)
    channels = 1 if len(audio.shape) == 1 else audio.shape[1]
    if len(audio.shape) > 1:
        audio = librosa.to_mono(audio.T)
    if sr != 16000:
        audio = librosa.resample(y=audio, orig_sr=sr, target_sr=16000)
    
    audio = (audio - audio.mean()) / (audio.std() + 1e-5)
    t1 = time.time()
    return audio, t1 - t0, sr, channels

def decode_greedy(logits, vocab_dict):
    id_to_token = {v: k for k, v in vocab_dict.items()}
    pred_ids = torch.argmax(logits, dim=-1)[0].tolist()
    
    collapsed = []
    for i in range(len(pred_ids)):
        if i == 0 or pred_ids[i] != pred_ids[i-1]:
            collapsed.append(pred_ids[i])
            
    final_tokens = [id_to_token.get(i, '') for i in collapsed if i != 42]
    return ''.join(final_tokens).replace('|', ' ')

def main():
    model_path = r'C:\study files\sih project\models\ho_asr'
    
    t0 = time.time()
    model = Wav2Vec2ForCTC.from_pretrained(model_path)
    model.eval()
    t1 = time.time()
    
    vocab_path = os.path.join(model_path, 'vocab.json')
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
        
    candidate_files = [
        'fleurs_hi/dev/14584887621258891555.wav',
        'fleurs_hi/dev/10691214664103820058.wav',
        'fleurs_hi/dev/2790069619537345490.wav',
        'fleurs_hi/dev/5958463932227431376.wav',
        'fleurs_hi/dev/1826521854378082525.wav'
    ]
    
    for f in candidate_files:
        if not os.path.exists(f):
            continue
        print('\n' + '-'*50)
        print('FILE')
        print('-' * 50)
        print(f'Path: {f}')
        
        audio, prep_time, orig_sr, channels = preprocess_audio(f)
        duration = len(audio) / 16000
        print(f'Audio duration: {duration:.2f}')
        print(f'Sample rate: {orig_sr}')
        print(f'Channels: {channels}')
        
        inputs = torch.tensor([audio], dtype=torch.float32)
        
        t2 = time.time()
        with torch.no_grad():
            logits = model(inputs).logits
        
        pred_text = decode_greedy(logits, vocab)
        t3 = time.time()
        
        inference_time = t3 - t2
        rtf = inference_time / duration if duration > 0 else 0
        
        print(f'Inference time: {inference_time:.2f} seconds')
        print(f'Real-time factor: {rtf:.2f}')
        try:
            print(f'Prediction: {pred_text}')
        except Exception:
            print(f'Prediction: {pred_text.encode("unicode_escape").decode("utf-8")}')
        print('-'*50)
        
if __name__ == '__main__':
    main()
