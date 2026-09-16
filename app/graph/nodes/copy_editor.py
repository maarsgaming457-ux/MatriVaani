from app.graph.state import MatriVaaniState
from app.services.llm_service import LLMService
from app.core.logging_config import logger
import time

def copy_editor_node(state: MatriVaaniState) -> MatriVaaniState:
    logger.info("--- ENTERING COPY EDITOR NODE ---")
    start_time = time.time()
    
    if state["node_status"].get("scriptwriter") == "failed" or not state.get("generated_script"):
        state["warnings"].append("No generated script available for copy editor.")
        state["node_status"]["copy_editor"] = "skipped"
        return state
        
    try:
        llm_service = LLMService()
        edited_script = llm_service.copy_edit(state["generated_script"])
        
        state["edited_script"] = edited_script
        state["node_status"]["copy_editor"] = "success"
    except Exception as e:
        logger.error(f"Copy Editor Node failed: {e}")
        state["errors"].append(f"Copy Editor Node error: {e}")
        state["node_status"]["copy_editor"] = "failed"
        
    state["processing_time"]["copy_editor"] = time.time() - start_time
    return state
