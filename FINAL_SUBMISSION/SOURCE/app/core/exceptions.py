class MatriVaaniException(Exception):
    """Base exception for MatriVaani."""
    pass

class AudioProcessingError(MatriVaaniException):
    """Raised when audio cannot be processed."""
    pass

class ASRError(MatriVaaniException):
    """Raised when ASR inference fails."""
    pass

class TranslationError(MatriVaaniException):
    """Raised when translation fails."""
    pass

class ScriptGenerationError(MatriVaaniException):
    """Raised when script generation fails."""
    pass

class CopyEditingError(MatriVaaniException):
    """Raised when copy editing fails."""
    pass

class TTSError(MatriVaaniException):
    """Raised when TTS generation fails."""
    pass
