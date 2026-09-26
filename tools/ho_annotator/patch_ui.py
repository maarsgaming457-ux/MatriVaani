with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

instructions = '''
    <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
        <strong>Ho ? Hindi Human Annotation Instructions:</strong>
        <ol style="margin-top: 5px; margin-bottom: 5px;">
            <li>Listen to the Ho recording.</li>
            <li>Review the Raw Ho ASR.</li>
            <li>Enter the Corrected Ho Transcription.</li>
            <li>Enter the Hindi meaning manually.</li>
            <li>Do not use machine translation as ground truth.</li>
            <li>Verify that the Hindi meaning matches the spoken Ho sentence.</li>
            <li>Mark Human Verified only after reviewing the complete pair.</li>
            <li>Save the record.</li>
        </ol>
        <p style="color: red; font-weight: bold; margin-bottom: 0;">WARNING: Only a competent Ho speaker should complete or verify the linguistic annotation.</p>
    </div>
'''

if 'Ho ? Hindi Human Annotation Instructions:' not in text:
    text = text.replace('<h2>MatriVaani Ho-Hindi Annotator</h2>', '<h2>MatriVaani Ho-Hindi Annotator</h2>\\n' + instructions)
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
