from app.graph.state import MatriVaaniState
from app.services.translation_service import TranslationService
from app.core.logging_config import logger
import time

def translator_node(state: MatriVaaniState) -> MatriVaaniState:
    logger.info("--- ENTERING TRANSLATOR NODE ---")
    start_time = time.time()
    
    if state["node_status"].get("cleaner") == "failed" or not state.get("cleaned_santali"):
        state["warnings"].append("No cleaned Santali text to translate.")
        state["node_status"]["translator"] = "skipped"
        return state
        
    try:
        translation_service = TranslationService()
        translated_text = translation_service.translate(
            text=state["cleaned_santali"],
            source_lang=state["source_language"],
            target_lang=state["target_language"]
        )
        
        state["translated_text"] = translated_text
        state["node_status"]["translator"] = "success"
    except Exception as e:
        logger.error(f"Translator Node failed: {e}")
        state["errors"].append(f"Translator Node error: {e}")
        state["node_status"]["translator"] = "failed"
        
    state["processing_time"]["translator"] = time.time() - start_time
    return state
