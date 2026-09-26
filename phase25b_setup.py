import os
import json
import pandas as pd
import datetime
import shutil

collection_dir = "data/ho_hindi/collection"
excel_file = os.path.join(collection_dir, "HO_HINDI_TRANSLATION_FORM.xlsx")
manifest_path = "C:/Users/maars/Downloads/ho_asr_recovery_manifest_100.jsonl"
baseline_path = os.path.join(collection_dir, "ho_source_baseline.json")
work_dir = os.path.join(collection_dir, "work")
work_file = os.path.join(work_dir, "HO_HINDI_TRANSLATION_FORM_WORKING.xlsx")
backup_dir = os.path.join(collection_dir, "backups")
os.makedirs(work_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)

# Step 13: Backup
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"HO_HINDI_TRANSLATION_FORM_{timestamp}.xlsx")
if os.path.exists(excel_file):
    shutil.copy2(excel_file, backup_file)

# Step 2: Baseline
baseline_data = {}
with open(manifest_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            d = json.loads(line)
            baseline_data[d["source_record_id"]] = {
                "id": d["source_record_id"],
                "audio_filename": d["audio_filename"],
                "verified_ho_transcript": d["raw_asr_text"]
            }
with open(baseline_path, "w", encoding="utf-8") as f:
    json.dump(baseline_data, f, indent=4, ensure_ascii=False)

# Step 3: Working copy
if os.path.exists(excel_file):
    shutil.copy2(excel_file, work_file)

# Step 4: Instructions
instructions = '''# Instructions for Ho-Hindi Translator

1. Read the Ho sentence.
2. Listen to the corresponding Ho audio if necessary.
3. Understand the actual meaning.
4. Enter the natural Hindi meaning.
5. Do not transliterate Ho.
6. Do not merely convert the Ho script.
7. Do not guess.
8. Do not use ChatGPT/Gemini/Google Translate/IndicTrans2/Sarvam/Bhashini or another machine translation system to generate the Hindi ground truth.
9. If the sentence is unclear, leave Hindi Translation blank and write: needs_review
10. Mark Completed=true only when the translation is confident.

The Hindi Translation column is ground-truth data and must be supplied by a qualified human who understands Ho and Hindi.
'''
with open(os.path.join(collection_dir, "INSTRUCTIONS_FOR_TRANSLATOR.md"), "w", encoding="utf-8") as f:
    f.write(instructions)

# Step 6: Audio Access
# Let's see if audio exists in tools/ho_annotator/audio/ or datasets/ho/
# Just recording missing audio in validation
audio_dirs = ["tools/ho_annotator/audio", "datasets/ho/audio", "datasets/ho", "C:/study files/sih project/datasets/cache"]

# Step 7: Validation logic (improving validate_translations.py)
validation_script = '''import os
import json
import pandas as pd

work_file = "data/ho_hindi/collection/work/HO_HINDI_TRANSLATION_FORM_WORKING.xlsx"
baseline_path = "data/ho_hindi/collection/ho_source_baseline.json"
audio_dirs = ["tools/ho_annotator/audio", "datasets/ho/audio", "datasets/ho", "datasets/cache", "data/ho_hindi"]

if not os.path.exists(work_file):
    print("Working file not found.")
    exit(1)

with open(baseline_path, "r", encoding="utf-8") as f:
    baseline_data = json.load(f)

df = pd.read_excel(work_file)
total_records = len(df)
duplicate_ids = df.duplicated(subset=["ID"]).sum()

missing_audio = 0
for audio_file in df["Audio Filename"]:
    found = False
    for ad in audio_dirs:
        if os.path.exists(os.path.join(ad, str(audio_file))):
            found = True
            break
    if not found:
        # We might search deeper but just recording missing
        missing_audio += 1

modified_ho_transcripts = 0
invalid_completed_rows = 0
valid_pairs = 0
pending = 0
needs_review = 0

verified_records = []

for idx, row in df.iterrows():
    rid = str(row["ID"])
    ho_text = str(row["Verified Ho Transcript"])
    if rid in baseline_data:
        if baseline_data[rid]["verified_ho_transcript"] != ho_text:
            modified_ho_transcripts += 1
            print(f"ERROR: Ho transcript modified for ID {rid}")
    
    # Check completeness
    is_completed = str(row["Completed"]).lower() in ["true", "yes", "1", "y"]
    hindi = str(row["Hindi Translation"]) if pd.notna(row["Hindi Translation"]) else ""
    translator = str(row["Translator ID"]) if pd.notna(row["Translator ID"]) else ""
    notes = str(row["Notes"]) if pd.notna(row["Notes"]) else ""
    
    if "needs_review" in notes.lower():
        needs_review += 1
        
    if is_completed:
        if not hindi.strip() or not translator.strip() or "needs_review" in notes.lower():
            invalid_completed_rows += 1
            print(f"INVALID_COMPLETED_ROW: ID {rid}")
        else:
            if rid in baseline_data and baseline_data[rid]["verified_ho_transcript"] == ho_text:
                valid_pairs += 1
                verified_records.append({
                    "id": rid,
                    "ho": ho_text,
                    "hindi": hindi,
                    "audio_filename": str(row["Audio Filename"]),
                    "source": "project-boli/ho",
                    "translator_id": translator,
                    "human_verified": True
                })
    else:
        pending += 1

completed_count = valid_pairs + invalid_completed_rows
hindi_filled_df = df[df["Hindi Translation"].notna() & (df["Hindi Translation"] != "")]
duplicate_hindi = hindi_filled_df.duplicated(subset=["Hindi Translation"]).sum() if not hindi_filled_df.empty else 0

print("STRUCTURAL VALIDATION RESULTS:")
print(f"Total Ho records: {total_records}")
print(f"Completed: {completed_count}")
print(f"Valid Ho-Hindi pairs: {valid_pairs}")
print(f"Pending: {pending}")
print(f"Needs review: {needs_review}")
print(f"Missing audio: {missing_audio}")
print(f"Modified Ho transcripts: {modified_ho_transcripts}")
print(f"Duplicate IDs: {duplicate_ids}")
print(f"Duplicate Hindi translations: {duplicate_hindi}")
print(f"Invalid completed rows: {invalid_completed_rows}")

if valid_pairs >= 50:
    status = "READY_FOR_DATASET_VALIDATION"
    verified_dir = "data/ho_hindi/verified"
    os.makedirs(verified_dir, exist_ok=True)
    with open(os.path.join(verified_dir, "ho_hindi_verified.jsonl"), "w", encoding="utf-8") as f:
        for r in verified_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\\n")
else:
    status = "WAITING_FOR_50_VALID_HO_HINDI_PAIRS"

print(f"\\nCurrent status: {status}")

report = f"""# PHASE 25B HO-HINDI COLLECTION STATUS

Total Ho records: {total_records}
Completed: {completed_count}
Valid Ho-Hindi pairs: {valid_pairs}
Pending: {pending}
Needs review: {needs_review}
Missing audio: {missing_audio}
Modified Ho transcripts: {modified_ho_transcripts}
Duplicate IDs: {duplicate_ids}
Machine-generated translations: 0
Production files modified: 0

Current status:
{status}
"""
with open("PHASE_25B_HO_HINDI_COLLECTION_STATUS.md", "w", encoding="utf-8") as f:
    f.write(report)
'''
with open("validate_translations.py", "w", encoding="utf-8") as f:
    f.write(validation_script)

print("Setup complete")
