import re

with open('tools/ho_annotator/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add progress counter div below h2
content = content.replace('<h2>MatriVaani Ho-Hindi Annotator</h2>', '<h2>MatriVaani Ho-Hindi Annotator</h2>\n    <div id="progress-counter" style="font-weight: bold; font-size: 1.2em; margin-bottom: 15px; color: #333; padding: 10px; background: #e9ecef; border-radius: 5px; text-align: center;"></div>')

# Modify Export section
old_export_section = '''    <div class="export-section">
        <h3>Export Data</h3>
        <button onclick="exportData('APPROVED')">Export Approved</button>
        <button onclick="exportData('ALL')">Export All Valid</button>
    </div>'''
new_export_section = '''    <div class="export-section">
        <h3>Export Data</h3>
        <button onclick="exportData('VERIFIED')">Export Verified (Phase 12 Pilot)</button>
    </div>'''
content = content.replace(old_export_section, new_export_section)

# Update loadRecords JS
old_loadRecords = '''            if(records.length > 0) {
                document.getElementById("editor").style.display = "block";
                showRecord(0);
            } else {'''
new_loadRecords = '''            if(records.length > 0) {
                document.getElementById("editor").style.display = "block";
                updateProgress();
                showRecord(0);
            } else {'''
content = content.replace(old_loadRecords, new_loadRecords)

# Add updateProgress function in JS
updateProgress_func = '''
        function updateProgress() {
            let verifiedCount = records.filter(r => r.human_verified && r.ho && r.ho.trim() !== '' && r.hindi && r.hindi.trim() !== '').length;
            let total = records.filter(r => !r.demo_only).length;
            let pendingCount = total - verifiedCount;
            document.getElementById("progress-counter").innerHTML = Verified:  /  &nbsp;&nbsp;|&nbsp;&nbsp; Pending:  / ;
        }
'''
content = content.replace('function showRecord(index)', updateProgress_func + '\n        function showRecord(index)')

# Update saveRecord JS to handle response
old_saveRecord_success = '''            if(result.error) {
                document.getElementById("msg").innerHTML = <div class="error"></div>;
                return false;
            } else {
                document.getElementById("msg").innerHTML = <div class="success">Saved  successfully.</div>;
                // update local cache
                Object.assign(records[currentIndex], data);
                return true;
            }'''
new_saveRecord_success = '''            if(result.error) {
                document.getElementById("msg").innerHTML = <div class="error"></div>;
                return false;
            } else {
                document.getElementById("msg").innerHTML = <div class="success">Saved  successfully.</div>;
                // update local cache with backend validated data
                data.human_verified = result.human_verified;
                data.review_status = result.review_status;
                Object.assign(records[currentIndex], data);
                updateProgress();
                if(data.human_verified === false && document.getElementById("human_verified").checked) {
                    document.getElementById("msg").innerHTML += <div class="error">Warning: Cannot verify empty translation. Marked as NEEDS REVIEW.</div>;
                    document.getElementById("human_verified").checked = false;
                }
                return true;
            }'''
content = content.replace(old_saveRecord_success, new_saveRecord_success)

with open('tools/ho_annotator/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
