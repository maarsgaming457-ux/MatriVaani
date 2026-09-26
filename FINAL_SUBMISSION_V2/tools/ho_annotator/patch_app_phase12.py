import re
import os

with open('tools/ho_annotator/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update update_record validation
old_validation = '''    if data.review_status == "APPROVED" and (not data.human_verified or not data.ho.strip() or not data.hindi.strip()):
        return {"error": "APPROVED records must be human verified and have non-empty Ho/Hindi text."}'''

new_validation = '''    if data.human_verified and (not data.ho.strip() or not data.hindi.strip()):
        data.human_verified = False
        data.review_status = "NEEDS REVIEW"
    elif data.human_verified:
        data.review_status = "APPROVED"
    else:
        if data.review_status == "APPROVED":
            data.review_status = "NEEDS REVIEW" '''

content = content.replace(old_validation, new_validation)

# Update export endpoint
old_export = '''@app.post("/api/export/{status}")
def export_records(status: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if status == "ALL":
        c.execute("SELECT * FROM annotations WHERE demo_only = 0")
    else:
        c.execute("SELECT * FROM annotations WHERE review_status = ? AND demo_only = 0", (status,))
    
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    
    export_dir = os.path.join("..", "..", "data", "ho_hindi", "pilot_v0.1")
    os.makedirs(export_dir, exist_ok=True)
    filename = os.path.join(export_dir, f"export_{status.lower()}.jsonl")
    
    with open(filename, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\\n")
            
    return {"status": "success", "file": filename, "count": len(rows)}'''

new_export = '''@app.post("/api/export/{status}")
def export_records(status: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM annotations WHERE human_verified = 1 AND demo_only = 0 AND ho != '' AND hindi != ''")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    
    # Load manifest to get audio_filenames
    manifest_path = r"C:\\Users\\maars\\Downloads\\ho_asr_recovery_manifest_100.jsonl"
    manifest_dict = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    manifest_dict[r.get("source_record_id")] = r.get("audio_filename")
    
    export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "ho_hindi", "pilot_v0.1"))
    os.makedirs(export_dir, exist_ok=True)
    filename = os.path.join(export_dir, f"export_verified.jsonl")
    
    exported_rows = []
    with open(filename, "w", encoding="utf-8") as f:
        for r in rows:
            audio_filename = manifest_dict.get(r.get("source_record_id"), "")
            export_record = {
                "id": r.get("id"),
                "audio_id": r.get("source_record_id"),
                "audio_filename": audio_filename,
                "ho": r.get("ho"),
                "hindi": r.get("hindi"),
                "source_dataset": r.get("source_dataset"),
                "source_split": r.get("source_split"),
                "verified": True
            }
            f.write(json.dumps(export_record, ensure_ascii=False) + "\\n")
            exported_rows.append(export_record)
            
    return {"status": "success", "file": filename, "count": len(exported_rows)}'''

content = content.replace(old_export, new_export)

with open('tools/ho_annotator/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
