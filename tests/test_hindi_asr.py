import torch
import soundfile as sf
import os
import io

try:
    print("Loading Parler-TTS for Hindi...")
    from parler_tts import ParlerTTSForConditionalGeneration, ParlerTTSConfig
    from transformers import AutoTokenizer, GenerationMixin, GenerationConfig
    
    # 1. Inject GenerationMixin
    if GenerationMixin not in ParlerTTSForConditionalGeneration.__bases__:
        ParlerTTSForConditionalGeneration.__bases__ = (GenerationMixin,) + ParlerTTSForConditionalGeneration.__bases__
    
    # 2. Add missing validate_kwargs
    if not hasattr(ParlerTTSForConditionalGeneration, "_validate_model_kwargs"):
        ParlerTTSForConditionalGeneration._validate_model_kwargs = lambda self, kwargs: None
    
    def custom_prepare_mask(self, inputs_tensor, *args, **kwargs):
        return torch.ones(inputs_tensor.shape[:2], dtype=torch.long, device=inputs_tensor.device)
    ParlerTTSForConditionalGeneration._prepare_attention_mask_for_generation = custom_prepare_mask

    import transformers
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
    
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "ai4bharat/indic-parler-tts", 
        local_files_only=True,
        low_cpu_mem_usage=False
    ).to("cpu")
    
    if not hasattr(model, "generation_config"):
        model.generation_config = GenerationConfig.from_model_config(model.config)
        if getattr(model.generation_config, "num_return_sequences", None) is None:
            model.generation_config.num_return_sequences = 1
            
    tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts", local_files_only=True)
    description_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large", local_files_only=True)
    
    text = "???? ??? ????? ???"
    description = "A male speaker delivers a clear and precise Hindi speech at a moderate speed and pitch."
    
    input_ids = description_tokenizer(description, return_tensors="pt").input_ids.to("cpu")
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cpu")
    
    print("Synthesizing Hindi audio...")
    with torch.no_grad():
        generation = model.generate(
            input_ids=input_ids, 
            prompt_input_ids=prompt_input_ids,
            use_cache=False
        )
        
    audio_arr = generation.cpu().numpy().squeeze()
    sample_rate = model.config.sampling_rate
    
    out_file = "test_hindi_voice.wav"
    sf.write(out_file, audio_arr, sample_rate, format='WAV')
    print("Saved test_hindi_voice.wav")
    
    import httpx
    print("Sending to /asr...")
    with open(out_file, "rb") as f:
        asr_resp = httpx.post("http://127.0.0.1:8000/asr", files={"file": ("test_hindi_voice.wav", f, "audio/wav")}, data={"language": "hi"}, timeout=30.0)
        
    print(f"ASR Status: {asr_resp.status_code}")
    print(f"ASR Result: {asr_resp.text}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
