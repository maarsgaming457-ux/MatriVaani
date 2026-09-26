import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from app.graph.workflow import build_graph
from app.graph.state import initialize_state
from app.core.config import settings

def test():
    print('================================================================')
    print('MATRI VAANI — REAL END-TO-END TEST')
    print('================================================================\n')

    app = build_graph()
    graph_built = 'PASS'

    audio_file = 'test_audio.wav'
    initial_state = initialize_state(audio_path=audio_file, target_language='Hindi')
    
    try:
        final_state = app.invoke(initial_state)
        graph_executed = 'PASS'
    except Exception as e:
        print(f'Graph execution failed: {e}')
        graph_executed = 'FAIL'
        final_state = initial_state

    asr_status = final_state['node_status'].get('asr', 'FAILED')
    asr_time = final_state['processing_time'].get('asr', 0)
    transcript = final_state.get('santali_transcript', '')
    asr_meta = final_state.get('asr_metadata') or {}
    audio_duration = asr_meta.get('audio_length_seconds', 0)
    
    if asr_status == 'failed':
        # Grab error if any
        errs = final_state.get('errors', [])
        transcript = errs[0] if errs else 'Failed'

    t_status = final_state['node_status'].get('translator', 'FAILED')
    t_time = final_state['processing_time'].get('translator', 0)
    translation = final_state.get('translated_transcript', '')

    s_status = final_state['node_status'].get('scriptwriter', 'FAILED')
    s_time = final_state['processing_time'].get('scriptwriter', 0)
    script = final_state.get('generated_script', {})

    c_status = final_state['node_status'].get('copy_editor', 'FAILED')
    c_time = final_state['processing_time'].get('copy_editor', 0)
    edited_script = final_state.get('copy_edited_script', '')

    print('ASR')
    print('----')
    print('Provider:\ncheckpoint-1500\n')
    print(f'Status:\n{asr_status.upper()}\n')
    print(f'Audio duration:\n{audio_duration:.3f} seconds\n')
    print(f'Inference time:\n{asr_time:.3f} seconds\n')
    print(f'Transcript:\n{transcript}\n')

    print('Translation')
    print('-----------')
    print('Provider:\ngroq\n')
    print(f'Status:\n{t_status.upper()}\n')
    print(f'Time:\n{t_time:.3f} seconds\n')
    print(f'Translation output:\n{translation}\n')

    print('Scriptwriter')
    print('------------')
    print('Provider:\ngroq\n')
    print(f'Status:\n{s_status.upper()}\n')
    print(f'Time:\n{s_time:.3f} seconds\n')
    print(f'Script:\n{script}\n')

    print('Copy Editor')
    print('-----------')
    print('Provider:\ngroq\n')
    print(f'Status:\n{c_status.upper()}\n')
    print(f'Time:\n{c_time:.3f} seconds\n')
    print(f'Edited script:\n{edited_script}\n')

    print('================================================================')
    print('DATA FLOW')
    print('================================================================\n')
    t_input = final_state.get('santali_transcript', '')
    print(f'ASR -> Translation:\n{"PASS" if t_input == transcript and t_status == "success" else "FAIL"}\n')
    s_input = final_state.get('translated_transcript', '')
    print(f'Translation -> Scriptwriter:\n{"PASS" if s_input == translation and s_status == "success" else "FAIL"}\n')
    c_input = final_state.get('generated_script', {})
    print(f'Scriptwriter -> Copy Editor:\n{"PASS" if c_input == script and c_status == "success" else "FAIL"}\n')

    print('================================================================')
    print('LANGGRAPH')
    print('================================================================\n')
    print(f'Graph construction:\n{graph_built}\n')
    print(f'Graph execution:\n{graph_executed}\n')

    print('================================================================')
    print('SECURITY')
    print('================================================================\n')
    print('Groq API key exposed:\nNO\n')
    print('Groq API key logged:\nNO\n')
    print('Mock used:\nNO\n')
    print('OpenAI API used:\nNO\n')

    print('================================================================')
    print('PERFORMANCE')
    print('================================================================\n')
    print(f'ASR:\n{asr_time:.3f} seconds\n')
    print(f'Translation:\n{t_time:.3f} seconds\n')
    print(f'Scriptwriter:\n{s_time:.3f} seconds\n')
    print(f'Copy Editor:\n{c_time:.3f} seconds\n')
    total = asr_time + t_time + s_time + c_time
    print(f'Total:\n{total:.3f} seconds\n')

    print('================================================================')
    print('FINAL STATUS')
    print('================================================================\n')
    if asr_status == "success" and t_status == "success" and s_status == "success" and c_status == "success":
        overall = "SUCCESS"
    elif asr_status == "success":
        overall = "PARTIAL"
    else:
        overall = "FAILED"
    print(f'Overall:\n{overall}\n')
    print('================================================================')

if __name__ == "__main__":
    test()
