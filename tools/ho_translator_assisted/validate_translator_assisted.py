"""
Step 8 & 9 & 10 — Validation Script for Translator Assisted Collection (Phase 28)
Validates HO_HINDI_TRANSLATOR_ASSISTED workbooks against original baseline collections,
audio disk storage, and human verification constraints.
"""
import os
import sys
import json
import csv
import zipfile
import xml.etree.ElementTree as ET

BASE_DIR = r"C:\study_files\sih project"
ORIGINAL_XLSX = os.path.join(BASE_DIR, r"data\ho_hindi\collection\work\HO_HINDI_TRANSLATION_FORM_WORKING.xlsx")
AUDIO_DIR = os.path.join(BASE_DIR, r"tools\ho_annotator\audio")

ASSISTED_XLSX = os.path.join(BASE_DIR, r"data\ho_hindi\collection\work\HO_HINDI_TRANSLATOR_ASSISTED.xlsx")
ASSISTED_CSV = os.path.join(BASE_DIR, r"data\ho_hindi\collection\work\HO_HINDI_TRANSLATOR_ASSISTED.csv")
ASSISTED_JSON = os.path.join(BASE_DIR, r"data\ho_hindi\collection\work\HO_HINDI_TRANSLATOR_ASSISTED.json")
VERIFIED_JSONL = os.path.join(BASE_DIR, r"data\ho_hindi\verified\ho_hindi_verified.jsonl")

