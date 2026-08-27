import time
import torch
import torchaudio
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration, Wav2Vec2ForCTC, Wav2Vec2Processor
from ai.asr.base import ASRModel

class WhisperASR(ASRModel):
    def __init__(self, model_id: str = "openai/whisper-tiny"):
        super().__init__(model_name=model_id, version="1.0")
        self.model_id = model_id
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self, language: str = "hi", quantize_int8: bool = False):
        if not self.is_loaded:
            self.processor = WhisperProcessor.from_pretrained(self.model_id)
            self.model = WhisperForConditionalGeneration.from_pretrained(self.model_id)
            
            if quantize_int8:
                self.model = torch.quantization.quantize_dynamic(
                    self.model, {torch.nn.Linear}, dtype=torch.qint8
                )
                
            self.model.to(self.device)
            self.is_loaded = True
            
    def transcribe(self, audio_path: str, language: str = "hi", quantize_int8: bool = False) -> str:
        if not self.is_loaded:
            self.load_model(language=language, quantize_int8=quantize_int8)
            
        import soundfile as sf
        waveform, sample_rate = sf.read(audio_path, dtype='float32')
        waveform = torch.from_numpy(waveform)
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        else:
            waveform = waveform.t()
            
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
            
        # Whisper processes mono
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
            
        input_features = self.processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_features
        input_features = input_features.to(self.device)
        
        # Determine task and language token
        # Santhali isn't officially in standard whisper tokenizer, but we map standard languages.
        forced_decoder_ids = self.processor.get_decoder_prompt_ids(language=language, task="transcribe")
        
        predicted_ids = self.model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return transcription.strip()

class MMSASR(ASRModel):
    def __init__(self, model_id: str = "facebook/mms-1b-all"):
        super().__init__(model_name=model_id, version="1.0")
        self.model_id = model_id
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self, language: str = "hi", quantize_int8: bool = False):
        if not self.is_loaded:
            self.processor = Wav2Vec2Processor.from_pretrained(self.model_id)
            self.model = Wav2Vec2ForCTC.from_pretrained(self.model_id)
            
            # Load adapter BEFORE quantizing
            lang_map = {"hi": "hin", "sat": "sat"}
            mms_lang = lang_map.get(language, language)
            
            self.processor.tokenizer.set_target_lang(mms_lang)
            self.model.load_adapter(mms_lang)
            
            if quantize_int8:
                self.model = torch.quantization.quantize_dynamic(
                    self.model, {torch.nn.Linear}, dtype=torch.qint8
                )
            
            self.model.to(self.device)
            self.is_loaded = True
            
    def transcribe(self, audio_path: str, language: str = "hi", quantize_int8: bool = False) -> str:
        if not self.is_loaded:
            self.load_model(language=language, quantize_int8=quantize_int8)
            
        # Target language must match what was loaded
        lang_map = {"hi": "hin", "sat": "sat"}
        mms_lang = lang_map.get(language, language)
        self.processor.tokenizer.set_target_lang(mms_lang)
        
        import soundfile as sf
        waveform, sample_rate = sf.read(audio_path, dtype='float32')
        waveform = torch.from_numpy(waveform)
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        else:
            waveform = waveform.t()
            
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
            
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
            
        inputs = self.processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
            
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription.strip()
