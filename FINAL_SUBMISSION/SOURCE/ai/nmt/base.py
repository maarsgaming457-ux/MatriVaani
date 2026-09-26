from abc import ABC, abstractmethod
from typing import Dict, Any

class NMTModel(ABC):
    """
    Abstract base class for MatriVaani NMT models.
    Every candidate model must implement this interface.
    """
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model and tokenizer into memory."""
        pass
        
    @abstractmethod
    def translate(self, text: str, source_lang: str = "hi", target_lang: str = "sat") -> str:
        """Translate a single sentence from source_lang to target_lang."""
        pass
        
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Return metadata about the loaded model."""
        pass
