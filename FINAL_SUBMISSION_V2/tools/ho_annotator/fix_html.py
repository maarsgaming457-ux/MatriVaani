with open('static/index.html', 'r') as f:
    text = f.read()

text = text.replace('            document.getElementById("audio_player").src = /api/audio/;\n', 
                    '            document.getElementById("audio_player").src = "/api/audio/" + r.id;\n')

with open('static/index.html', 'w') as f:
    f.write(text)
