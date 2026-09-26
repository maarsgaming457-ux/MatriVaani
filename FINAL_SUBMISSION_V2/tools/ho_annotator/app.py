import sqlite3
import json
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
DB_FILE = "annotations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS annotations (
            id TEXT PRIMARY KEY,
            raw_asr_text TEXT,
            ho TEXT,
            hindi TEXT,
            category TEXT,
            source TEXT,
            machine_draft BOOLEAN,
            human_verified BOOLEAN,
            translator_id TEXT,
            reviewer_id TEXT,
            review_status TEXT,
            notes TEXT,
            demo_only BOOLEAN
        )
    ''')
    conn.commit()
    # Insert demo record if empty
    c.execute("SELECT COUNT(*) FROM annotations")
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO annotations VALUES (
            "DEMO_001", "[ENTER HO SENTENCE]", "[ENTER HO SENTENCE]", "[ENTER HINDI TRANSLATION]", 
            "general_conversation", "manual", 0, 0, "ANON_001", NULL, "NEW", "", 1)''')
        conn.commit()
    conn.close()

init_db()

class AnnotationUpdate(BaseModel):
    ho: str
    hindi: str
    category: str
    human_verified: bool
    review_status: str
    notes: str

@app.get("/api/records")
def get_records():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM annotations WHERE source_record_id IS NOT NULL ORDER BY source_split ASC, source_record_id ASC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

@app.post("/api/records/{record_id}")
def update_record(record_id: str, data: AnnotationUpdate):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if data.human_verified and (not data.ho.strip() or not data.hindi.strip()):
        data.human_verified = False
        data.review_status = "NEEDS REVIEW"
    elif data.human_verified:
        data.review_status = "APPROVED"
    else:
        if data.review_status == "APPROVED":
            data.review_status = "NEEDS REVIEW"
    
    c.execute('''
        UPDATE annotations SET
        ho = ?, hindi = ?, category = ?, human_verified = ?, review_status = ?, notes = ?
        WHERE id = ?
    ''', (data.ho, data.hindi, data.category, data.human_verified, data.review_status, data.notes, record_id))
    conn.commit()
    conn.close()
    return {"status": "success", "human_verified": data.human_verified, "review_status": data.review_status}

@app.get("/api/audio/{record_id}")
def get_audio(record_id: str):
    from fastapi import HTTPException
    from fastapi.responses import FileResponse
    import sqlite3, json, os
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT source_record_id FROM annotations WHERE id = ?", (record_id,))
    row = c.fetchone()
    conn.close()
    
    if not row or not row[0]:
        raise HTTPException(status_code=404, detail="Record not found")
        
    source_record_id = row[0]
    manifest_path = r"C:\Users\maars\Downloads\ho_asr_recovery_manifest_100.jsonl"
    audio_filename = None
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    if r.get("source_record_id") == source_record_id:
                        audio_filename = r.get("audio_filename")
                        break
                    
    if not audio_filename:
        raise HTTPException(status_code=404, detail="Audio not found in manifest")
        
    audio_dir = os.path.abspath("audio")
    audio_path = os.path.abspath(os.path.join(audio_dir, audio_filename))
    
    if not audio_path.startswith(audio_dir):
        raise HTTPException(status_code=403, detail="Forbidden")
        
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(audio_path, media_type="audio/wav")

@app.post("/api/export/{status}")
def export_records(status: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM annotations WHERE human_verified = 1 AND demo_only = 0 AND ho != '' AND hindi != ''")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    
    # Load manifest to get audio_filenames
    manifest_path = r"C:\Users\maars\Downloads\ho_asr_recovery_manifest_100.jsonl"
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
            f.write(json.dumps(export_record, ensure_ascii=False) + "\n")
            exported_rows.append(export_record)
            
    return {"status": "success", "file": filename, "count": len(exported_rows)}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