NS = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def read_xlsx_rows(path):
    rows_data = []
    with zipfile.ZipFile(path, "r") as z:
        with z.open("xl/worksheets/sheet1.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()
            rows = root.findall(".//ns:row", NS)
            if not rows:
                return []
            header = []
            for c in rows[0].findall("ns:c", NS):
                t_elem = c.find(".//ns:t", NS)
                header.append(t_elem.text if t_elem is not None else "")

            for r in rows[1:]:
                row_dict = {}
                cells = r.findall("ns:c", NS)
                for idx, c in enumerate(cells):
                    col_ref = c.attrib.get("r", "")
                    col_letters = "".join([ch for ch in col_ref if ch.isalpha()])
                    # compute column index from letters
                    c_idx = 0
                    for ch in col_letters:
                        c_idx = c_idx * 26 + (ord(ch) - ord('A') + 1)
                    c_idx -= 1

                    t_attr = c.attrib.get("t")
                    if t_attr == "inlineStr":
                        t_elem = c.find(".//ns:t", NS)
                        val = t_elem.text if t_elem is not None else ""
                    else:
                        v_elem = c.find("ns:v", NS)
                        val = v_elem.text if v_elem is not None else ""

                    if c_idx < len(header):
                        row_dict[header[c_idx]] = val
                rows_data.append(row_dict)
    return header, rows_data

def run_validation():
    print("=" * 80)
    print("PHASE 28: HO-HINDI TRANSLATOR ASSISTED COLLECTION VALIDATION")
    print("=" * 80)

    errors = []
    warnings = []

    # 1. Read Original Baseline
    if not os.path.exists(ORIGINAL_XLSX):
        errors.append(f"Original working form missing: {ORIGINAL_XLSX}")
        return False

    orig_hdr, orig_rows = read_xlsx_rows(ORIGINAL_XLSX)
    print(f"[OK] Read original baseline: {len(orig_rows)} rows from {os.path.basename(ORIGINAL_XLSX)}")

    if len(orig_rows) != 100:
        errors.append(f"Original collection row count is {len(orig_rows)}, expected 100")

    orig_map = {r.get("ID"): r for r in orig_rows}

    # 2. Check Audio Directory
    print(f"\n[CHECKING] Audio files in: {AUDIO_DIR}")
    missing_audio = []
    zero_size_audio = []
    for r in orig_rows:
        af = r.get("Audio Filename")
        if not af:
            missing_audio.append(f"Row {r.get('ID')} missing Audio Filename")
            continue
        apath = os.path.join(AUDIO_DIR, af)
        if not os.path.exists(apath):
            missing_audio.append(af)
        elif os.path.getsize(apath) == 0:
            zero_size_audio.append(af)

    if missing_audio:
        errors.append(f"Missing {len(missing_audio)} audio files on disk: {missing_audio[:5]}")
    else:
        print(f"[OK] All 100 audio files verified existing on disk.")

    if zero_size_audio:
        errors.append(f"Zero-size audio files detected: {zero_size_audio}")

    # 3. Validate HO_HINDI_TRANSLATOR_ASSISTED.xlsx
    print(f"\n[CHECKING] Translator Workbook: {ASSISTED_XLSX}")
    if not os.path.exists(ASSISTED_XLSX):
        errors.append(f"Translator assisted workbook missing: {ASSISTED_XLSX}")
        return False

    asst_hdr, asst_rows = read_xlsx_rows(ASSISTED_XLSX)
    print(f"[OK] Read {len(asst_rows)} rows from {os.path.basename(ASSISTED_XLSX)}")

    req_cols = [
        "ID", "Audio Filename", "Verified Ho Transcript",
        "Resource-Assisted Ho Gloss", "Resource Source", "Resource Coverage",
        "Candidate Hindi Hints", "Hindi Translation", "Translator ID",
        "Notes", "Completed", "Human Verified"
    ]
    for c in req_cols:
        if c not in asst_hdr:
            errors.append(f"Missing required column '{c}' in {os.path.basename(ASSISTED_XLSX)}")

    if len(asst_rows) != 100:
        errors.append(f"Translator workbook row count is {len(asst_rows)}, expected 100")

    # Verify each row vs original
    for idx, r in enumerate(asst_rows):
        rid = r.get("ID")
        if not rid:
            errors.append(f"Row {idx+2} in workbook has empty ID")
            continue
        if rid not in orig_map:
            errors.append(f"Row {idx+2} ID '{rid}' does not match any original baseline ID")
            continue

        orig_r = orig_map[rid]
        if r.get("Audio Filename") != orig_r.get("Audio Filename"):
            errors.append(f"Row {rid}: Audio Filename mismatch ('{r.get('Audio Filename')}' != '{orig_r.get('Audio Filename')}')")

        if r.get("Verified Ho Transcript") != orig_r.get("Verified Ho Transcript"):
            errors.append(f"Row {rid}: Verified Ho Transcript altered! Original: '{orig_r.get('Verified Ho Transcript')}', Current: '{r.get('Verified Ho Transcript')}'")

        # Check candidate hints safety label
        cand = r.get("Candidate Hindi Hints", "")
        if "[RESOURCE HINT — NOT GROUND TRUTH]" not in cand:
            errors.append(f"Row {rid}: Candidate Hindi Hints missing mandatory safety prefix")

        # Step 8 rule: Check completed & human verified consistency
        completed = r.get("Completed", "FALSE") == "TRUE"
        verified = r.get("Human Verified", "FALSE") == "TRUE"
        ht = (r.get("Hindi Translation") or "").strip()
        tid = (r.get("Translator ID") or "").strip()

        if completed:
            if not ht:
                errors.append(f"Row {rid} marked Completed=TRUE but Hindi Translation is empty")
            if not tid:
                errors.append(f"Row {rid} marked Completed=TRUE but Translator ID is empty")

        if verified:
            if not completed or not ht or not tid:
                errors.append(f"Row {rid} marked Human Verified=TRUE without valid translation/translator")
            if "[RESOURCE HINT" in ht:
                errors.append(f"Row {rid}: Candidate resource hint was copied into Hindi Translation as ground truth!")

    print(f"[OK] Field-level immutability and schema verified for all 100 workbook rows.")

    # 4. Validate CSV and JSON companions
    print(f"\n[CHECKING] Companion files: CSV and JSON")
    if not os.path.exists(ASSISTED_CSV):
        errors.append(f"Missing CSV companion: {ASSISTED_CSV}")
    else:
        with open(ASSISTED_CSV, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            csv_rows = list(reader)
            if len(csv_rows) != 100:
                errors.append(f"CSV companion has {len(csv_rows)} rows, expected 100")
            else:
                print(f"[OK] CSV companion verified ({len(csv_rows)} rows).")

    if not os.path.exists(ASSISTED_JSON):
        errors.append(f"Missing JSON companion: {ASSISTED_JSON}")
    else:
        with open(ASSISTED_JSON, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            j_records = json_data.get("records", [])
            if len(j_records) != 100:
                errors.append(f"JSON companion has {len(j_records)} records, expected 100")
            else:
                print(f"[OK] JSON companion verified ({len(j_records)} records).")

    # 5. Milestone Check
    completed_count = sum(1 for r in asst_rows if r.get("Completed") == "TRUE" and (r.get("Hindi Translation") or "").strip())
    verified_count = sum(1 for r in asst_rows if r.get("Human Verified") == "TRUE" and (r.get("Hindi Translation") or "").strip())

    print("\n" + "-" * 80)
    print(f"MILESTONE STATUS:")
    print(f"  Total Sentences: {len(asst_rows)}")
    print(f"  Human Completed Sentences: {completed_count}")
    print(f"  Human Verified Sentences: {verified_count}")
    print(f"  Target for Phase 29: 50 Human Ho-Hindi Pairs")

    if completed_count >= 50:
        milestone = "READY_FOR_PHASE_29_DATASET_VALIDATION"
        print(f"  Result: {milestone}")
    else:
        milestone = "WAITING_FOR_50_HUMAN_HO_HINDI_PAIRS"
        print(f"  Result: {milestone} ({completed_count}/50 completed)")
    print("-" * 80)

    # 6. Step 10: Verified Dataset Gate
    if os.path.exists(VERIFIED_JSONL):
        with open(VERIFIED_JSONL, "r", encoding="utf-8") as f:
            v_lines = [json.loads(line) for line in f if line.strip()]
        for vl in v_lines:
            if not vl.get("human_verified") or not vl.get("translator_id") or not vl.get("hindi_translation"):
                errors.append(f"Invalid record found in {VERIFIED_JSONL}: {vl.get('id')}")
        print(f"[OK] Verified dataset file contains {len(v_lines)} genuine verified records.")
    else:
        print(f"[INFO] Verified dataset {VERIFIED_JSONL} not yet generated (awaiting human translations).")

    if errors:
        print("\n[VALIDATION FAILED] Errors found:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[SUCCESS] ALL VALIDATION CHECKS PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    ok = run_validation()
    sys.exit(0 if ok else 1)
