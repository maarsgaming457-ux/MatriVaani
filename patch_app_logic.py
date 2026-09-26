import re

with open("tools/ho_annotator/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add translator_id to model
content = content.replace("class AnnotationUpdate(BaseModel):", "class AnnotationUpdate(BaseModel):\n    translator_id: str")

# Update logic
new_logic = '''
@app.post("/api/records/{record_id}")
def update_record(record_id: str, data: AnnotationUpdate):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if data.human_verified and (not data.ho.strip() or not data.hindi.strip() or not data.translator_id.strip()):
        data.human_verified = False
        data.review_status = "NEEDS REVIEW"
        return {"status": "error", "error": "Verification rejected: Corrected Ho, Hindi translation, and Translator ID must all be non-empty."}
    elif data.human_verified:
        data.review_status = "APPROVED"
    else:
        if data.review_status == "APPROVED":
            data.review_status = "NEEDS REVIEW"
    
    c.execute(\'''
        UPDATE annotations SET
        ho = ?, hindi = ?, category = ?, human_verified = ?, review_status = ?, notes = ?, translator_id = ?
        WHERE id = ?
    \''', (data.ho, data.hindi, data.category, data.human_verified, data.review_status, data.notes, data.translator_id, record_id))
    conn.commit()
    conn.close()
    return {"status": "success", "human_verified": data.human_verified, "review_status": data.review_status}
'''

content = re.sub(r'@app\.post\("/api/records/\{record_id\}"\).*?return \{"status": "success", "human_verified": data\.human_verified, "review_status": data\.review_status\}', new_logic.strip(), content, flags=re.DOTALL)

with open("tools/ho_annotator/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched app.py logic")
