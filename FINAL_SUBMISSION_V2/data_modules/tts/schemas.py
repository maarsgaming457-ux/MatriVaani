from pydantic import BaseModel, Field, validator
from typing import Optional

class TTSAudioRecord(BaseModel):
    audio_id: str = Field(..., description="Unique identifier for the audio file")
    transcript: str = Field(..., description="The verified transcript of the audio")
    speaker_id: Optional[str] = Field(None, description="Identifier for the speaker")
    sample_rate: int = Field(22050, description="Sample rate of the audio file")
    duration_sec: float = Field(..., description="Duration of the audio clip in seconds")
    language: str = Field(..., description="Language code, e.g., 'sat'")
    script: str = Field(..., description="Script used in transcript, e.g., 'Ol_Chiki'")

    @validator('duration_sec')
    def check_duration(cls, v):
        if v < 1.0 or v > 15.0:
            raise ValueError("TTS audio clips should be between 1.0 and 15.0 seconds")
        return v
    
    @validator('language')
    def check_language(cls, v):
        allowed = ['sat', 'hi']
        if v not in allowed:
            raise ValueError(f"Language must be one of {allowed}")
        return v
    
    @validator('script')
    def check_script(cls, v):
        allowed = ['Ol_Chiki', 'Devanagari', 'Roman']
        if v not in allowed:
            raise ValueError(f"Script must be one of {allowed}")
        return v
