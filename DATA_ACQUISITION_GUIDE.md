# MatriVaani Data Acquisition Guide

This guide outlines the steps required to acquire the necessary datasets to unblock the MatriVaani pipeline for ASR, NMT, and TTS model training.

## Overview

The project is currently blocked at the data validation gate because the required raw data directories are empty:
- `datasets/asr/raw/` (for ASR/TTS)
- `datasets/nmt/raw/` (for NMT)

The system prohibits data fabrication, so you must manually acquire the data from the specified sources.

## 1. ASR and TTS Data (Mozilla Common Voice Santhali)

### Requirements
- A Mozilla Common Voice account
- Acceptance of the Santhali language terms on Common Voice
- An authentication token from Mozilla Common Voice

### Steps

1. **Visit Mozilla Common Voice**: Go to https://commonvoice.mozilla.org/ and sign in or create an account.
2. **Accept Santhali Terms**: Navigate to the Santhali language section and accept the terms and conditions for data usage.
3. **Generate Auth Token**:
   - While logged in, go to your account settings or the API section to generate a personal access token.
   - Note: The exact process may vary; refer to Mozilla Common Voice documentation for token generation.
4. **Set Environment Variable**:
   ```powershell
   $env:MOZILLA_CV_TOKEN="your_generated_token_here"
   ```
   To make it persistent, you can add it to your system environment variables or a `.env` file (though note `.env` is gitignored).
5. **Run the Download Script**:
   ```powershell
   .venv\Scripts\python.exe scripts\data_acquisition\download_asr_data.py
   .venv\Scripts\python.exe scripts\data_acquisition\download_tts_data.py
   ```
   These scripts will download the Santhali subset of Mozilla Common Voice for ASR and TTS into the respective `raw/` directories.

### Verification
After running the scripts, check that `datasets/asr/raw/` and `datasets/tts/raw/` contain audio files (e.g., `.mp3`) and associated metadata files (e.g., `.tsv`, `.json`).

## 2. NMT Data (Manual Curation)

### Requirements
- Fluency in Hindi and Santhali (preferably with knowledge of Ol Chiki script)
- Understanding of the FLN (Foundational Literacy and Numeracy) context for primary education

### Steps

1. **Launch the Curation Tool**:
   ```powershell
   .venv\Scripts\python.exe scripts\nmt_manual_curation_tool.py
   ```
2. **Enter Sentence Pairs**:
   - The tool will prompt you for:
     - Hindi sentence (FLN/Primary Education context)
     - Santhali translation (Ol Chiki preferred)
     - Your Translator ID (e.g., JD01)
   - Type `exit` at any prompt to quit the tool.
3. **Save and Review**:
   - Each entry is saved as a JSON file in `datasets/nmt/raw/` with a unique ID (e.g., `SAT-NMT-00001.json`).
   - The initial status is `TRANSLATED` and requires reviewer verification (which can be done by another expert or by you in a second pass).

### Example Entry
```json
{
    "id": "SAT-NMT-00001",
    "hindi": "पानी पीजिए",
    "santhali": "� poté𑓈𑓍𑓢𑓎 𑓏𑓢𑓍𑓣𑓈",
    "script": "Ol Chiki",
    "domain": "primary_education",
    "translator_id": "JD01",
    "reviewer_id": null,
    "status": "TRANSLATED",
    "timestamp": 1726000000.0
}
```
*Note: The Santhali text above is illustrative; you must provide accurate translations.*

### Verification
After curating, check that `datasets/nmt/raw/` contains one or more JSON files following the schema above.

## 3. Validate Data Readiness

Once you have placed data in the raw directories, run the data readiness gate:

```powershell
.venv\Scripts\python.exe scripts\data_readiness_gate.py
```

### Expected Output
```
--- Checking Readiness: ASR ---
Status: READY
--- Checking Readiness: NMT ---
Status: READY
--- Checking Readiness: TTS ---
Status: READY

OVERALL STATUS: READY
```

If the status is `READY` for all three, the pipeline is unblocked and you can proceed with training, evaluation, and Android integration.

## 4. Next Steps After Data Acquisition

1. **Run Tests**: Verify the codebase works with the new data.
   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```
2. **Run Benchmarks**: Execute the baseline and evaluation scripts to measure model performance.
   - ASR: `scripts\run_asr_baseline.py`, `scripts\evaluate_asr_10k.py`
   - NMT: `scripts\nmt_dataset_audit.py`
   - TTS: `scripts\tts_dataset_audit.py`
3. **Train Models**: Use the training scripts in `ai/asr/train_santhali_asr.py`, `ai/nmt/trainer.py`, and `ai/tts/trainer_smoke_test.py` (note: TTS trainer is a smoke test; refer to documentation for full training).
4. **Android Integration**: Once models are trained and validated, proceed to Phase 7 (Android integration) as outlined in the README.

## Troubleshooting

- **Download Scripts Fail with Auth Error**: Double-check that the `MOZILLA_CV_TOKEN` environment variable is set correctly and that the token has the necessary scopes.
- **No Data After Download**: Ensure you have accepted the Santhali terms on Mozilla Common Voice; without acceptance, the API will not return data.
- **Curation Tool Issues**: Ensure you are entering non-empty strings for Hindi and Santhali. The tool does not currently validate the Santhali script; it is your responsibility to provide accurate translations.

## Important Notes

- **Do Not Fabricate Data**: The project's integrity relies on using only real, verified datasets. Fabricating data will violate the project's principles and may lead to incorrect model behavior.
- **Data Licensing**: 
  - Mozilla Common Voice data is licensed under CC0 (public domain).
  - The manually curated NMT data is considered project proprietary; ensure you have the right to share any translations you provide.
- **Storage**: The raw data directories are intentionally excluded from version control (via `.gitignore`). You are responsible for backing up your acquired data.

## Contact

If you encounter issues or have questions about the data acquisition process, please refer to the phase reports (e.g., `PHASE8_FINAL_REPORT.md`) or reach out to the project maintainers.

--- 
*Once you have completed the data acquisition steps, the MatriVaani pipeline will be fully operational for training and evaluation.*