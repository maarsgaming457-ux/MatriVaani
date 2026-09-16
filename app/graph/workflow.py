from langgraph.graph import StateGraph, END
from app.graph.state import MatriVaaniState, initialize_state
from app.graph.nodes.asr import asr_node
from app.graph.nodes.cleaner import cleaner_node
from app.graph.nodes.translator import translator_node
from app.graph.nodes.scriptwriter import scriptwriter_node
from app.graph.nodes.copy_editor import copy_editor_node
from app.graph.nodes.finalizer import finalizer_node

def build_graph():
    # 1. Initialize StateGraph
    workflow = StateGraph(MatriVaaniState)

    # 2. Add nodes
    workflow.add_node("asr", asr_node)
    workflow.add_node("cleaner", cleaner_node)
    workflow.add_node("translator", translator_node)
    workflow.add_node("scriptwriter", scriptwriter_node)
    workflow.add_node("copy_editor", copy_editor_node)
    
    # 3. Add edges (Linear pipeline)
    # Conditional logic could be added here, but for now we rely on nodes skipping themselves if state is invalid
    workflow.add_edge("asr", "cleaner")
    workflow.add_edge("cleaner", "translator")
    workflow.add_edge("translator", "scriptwriter")
    workflow.add_edge("scriptwriter", "copy_editor")
    
    # Finalizer is not technically a node returning MatriVaaniState, it returns a dict.
    # In LangGraph, nodes must return a dict matching the state structure.
    # So we should modify finalizer to just return state, or execute it outside the graph.
    # Let's execute finalizer OUTSIDE the graph as a post-processing step to get the structured result.
    workflow.add_edge("copy_editor", END)
    
    # 4. Set entry point
    workflow.set_entry_point("asr")
    
    # 5. Compile graph
    app = workflow.compile()
    return app

def run_pipeline(audio_path: str, target_language: str = "hi") -> dict:
    app = build_graph()
    initial_state = initialize_state(audio_path=audio_path, target_language=target_language)
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    # Run the finalizer on the final state
    result = finalizer_node(final_state)
    return result
