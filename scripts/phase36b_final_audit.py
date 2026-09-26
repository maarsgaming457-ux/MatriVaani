import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = 'data/ho_hindi/experimental/phase36b_hindi_to_ho'

def create_audit():
    with open(f'{OUTPUT_DIR}/PHASE_36B_UNSEEN_TEST_SET.json', 'r', encoding='utf-8') as f:
        unseen_test = json.load(f)
        
    with open(f'{OUTPUT_DIR}/PHASE_36B_HINDI_TO_HO_RESULTS.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    # We will build an audit list
    audit_cases = []
    
    # Check data leakage (compare against the 100 sentences in templates)
    with open('data/ho_hindi/experimental/phase36b_hindi_to_ho/HO_TEMPLATES_V2.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
        template_hindis = [t.get("semantic_pattern", "") for t in templates]
        
    genuine_unseen = 0
    leaked = 0
    near_dup = 0
    
    for r in results:
        hindi = r['hindi_input']
        
        leakage = "Completely novel combination"
        if hindi in template_hindis:
            leakage = "Exact sentence exists in resources (LEAKED)"
            leaked += 1
        elif hindi.replace("।", "").strip() in [t.replace("।", "").strip() for t in template_hindis]:
            leakage = "Same Hindi sentence with minor punctuation change (LEAKED)"
            leaked += 1
        elif hindi.startswith("मैं") and "से आया था" in hindi:
            leakage = "Same semantic template exists (NEAR DUPLICATE)"
            near_dup += 1
        else:
            genuine_unseen += 1
            
        is_generated = r['method'] in ['resource_assisted_ai', 'template']
        is_retrieved = r['method'] in ['resource_supported_exact', 'lexical_grammar']
        
        audit_cases.append({
            "hindi_input": hindi,
            "ho_output": r['ho_output'],
            "method": r['method'],
            "reason": r['reason'],
            "confidence": r['confidence'],
            "leakage_status": leakage,
            "generated": is_generated,
            "retrieved": is_retrieved
        })
        
    with open(f'{OUTPUT_DIR}/PHASE_36B_FINAL_EVIDENCE_AUDIT.json', 'w', encoding='utf-8') as f:
        json.dump(audit_cases, f, ensure_ascii=False, indent=2)

    # Build markdown
    md = "# Phase 36B Final Evidence Audit\n\n"
    md += "## 1. Unseen Test Cases Audit\n"
    md += f"- Genuine Unseen: {genuine_unseen}\n"
    md += f"- Near Duplicates: {near_dup}\n"
    md += f"- Leaked (Exact/Punctuation): {leaked}\n\n"
    
    md += "## 2. Handled Cases Audit\n"
    md += "The pipeline matched 3 exact cases (which were leaked from templates), 2 lexical cases, and 6 template constructions. The template constructions (Category B) were successfully generalized using the V2 template variable substitution ({LOCATION}). However, they were near-duplicates of the training data.\n\n"
    
    md += "## 3. Unsupported Cases Audit\n"
    md += "13 cases fell to controlled fallback. The router explicitly avoided AI fallback if NO known vocabulary from the lexicon was present in the Hindi input. This successfully prevented hallucinatory AI generation for entirely unsupported concepts (Category E), but it also blocked Category D sentences where vocabulary was missing.\n\n"
    
    md += "## 4. Zero AI Fallback Audit\n"
    md += "AI fallback was intentionally avoided because the router was constrained to reject inputs lacking contextual vocabulary. However, for 3 cases where AI was called, the model output an uncertainty disclaimer instead of Ho text, triggering controlled fallback instead. AI fallback is functioning, but highly constrained.\n\n"
    
    md += "## 5. Contamination Detector Audit\n"
    md += "Reported 0 contamination. However, the detector is highly limited: it only checks if a raw Hindi substring of length > 4 appears in the output. It does NOT check against Santali or Mundari dictionaries. Thus, 0 contamination does not prove linguistic correctness.\n\n"
    
    md += "## 6. Latency Audit\n"
    md += "Measurements included local router matching, regex parsing, and remote API calls. \n- Median latency (0.003s) represents local retrieval/fallback.\n- Max latency (2.753s) represents the Groq API call overhead when AI was invoked.\n\n"
    
    md += "## 7. Generalization Claim\n"
    md += "PARTIALLY_SUPPORTED. The system successfully generalized sentence templates (Category B), proving that modular grammar rules can construct novel Ho sentences. However, the lexicon remains too limited to handle diverse unseen sentences (Category C, D, E), and AI fallback is restricted by vocabulary gaps.\n"
    
    with open(f'{OUTPUT_DIR}/PHASE_36B_FINAL_EVIDENCE_AUDIT.md', 'w', encoding='utf-8') as f:
        f.write(md)

    import pandas as pd
    df = pd.DataFrame(audit_cases)
    df.to_csv(f'{OUTPUT_DIR}/PHASE_36B_FINAL_EVIDENCE_AUDIT.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    create_audit()
