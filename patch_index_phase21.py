import re

with open("tools/ho_annotator/static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add translator_id field
translator_html = '''
        <div class="field">
            <label>Translator / Reviewer ID</label>
            <input type="text" id="translator_id">
        </div>
'''
content = content.replace('<div class="field">\n            <label>Notes</label>', translator_html + '        <div class="field">\n            <label>Notes</label>')

# Update progress text
progress_js = '''
        function updateProgress() {
            let verifiedCount = records.filter(r => r.human_verified && r.ho && r.ho.trim() !== '' && r.hindi && r.hindi.trim() !== '').length;
            let total = records.filter(r => !r.demo_only).length;
            let pendingCount = total - verifiedCount;
            document.getElementById("progress-counter").innerHTML = Verified:  /  &nbsp;&nbsp;|&nbsp;&nbsp; Pending:  /  &nbsp;&nbsp;|&nbsp;&nbsp; Ho-Hindi verified pairs: ;
        }
'''
content = re.sub(r'function updateProgress\(\) \{.*?(?=function showRecord)', progress_js.strip() + '\n\n        ', content, flags=re.DOTALL)

# Add translator_id to load and save
content = content.replace('document.getElementById("notes").value = r.notes || "";', 'document.getElementById("translator_id").value = r.translator_id || "";\n            document.getElementById("notes").value = r.notes || "";')
content = content.replace('review_status: document.getElementById("review_status").value,', 'review_status: document.getElementById("review_status").value,\n                translator_id: document.getElementById("translator_id").value,')

# Add missing JS fields update after save
content = content.replace('Object.assign(records[currentIndex], data);', '''
                Object.assign(records[currentIndex], data);
                updateProgress();
''')

# Ensure error message handling handles python backend error string
content = content.replace('if(result.error) {', 'if(result.status === "error" || result.error) {')

with open("tools/ho_annotator/static/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched index.html")
