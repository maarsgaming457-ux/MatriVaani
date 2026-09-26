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
    print("MATRI VAANI — GROQ PROVIDER TEST")
    print("============================================================")

    api_key_configured = "YES" if os.getenv("GROQ_API_KEY") else "NO"
    print(f"\nGROQ_API_KEY configured: {api_key_configured}")
    print(f"\nGroq model:\n{settings.GROQ_MODEL}")

    t_provider = settings.TRANSLATION_PROVIDER
    l_provider = settings.LLM_PROVIDER

    santali_transcript = "ᱠᱷᱚᱫᱮ ᱪᱟᱣᱞᱮ"

    # Translation
    print(f"\nTranslation provider:\n{t_provider}")
    t_status = "FAILED"
    t_time = 0
    translation_output = ""
    if api_key_configured == "YES" and t_provider == "groq":
        try:
            t_service = TranslationService()
            start = time.time()
            translation_output = t_service.translate(santali_transcript, "Santali", "Hindi")
            t_time = time.time() - start
            t_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    elif api_key_configured == "NO":
        print("Error: Missing API Key")
    print(f"Translation status:\n{t_status}")
    print(f"Translation time:\n{t_time:.2f}")
    
    # Scriptwriter
    print(f"\nScriptwriter provider:\n{l_provider}")
    s_status = "FAILED"
    s_time = 0
    scriptwriter_output = {}
    if t_status == "SUCCESS" and l_provider == "groq":
        try:
            l_service = LLMService()
            start = time.time()
            scriptwriter_output = l_service.generate_script(translation_output)
            s_time = time.time() - start
            s_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    print(f"Scriptwriter status:\n{s_status}")
    print(f"Scriptwriter time:\n{s_time:.2f}")

    # Copy Editor
    print(f"\nCopy Editor provider:\n{l_provider}")
    c_status = "FAILED"
    c_time = 0
    copy_editor_output = ""
    # Convert script output to string as expected by copy editor
    script_str = ""
    if scriptwriter_output:
        script_str = f"{scriptwriter_output.get('title', '')}\n\n{scriptwriter_output.get('introduction', '')}\n\n{scriptwriter_output.get('main_content', '')}\n\n{scriptwriter_output.get('conclusion', '')}"
        
    if s_status == "SUCCESS" and l_provider == "groq":
        try:
            start = time.time()
            copy_editor_output = l_service.copy_edit(script_str)
            c_time = time.time() - start
            c_status = "SUCCESS"
        except Exception as e:
            print(f"Error: {e}")
    print(f"Copy Editor status:\n{c_status}")
    print(f"Copy Editor time:\n{c_time:.2f}")

    print("\nData flow:")
    print(f"Translation -> Scriptwriter:\n{'PASS' if t_status == 'SUCCESS' and s_status == 'SUCCESS' else 'FAIL'}")
    print(f"Scriptwriter -> Copy Editor:\n{'PASS' if s_status == 'SUCCESS' and c_status == 'SUCCESS' else 'FAIL'}")

    overall = "FAILED"
    if t_status == "SUCCESS" and s_status == "SUCCESS" and c_status == "SUCCESS":
        overall = "SUCCESS"
    elif t_status == "SUCCESS":
        overall = "PARTIAL"
        
    print(f"\nOverall:\n{overall}")
    print("============================================================")

if __name__ == "__main__":
    run_test()
