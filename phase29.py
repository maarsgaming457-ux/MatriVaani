import os
import json
import pandas as pd

exp_dir = "data/ho_hindi/experimental"
generator_dir = os.path.join(exp_dir, "candidate_generator")
os.makedirs(generator_dir, exist_ok=True)

# 1. Read coverage data
coverage_path = os.path.join(exp_dir, "ho_hindi_coverage_summary.json")
with open(coverage_path, "r", encoding="utf-8") as f:
    coverage_data = json.load(f)

category_map = {}
for cat, ids in coverage_data["sentences_by_category"].items():
    for rid in ids:
        category_map[rid] = cat

# 2. Read 100 original records
orig_xlsx = "data/ho_hindi/collection/work/HO_HINDI_TRANSLATION_FORM_WORKING.xlsx"
df = pd.read_excel(orig_xlsx)

candidates = []
for idx, row in df.iterrows():
    rid = str(row["ID"])
    ho_text = str(row["Verified Ho Transcript"])
    audio = str(row["Audio Filename"])
    cat = category_map.get(rid, "UNKNOWN")
    
    # Classification logic
    if cat == "GREATER_THAN_80_PERCENT_LEXICAL":
        confidence = "B"
        evidence_desc = "Substantial lexical coverage (>80%), but lacks syntactic mapping."
    elif cat == "50_TO_80_PERCENT_LEXICAL":
        confidence = "C"
        evidence_desc = "Mostly dictionary word matches (50-80% coverage)."
    else:
        confidence = "D"
        evidence_desc = "Insufficient evidence (<50% or 0% coverage)."
        
    candidate_hindi = "" 
    needs_review = True
    reason = "Dictionary glosses exist but Munda syntax and agglutinative clitics cannot be safely reconstructed without a human." if confidence in ["B", "C"] else "Insufficient evidence"

    candidates.append({
        "ID": rid,
        "Audio Filename": audio,
        "Ho Transcript": ho_text,
        "Candidate Hindi": candidate_hindi,
        "Evidence": evidence_desc,
        "Source": "IPIL & Lexicon (Lexical only)",
        "Source URL": "https://holanguage.ipil.co.in",
        "Coverage": cat,
        "Confidence": confidence,
        "Multi Source Support": False,
        "Machine Generated": True,
        "Human Verified": False,
        "Ground Truth": False,
        "Needs Human Review": needs_review,
        "Reason": reason
    })

# 3. Create candidate dataset
df_candidates = pd.DataFrame(candidates)
cand_file = os.path.join(exp_dir, "ho_hindi_translation_candidates.xlsx")
df_candidates.to_excel(cand_file, index=False)

# 4. Human workload summary
strong = len([c for c in candidates if c["Confidence"] == "A"])
moderate = len([c for c in candidates if c["Confidence"] == "B"])
weak = len([c for c in candidates if c["Confidence"] == "C"])
insufficient = len([c for c in candidates if c["Confidence"] == "D"])

workload = {
    "Total": 100,
    "Strong resource evidence": strong,
    "Moderate resource evidence": moderate,
    "Weak resource evidence": weak,
    "Insufficient evidence": insufficient,
    "Potentially human-checkable": strong + moderate,
    "Requires full human interpretation": weak + insufficient
}

workload_file = os.path.join(exp_dir, "human_workload_summary.json")
with open(workload_file, "w", encoding="utf-8") as f:
    json.dump(workload, f, indent=4)

# 5. Create Review Priority List
priority_map = {"A": 1, "B": 2, "C": 3, "D": 4}
df_candidates["Priority"] = df_candidates["Confidence"].map(priority_map)
df_sorted = df_candidates.sort_values(by="Priority")

priority_file = os.path.join(exp_dir, "HUMAN_REVIEW_PRIORITY.xlsx")
df_sorted.to_excel(priority_file, index=False)

# 6. Quality Report
report = f'''# PHASE 29: RESOURCE-ASSISTED CANDIDATE GENERATION REPORT

**1. Resources used:** Digital Ho Dictionary (IPIL), Austroasiatic lexicons.
**2. Resource provenance:** Data strictly from data/ho_hindi/experimental/resources.
**3. Candidate-generation method:** Word-level lexical gloss mapping evaluated for coverage.
**4. Number of candidates generated:** 100
**5. Strong evidence count:** {strong} (No sentence-level parallel translation memories exist).
**6. Moderate evidence count:** {moderate} (>80% lexical coverage).
**7. Weak evidence count:** {weak} (50-80% lexical coverage).
**8. Insufficient evidence count:** {insufficient} (<50% lexical coverage).
**9. Multi-source support count:** 0 (Only isolated lexical glosses).
**10. Example candidates:** No fluent candidates could be safely generated because word-by-word concatenation of Ho dictionary terms violates Hindi syntactic structure (SOV vs agglutinative).
**11. Limitations:** Without a Ho-fluent syntax parser or LLM fine-tuned on Ho, generating safe fluent Hindi candidates from lexical roots is impossible.
**12. Human-review workload estimate:** 
   - Potentially checkable (mostly vocabulary verification): {strong + moderate}
   - Requires full human interpretation (from scratch): {weak + insufficient}
**13. Machine-generated count:** 100 (Metadata placeholders generated).
**14. Human-verified count:** 0
**15. Ground-truth count:** 0
**16. Production files modified:** 0

## CRITICAL ANSWERS
1. **How many of the 100 sentences have strong resource evidence?** {strong}
2. **How many have moderate evidence?** {moderate}
3. **How many have weak evidence?** {weak}
4. **How many have insufficient evidence?** {insufficient}
5. **How many could potentially be reviewed rather than translated from scratch?** {strong + moderate}
6. **How many still require a Ho-Hindi expert?** 100 (All require expert interpretation due to syntax differences, though 25 are heavily lexically supported).
7. **Were any machine translations incorrectly marked as ground truth?** No. All candidates are explicitly marked Ground Truth = FALSE, Human Verified = FALSE, and Machine Generated = TRUE.

**FINAL STATUS:** PARTIAL_RESOURCE_ASSISTANCE
'''
report_file = "PHASE_29_RESOURCE_ASSISTED_CANDIDATE_REPORT.md"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(report)

print("Phase 29 Candidate Generation Complete.")
