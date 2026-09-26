# MatriVaani Ho Annotator Tool

## What is this tool?
This is a lightweight, offline-first annotation tool designed to allow human bilingual speakers to correct Ho ASR transcripts and translate them into Hindi.

## Why use this tool?
Ho is an extremely low-resource language. Machine translation cannot be trusted for generating training data. All translations must be human verified. This tool ensures that your work is safely saved to a local SQLite database and can be exported as JSONL dataset files.

## How to use
1. Make sure you have the Python `venv` activated.
2. Run `uvicorn app:app --host 127.0.0.1 --port 8080` from this directory.
3. Open your browser to `http://127.0.0.1:8080`.
4. For each record:
   - **Do not edit** the Raw Ho ASR field.
   - Enter the **Corrected Ho** text in Devanagari.
   - Enter the natural **Hindi Translation** in Devanagari.
   - Select the appropriate educational category.
   - **IMPORTANT:** Check "Human Verified" only if you are confident in the translation.
   - Set Status to APPROVED, or NEEDS_REVIEW if uncertain.
5. Click Save or Next. Your progress is saved instantly to the local `annotations.db`.
6. When finished, use the Export buttons to generate the JSONL files in `data/ho_hindi/pilot_v0.1/`.

## Privacy & Safety
This tool does not connect to the internet. It does not collect personal information (annotators use anonymous IDs). It will not overwrite your ASR transcripts or the production translation model.
