import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
os.environ["TRANSLATION_PROVIDER"] = "indictrans2_local"
sys.path.insert(0, os.path.abspath('.'))

from app.services.translation_service import TranslationService
from app.core.exceptions import TranslationError

def main():
    print("Testing Local IndicTrans2 Service integration...", flush=True)
    ts = TranslationService()
    ts.provider = "indictrans2_local"
    
    sentences = [
        "नमस्ते बच्चों।",
        "आज हम गिनती सीखेंगे।",
        "अपने सामने रखी वस्तुओं को गिनिए।"
    ]
    
    t0 = time.time()
    try:
        res = ts.translate("नमस्ते", "Hindi", "Santali")
        t1 = time.time()
        print(f"Cold Request (Warmup): नमस्ते -> {res} (took {t1-t0:.2f}s)")
    except Exception as e:
        print(f"Cold Request failed: {e}")
        return

    total_warm = 0
    for s in sentences:
        t0 = time.time()
        res = ts.translate(s, "Hindi", "Santali")
        t1 = time.time()
        latency = t1 - t0
        total_warm += latency
        print(f"Warm Request: {s} -> {res} (took {latency:.2f}s)")
        
    print(f"\nAverage warm request: {total_warm / len(sentences):.2f}s")
    
    print("\nTesting Ho Unsupported Behavior:")
    try:
        ts.translate("test", "Ho", "Santali")
        print("FAIL: Expected Ho translation to fail.")
    except TranslationError as e:
        print(f"PASS: Caught expected error for Ho: {e}")

if __name__ == '__main__':
    main()
