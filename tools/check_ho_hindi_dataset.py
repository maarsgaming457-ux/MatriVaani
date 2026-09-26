import sqlite3
import os
import json

db_path = "tools/ho_annotator/annotations.db"
verified_path = "data/ho_hindi/verified/ho_hindi_verified.jsonl"
splits_dir = "data/ho_hindi/splits"

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT * FROM annotations WHERE demo_only = 0")
all_records = c.fetchall()

total = len(all_records)
verified = len([r for r in all_records if r['human_verified'] == 1])
unverified = total - verified
empty_ho = len([r for r in all_records if not r['ho'] or not r['ho'].strip()])
empty_hindi = len([r for r in all_records if not r['hindi'] or not r['hindi'].strip()])

# Duplicates among verified
verified_records = [r for r in all_records if r['human_verified'] == 1]
ho_set = set()
hindi_set = set()
pair_set = set()
duplicate_ho = 0
duplicate_hindi = 0
duplicate_pair = 0

for r in verified_records:
    ho = r['ho'].strip()
    hi = r['hindi'].strip()
    if ho in ho_set: duplicate_ho += 1
    if hi in hindi_set: duplicate_hindi += 1
    if (ho, hi) in pair_set: duplicate_pair += 1
    ho_set.add(ho)
    hindi_set.add(hi)
    pair_set.add((ho, hi))

train_count = 0
val_count = 0
test_count = 0
license_status = "CC-BY-NC 4.0 (Pending Assignment)"
provenance_status = "project-boli/ho ASR transcripts"

train_file = os.path.join(splits_dir, "train.jsonl")
if os.path.exists(train_file):
    with open(train_file, "r", encoding="utf-8") as f:
        train_count = len(f.readlines())

print("Ho-Hindi Dataset Quality Check")
print("==============================")
print(f"Total records: {total}")
print(f"Verified records: {verified}")
print(f"Unverified records: {unverified}")
print(f"Empty Ho: {empty_ho}")
print(f"Empty Hindi: {empty_hindi}")
print(f"Duplicate Ho (in verified): {duplicate_ho}")
print(f"Duplicate Hindi (in verified): {duplicate_hindi}")
print(f"Duplicate pairs (in verified): {duplicate_pair}")
print(f"Train count: {train_count}")
print(f"Validation count: {val_count}")
print(f"Test count: {test_count}")
print(f"License status: {license_status}")
print(f"Provenance status: {provenance_status}")

if verified >= 50 and duplicate_pair == 0:
    print("\nREADY_FOR_TRAINING")
else:
    print("\nNOT_READY_FOR_TRAINING")
