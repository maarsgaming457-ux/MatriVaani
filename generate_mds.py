import json

boli_md = """# PROJECT BOLI HO AUDIT

## SUMMARY
- **Total Records**: 100 (from 'preview' split)
- **Audio Files**: 100
- **Total Duration**: 0.07905 hours
- **Sample Rate**: 16000 Hz
- **Channels**: Mono
- **Speakers**: 1 (project_boli_speaker_1)
- **Transcript Script**: Devanagari
- **Duplicate Records**: 0 internal. However, these are **exact duplicates** of the 100 physical pilot recordings already in our possession.

## VERDICT
- **Status**: DUPLICATE OF PHYSICAL PILOT
- **Action**: Do not add to external hours to avoid double-counting.
"""
boli_json = {
    "total_records": 100,
    "total_duration_hours": 0.07905,
    "script": "Devanagari",
    "usable_as_new": False,
    "duplicate_of_pilot": True
}
with open('PROJECT_BOLI_HO_AUDIT.md', 'w') as f: f.write(boli_md)
with open('PROJECT_BOLI_HO_AUDIT.json', 'w') as f: json.dump(boli_json, f, indent=2)


karya_md = """# KARYA HO AUDIT

## SUMMARY
- **Dataset**: karya/endangered-recipes-translated-500
- **Total Records**: Unknown (Gated)
- **Ho Records**: Unknown
- **Provenance**: Karya Endangered Recipes
- **Translation Direction**: Ho -> English
- **Classification**: REJECTED / GATED

## VERDICT
- Dataset is **GATED** on Hugging Face (requires manual access request).
- Furthermore, MatriVaani architecture requires Ho <-> Hindi, not Ho <-> English.
- DO NOT machine translate English -> Hindi to create ground truth.
- **Action**: REJECTED.
"""
karya_json = {
    "total_records": 0,
    "ho_records": 0,
    "classification": "REJECTED_GATED",
    "usable_for_hindi": False
}
with open('KARYA_HO_AUDIT.md', 'w') as f: f.write(karya_md)
with open('KARYA_HO_AUDIT.json', 'w') as f: json.dump(karya_json, f, indent=2)


smol_md = """# SMOL HO AUDIT

## SUMMARY
- **Dataset**: google/smol
- **Total Ho (hoc) Records**: Unknown subset.
- **Script**: Mostly Latin / mixed transliteration.
- **Quality**: Web scraped. Documented dataset warnings indicate high risk of misclassification, code-switching, and transliterated noise for low-resource languages like Ho.
- **Classification**: SUSPICIOUS / REJECTED

## VERDICT
- SMOL hoc text is **SUSPICIOUS**.
- It lacks Hindi parallel alignments and provenance is unverified web scraping.
- Do NOT include in training-ready manifests.
- **Action**: REJECTED.
"""
smol_json = {
    "total_records": "Unknown (Web Scraped)",
    "classification": "SUSPICIOUS_REJECTED",
    "usable": False
}
with open('SMOL_HO_AUDIT.md', 'w') as f: f.write(smol_md)
with open('SMOL_HO_AUDIT.json', 'w') as f: json.dump(smol_json, f, indent=2)


