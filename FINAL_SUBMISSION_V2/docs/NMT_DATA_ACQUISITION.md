# MatriVaani NMT Data Acquisition Protocol

This document outlines the strict protocols for acquiring and ingesting Hindi-Santhali parallel data for the MatriVaani NMT pipeline.

## Status: ACCESS UNAVAILABLE
As of Phase 5.5, no raw data exists locally. Attempted automated acquisition of `ainlpml-iitp/COILD-MT-Corpus` (20,603 pairs) from Hugging Face failed because the dataset requires manual user authentication and acceptance of terms.

## Data Acquisition Rules
1. **No Hallucinations**: We will not employ LLMs to synthesize parallel text in place of real human ground-truth.
2. **Provenance**: Every dataset must be downloaded manually by an authenticated user and placed into `datasets/nmt/raw/<source_name>/`.
3. **No Automatic Fine-Tuning**: The `ai/nmt/trainer.py` will explicitly crash if zero verified pairs are found.

## Action Required
To unblock the NMT pipeline:
1. Log in to Hugging Face or the CIIL repository.
2. Download the Hindi-Santhali parallel `.csv` or `.txt` files.
3. Place them in `datasets/nmt/raw/`.
4. Re-run `python scripts/nmt_create_splits.py`.
