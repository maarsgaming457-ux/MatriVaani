from abc import ABC, abstractmethod
import time
import psutil
import os
from typing import Dict, Any

class ASRModel(ABC):
    def __init__(self, model_name: str, version: str):
        self.model_name = model_name
        self.version = version
        self.is_loaded = False
        
    @abstractmethod
    def load_model(self, language: str = "hi", quantize_int8: bool = False) -> None:
        """Loads the model into memory (CPU/GPU)."""
        pass
        
    @abstractmethod
    def transcribe(self, audio_path: str, language: str) -> str:
        """Transcribes the given audio file."""
        pass
        
    def get_model_info(self) -> Dict[str, Any]:
        """Returns metadata about the model."""
        return {
            "model_name": self.model_name,
            "version": self.version,
            "is_loaded": self.is_loaded
        }
        
    def get_memory_usage(self) -> float:
        """Returns current memory usage of the process in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
