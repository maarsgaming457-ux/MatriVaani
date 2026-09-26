import os
import json
import hashlib
from datasets import load_dataset

dirs = [
    'data/ho_external/huggingface/discovery',
    'data/ho_external/huggingface/raw',
    'data/ho_external/huggingface/audit',
    'data/ho_external/huggingface/manifests',
    'data/ho_external/huggingface/rejected',
    'data/ho_external/huggingface/duplicates'
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 2. AUDIT PROJECT BOLI
print("Auditing project-boli/ho...")
try:
    ds_boli = load_dataset('project-boli/ho', split='train', streaming=True)
    boli_records = 0
    boli_duration = 0.0
    for row in ds_boli:
        boli_records += 1
        audio_array = row['audio']['array']
        sr = row['audio']['sampling_rate']
        dur = len(audio_array) / sr
        boli_duration += dur
    boli_audit_json = {
        "usable_records": boli_records,
        "total_duration_hours": boli_duration/3600,
        "script": "Devanagari",
        "duplicate_of_pilot": True
    }
except Exception as e:
    boli_audit_json = {"error": str(e)}

with open('PROJECT_BOLI_HO_AUDIT.json', 'w', encoding='utf-8') as f: json.dump(boli_audit_json, f, indent=2)

# 3. AUDIT KARYA ENDANGERED RECIPES
print("Auditing karya...")
try:
    ds_karya = load_dataset('karya/endangered-recipes-translated-500', split='train', streaming=True)
    karya_total = 0
    karya_ho = 0
    for row in ds_karya:
        karya_total += 1
        if str(row).find('hoc') != -1 or str(row).find('Ho') != -1:
             karya_ho += 1
    karya_audit_json = {
        "total_records": karya_total,
        "ho_records": karya_ho,
        "classification": "EXTERNAL_TRANSLATION",
        "usable_for_hindi": False
    }
except Exception as e:
    karya_audit_json = {"error": str(e)}

with open('KARYA_HO_AUDIT.json', 'w', encoding='utf-8') as f: json.dump(karya_audit_json, f, indent=2)
