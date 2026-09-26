with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Record  / ', 'Annotated:  / ')
text = text.replace('<label>Raw Ho ASR (Do not edit)</label>', '<label>Raw Ho ASR</label><small style="display:block;margin-bottom:5px;color:#555;">Do not edit. This is the machine generated ASR.</small>')
text = text.replace('<label>Corrected Ho (Devanagari)</label>', '<label>Corrected Ho Transcription</label><small style="display:block;margin-bottom:5px;color:#555;">Listen carefully to the recording and correct the Raw Ho ASR only when you are confident about the spoken Ho.</small>')
text = text.replace('<label>Hindi Translation (Natural meaning in Devanagari)</label>', '<label>Human Hindi Translation</label><small style="display:block;margin-bottom:5px;color:#555;">Listen to the Ho recording and enter the Hindi meaning manually. Do not use machine-generated translation as ground truth.</small>')

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
