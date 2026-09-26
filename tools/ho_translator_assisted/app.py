"""
Isolated Translator-Assisted Annotation Server (Phase 28)
Reads/writes records from HO_HINDI_TRANSLATOR_ASSISTED.json and HO_HINDI_TRANSLATOR_ASSISTED.xlsx / CSV.
Provides endpoints for the translator UI.
"""
import json
import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="MatriVaani Ho-Hindi Translator Assisted Interface")

DATA_JSON = r"C:\study_files\sih project\data\ho_hindi\collection\work\HO_HINDI_TRANSLATOR_ASSISTED.json"
AUDIO_DIR = r"C:\study_files\sih project\tools\ho_annotator\audio"

def load_records():
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metadata": {}, "records": []}

def save_records(data):
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class RecordUpdate(BaseModel):
    hindi_translation: str
    translator_id: str
    notes: str
    completed: bool
    human_verified: bool

@app.get("/api/records")
def get_records():
    data = load_records()
    return data.get("records", [])

@app.post("/api/records/{record_id}")
def update_record(record_id: str, update: RecordUpdate):
    data = load_records()
    records = data.get("records", [])

    target_rec = None
    for r in records:
        if r.get("ID") == record_id:
            target_rec = r
            break

    if not target_rec:
        raise HTTPException(status_code=404, detail="Record not found")

    # Validation rules (Step 8)
    if update.completed and (not update.hindi_translation.strip() or not update.translator_id.strip()):
        raise HTTPException(status_code=400, detail="Validation error: Hindi Translation and Translator ID must be non-empty when marked Completed.")

    target_rec["Hindi Translation"] = update.hindi_translation
    target_rec["Translator ID"] = update.translator_id
    target_rec["Notes"] = update.notes
    target_rec["Completed"] = "TRUE" if update.completed else "FALSE"

    # Strictly ensure human_verified cannot be arbitrarily marked true if invalid, or enforce Step 7/10 rules
    if update.human_verified and (not update.hindi_translation.strip() or not update.translator_id.strip()):
        target_rec["Human Verified"] = "FALSE"
    else:
        target_rec["Human Verified"] = "TRUE" if update.human_verified else "FALSE"

    save_records(data)
    return {"status": "success", "id": record_id, "completed": target_rec["Completed"], "human_verified": target_rec["Human Verified"]}

@app.get("/api/audio/{record_id}")
def get_audio(record_id: str):
    data = load_records()
    audio_filename = None
    for r in data.get("records", []):
        if r.get("ID") == record_id:
            audio_filename = r.get("Audio_File") or r.get("Audio Filename")
            break

    if not audio_filename:
        raise HTTPException(status_code=404, detail="Audio file not found for record")

    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail=f"Audio file {audio_filename} missing from disk")

    return FileResponse(audio_path, media_type="audio/wav")

@app.get("/api/status")
def get_status():
    data = load_records()
    records = data.get("records", [])
    completed_count = sum(1 for r in records if r.get("Completed") == "TRUE" and r.get("Hindi Translation", "").strip())
    verified_count = sum(1 for r in records if r.get("Human Verified") == "TRUE" and r.get("Hindi Translation", "").strip())

    milestone = "READY_FOR_PHASE_29_DATASET_VALIDATION" if completed_count >= 50 else "WAITING_FOR_50_HUMAN_HO_HINDI_PAIRS"

    return {
        "total_records": len(records),
        "completed_count": completed_count,
        "verified_count": verified_count,
        "remaining_records": len(records) - completed_count,
        "milestone_status": milestone
    }

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8081)