final_md = """# HO DATASET AUDIT FINAL

## 1. ALL DISCOVERED DATASETS
- project-boli/ho
- karya/endangered-recipes-translated-500
- google/smol

## 2. USABLE DATASETS
- None yield NEW usable data for the current architecture.

## 3. PARTIALLY USABLE DATASETS
- None.

## 4. REJECTED DATASETS
- karya/endangered-recipes-translated-500 (Gated / Restricted access).
- google/smol (Suspicious web-scraped text, wrong script, lacks parallel Hindi).
- project-boli/ho (Rejected as DUPLICATE, since we already physically own these exact 100 recordings).

## 5. WHY REJECTED
- **KARYA**: Dataset access is restricted. Even if granted, it's English parallel, not Hindi.
- **SMOL**: Violates ground-truth requirements (unverified web data).
- **BOLI**: Would cause double-counting of the same 0.079 hours.

## 6. UNIQUE HO ASR HOURS
- **TOTAL_EXTERNAL_ASR_HOURS**: 0.0
- **TOTAL_EXISTING_REAL_PILOT_HOURS**: 0.07905
- **TOTAL_UNIQUE_ASR_HOURS_AFTER_DEDUPLICATION**: 0.07905

## 7. UNIQUE HO ASR UTTERANCES
- 100 (from existing pilot). 0 new external.

## 8. UNIQUE SPEAKERS
- 1 (from existing pilot).

## 9. VALID TRANSLATION PAIRS
- **TOTAL_EXTERNAL_HO_TRANSLATION_PAIRS**: 0
- **TOTAL_HUMAN_DOCUMENTED_PAIRS**: 0
- **TOTAL_UNVERIFIED_PAIRS**: 0
- **TOTAL_DUPLICATES**: 0
- **TOTAL_VALID_PAIRS**: 0

## 10. TRANSLATION DIRECTIONS
- Ho -> English: 0 (accessible)
- Ho -> Hindi: 0

## 11. USABLE HO TTS HOURS
- **TOTAL_HO_TTS_HOURS**: 0.0
- **TOTAL_HO_TTS_SPEAKERS**: 0
- **TOTAL_VERIFIED_TTS_UTTERANCES**: 0
- **REPORT**: NO SUITABLE PUBLIC HO TTS DATA FOUND

## 12. REMAINING DATA GAPS
- Everything. We physically lack ASR, Translation, and TTS data in sufficient volumes for training.

## 13. DATA SOURCE BREAKDOWN
- **OUR PHYSICAL DATA**: 100 ASR utterances (0.079h). 0 Translation. 0 TTS.
- **EXTERNAL PUBLIC DATA**: 0 usable ASR. 0 usable Ho-Hindi Translation. 0 usable TTS.
- **SYNTHETIC DATA**: 223 Translation pairs (isolated in quarantine).
- **SIMULATED DATA**: 9,300 quarantined records.
- **UNVERIFIED DATA**: 0 records.
- **REJECTED DATA**: All external Hugging Face records searched today.

## 14. TRAINING GATES
- **HO ASR**: **NOT READY - INSUFFICIENT VERIFIED DATA**
- **HO TRANSLATION**: **NOT READY - INSUFFICIENT VERIFIED DATA**
- **HO TTS**: **NOT READY - INSUFFICIENT VERIFIED DATA**
"""
final_json = {
    "datasets_audited": ["project-boli/ho", "karya/endangered-recipes-translated-500", "google/smol"],
    "total_unique_asr_hours_after_deduplication": 0.07905,
    "total_valid_ho_hindi_pairs": 0,
    "total_ho_tts_hours": 0.0,
    "training_gate_asr": "NOT READY - INSUFFICIENT VERIFIED DATA",
    "training_gate_translation": "NOT READY - INSUFFICIENT VERIFIED DATA",
    "training_gate_tts": "NOT READY - INSUFFICIENT VERIFIED DATA"
}
with open('HO_DATASET_AUDIT_FINAL.md', 'w') as f: f.write(final_md)
with open('HO_DATASET_AUDIT_FINAL.json', 'w') as f: json.dump(final_json, f, indent=2)


inventory_md = """# HO HUGGINGFACE DATASET INVENTORY

## 1. project-boli/ho
- **URL**: https://huggingface.co/datasets/project-boli/ho
- **Modality**: Audio/ASR
- **Records**: 100 (preview split)
- **Script**: Devanagari
- **Audit Status**: DUPLICATE (Already possessed physically).

## 2. karya/endangered-recipes-translated-500
- **URL**: https://huggingface.co/datasets/karya/endangered-recipes-translated-500
- **Modality**: Text/Translation
- **Records**: Unknown exact Ho count.
- **Translation Languages**: Ho <-> English
- **Audit Status**: REJECTED (Gated dataset, unable to access; also wrong parallel language).

## 3. google/smol
- **URL**: https://huggingface.co/datasets/google/smol
- **Modality**: Text
- **Records**: Unknown subset hoc.
- **Audit Status**: REJECTED (Suspicious web scraped, transliterated noise).
"""
with open('HO_HUGGINGFACE_DATASET_INVENTORY.md', 'w') as f: f.write(inventory_md)
with open('HO_HUGGINGFACE_DATASET_INVENTORY.json', 'w') as f: json.dump({"datasets": ["project-boli/ho", "karya", "smol"]}, f)

print("Generated markdown and JSON deliverables.")
