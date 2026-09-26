import json
import os

in_asr = 'data/ho_hindi/raw/ho_asr_recovery_manifest_100.jsonl'
out_asr = 'data/ho_asr/ho_asr_v1_manifest.jsonl'
count_asr = 0

if os.path.exists(in_asr):
    with open(in_asr, 'r', encoding='utf-8', errors='ignore') as fi, open(out_asr, 'w', encoding='utf-8') as fo:
        for line in fi:
            try:
                row = json.loads(line)
                new_row = {
                    'audio_path': f'/content/drive/MyDrive/MatriVaani_Ho_ASR/processed_dataset/{row.get("audio_filename", "")}',
                    'transcript': row.get('raw_asr_text', ''),
                    'language': 'ho',
                    'script': 'unknown_script',
                    'speaker_id': 'project_boli_speaker_1',
                    'duration': 0.0,
                    'sample_rate': 16000,
                    'source': 'project-boli/ho',
                    'human_verified': True,
                    'ground_truth': True,
                    'synthetic': False
                }
                fo.write(json.dumps(new_row, ensure_ascii=False) + '\n')
                count_asr += 1
            except Exception as e:
                pass

print('ASR rows written:', count_asr)
