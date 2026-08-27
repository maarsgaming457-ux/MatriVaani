# COILD-MT-Corpus Dataset Analysis

## Current Status
**ACCESS UNAVAILABLE**

No manual ingestion files have been placed in `datasets/nmt/raw/COILD-MT-Corpus/`.

## Purpose of this Document
When the human project lead successfully authenticates and downloads the raw dataset (reported size: ~20,603 Hindi-Santhali pairs) from Hugging Face, this document will be updated with:

1. **Format Validation**: E.g., CSV, TSV, or JSONL structures.
2. **Language Validation**: Confirming the pairs strictly map Hindi to Santhali (and vice versa) and not to a separate related tribal dialect mislabelled as Santhali.
3. **Script Analysis**: Mapping the distribution of Devanagari vs. Ol Chiki in the target columns.
4. **Domain Classification**: Evaluating how many of the 20,603 pairs are suitable for MatriVaani's primary educational, primary classroom, and literacy directives.
5. **Quality Tiers**: Placing pairs into TIER A (Verified), TIER B (Good but unverified), TIER C (Questionable), and REJECTED (misaligned or empty).

## Next Steps
This analysis is blocked until the dataset is provided. Once provided, run `python scripts/nmt_dataset_audit.py` to populate this analysis automatically.
