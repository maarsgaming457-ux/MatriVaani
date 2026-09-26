import os
import sys
import json
import time
import pandas as pd
from difflib import SequenceMatcher

def levenshtein_ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

# Make sure we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()

from app.services.asr_service import ASRService
from app.services.experimental_ho_translation.translator import experimental_ho_translator

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'ho_hindi', 'experimental', 'phase35a_100_sentence_validation'))
os.makedirs(OUT_DIR, exist_ok=True)

XLSX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'ho_hindi', 'collection', 'work', 'HO_HINDI_TRANSLATION_FORM_WORKING.xlsx'))
AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools', 'ho_annotator', 'audio'))

def get_similarity(s1, s2):
    return levenshtein_ratio(s1.strip(), s2.strip())

def main():
    print("============================================================")
    print("MATRI VAANI — PHASE 35A EVALUATION")
    print("============================================================")

    # 1. VERIFY AUDIO FILES
    if not os.path.exists(XLSX_PATH):
        print(f"ERROR: Cannot find {XLSX_PATH}")
        sys.exit(1)
        
    df = pd.read_excel(XLSX_PATH)
    total_expected = 100
    if len(df) != total_expected:
        print(f"ERROR: Expected 100 records, found {len(df)}")
        sys.exit(1)
        
    valid_audio_count = 0
    for idx, row in df.iterrows():
        audio_path = os.path.join(AUDIO_DIR, str(row["Audio Filename"]))
        if os.path.exists(audio_path):
            valid_audio_count += 1
            
    print(f"DATASET\\nExpected: {total_expected}\\nFound: {len(df)}\\nValid: {valid_audio_count}")
    
    if valid_audio_count != total_expected:
        print("ERROR: Not all 100 audio files were found. Stopping.")
        sys.exit(1)

    # 2. INIT SERVICES
    print("\\nInitializing ASR & Translator...")
    asr_service = ASRService()
    asr_service._load_model("ho")  # Force load Ho ASR explicitly

    results = []
    
    asr_latencies = []
    trans_latencies = []
    total_latencies = []
    
    asr_stats = {"non_empty": 0, "exact": 0, "partial": 0, "failure": 0}
    ref_stats = {"exact": 0, "grammar": 0, "similarity": 0, "ai": 0, "fallback": 0, "failure": 0}
    audio_stats = {"success": 0, "failure": 0}
    
    ai_fallback_ids = []
    controlled_fallback_ids = []
    
    suspicious_cases = []
    ho2_details = {}

    print("Running 100-sentence evaluation...")

    for idx, row in df.iterrows():
        r_id = str(row["ID"])
        audio_file = str(row["Audio Filename"])
        ref_ho = str(row["Verified Ho Transcript"])
        
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        
        # --- A. Reference Ho -> Translator ---
        try:
            t0 = time.time()
            ref_trans = experimental_ho_translator.translate(ref_ho)
            ref_lat = time.time() - t0
            
            t_tier = ref_trans["method"]
            if t_tier == "resource_supported_exact_retrieval": ref_stats["exact"] += 1
            elif t_tier == "grammar_rule": ref_stats["grammar"] += 1
            elif t_tier == "similarity_retrieval": ref_stats["similarity"] += 1
            elif t_tier == "resource_assisted_ai": 
                ref_stats["ai"] += 1
                ai_fallback_ids.append(r_id)
            else: 
                ref_stats["fallback"] += 1
                controlled_fallback_ids.append(r_id)
        except Exception as e:
            ref_stats["failure"] += 1
            ref_trans = {"translation": "ERROR", "method": "error", "confidence": "NONE", "error": str(e)}
            ref_lat = 0
            
        # --- B. Real Audio -> ASR -> Translator ---
        try:
            t0_asr = time.time()
            asr_res = asr_service.transcribe(audio_path, language="ho")
            lat_asr = time.time() - t0_asr
            
            asr_ho = asr_res.get("transcript", "")
            if not asr_ho:
                asr_stats["failure"] += 1
                is_nonempty = False
                is_exact = False
                sim = 0.0
            else:
                asr_stats["non_empty"] += 1
                is_nonempty = True
                sim = get_similarity(ref_ho, asr_ho)
                if asr_ho.strip() == ref_ho.strip():
                    asr_stats["exact"] += 1
                    is_exact = True
                else:
                    asr_stats["partial"] += 1
                    is_exact = False
                    
            t0_trans = time.time()
            audio_trans = experimental_ho_translator.translate(asr_ho) if asr_ho else {"translation": "", "method": "none", "confidence": "NONE"}
            lat_trans = time.time() - t0_trans
            
            audio_stats["success"] += 1
            lat_total = lat_asr + lat_trans
            
            asr_latencies.append(lat_asr)
            trans_latencies.append(lat_trans)
            total_latencies.append(lat_total)
            
            error_msg = ""
            
            if sim < 0.8 and is_nonempty:
                suspicious_cases.append(r_id)
                
        except Exception as e:
            audio_stats["failure"] += 1
            asr_ho = ""
            is_nonempty = False
            is_exact = False
            sim = 0.0
            audio_trans = {"translation": "ERROR", "method": "error", "confidence": "NONE"}
            lat_asr = lat_trans = lat_total = 0
            error_msg = str(e)
            
        res_entry = {
            "id": r_id,
            "audio_filename": audio_file,
            "reference_ho": ref_ho,
            "asr_ho": asr_ho,
            "asr_nonempty": is_nonempty,
            "asr_exact_match": is_exact,
            "asr_similarity": round(sim, 4),
            "hindi_translation": audio_trans.get("translation", ""),
            "translation_tier": audio_trans.get("method", ""),
            "confidence": audio_trans.get("confidence", ""),
            "asr_latency_seconds": round(lat_asr, 3),
            "translation_latency_seconds": round(lat_trans, 3),
            "total_latency_seconds": round(lat_total, 3),
            "experimental": audio_trans.get("experimental", True),
            "human_verified": audio_trans.get("human_verified", False),
            "ground_truth": audio_trans.get("ground_truth", False),
            "disclaimer": audio_trans.get("disclaimer", ""),
            "error": error_msg,
            "notes": ""
        }
        
        results.append(res_entry)
        
        if "ho2.wav" in audio_file.lower():
            ho2_details = res_entry

    df_res = pd.DataFrame(results)
    
    # Save files
    df_res.to_csv(os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_RESULTS.csv"), index=False)
    with open(os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_RESULTS.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    # Latency Math
    def get_stats(arr):
        if not arr: return 0,0,0,0
        return min(arr), max(arr), sum(arr)/len(arr), sorted(arr)[len(arr)//2]
        
    asr_min, asr_max, asr_mean, asr_med = get_stats(asr_latencies)
    tr_min, tr_max, tr_mean, tr_med = get_stats(trans_latencies)
    tot_min, tot_max, tot_mean, tot_med = get_stats(total_latencies)
    
    # Parse test suite for cat_a and cat_b dynamically
    with open(os.path.join(os.path.dirname(__file__), '..', 'phase34_cats.json'), 'r', encoding='utf-8') as f:
        cats = json.load(f)
        
    cat_a = cats['cat_a']
    cat_b = cats['cat_b']
    
    known_success = 0
    for item in cat_a:
        if experimental_ho_translator.translate(item["input"])["method"] == "resource_supported_exact_retrieval":
            known_success += 1
            
    grammar_success = 0
    for item in cat_b:
        method = experimental_ho_translator.translate(item["input"])["method"]
        if method == "grammar_rule" or method == "grammar_rule_transformation":
            grammar_success += 1
            
    # Regression
    print("\\nRunning Phase 34 Regression...")
    try:
        import subprocess
        test_suite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_phase34_structured_suite.py'))
        result = subprocess.run([sys.executable, test_suite_path], capture_output=True, text=True)
        regression_pass = "PASS" if result.returncode == 0 else "FAIL"
    except Exception as e:
        regression_pass = "FAIL (Error)"

    # Markdown Report
    report = f'''# Phase 35A — Full 100-Sentence Ho Evaluation

## 1. Dataset
Expected: 100
Found: 100
Valid: 100

## 2. Ho ASR
Non-empty: {asr_stats['non_empty']}/100
Exact match: {asr_stats['exact']}/100
Partial/similar: {asr_stats['partial']}/100
Failure: {asr_stats['failure']}/100

## 3. Reference Ho -> Hindi
Exact retrieval: {ref_stats['exact']}/100
Grammar transformation: {ref_stats['grammar']}/100
Similarity retrieval: {ref_stats['similarity']}/100
Resource-assisted AI: {ref_stats['ai']}/100
Controlled fallback: {ref_stats['fallback']}/100
Failure: {ref_stats['failure']}/100

## 4. Real Audio -> ASR -> Hindi
Successful: {audio_stats['success']}/100
Failed: {audio_stats['failure']}/100

## 5. Known Sentences
{known_success}/5 exact retrieval

## 6. Grammar Variants
{grammar_success}/5 successful

## 7. Latency
ASR:
min: {asr_min:.3f}s
mean: {asr_mean:.3f}s
median: {asr_med:.3f}s
max: {asr_max:.3f}s

Translation:
min: {tr_min:.3f}s
mean: {tr_mean:.3f}s
median: {tr_med:.3f}s
max: {tr_max:.3f}s

Total:
min: {tot_min:.3f}s
mean: {tot_mean:.3f}s
median: {tot_med:.3f}s
max: {tot_max:.3f}s

## 8. AI Fallback
Count: {len(ai_fallback_ids)}

IDs:
{json.dumps(ai_fallback_ids, indent=2)}

## 9. Controlled Fallback
Count: {len(controlled_fallback_ids)}

IDs:
{json.dumps(controlled_fallback_ids, indent=2)}

## 10. Important/Suspicious Cases
IDs with ASR similarity < 0.8: 
{json.dumps(suspicious_cases, indent=2)}

## 11. ho2.wav
Reference Ho: {ho2_details.get('reference_ho')}
Actual ASR: {ho2_details.get('asr_ho')}
Hindi: {ho2_details.get('hindi_translation')}
Translation tier: {ho2_details.get('translation_tier')}
Confidence: {ho2_details.get('confidence')}
ASR latency: {ho2_details.get('asr_latency_seconds')}
Translation latency: {ho2_details.get('translation_latency_seconds')}

## 12. Full 100-Sentence Results
Available in PHASE_35A_HO_100_SENTENCE_RESULTS.csv.
'''
    with open(os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_REPORT.md"), "w", encoding="utf-8") as f:
        f.write(report)
        
    print("\\n============================================================")
    print("MATRI VAANI — PHASE 35A")
    print("FULL 100 HO SENTENCE EVALUATION")
    print("============================================================")
    print(f"\\nDATASET\\nExpected: 100\\nFound: 100\\nValid: 100")
    print(f"\\nHO ASR\\nNon-empty: {asr_stats['non_empty']}/100\\nExact match: {asr_stats['exact']}/100\\nPartial/similar: {asr_stats['partial']}/100\\nFailure: {asr_stats['failure']}/100")
    print(f"\\nREFERENCE -> HINDI\\nExact retrieval: {ref_stats['exact']}/100\\nGrammar transformation: {ref_stats['grammar']}/100\\nSimilarity retrieval: {ref_stats['similarity']}/100\\nAI fallback: {ref_stats['ai']}/100\\nControlled fallback: {ref_stats['fallback']}/100\\nFailure: {ref_stats['failure']}/100")
    print(f"\\nREAL AUDIO -> ASR -> HINDI\\nSuccess: {audio_stats['success']}/100\\nFailure: {audio_stats['failure']}/100")
    print(f"\\nKNOWN SENTENCES\\n{known_success}/5 exact retrieval")
    print(f"\\nGRAMMAR VARIANTS\\n{grammar_success}/5")
    print(f"\\nLATENCY\\nASR mean: {asr_mean:.3f} sec\\nTranslation mean: {tr_mean:.3f} sec\\nTotal mean: {tot_mean:.3f} sec")
    print(f"\\nPHASE 34 REGRESSION\\n{regression_pass}")
    print("\\nPRODUCTION MODIFIED:\\nNO")
    print("============================================================")
    print("\\nOUTPUT FILES:")
    print("1.", os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_RESULTS.json"))
    print("2.", os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_RESULTS.csv"))
    print("3.", os.path.join(OUT_DIR, "PHASE_35A_HO_100_SENTENCE_REPORT.md"))

if __name__ == "__main__":
    main()
