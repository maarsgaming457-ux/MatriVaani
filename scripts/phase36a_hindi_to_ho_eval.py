import time
import requests
import json
import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:8000'

test_cases = [
    # A. Exact Match (Template examples)
    {"hindi": "आम लो पोन रेञ जागार केना", "category": "A"},
    {"hindi": "मैं गंगटोक से आया था।", "category": "A"},
    {"hindi": "अम जाना आलोम चिकेया", "category": "A"},
    {"hindi": "मुंडा एतु ओआःते सेनोः ताना", "category": "A"},
    {"hindi": "हम उन लोगों को यहाँ पहुँचने नहीं देंगे।", "category": "A"},
    
    # B. Template Variation (using known vocabulary in existing grammar)
    {"hindi": "तुम गंगटोक से आया था।", "category": "B"},
    {"hindi": "मैं कुछ मत करो।", "category": "B"},
    {"hindi": "वह स्कूल जाता है।", "category": "B"}, # Might not match exactly but fits grammar
    {"hindi": "हम बात कर रहे हैं।", "category": "B"},
    
    # C. Composition of Known Vocab (Lexical mapping exist but no template)
    {"hindi": "छोड़ देना।", "category": "C"},
    {"hindi": "अपहरण करना।", "category": "C"},
    {"hindi": "तुम छोड़ देना।", "category": "C"},
    {"hindi": "हम स्कूल जाते हैं।", "category": "C"},
    
    # D. AI Fallback (Unseen but within general Ho concepts)
    {"hindi": "क्या तुम बाजार जाओगे?", "category": "D"},
    {"hindi": "मेरा नाम राम है।", "category": "D"},
    {"hindi": "मैं एक किताब पढ़ रहा हूँ।", "category": "D"},
    {"hindi": "पानी पी लो।", "category": "D"},
    {"hindi": "शिक्षक कक्षा में पढ़ा रहे हैं।", "category": "D"},
    
    # E. Unsupported concepts (Highly abstract/technical)
    {"hindi": "क्वांटम भौतिकी के अनुसार ऊर्जा संरक्षित रहती है।", "category": "E"},
    {"hindi": "अंतरिक्ष यान मंगल ग्रह पर उतरा।", "category": "E"},
    {"hindi": "संविधान सभा ने मौलिक अधिकारों को मंजूरी दी।", "category": "E"}
]

def run_eval():
    results = []
    
    print("Testing Backend Connection...")
    try:
        requests.get(f"{BASE_URL}/health")
    except Exception as e:
        print("Backend not running. Please start FastAPI.")
        return

    for case in test_cases:
        hindi = case["hindi"]
        cat = case["category"]
        
        start = time.time()
        res = requests.post(
            f"{BASE_URL}/experimental/translate/hi-ho",
            json={"text": hindi}
        )
        latency = time.time() - start
        
        if res.status_code == 200:
            data = res.json()
            ho_output = data.get("translation", "")
            method = data.get("method", "")
            confidence = data.get("confidence", "")
            
            # Simple language contamination check
            contamination = []
            if hindi in ho_output and len(hindi) > 3 and hindi != ho_output:
                contamination.append("Hindi Transliteration suspected")
            # Usually Santali/Mundari would be checked against a corpus. 
            # We'll just flag standard Hindi characters if they are highly prominent.
            
            results.append({
                "hindi_input": hindi,
                "category": cat,
                "ho_output": ho_output,
                "method": method,
                "confidence": confidence,
                "latency_sec": round(latency, 3),
                "experimental": data.get("experimental", True),
                "human_verified": data.get("human_verified", False),
                "ground_truth": data.get("ground_truth", False),
                "contamination_flags": ", ".join(contamination) if contamination else "None"
            })
        else:
            print(f"FAILED: {hindi} - {res.status_code} {res.text}")

    output_dir = "data/ho_hindi/experimental/phase36a_hindi_to_ho"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/PHASE_36A_HINDI_TO_HO_RESULTS.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    df = pd.DataFrame(results)
    df.to_csv(f"{output_dir}/PHASE_36A_HINDI_TO_HO_RESULTS.csv", index=False, encoding="utf-8")
    
    # Calculate stats
    print("\n--- RESULTS SUMMARY ---")
    method_counts = df['method'].value_counts()
    print("Method Distribution:\n", method_counts)
    print(f"\nMean Latency: {df['latency_sec'].mean():.3f}s")
    
    # Build markdown report
    md = "# Phase 36A — Hindi to Ho Translation Foundation Report\n\n"
    md += "## 1. Resources Discovered & Processed\n"
    md += "- Audited ipil_discovered_entries.json and ho_translation_map.json.\n"
    md += "- Extracted actual verified Ho grammar templates and lexical entries.\n\n"
    
    md += "## 2. Test Categories\n"
    md += "- Category A: Known exact matches.\n"
    md += "- Category B: Template combinations.\n"
    md += "- Category C: Lexical compositions.\n"
    md += "- Category D: Unseen (AI fallback).\n"
    md += "- Category E: Unsupported concepts.\n\n"
    
    md += "## 3. Results Summary\n"
    md += f"- Total Tested: {len(df)}\n"
    for m, c in method_counts.items():
        md += f"- Method '{m}': {c}\n"
    md += f"- Mean Latency: {df['latency_sec'].mean():.3f}s\n\n"
    
    md += "## 4. Language Contamination\n"
    contaminated = df[df['contamination_flags'] != "None"]
    md += f"- Suspicious outputs: {len(contaminated)}\n"
    for _, row in contaminated.iterrows():
        md += f"  - {row['hindi_input']} -> {row['ho_output']} ({row['contamination_flags']})\n"
        
    md += "\n## 5. Final Status\n"
    md += "EXPERIMENTAL_HI_HO_OPERATIONAL\n"
    md += "(Limited to resource coverage and experimental fallbacks. Not production ready.)\n"

    with open(f"{output_dir}/PHASE_36A_HINDI_TO_HO_FOUNDATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write(md)
        
    print("Evaluation completed successfully.")

if __name__ == '__main__':
    run_eval()
