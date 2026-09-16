import os
import sys
import time

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.services.translation_service import TranslationService
from app.services.llm_service import LLMService

def run_test():
    print("============================================================")
    print("MATRI VAANI — REAL OPENAI PROVIDER TEST")
    print("============================================================")

    api_key_configured = "YES" if os.getenv("OPENAI_API_KEY") else "NO"
    print(f"\nOPENAI API configured:\n{api_key_configured}")

    t_provider = settings.TRANSLATION_PROVIDER
    l_provider = settings.LLM_PROVIDER

    santali_transcript = "ᱠᱷᱚᱫᱮ ᱪᱟᱣᱞᱮ"

    # Translation
    print(f"\nTranslation:\nProvider: {t_provider}")
    t_status = "FAILED"
    t_time = 0
    translation_output = ""
    if api_key_configured == "YES" and t_provider == "openai":
        try:
            t_service = TranslationService()
            start = time.time()
            translation_output = t_service.translate(santali_transcript, "Santali", "Hindi")
            t_time = time.time() - start
            t_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    print(f"Status: {t_status}")
    print(f"Time: {t_time:.2f}s")
    
    # Scriptwriter
    print(f"\nScriptwriter:\nProvider: {l_provider}")
    s_status = "FAILED"
    s_time = 0
    scriptwriter_output = {}
    if t_status == "SUCCESS" and l_provider == "openai":
        try:
            l_service = LLMService()
            start = time.time()
            scriptwriter_output = l_service.generate_script(translation_output)
            s_time = time.time() - start
            s_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    print(f"Status: {s_status}")
    print(f"Time: {s_time:.2f}s")

    # Copy Editor
    print(f"\nCopy Editor:\nProvider: {l_provider}")
    c_status = "FAILED"
    c_time = 0
    copy_editor_output = ""
    # Convert script output to string as expected by copy editor
    script_str = ""
    if scriptwriter_output:
        script_str = f"{scriptwriter_output.get('title', '')}\n\n{scriptwriter_output.get('introduction', '')}\n\n{scriptwriter_output.get('main_content', '')}\n\n{scriptwriter_output.get('conclusion', '')}"
        
    if s_status == "SUCCESS" and l_provider == "openai":
        try:
            start = time.time()
            copy_editor_output = l_service.copy_edit(script_str)
            c_time = time.time() - start
            c_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    print(f"Status: {c_status}")
    print(f"Time: {c_time:.2f}s")

    print("\nData flow:")
    print(f"Translation -> Scriptwriter: {'PASS' if t_status == 'SUCCESS' and s_status == 'SUCCESS' else 'FAIL'}")
    print(f"Scriptwriter -> Copy Editor: {'PASS' if s_status == 'SUCCESS' and c_status == 'SUCCESS' else 'FAIL'}")

    overall = "FAILED"
    if t_status == "SUCCESS" and s_status == "SUCCESS" and c_status == "SUCCESS":
        overall = "SUCCESS"
    elif t_status == "SUCCESS":
        overall = "PARTIAL"
        
    print(f"\nOverall:\n{overall}")
    print("============================================================")

if __name__ == "__main__":
    run_test()
