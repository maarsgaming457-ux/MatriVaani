import os
import torch
import unicodedata
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.core.logging_config import logger

class MundariTranslationService:
    def __init__(self):
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/best_model_main2"))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        # Model config constants
        self.decoder_start_token_id = 2
        self.pad_token_id = 1
        self.eos_token_id = 2

    def _load_model(self):
        if self.model is None:
            logger.info("Loading Mundari IndicTrans2 model...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path, trust_remote_code=True)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Mundari IndicTrans2 model loaded on {self.device}.")

    def _normalize_hindi(self, text: str) -> str:
        if not text:
            return ""
        norm = unicodedata.normalize("NFKC", text.strip())
        
        # Add Purnaviram if no terminal punctuation exists
        terminal_punctuations = ("।", "?", "!", ".")
        if not norm.endswith(terminal_punctuations):
            norm += "।"
            
        return norm

    def translate(self, text: str) -> str:
        if not text:
            return ""
            
        logger.info(f"[MATRI-NMT] ASR text: {text}")
        norm_text = self._normalize_hindi(text)
        logger.info(f"[MATRI-NMT] normalized text: {norm_text}")
        
        self._load_model()
        
        # Format input string for IndicTrans2 tokenization
        # source_lang target_lang text
        input_str = f"hin_Deva unr_Deva {norm_text}"
        
        inputs = self.tokenizer(input_str, return_tensors="pt").to(self.device)
        
        gen_params = dict(
            num_beams=5,
            repetition_penalty=1.2,
            length_penalty=0.7,
            max_new_tokens=256,
            decoder_start_token_id=self.decoder_start_token_id,
            pad_token_id=self.pad_token_id,
            eos_token_id=self.eos_token_id,
            use_cache=False,
            do_sample=False,
        )
        
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                **gen_params
            )
            
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Clean up any leftover language tags if present
        decoded = decoded.replace("unr_Deva", "").replace("hin_Deva", "").replace("▁", " ").strip()
        
        logger.info(f"[MATRI-NMT] translation: {decoded}")
        
        return decoded

mundari_translation_service = MundariTranslationService()
