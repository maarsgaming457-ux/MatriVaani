from app.graph.state import MatriVaaniState
from data_modules.santali.text_normalizer import SantaliNormalizer
from app.core.logging_config import logger
import time
import re

def cleaner_node(state: MatriVaaniState) -> MatriVaaniState:
    logger.info("--- ENTERING CLEANER NODE ---")
    start_time = time.time()
    
    if state["node_status"].get("asr") == "failed" or not state.get("santali_transcript"):
        state["warnings"].append("No valid transcript to clean.")
        state["node_status"]["cleaner"] = "skipped"
        return state
        
    try:
        normalizer = SantaliNormalizer()
        raw_text = state["santali_transcript"]
        
        # Additional rule for <unintelligible>
        raw_text = re.sub(r'<unintelligible>', '', raw_text, flags=re.IGNORECASE)
        
        # Remove multiple spaces if any were left by removing unintelligible
        raw_text = re.sub(r'\s+', ' ', raw_text).strip()

        normalized_result = normalizer.normalize(raw_text)
        state["cleaned_santali"] = normalized_result["normalized_text"]
        
        if not state["cleaned_santali"]:
            state["warnings"].append("Transcript became empty after cleaning.")
            
        state["node_status"]["cleaner"] = "success"
    except Exception as e:
        logger.error(f"Cleaner Node failed: {e}")
        state["errors"].append(f"Cleaner Node error: {e}")
        state["node_status"]["cleaner"] = "failed"
        
    state["processing_time"]["cleaner"] = time.time() - start_time
    return state
