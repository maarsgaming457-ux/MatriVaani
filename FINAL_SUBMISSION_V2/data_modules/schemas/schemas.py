from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal
from enum import Enum

class QualityStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Language(str, Enum):
    HINDI = "hi"
    SANTHALI = "sat"
    HO = "hoc"
    MUNDARI = "unv"
    
class ASRRecord(BaseModel):
    sample_id: str
    language: Language
    speaker_id: str
    audio_path: str
    transcript: str = Field(min_length=1)
    domain: str
    dialect: Optional[str] = None
    duration_seconds: float = Field(gt=0)
    sample_rate: int = Field(gt=0)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    verification_status: QualityStatus = QualityStatus.PENDING
    dataset_version: str

class NMTRecord(BaseModel):
    sample_id: str
    source_language: Language
    target_language: Language
    source_text: str = Field(min_length=1)
    target_text: str = Field(min_length=1)
    domain: str
    subcategory: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    verification_status: QualityStatus = QualityStatus.PENDING
    dataset_version: str

class TTSRecord(BaseModel):
    sample_id: str
    language: Language
    speaker_id: str
    audio_path: str
    transcript: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0)
    sample_rate: int = Field(gt=0)
    domain: str
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    verification_status: QualityStatus = QualityStatus.PENDING
    dataset_version: str
