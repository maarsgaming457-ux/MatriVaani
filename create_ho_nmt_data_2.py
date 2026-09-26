# -*- coding: utf-8 -*-
import os
import json

base_dir = "data/ho_translation/open_source"
os.makedirs(base_dir, exist_ok=True)

# 1. dataset_inventory.md
inventory = """# HINDI-HO OPEN-SOURCE DATASET INVENTORY

| Source | Platform | Hindi | Ho | Direct Pair? |
|--------|----------|-------|----|--------------|
| Bhashik Parallel Corpora | Hugging Face (ltrciiith) | hin_Deva (claimed) | hoc_Wara (claimed) | UNKNOWN (Gated) |
| Tatoeba | Tatoeba / OPUS | hin | hoc | NO (No Direct Links) |
| Kaji-Buru (Ho-Hindi Dictionary) | Bharatavani / CIIL | Hindi | Ho | NO (Lexical/Dictionary) |
| Ho Durang Hisir | Bharatavani | Hindi | Ho | NO (Restricted Literature) |
| English-Ho Corpus | Academic (Biruli) | N/A | hoc | NO (English Pivot) |
| All other platforms (Kaggle, GitHub, Zenodo) | Various | N/A | N/A | NO (No Matches) |

| Source | Raw Pairs | Valid | Suspicious | Invalid |
|--------|-----------|-------|------------|---------|
| Bhashik | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| All Others | 0 | 0 | 0 | 0 |

| Source | License | Access | Training Use |
|--------|---------|--------|--------------|
| Bhashik | cc-by-nc-4.0 | BLOCKED (Gated) | UNKNOWN |
| Bharatavani Dictionaries | Copyrighted | RESTRICTED | NO |
"""

# 2. source_evidence.md
evidence = """# SOURCE EVIDENCE & VALIDATION

## Bhashik Parallel Corpora (BhashaVerse / IIIT-H)
- **Status**: The dataset ltrciiith/bhashik-parallel-corpora-generic officially lists both hin_Deva and hoc_Wara in its language metadata and README.
- **Evidence of Data**: The README was successfully fetched via API. It contains 775 parquet shards and represents a massive general domain web corpus for Indian languages.
- **Validation**: Validation could NOT be performed because the dataset is gated. The exact number of hin_Deva <-> hoc_Wara pairs cannot be extracted or verified without approval.

## OPUS / Tatoeba
- **Evidence of Data**: Searches against OPUS API for source=hin and 	arget=hoc return a 404 HTTP Error (Not Found). Tatoeba contains Ho (hoc) sentences, but they are almost exclusively mapped to English, not Hindi.

## GitHub / Kaggle / AI4Bharat
- **Evidence of Data**: AI4Bharat's IndicTrans2 supports Santali (sat_Olck) but explicitly omits Ho (hoc). Kaggle and GitHub searches for "Hindi Ho parallel" yield 0 matching digital corpora.
"""

# 3. access_status.md
access = """# ACCESS STATUS REPORT

## BHASHIK_ACCESS = BLOCKED
- **What was accessible**: The dataset card (README.md) and metadata, which confirm the presence of hin_Deva and hoc_Wara language tags.
- **What was not accessible**: The actual .parquet data shards. 
- **Why it could not be inspected**: The dataset is structurally gated on Hugging Face. The datasets.load_dataset API returns: Error: Dataset 'ltrciiith/bhashik-parallel-corpora-generic' is a gated dataset on the Hub.
- **Exact user action required**: A registered Hugging Face user must navigate to https://huggingface.co/datasets/ltrciiith/bhashik-parallel-corpora-generic, agree to the terms/conditions, and request access from LTRC IIIT-Hyderabad.

## BHARATAVANI_ACCESS = BLOCKED
- **What was accessible**: Metadata for Ho-Hindi print dictionaries.
- **What was not accessible**: Downloadable PDFs.
- **Why**: Requires login/registration and is strictly copyright-restricted.
"""

# 4. pair_statistics.json
pair_stats = {
    "TOTAL_RAW_HINDI_HO_PAIRS": 0,
    "TOTAL_UNIQUE_HINDI_HO_PAIRS": 0,
    "TOTAL_VALID_HINDI_HO_PAIRS": 0,
    "TOTAL_SUSPICIOUS_HINDI_HO_PAIRS": 0,
    "TOTAL_INVALID_HINDI_HO_PAIRS": 0,
    "TOTAL_SYNTHETIC_HINDI_HO_PAIRS": 0,
    "TOTAL_TRAINING_READY_HINDI_HO_PAIRS": 0,
    "TOTAL_ACCESSIBLE_HINDI_HO_PAIRS": 0,
    "TOTAL_BLOCKED_SOURCE_PAIRS": "UNKNOWN"
}

# 5. validation_report.md
validation = """# DATA VALIDATION REPORT

No automated data validation (e.g., duplicate checking, language ID filtering, sentence length constraints) could be performed because **0 accessible candidate sentence pairs** were acquired. 

The only promising candidate dataset (Bhashik Parallel Corpora) is gated and its internal language pairing structure (whether hin_Deva actually aligns directly with hoc_Wara) remains unverified. 

Therefore:
- **VALID_PAIRS**: 0
- **SUSPICIOUS_PAIRS**: 0
- **INVALID_PAIRS**: 0
"""

# 6. README.md
readme = """# MATRI VAANI HO-NMT-DATA-2 AUDIT

## FINAL DECISION
**OPTION C: POTENTIAL_DATA_FOUND_BUT_ACCESS_BLOCKED**

## SUMMARY
An exhaustive search of public datasets revealed that the only major digital corpus claiming to host both Hindi (hin_Deva) and Ho (hoc_Wara) is the **Bhashik Parallel Corpora** (ltrciiith/bhashik-parallel-corpora-generic) on Hugging Face. 

However, this dataset is **GATED**. We cannot verify if it actually contains direct hin_Deva <-> hoc_Wara alignments, nor can we download the pairs for training without human intervention (requesting access via the Hugging Face portal).

All other public open-source channels (OPUS, Tatoeba, Kaggle, GitHub) possess **0** verified Hindi-Ho pairs.

**NO MODEL TRAINING WAS EXECUTED.**
"""

files = {
    "dataset_inventory.md": inventory,
    "source_evidence.md": evidence,
    "access_status.md": access,
    "pair_statistics.json": json.dumps(pair_stats, indent=2),
    "validation_report.md": validation,
    "README.md": readme
}

for fname, content in files.items():
    with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)

