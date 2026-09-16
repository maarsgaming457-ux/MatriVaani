import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "MatriVaani"
    LOG_LEVEL: str = "INFO"
    
    # ASR Config
    ASR_PROVIDER: str = "checkpoint"
    ASR_MODEL_PATH: str = "/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500"
    ASR_PROCESSOR_PATH: str = "/content/drive/MyDrive/MatriVaani_ASR/processor"
    
    HO_ASR_MODEL_PATH: str = ""
    HO_ASR_PROCESSOR_PATH: str = ""
    
    # Translation Config
    TRANSLATION_PROVIDER: str = os.getenv("TRANSLATION_PROVIDER", "mock")
    TARGET_LANGUAGE: str = os.getenv("TARGET_LANGUAGE", "hi")
    
    # LLM Config (Scriptwriter, Editor)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY", None)
    
    # TTS Config
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "parler-tts")
    SARVAM_API_KEY: str | None = os.getenv("SARVAM_API_KEY", None)
    SARVAM_TTS_MODEL: str = os.getenv("SARVAM_TTS_MODEL", "bulbul:v3")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
