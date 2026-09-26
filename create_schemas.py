import os, json

dirs = ['data/ho_asr/collection_v1', 'data/ho_translation/collection_v1', 'data/ho_tts/collection_v1']
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Create ASR files
with open('data/ho_asr/collection_v1/metadata_schema.json', 'w', encoding='utf-8') as f:
    json.dump({'audio_path': 'string', 'transcript': 'string', 'speaker_id': 'string', 'duration': 'float', 'sample_rate': 'int', 'script': 'string', 'source': 'string', 'human_verified': 'bool', 'ground_truth': 'bool', 'recording_quality': 'string'}, f, indent=2)
with open('data/ho_asr/collection_v1/manifest_template.jsonl', 'w', encoding='utf-8') as f:
    f.write('{"audio_path": "", "transcript": "", "speaker_id": "", "duration": 0.0, "sample_rate": 16000, "script": "Devanagari", "source": "", "human_verified": false, "ground_truth": false, "recording_quality": ""}\n')
with open('data/ho_asr/collection_v1/README.md', 'w', encoding='utf-8') as f:
    f.write('# Ho ASR Collection Pilot V1\nContains scripts, schemas, and instructions for ASR data collection.')

# Create Translation files
with open('data/ho_translation/collection_v1/metadata_schema.json', 'w', encoding='utf-8') as f:
    json.dump({'id': 'string', 'ho_text': 'string', 'hi_text': 'string', 'ho_script': 'string', 'hi_script': 'string', 'domain': 'string', 'source': 'string', 'reviewer_id': 'string', 'human_verified': 'bool', 'ground_truth': 'bool', 'synthetic': 'bool', 'verification_status': 'string'}, f, indent=2)
with open('data/ho_translation/collection_v1/manifest_template.jsonl', 'w', encoding='utf-8') as f:
    f.write('{"id": "", "ho_text": "", "hi_text": "", "ho_script": "Devanagari", "hi_script": "Devanagari", "domain": "", "source": "", "reviewer_id": "", "human_verified": false, "ground_truth": false, "synthetic": false, "verification_status": "UNVERIFIED"}\n')
with open('data/ho_translation/collection_v1/README.md', 'w', encoding='utf-8') as f:
    f.write('# Ho Translation Collection Pilot V1\nContains templates for parallel data collection.')

# Create TTS files
with open('data/ho_tts/collection_v1/metadata_schema.json', 'w', encoding='utf-8') as f:
    json.dump({'audio_path': 'string', 'text': 'string', 'speaker_id': 'string', 'duration': 'float', 'sample_rate': 'int', 'script': 'string', 'source': 'string', 'human_verified': 'bool', 'transcript_verified': 'bool', 'recording_quality': 'string'}, f, indent=2)
with open('data/ho_tts/collection_v1/manifest_template.jsonl', 'w', encoding='utf-8') as f:
    f.write('{"audio_path": "", "text": "", "speaker_id": "", "duration": 0.0, "sample_rate": 16000, "script": "Devanagari", "source": "", "human_verified": false, "transcript_verified": false, "recording_quality": ""}\n')
with open('data/ho_tts/collection_v1/README.md', 'w', encoding='utf-8') as f:
    f.write('# Ho TTS Collection Pilot V1\nContains schemas and instructions for high-quality TTS voice collection.')

print('Directories and schema files created.')
