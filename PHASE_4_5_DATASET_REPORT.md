# PHASE 4.5 DATASET REPORT

## 1. Current Verified Pair Count
**0 verified Hindi-Santhali pairs.** 
The data ingestion pipeline has been fully architected, but no actual verified data has been pulled into the `datasets/nmt/raw` directory yet.

## 2. Public Datasets Discovered
During web research, the following potential dataset targets were identified:
- **AdiBhashaa**: 20,000 sentence pairs for Hindi-Santali (part of an 80,000 tribal corpus).
- **EnSanCorp**: English-Santali Neural Machine Translation corpus with 5,930 aligned sentences. (Can be pivoted to Hindi-Santali via English pivot if necessary, though direct is preferred).
- **The Mother Tongue Parallel Text Corpus of India (Vol. I)**: Curated by CIIL, containing 5,332 sentences for Santhali.
- **HuggingFace Community Datasets**: Small-scale repositories (e.g., `english-santali-dataset`) generally lacking educational domain specificity.

## 3. Licenses
- **AdiBhashaa**: Open parallel corpus (precise open-source license to be verified upon download).
- **EnSanCorp**: Academic research (researchgate). 
- **CIIL**: Government/academic resource; restricted for non-commercial research use.

## 4. Data Sources
- Central Institute of Indian Languages (CIIL)
- Academic institutions (KISS-DU)
- BhashaVerse / Bhashini (Government of India initiatives)

## 5. Data Quality
Public dataset quality is highly variable. The CIIL and AdiBhashaa datasets are presumed to be of high linguistic quality, but lack the specific FLN/Primary Education domain targeting required for MatriVaani.

## 6. Script Distribution
Santhali in these datasets is found in **Ol Chiki**, **Devanagari**, and **Roman**. The MatriVaani ingestion pipeline is configured to explicitly track `source_script` and `target_script` to prevent silent corruption, as Ol Chiki is our ultimate deployment target.

## 7. Domain Distribution
Currently, the public datasets are heavily skewed towards General, News, and Government domains. The Educational/FLN domain is severely underrepresented.

## 8. Verified vs Synthetic
Unknown until datasets are formally audited. The pipeline schema strictly mandates `synthetic: bool` and `verification_status: Enum` to prevent synthetic data from polluting the Gold test set.

## 9. Speaker/Translator Information
The schema requires a `source` (e.g., "AdiBhashaa") and supports an optional `translator_id` to preserve provenance.

## 10. Dataset Gaps
- **Critical Gap**: A complete lack of Foundational Literacy and Numeracy (FLN) domain translations (numbers, classroom instructions, shapes). 
- **Recommendation**: Launch a targeted data-collection drive using PALASH-affiliated educators.

## 11. GOLD Test Set Strategy
The pipeline guarantees that the test split (`generate_splits`) only receives data marked explicitly as `VERIFIED_HUMAN` and `synthetic=False`. 

## 12. Recommended Data Collection Strategy
1. Attempt to formally request the CIIL and AdiBhashaa datasets.
2. Ingest them through `validate_and_ingest` to filter duplicates and normalize Ol Chiki.
3. Extract any sentences related to education, assigning them to the `MATRI-NMT-HI-SAT-EDU-v0.1` subset.
4. Hire 2-3 native Santhali teachers to independently translate the `EDUCATIONAL_TRANSLATION_VOCABULARY.md` (creating the GOLD educational set).

## 13. Recommended Next NMT Step
Do **not** begin fine-tuning IndicTrans2. Wait for the ingestion of at least the AdiBhashaa or CIIL dataset, plus the human-translated educational baseline, before proceeding to NMT training. 
