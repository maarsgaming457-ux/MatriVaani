with open('static/index.html', 'r') as f:
    lines = f.readlines()
    
# Insert audio player after h3 record-id
for i, line in enumerate(lines):
    if '<h3 id="record-id"></h3>' in line:
        insert_idx = i + 1
        break

audio_html = '''        
        <div class="field">
            <label>Ho Audio</label>
            <audio id="audio_player" controls style="width: 100%;"></audio>
        </div>
'''
lines.insert(insert_idx, audio_html)

# Insert audio source update in showRecord
for i, line in enumerate(lines):
    if 'document.getElementById("msg").innerHTML = "";' in line:
        insert_idx2 = i
        break

js_html = '            document.getElementById("audio_player").src = /api/audio/;\n'
lines.insert(insert_idx2, js_html)

with open('static/index.html', 'w') as f:
    f.writelines(lines)
