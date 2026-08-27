from .model_loader import load_nmt_model

def translate_text(text: str, model_name: str, source_lang: str = "hi", target_lang: str = "sat") -> str:
    """
    Main entry point for translation inference.
    """
    if not text.strip():
        return ""
        
    model = load_nmt_model(model_name)
    if model is None:
        return "[Translation Error: Model not loaded]"
        
    return model.translate(text, source_lang, target_lang)
