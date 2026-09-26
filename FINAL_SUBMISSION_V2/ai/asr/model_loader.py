from ai.asr.inference import WhisperASR, MMSASR

def get_asr_model(model_name: str, **kwargs):
    if "whisper" in model_name.lower():
        return WhisperASR(model_id=model_name, **kwargs)
    elif "mms" in model_name.lower():
        return MMSASR(model_id=model_name, **kwargs)
    else:
        raise ValueError(f"Unknown model family for {model_name}")
