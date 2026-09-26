import os

with open('app.py', 'r') as f:
    lines = f.readlines()
    
endpoint_code = r'''
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
'''

insert_idx = 0
for i, line in enumerate(lines):
    if line.startswith('@app.post("/api/export/{status}")'):
        insert_idx = i
        break

lines.insert(insert_idx, endpoint_code + '\n')

with open('app.py', 'w') as f:
    f.writelines(lines)
