# PHASE 5.5 DATA ACQUISITION REPORT

## 1. Data Sources Investigated
- **COILD-MT-Corpus (HuggingFace)**: Evaluated directly via the HuggingFace `datasets` API.
- **AdiBhashaa**: Reviewed via literature.
- **EnSanCorp**: Reviewed via literature.
- **CIIL Mother Tongue Parallel Text Corpus**: Reviewed via literature.

## 2. Actual Datasets Obtained
**NO DATA ACQUIRED.** 
While the COILD-MT-Corpus contains approximately 20,603 pairs on Hugging Face, it is explicitly gated. When the automated ingestion pipeline attempted to pull it via API, it was rejected for lacking a verified user token. 

## 3. Actual Usable Hindi–Santhali Pair Counts
**0 pairs.**

## 4. Licenses
- **COILD-MT-Corpus**: LICENSE UNKNOWN (Requires access approval to view terms).
- **CIIL / AdiBhashaa**: ACCESS UNAVAILABLE.

## 5. Scripts
Not evaluated on raw data (No data acquired). However, the ingestion pipeline explicitly enforces `Ol_Chiki`, `Devanagari`, or `Roman` categorizations.

## 6. Dataset Quality
Not evaluated.

## 7. Duplicate Analysis
Not evaluated.

## 8. Educational Data Count
0 pairs.

## 9. Verified Data Count
0 pairs.

## 10. GOLD Set Count
GOLD SET INSUFFICIENT (0 pairs).

## 11. Train Count
0 pairs.

## 12. Validation Count
0 pairs.

## 13. Test Count
0 pairs.

## 14. Data Gaps
There is a 100% gap across all domains. We possess 0 bytes of parallel text in the raw datasets directory.

## 15. Human-Review Requirements
Once data is eventually acquired, human review will be strictly required for the Educational subset to form the GOLD test set.

## 16. NMT Training Status
**NMT TRAINING CANNOT BEGIN.** The data blocker holds firm.

## 17. Exact Recommendation for Phase 5.6
Halt all automated scraping attempts on gated academic datasets. The Project Lead must manually authenticate and download the `.csv` or `.jsonl` files from Hugging Face or CIIL and place them into `datasets/nmt/raw/`. Until this manual intervention occurs, the AI NMT pipeline is correctly frozen to prevent hallucinated model training. Proceed to TTS (Phase 6) in the meantime.
