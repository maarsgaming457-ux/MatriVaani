import re

with open("tools/ho_annotator/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the export endpoint
new_export = '''@app.post("/api/export/{status}")
def export_records(status: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM annotations WHERE human_verified = 1 AND demo_only = 0 AND ho != '' AND hindi != ''")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    
    export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "ho_hindi", "verified"))
    os.makedirs(export_dir, exist_ok=True)
    filename = os.path.join(export_dir, "ho_hindi_verified.jsonl")
    
    exported_rows = []
    with open(filename, "w", encoding="utf-8") as f:
        for r in rows:
            export_record = {
                "id": r.get("id"),
                "ho": r.get("ho"),
                "hindi": r.get("hindi"),
                "source": r.get("source_dataset", "project-boli/ho"),
                "license": "CC-BY-NC 4.0",
                "human_verified": True
            }
            f.write(json.dumps(export_record, ensure_ascii=False) + "\\n")
            exported_rows.append(export_record)
            
    return {"status": "success", "file": filename, "count": len(exported_rows)}'''

content = re.sub(r'@app\.post\("/api/export/\{status\}"\).*?return \{"status": "success", "file": filename, "count": len\(exported_rows\)\}', new_export, content, flags=re.DOTALL)

with open("tools/ho_annotator/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched app.py")
