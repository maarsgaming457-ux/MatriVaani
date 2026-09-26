import os
import json
import time
import torch
import numpy as np
import scipy.io.wavfile as wavfile
from transformers import VitsModel, AutoTokenizer

MODEL_ID = 'facebook/mms-tts-hoc'
TEST_FILE = 'data/ho_hindi/experimental/master_task2/ho_tts_test_sentences.json'
AUDIO_DIR = 'data/ho_hindi/experimental/master_task2/audio'

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(TEST_FILE, 'r', encoding='utf-8') as f:
    sentences = json.load(f)

print(f"Loading {MODEL_ID}...")
start_time = time.time()
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = VitsModel.from_pretrained(MODEL_ID)
except Exception as e:
    print(f"Failed to load model: {e}")
    exit(1)
load_time = time.time() - start_time
print(f"Model loaded in {load_time:.2f}s")

# Inspect Model
model_info = {
    'model_class': model.__class__.__name__,
    'tokenizer_class': tokenizer.__class__.__name__,
    'language_code': getattr(model.config, 'lang', 'unknown'),
    'sampling_rate': model.config.sampling_rate,
    'vocab_size': tokenizer.vocab_size,
    'vocab': list(tokenizer.get_vocab().keys())[:10], # sample
}
with open('data/ho_hindi/experimental/master_task2/model_info.json', 'w', encoding='utf-8') as f:
    json.dump(model_info, f, indent=2)

tokenization_results = []
audio_stats = []
performance = {'cold': [], 'warm': []}

for i, record in enumerate(sentences):
    ho_text = record['ho_text']
    sid = record['id']
    
    # Tokenize
    inputs = tokenizer(ho_text, return_tensors='pt')
    token_ids = inputs['input_ids'][0].tolist()
    unk_id = tokenizer.unk_token_id
    unk_count = token_ids.count(unk_id)
    
    tokenization_results.append({
        'id': sid,
        'text': ho_text,
        'token_count': len(token_ids),
        'unk_count': unk_count,
        'tokens': token_ids,
        'success': unk_count == 0
    })
    
    # Inference (Cold start for first 3)
    t0 = time.time()
    with torch.no_grad():
        output = model(**inputs).waveform
    inf_time = time.time() - t0
    
    if i < 3:
        performance['cold'].append(inf_time)
    
    waveform = output[0].cpu().numpy()
    
    audio_path = os.path.join(AUDIO_DIR, f"{sid}.wav")
    wavfile.write(audio_path, model.config.sampling_rate, waveform)
    
    audio_stats.append({
        'id': sid,
        'shape': waveform.shape,
        'sample_count': len(waveform),
        'min': float(np.min(waveform)),
        'max': float(np.max(waveform)),
        'rms': float(np.sqrt(np.mean(waveform**2))),
        'has_nan': bool(np.isnan(waveform).any()),
        'has_inf': bool(np.isinf(waveform).any())
    })

# Warm start tests
warm_text = sentences[0]['ho_text']
for _ in range(10):
    inputs = tokenizer(warm_text, return_tensors='pt')
    t0 = time.time()
    with torch.no_grad():
        _ = model(**inputs).waveform
    performance['warm'].append(time.time() - t0)

perf_stats = {
    'load_time': load_time,
    'cold_times': performance['cold'],
    'warm_min': min(performance['warm']),
    'warm_max': max(performance['warm']),
    'warm_mean': np.mean(performance['warm']),
    'warm_median': np.median(performance['warm']),
}

with open('data/ho_hindi/experimental/master_task2/tokenization_results.json', 'w', encoding='utf-8') as f:
    json.dump(tokenization_results, f, indent=2)

with open('data/ho_hindi/experimental/master_task2/audio_stats.json', 'w', encoding='utf-8') as f:
    json.dump(audio_stats, f, indent=2)

with open('data/ho_hindi/experimental/master_task2/performance_stats.json', 'w', encoding='utf-8') as f:
    json.dump(perf_stats, f, indent=2)

print("Verification complete.")
