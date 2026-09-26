# PHASE 5.6 COILD-MT-CORPUS VERIFICATION REPORT

## 1. Access Status
**ACCESS UNAVAILABLE**

## 2. Actual File Obtained
None. No file exists at `datasets/nmt/raw/COILD-MT-Corpus/`.

## 3. File Checksum
NOT MEASURED.

## 4. Reported Dataset Size
~20,603 pairs (via Hugging Face: `ainlpml-iitp/COILD-MT-Corpus`).

## 5. Actual Dataset Size
0 pairs.

## 6. Actual Hindi–Santhali Pair Count
0 pairs.

## 7. Language Distribution
NOT MEASURED.

## 8. Script Distribution
NOT MEASURED.

## 9. Ol Chiki Count
0.

## 10. Duplicate Count
0.

## 11. Invalid Count
0.

## 12. Quality Tiers
- TIER A: 0
- TIER B: 0
- TIER C: 0
- REJECTED: 0

## 13. Educational Data Count
0.

## 14. Gold Candidate Count
0 (INSUFFICIENT DATA).

## 15. Training Count
0.

## 16. Validation Count
0.

## 17. Test Count
0.

## 18. License/Usage Status
LICENSE UNKNOWN (Requires accepting academic terms on Hugging Face).

## 19. Problems Discovered
The automated ingestion pipeline was blocked by the Hugging Face gate. Legitimate automated downloads are impossible without a human user's verified token.

## 20. Data Cleaning Performed
None.

## 21. Remaining Human-Review Requirements
**CRITICAL**: A human must authenticate to Hugging Face, download the `.csv` or `.txt` file for `COILD-MT-Corpus`, and manually place it into `datasets/nmt/raw/COILD-MT-Corpus/`. Afterwards, a native Santhali speaker must review the Educational subsets to establish the GOLD test set.

## 22. Whether NMT Training Can Begin
**NO.** NMT fine-tuning remains frozen. Initiating training now would require dataset fabrication, which is strictly forbidden.
