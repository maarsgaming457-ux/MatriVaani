import os
import json
import base64
import time
import requests
from abc import ABC, abstractmethod

from app.core.config import settings
from app.core.logging_config import logger
from app.core.exceptions import TTSError

class TTSUnavailableError(TTSError):
    """Raised when the requested TTS provider or language is not available."""
    pass

class TTSProviderBase(ABC):
    @abstractmethod
    def synthesize(self, text: str, language: str) -> bytes:
        pass

class UnavailableTTSProvider(TTSProviderBase):
    def synthesize(self, text: str, language: str) -> bytes:
        raise TTSUnavailableError("TTS provider is not configured or unavailable.")

class BhashiniTTSProvider(TTSProviderBase):
    def synthesize(self, text: str, language: str) -> bytes:
        raise TTSUnavailableError("Bhashini TTS provider is ON HOLD pending credentials.")

class LocalTTSProvider(TTSProviderBase):
    def synthesize(self, text: str, language: str) -> bytes:
        raise TTSUnavailableError("Local TTS provider is NOT FEASIBLE on current hardware.")

class SarvamTTSProvider(TTSProviderBase):
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.model = settings.SARVAM_TTS_MODEL
        self.url = "https://api.sarvam.ai/text-to-speech"

    def synthesize(self, text: str, language: str) -> bytes:
        if not self.api_key:
            raise TTSUnavailableError("SARVAM_API_KEY is not configured.")
            
        if language != "hi":
            raise TTSUnavailableError(f"Sarvam Bulbul TTS currently only supports Hindi (hi-IN). Requested: {language}")
            
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": [text],
            "target_language_code": "hi-IN",
            "speaker": "ritu",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": self.model
        }
        
        try:
            start_time = time.time()
            response = requests.post(self.url, json=payload, headers=headers, timeout=5.0)
            response.raise_for_status()
            
            data = response.json()
            if "audios" not in data or not data["audios"]:
                raise TTSError("Invalid response from Sarvam API: missing 'audios' array.")
                
            audio_base64 = data["audios"][0]
            audio_bytes = base64.b64decode(audio_base64)
            
            elapsed = time.time() - start_time
            logger.info(f"[TTS ROUTER] Sarvam TTS synthesized {len(audio_bytes)} bytes in {elapsed:.3f}s")
            return audio_bytes
            
        except requests.exceptions.HTTPError as e:
            err_msg = e.response.text if e.response is not None else str(e)
            logger.error(f"[TTS ROUTER] Sarvam API HTTP error: {e}. Details: {err_msg}")
            raise TTSUnavailableError(f"Sarvam HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"[TTS ROUTER] Sarvam API network error: {e}")
            raise TTSUnavailableError(f"Sarvam network error: {e}")
        except Exception as e:
            logger.error(f"[TTS ROUTER] Sarvam API unexpected error: {e}")
            raise TTSUnavailableError(f"Sarvam unexpected error: {e}")

class TTSService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TTSService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        self.default_provider_name = os.getenv("TTS_PROVIDER", "none").lower()
        self.providers = {
            "sarvam": SarvamTTSProvider(),
            "bhashini": BhashiniTTSProvider(),
            "local": LocalTTSProvider(),
            "parler-tts": LocalTTSProvider(),
        }
        
        self.initialized = True

    def _get_provider(self, name: str) -> TTSProviderBase:
        return self.providers.get(name, UnavailableTTSProvider())
        
    def _normalize_language(self, language: str) -> str:
        lang = language.lower().strip()
        if lang in ["santali", "sat", "santhali"]:
            return "sat"
        elif lang in ["hindi", "hi"]:
            return "hi"
        return lang

    def synthesize(self, text: str, language: str, provider_override: str = None) -> bytes:
        if not text:
            return b""
            
        normalized_lang = self._normalize_language(language)
        
        target_provider_name = (provider_override or self.default_provider_name).lower()
        
        # Define fallback sequence
        fallback_sequence = [target_provider_name]
        
        # Add fallbacks if not explicitly listed
        for fallback in ["sarvam", "bhashini", "local"]:
            if fallback not in fallback_sequence:
                fallback_sequence.append(fallback)
                
        logger.info(f"[TTS ROUTER] Requested TTS for language '{normalized_lang}'. Fallback sequence: {fallback_sequence}")
        
        last_error = None
        for p_name in fallback_sequence:
            try:
                logger.info(f"[TTS ROUTER] Attempting provider '{p_name}'")
                provider = self._get_provider(p_name)
                audio_bytes = provider.synthesize(text, normalized_lang)
                logger.info(f"[TTS ROUTER] Successfully synthesized using '{p_name}'")
                return audio_bytes
            except TTSUnavailableError as e:
                logger.warning(f"[TTS ROUTER] Provider '{p_name}' unavailable or failed: {e}")
                last_error = e
                continue
                
        logger.error("[TTS ROUTER] All TTS providers failed.")
        raise last_error or TTSUnavailableError("No TTS providers available.")
