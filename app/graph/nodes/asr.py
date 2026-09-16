from app.graph.state import MatriVaaniState
from app.services.asr_service import ASRService
from app.core.logging_config import logger
import time

def asr_node(state: MatriVaaniState) -> MatriVaaniState:
    logger.info("--- ENTERING ASR NODE ---")
    start_time = time.time()
    
    if not state.get("audio_path"):
        state["warnings"].append("No audio_path provided to ASR node.")
        state["node_status"]["asr"] = "skipped"
        return state
        
    try:
        asr_service = ASRService()
        result = asr_service.transcribe(state["audio_path"])
        
        state["santali_transcript"] = result["transcript"]
        state["confidence"] = result["confidence"]
        state["asr_metadata"] = {"audio_length_seconds": result["audio_length_seconds"]}
        state["node_status"]["asr"] = "success"
    except Exception as e:
        logger.error(f"ASR Node failed: {e}")
        state["errors"].append(f"ASR Node error: {e}")
        state["node_status"]["asr"] = "failed"
        
    state["processing_time"]["asr"] = time.time() - start_time
    return state
