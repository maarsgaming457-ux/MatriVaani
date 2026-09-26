import os
import torch
import soundfile as sf
import numpy as np
from transformers import AutoFeatureExtractor, Wav2Vec2ForCTC
from app.core.config import settings
from app.core.logging_config import logger
from app.core.exceptions import ASRError, AudioProcessingError
from training.asr.santali.tokenizer import get_santali_tokenizer

class ASRService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ASRService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Initializing ASRService on device: {self.device}")
        
        self.models = {}
        self.processors = {}
        
        self.initialized = True
        logger.info("ASRService initialized successfully.")

    def _resolve_path(self, p):
        if p and p.startswith("./"):
            root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            return os.path.normpath(os.path.join(root, p[2:]))
        return p

    def _load_model(self, lang: str):
        if lang in self.models:
            return
            
        if settings.ASR_PROVIDER == "mock":
            return
            
        logger.info(f"Loading ASR model for {lang}")
        
        if lang == "ho":
            model_path = self._resolve_path(settings.HO_ASR_MODEL_PATH)
            if not model_path:
                raise ASRError(f"Model path not configured for {lang} ASR.")
            if not os.path.exists(os.path.join(model_path, "model.safetensors")):
                raise ASRError(f"model.safetensors missing in: {model_path}")
            
            import json
            vocab_path = os.path.join(model_path, 'vocab.json')
            if not os.path.exists(vocab_path):
                raise ASRError(f"vocab.json missing in: {model_path}")
                
            with open(vocab_path, 'r', encoding='utf-8') as f:
                vocab = json.load(f)
                
            model = Wav2Vec2ForCTC.from_pretrained(model_path).to(self.device)
            model.eval()
            self.processors[lang] = vocab
            self.models[lang] = model
            logger.info(f"Successfully loaded ASR model and vocab for {lang}")
            return
            
        if lang == "santali":
            model_path_cfg = settings.ASR_MODEL_PATH
            processor_path_cfg = settings.ASR_PROCESSOR_PATH
        else:
            raise ASRError(f"Unsupported ASR language for local loading: {lang}")
            
        if not model_path_cfg:
            raise ASRError(f"Model path not configured for {lang} ASR.")
            
        model_path = self._resolve_path(model_path_cfg)
        processor_path = self._resolve_path(processor_path_cfg)
        
        from transformers import Wav2Vec2Processor
        
        if not os.path.exists(processor_path) and not processor_path.startswith("facebook/"):
            raise ASRError(f"PROCESSOR_PATH does not exist: {processor_path}")
            
        processor = Wav2Vec2Processor.from_pretrained(processor_path)
        
        if settings.ASR_PROVIDER == "huggingface":
            model_path = processor_path
        elif settings.ASR_PROVIDER == "checkpoint":
            if not os.path.exists(model_path) and not model_path.startswith("facebook/"):
                raise ASRError(f"Configured ASR_MODEL_PATH does not exist: {model_path}. DO NOT silently fallback.")
            if not os.path.exists(os.path.join(model_path, "model.safetensors")) and not model_path.startswith("facebook/"):
                raise ASRError(f"model.safetensors missing in: {model_path}")
        else:
            raise ASRError(f"Unknown ASR_PROVIDER: {settings.ASR_PROVIDER}")

        model = Wav2Vec2ForCTC.from_pretrained(model_path).to(self.device)
        model.eval()
        
        self.processors[lang] = processor
        self.models[lang] = model
        logger.info(f"Successfully loaded ASR model for {lang}")

    def process_audio(self, audio_path: str) -> np.ndarray:
        if not os.path.exists(audio_path):
            raise AudioProcessingError(f"Audio file not found: {audio_path}")
            
        try:
            audio_array, sample_rate = sf.read(audio_path, dtype='float32')
            
            # --- Diagnostic Logging for the User ---
            file_size = os.path.getsize(audio_path)
            logger.info("================ WAV DIAGNOSTICS ================")
            logger.info(f"WAV Path: {audio_path}")
            logger.info(f"WAV File Size: {file_size} bytes")
            logger.info(f"WAV Sample Rate: {sample_rate} Hz")
            logger.info(f"WAV Channels: {1 if len(audio_array.shape) == 1 else audio_array.shape[1]}")
            logger.info(f"WAV Frames: {len(audio_array)}")
            logger.info(f"WAV Duration: {len(audio_array) / sample_rate:.2f} seconds")
            
            non_zero_samples = np.count_nonzero(audio_array)
            max_amp = np.max(np.abs(audio_array)) if len(audio_array) > 0 else 0.0
            logger.info(f"Non-zero sample count: {non_zero_samples}")
            logger.info(f"Maximum amplitude: {max_amp}")
            logger.info("=================================================")
            
            if len(audio_array.shape) > 1:
                audio_array = audio_array.mean(axis=1)
            if sample_rate != 16000:
                import librosa
                audio_array = librosa.resample(y=audio_array, orig_sr=sample_rate, target_sr=16000)
            return audio_array
        except Exception as e:
            logger.error(f"Error processing audio {audio_path}: {e}")
            raise AudioProcessingError(f"Audio processing failed: {str(e)}")

    def _normalize_lang(self, lang: str) -> str:
        lang = lang.lower().strip()
        if lang in ["santali", "sat", "santhali"]:
            return "santali"
        if lang in ["ho", "hoc"]:
            return "ho"
        if lang in ["hi", "hindi"]:
            return "hi"
        raise ASRError(f"Unsupported language: {lang}")

    def transcribe(self, audio_path: str, language: str = "santali") -> dict:
        norm_lang = self._normalize_lang(language)
        
        audio_array = self.process_audio(audio_path)
        
        if len(audio_array) == 0:
            raise AudioProcessingError("Audio array is empty.")
            
        max_amp = np.max(np.abs(audio_array))
        if max_amp < 0.001:
            logger.warning(f"Audio is pure silence (max_amp={max_amp}). Skipping ASR.")
            return {"transcript": "[SILENCE DETECTED]", "confidence": 0.0}

        if norm_lang == "hi":
            try:
                import openai
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    return {"transcript": "[MOCK HINDI ASR] ?? ?? ????? ????? ???", "confidence": 1.0}
                
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                with open(audio_path, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=(os.path.basename(audio_path), audio_file.read()),
                        model="whisper-large-v3",
                        language="hi",
                        temperature=0.0
                    )
                logger.info(f"Groq ASR Hindi Result: '{transcription.text}'")
                return {"transcript": transcription.text, "confidence": 1.0}
            except Exception as e:
                logger.error(f"Hindi Groq ASR failed: {e}")
                return {"transcript": f"[FAILED HINDI ASR] {e}", "confidence": 0.0}
            
        if settings.ASR_PROVIDER == "mock":
            return {
                "transcript": f"[MOCK {norm_lang.upper()} ASR TRANSCRIPT] ?? ????",
                "confidence": 1.0,
                "audio_length_seconds": len(audio_array) / 16000.0
            }
            
        self._load_model(norm_lang)
        model = self.models[norm_lang]
        
        if norm_lang == "ho":
            # Manual processing for Ho
            audio_array = (audio_array - audio_array.mean()) / (audio_array.std() + 1e-5)
            inputs = torch.tensor([audio_array], dtype=torch.float32).to(self.device)
            try:
                with torch.no_grad():
                    logits = model(inputs).logits
                vocab = self.processors[norm_lang]
                id_to_token = {v: k for k, v in vocab.items()}
                pred_ids = torch.argmax(logits, dim=-1)[0].tolist()
                
                collapsed = []
                for i in range(len(pred_ids)):
                    if i == 0 or pred_ids[i] != pred_ids[i-1]:
                        collapsed.append(pred_ids[i])
                        
                final_tokens = [id_to_token.get(i, '') for i in collapsed if i != 42]
                transcription = "".join(final_tokens).replace('|', ' ')
                
                return {
                    "transcript": transcription,
                    "confidence": 1.0,
                    "audio_length_seconds": len(audio_array) / 16000.0
                }
            except Exception as e:
                logger.error(f"Ho ASR inference failed: {e}")
                raise ASRError(f"Ho ASR inference failed: {str(e)}")
        
        # Default processing (Santali)
        processor = self.processors[norm_lang]
        inputs = processor(audio_array, sampling_rate=16000, return_tensors="pt", padding=True)
        input_values = inputs.input_values.to(self.device)
        
        try:
            with torch.no_grad():
                logits = model(input_values).logits
                
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = processor.batch_decode(predicted_ids)[0]
            
            return {
                "transcript": transcription,
                "confidence": 1.0,
                "audio_length_seconds": len(audio_array) / 16000.0
            }
        except Exception as e:
            logger.error(f"ASR inference failed: {e}")
            raise ASRError(f"ASR inference failed: {str(e)}")
