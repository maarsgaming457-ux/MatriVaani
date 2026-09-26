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
    c.execute("""
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
    """)
    conn.commit()
    # Insert demo record if empty
    c.execute("SELECT COUNT(*) FROM annotations")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO annotations VALUES (
            "DEMO_001", "[ENTER HO SENTENCE]", "[ENTER HO SENTENCE]", "[ENTER HINDI TRANSLATION]", 
            "general_conversation", "manual", 0, 0, "ANON_001", NULL, "NEW", "", 1)""")
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
    c.execute("SELECT * FROM annotations")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

@app.post("/api/records/{record_id}")
def update_record(record_id: str, data: AnnotationUpdate):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Validation checks
    if data.review_status == "APPROVED" and (not data.human_verified or not data.ho.strip() or not data.hindi.strip()):
        return {"error": "APPROVED records must be human verified and have non-empty Ho/Hindi text."}
    
    c.execute("""
        UPDATE annotations SET
        ho = ?, hindi = ?, category = ?, human_verified = ?, review_status = ?, notes = ?
        WHERE id = ?
    """, (data.ho, data.hindi, data.category, data.human_verified, data.review_status, data.notes, record_id))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/api/export/{status}")
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
            
    return {"status": "success", "file": filename, "count": len(rows)}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

