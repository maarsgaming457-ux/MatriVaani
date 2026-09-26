from typing import TypedDict, Optional, List, Dict, Any

class MatriVaaniState(TypedDict):
    """Shared state for the LangGraph workflow."""
    
    # Input
    audio_path: Optional[str]
    audio_metadata: Optional[Dict[str, Any]]
    
    # ASR Stage
    santali_transcript: Optional[str]
    asr_metadata: Optional[Dict[str, Any]]
    
    # Cleaning Stage
    cleaned_santali: Optional[str]
    
    # Translation Stage
    source_language: str
    target_language: str
    translated_text: Optional[str]
    
    # Scriptwriter Stage
    script_title: Optional[str]
    generated_script: Optional[str]
    
    # Copy Editor Stage
    edited_script: Optional[str]
    
    # Final Output
    final_content: Optional[str]
    
    # Metadata and Status
    confidence: Optional[float]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]
    processing_time: Dict[str, float]
    node_status: Dict[str, str]

def initialize_state(audio_path: Optional[str] = None, target_language: str = "hi") -> MatriVaaniState:
    """Helper to initialize an empty state."""
    return {
        "audio_path": audio_path,
        "audio_metadata": None,
        "santali_transcript": None,
        "asr_metadata": None,
        "cleaned_santali": None,
        "source_language": "sat",
        "target_language": target_language,
        "translated_text": None,
        "script_title": None,
        "generated_script": None,
        "edited_script": None,
        "final_content": None,
        "confidence": None,
        "warnings": [],
        "errors": [],
        "metadata": {},
        "processing_time": {},
        "node_status": {}
    }
