import os
import json
import pandas as pd

# Create directory
collection_dir = "data/ho_hindi/collection"
os.makedirs(collection_dir, exist_ok=True)

manifest_path = "C:/Users/maars/Downloads/ho_asr_recovery_manifest_100.jsonl"
records = []

# Extract required fields from manifest
with open(manifest_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            # The ASR transcripts have already been verified by the user as per prompt
            # So the raw_asr_text is effectively the Verified Ho Transcript
            records.append({
                "ID": data.get("source_record_id"),
                "Audio Filename": data.get("audio_filename"),
                "Verified Ho Transcript": data.get("raw_asr_text"),
                "Hindi Translation": "",
                "Translator ID": "",
                "Notes": "",
                "Completed": ""
            })

df = pd.DataFrame(records)

# Save as CSV
csv_path = os.path.join(collection_dir, "HO_HINDI_TRANSLATION_FORM.csv")
df.to_csv(csv_path, index=False, encoding='utf-8')

# Save as XLSX
xlsx_path = os.path.join(collection_dir, "HO_HINDI_TRANSLATION_FORM.xlsx")
df.to_excel(xlsx_path, index=False)

# Write INSTRUCTIONS_FOR_TRANSLATOR.md
instructions = '''# Instructions for Ho-Hindi Translator

1. Read/listen to the Ho sentence if necessary.
2. Use the provided Ho transcript as the source.
3. Enter the natural Hindi meaning.
4. Do not provide a transliteration.
5. Do not use machine translation.
6. If the meaning is unclear, leave Hindi Translation empty and write "needs_review" in Notes.
7. Do not guess.

### Note on Quality
A completed row requires:
- Verified Ho Transcript (already populated)
- Natural Hindi Translation
- Translator ID

The translator must be a person who understands both Ho and Hindi.
'''
with open(os.path.join(collection_dir, "INSTRUCTIONS_FOR_TRANSLATOR.md"), "w", encoding="utf-8") as f:
    f.write(instructions)

# Write SOURCE_PROVENANCE.md
provenance = '''# Source Provenance

- **Original dataset:** project-boli/ho
- **Records:** Existing 100 Ho records
- **Ho Verification:** The existing Ho ASR recordings and transcripts have been verified by the user.
- **Hindi Translation Origin:** No Hindi translations were generated automatically by AI or machine translation tools. The Hindi side will be supplied entirely externally by a qualified human translator.
- **Attribution:** The translation source/person must be recorded in the "Translator ID" field of the form.
'''
with open(os.path.join(collection_dir, "SOURCE_PROVENANCE.md"), "w", encoding="utf-8") as f:
    f.write(provenance)

print(f"Collection package created successfully with {len(df)} records.")
