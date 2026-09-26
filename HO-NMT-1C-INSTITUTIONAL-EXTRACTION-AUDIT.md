# HO-NMT-1C INSTITUTIONAL EXTRACTION AUDIT

## EXECUTIVE SUMMARY
This audit investigated publicly available institutional resources from Bharatavani and CIIL, specifically evaluating published Ho-Hindi books, dictionaries, and literature. While several highly relevant resources exist, they are structurally gated by login requirements and strict publisher copyright. 

Consequently, **no bulk-extractable, legally permissible Hindi-Ho sentence pairs were found**.

## 1. INSTITUTIONAL RESOURCE INVENTORY

### Resource 1: ???-???? | ??-?????? ??????? (An Ho-Hindi Dictionary)
- **URL**: site:bharatavani.in
- **Author**: Damyanti Sinku
- **Publisher**: Ho Bhasha Sahitya Vikas Manch, Ranchi, Jharkhand
- **Year**: 2007
- **File Size**: ~24.75 MB
- **Resource Type**: DICTIONARY (with potential example sentences)
- **Access Status**: LOGIN_REQUIRED / ACCESS_RESTRICTED
- **License/Copyright**: COPYRIGHT_RESTRICTED (Publisher Copyright)
- **Extraction Possible**: FALSE (Legally and technically restricted)

### Resource 2: Ho Durang Hisir (?? ????? ?????)
- **URL**: site:bharatavani.in
- **Author**: Dr. Damyanti Sinku
- **Publisher**: Jharkhand Jharokha, Ranchi
- **Resource Type**: LITERATURE
- **Access Status**: LOGIN_REQUIRED / ACCESS_RESTRICTED
- **License/Copyright**: COPYRIGHT_RESTRICTED (Publisher Copyright)
- **Extraction Possible**: FALSE

### Resource 3: Ho Bhasha Ka Vaigyanik Adhyayan (?? ???? ?? ????????? ??????)
- **URL**: site:bharatavani.in
- **Author**: Saraswati Gagrai
- **Publisher**: K. K. Publications, Allahabad
- **Resource Type**: LINGUISTICS
- **Access Status**: LOGIN_REQUIRED / ACCESS_RESTRICTED
- **License/Copyright**: COPYRIGHT_RESTRICTED
- **Extraction Possible**: FALSE

### Resource 4: ????? : ??????? "??" ????
- **URL**: site:bharatavani.in
- **Resource Type**: BILINGUAL_REFERENCE
- **Access Status**: LOGIN_REQUIRED / ACCESS_RESTRICTED
- **License/Copyright**: COPYRIGHT_RESTRICTED
- **Extraction Possible**: FALSE

## 2. EXTRACTION FEASIBILITY & COMPLIANCE
Per project directives, scraping login-gated or DRM-protected PDFs without explicit copyright permission is prohibited. Thus, no automatic OCR or PDF text extraction was executed against the Bharatavani repository.

## 3. AUDIT METRICS
1. **Every institutional resource inspected**: Yes (Bharatavani portal).
2. **URLs**: bharatavani.in (specific document pages).
3. **Authors**: Damyanti Sinku, Saraswati Gagrai.
4. **Publishers**: Ho Bhasha Sahitya Vikas Manch, Jharkhand Jharokha, K.K. Publications.
5. **Years**: 2007, etc.
6. **File sizes**: ~24.75 MB (Dictionary).
7. **Access status**: ACCESS_RESTRICTED (Login required).
8. **License/copyright**: COPYRIGHT_RESTRICTED.
9. **Dictionary entry count**: 0 (extracted).
10. **Example sentence count**: 0 (extracted).
11. **Raw candidate sentence pairs**: 0
12. **Unique candidate sentence pairs**: 0
13. **Accepted pairs**: 0
14. **Probable pairs**: 0
15. **Uncertain pairs**: 0
16. **Rejected pairs**: 0
17. **Duplicate count**: 0
18. **Script distribution**: Unknown (Likely Devanagari based on title metadata, but unverified).
19. **Source/page provenance**: N/A
20. **Final training candidate count**: 0

## 4. CRITICAL COUNTS
- **FINAL_UNIQUE_HINDI_HO_SENTENCE_PAIRS = 0**
- **FINAL_TRAINING_CANDIDATE_PAIRS = 0**

## 5. INFRASTRUCTURE & READINESS
The output directory data/ho_translation/open_hindi_ho_institutional_v1/ has been created. The dataset files (sentence_pairs.jsonl, dictionaries.jsonl, etc.) remain strictly empty.

Because the pair count is <20:
**NMT TRAINING READINESS = NMT_TRAINING_NOT_READY**
