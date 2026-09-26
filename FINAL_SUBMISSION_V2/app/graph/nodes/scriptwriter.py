from app.graph.state import MatriVaaniState
from app.services.llm_service import LLMService
from app.core.logging_config import logger
import time

def scriptwriter_node(state: MatriVaaniState) -> MatriVaaniState:
    logger.info("--- ENTERING SCRIPTWRITER NODE ---")
    start_time = time.time()
    
    if state["node_status"].get("translator") == "failed" or not state.get("translated_text"):
        state["warnings"].append("No translated text available for scriptwriter.")
        state["node_status"]["scriptwriter"] = "skipped"
        return state
        
    try:
        llm_service = LLMService()
        result = llm_service.generate_script(state["translated_text"])
        
        state["script_title"] = result.get("title")
        
        # Build the script text from the structured parts
        parts = []
        if result.get("introduction"):
            parts.append(f"INTRODUCTION:\n{result['introduction']}\n")
        if result.get("main_content"):
            parts.append(f"MAIN CONTENT:\n{result['main_content']}\n")
        if result.get("conclusion"):
            parts.append(f"CONCLUSION:\n{result['conclusion']}\n")
            
        script_text = "\n".join(parts) if parts else result.get("script", "")
        
        state["generated_script"] = script_text
        state["node_status"]["scriptwriter"] = "success"
    except Exception as e:
        logger.error(f"Scriptwriter Node failed: {e}")
        state["errors"].append(f"Scriptwriter Node error: {e}")
        state["node_status"]["scriptwriter"] = "failed"
        
    state["processing_time"]["scriptwriter"] = time.time() - start_time
    return state
