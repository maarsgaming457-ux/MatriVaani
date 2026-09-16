import time
import os
import io
import torch
import soundfile as sf
import numpy as np
import traceback
import sys

import transformers
transformers.logging.set_verbosity_error()

start_load = time.time()
try:
    from parler_tts import ParlerTTSForConditionalGeneration, ParlerTTSConfig
    from transformers import AutoTokenizer, GenerationMixin

    if GenerationMixin not in ParlerTTSForConditionalGeneration.__bases__:
        ParlerTTSForConditionalGeneration.__bases__ = (GenerationMixin,) + ParlerTTSForConditionalGeneration.__bases__

    if not hasattr(ParlerTTSForConditionalGeneration, "_validate_model_kwargs"):
        ParlerTTSForConditionalGeneration._validate_model_kwargs = lambda self, kwargs: None

    def custom_prepare_mask(self, inputs_tensor, *args, **kwargs):
        return torch.ones(inputs_tensor.shape[:2], dtype=torch.long, device=inputs_tensor.device)
    ParlerTTSForConditionalGeneration._prepare_attention_mask_for_generation = custom_prepare_mask

    original_expand = transformers.GenerationMixin._expand_inputs_for_generation
    
    @classmethod
    def patched_expand(cls, *args, **kwargs):
        if kwargs.get('expand_size') is None:
            kwargs['expand_size'] = 1
        return original_expand(*args, **kwargs)
        
    ParlerTTSForConditionalGeneration._expand_inputs_for_generation = patched_expand

    ParlerTTSConfig.to_diff_dict = lambda self: self.to_dict()
    
    original_init = ParlerTTSConfig.__init__
    def patched_init(self, **kwargs):
        original_init(self, **kwargs)
        if not hasattr(self, 'tie_encoder_decoder'):
            self.tie_encoder_decoder = False
        if not hasattr(self, 'tie_word_embeddings'):
            self.tie_word_embeddings = False
    ParlerTTSConfig.__init__ = patched_init

    original_tie_weights = ParlerTTSForConditionalGeneration.tie_weights
    def patched_tie_weights(self, *args, **kwargs):
        if hasattr(self, "text_encoder") and hasattr(self.text_encoder, "tie_weights"):
            self.text_encoder.tie_weights()
        if hasattr(self, "decoder") and hasattr(self.decoder, "tie_weights"):
            self.decoder.tie_weights()
        return original_tie_weights(self)
    ParlerTTSForConditionalGeneration.tie_weights = patched_tie_weights

    device = "cpu"
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "ai4bharat/indic-parler-tts", 
        low_cpu_mem_usage=False
    ).to(device)
    
    from transformers import GenerationConfig
    if not hasattr(model, "generation_config"):
        model.generation_config = GenerationConfig.from_model_config(model.config)
        if getattr(model.generation_config, "num_return_sequences", None) is None:
            model.generation_config.num_return_sequences = 1
    
    tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
    flan_path = os.path.expanduser("~/.cache/huggingface/hub/models--google--flan-t5-large/snapshots/a178bb092025170d18bcff70125d19db2fb6e98b")
    description_tokenizer = AutoTokenizer.from_pretrained(flan_path)
    
except Exception as e:
    traceback.print_exc()
    sys.exit(1)

santali_text = '???'
description = "A male speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."

try:
    input_ids = description_tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(santali_text, return_tensors="pt").input_ids.to(device)

    with torch.no_grad():
        # use_cache=False to avoid DynamicCache attribute issues in transformers 4.45+
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids, use_cache=False)
        
    audio_arr = generation.cpu().numpy().squeeze()
    sample_rate = model.config.sampling_rate
    
    out_file = "test_parler_output.wav"
    sf.write(out_file, audio_arr, sample_rate, format='WAV')
    
    with open(out_file, "rb") as f:
        header = f.read(16)
        if not header.startswith(b'RIFF') or b'WAVE' not in header:
            print("ERROR: Invalid WAV header.")
            sys.exit(1)
            
    data, sr = sf.read(out_file)
    duration = len(data) / sr
    
    print("=== WAV VERIFICATION ===")
    print(f"Size: {os.path.getsize(out_file)} bytes")
    print(f"Sample Rate: {sr} Hz")
    print(f"Channels: {1 if len(data.shape) == 1 else data.shape[1]}")
    print(f"Frames: {len(data)}")
    print(f"Duration: {duration:.2f} seconds")
    
    max_amp = np.max(np.abs(data))
    print(f"Max Amplitude: {max_amp:.4f}")
    
    if duration <= 0:
        print("ERROR: Duration is 0!")
    elif max_amp == 0.0:
        print("ERROR: Audio contains only silence (all zeros)!")
    else:
        print("SUCCESS: Audio contains non-zero samples and is a valid WAV.")
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
