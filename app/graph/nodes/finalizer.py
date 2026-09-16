from app.graph.state import MatriVaaniState
from app.core.logging_config import logger
import time

def finalizer_node(state: MatriVaaniState) -> dict:
    logger.info("--- ENTERING FINALIZER NODE ---")
    start_time = time.time()
    
    # Validation logic
    status = "success"
    
    if state["errors"]:
        status = "failed"
    elif state["node_status"].get("asr") != "success":
        status = "failed"
        state["errors"].append("ASR failed or was skipped. Pipeline cannot succeed.")
    elif state["node_status"].get("translator") == "not_configured" or state["node_status"].get("scriptwriter") == "not_configured":
        status = "partial"
    elif not state.get("edited_script") and not state.get("generated_script"):
        status = "partial"
        state["warnings"].append("No final script was generated.")
        
    final_script = state.get("edited_script") or state.get("generated_script") or ""
    
    state["final_content"] = final_script
    state["node_status"]["finalizer"] = "success"
    state["processing_time"]["finalizer"] = time.time() - start_time
    
    return {
        "status": status,
        "transcript": state.get("santali_transcript", ""),
        "cleaned_transcript": state.get("cleaned_santali", ""),
        "translation": state.get("translated_text", ""),
        "script": state.get("generated_script", ""),
        "final_script": final_script,
        "metadata": {
            "processing_time": state["processing_time"],
            "node_status": state["node_status"]
        },
        "warnings": state["warnings"],
        "errors": state["errors"]
    }
