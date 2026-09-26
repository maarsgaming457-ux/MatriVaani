# PHASE 21 HO ↔ HINDI HUMAN-VERIFIED DATASET CREATION PIPELINE

## 1. Dataset Location
The human-verification dataset workspace was established at data/ho_hindi/ with subdirectories aw/, nnotations/, erified/, splits/, and provenance/. The 100 Ho records from project-boli/ho were preserved safely in aw/ho_asr_recovery_manifest_100.jsonl.

## 2. Number of Ho Records
100 genuine Ho speech/transcript records exist in the database.

## 3. Number Verified
0 pairs are verified.

## 4. Number Pending
100 records are pending verification.

## 5. Annotation Schema
The schema requires capturing both the machine-generated raw ASR and the human-corrected data:
- id
- udio_id
- udio_filename
- ho_raw (Raw ASR)
- ho_corrected (Human Corrected Ho)
- hindi (Human Hindi Translation)
- source
- human_verified (Boolean)
- 	ranslator_id (Identifier)
- erification_notes
- license

## 6. UI Workflow
The local UI at 	ools/ho_annotator was modified to present the audio player alongside the read-only Raw Ho ASR. The annotator listens to the audio and corrects the Ho transcription, inputs the manual Hindi translation, and records their Translator ID. A prominent warning displays the requirement that no machine translation can be used and that a qualified Ho-speaker must complete the task.

## 7. Validation Rules
The UI and Backend (pp.py) reject verification if:
- Corrected Ho is empty.
- Hindi translation is empty.
- Translator/Reviewer ID is empty.
Only when all conditions are met and the Human Verified checkbox is ticked can the record attain human_verified = true and eview_status = APPROVED.

## 8. Export Format
Verified records are exported via the UI directly to data/ho_hindi/verified/ho_hindi_verified.jsonl matching the required format:
`json
{
  "id": "...",
  "ho": "...",
  "hindi": "...",
  "source": "...",
  "license": "...",
  "human_verified": true
}
`

## 9. Quality-Control Method
Dual-review is supported through the 	ranslator_id and eviewer_id fields, with a single_reviewer = true fallback note to distinguish solo-annotated data from independently reviewed data. The eview_status tracks progress.

## 10. Training Readiness
	ools/check_ho_hindi_dataset.py was created to evaluate dataset quality (empties, duplicates). It currently reports NOT_READY_FOR_TRAINING. It strictly prevents training until at least 50 non-duplicate verified pairs are obtained.

## 11. TTS Findings
A separate TTS workspace was established at 	ools/ho_tts/. acebook/mms-tts-hoc requires a deterministic Ho Devanagari → Odia script converter. This bridge does not perform translation, merely transliteration. Due to phonetic complexities, this bridge REQUIRES_VALIDATION by a native speaker before use.

## 12. Production Files Protected
Absolutely no production files (	ranslation_service.py, sr_service.py, 	ts_service.py, Flutter) or machine-learning models (IndicTrans2, ho_asr) were touched. All logic was confined to the annotation tooling.

## 13. Exact Next Action
Launch the Ho Annotator UI (python tools/ho_annotator/app.py), onboard a qualified Ho-Hindi bilingual annotator, and annotate the 100 Ho records.

---

CURRENT STATUS:

Ho ASR: AVAILABLE
Ho-Hindi Translation: WAITING FOR HUMAN-VERIFIED DATA
Hindi-Ho Translation: WAITING FOR HUMAN-VERIFIED DATA
Ho TTS: EXPERIMENTALLY AVAILABLE
Ho TTS Script Bridge: REQUIRES VALIDATION
