# HO-NMT-DATA-8 — PUBLIC DATA EXPANSION

## 1. Current Tatoeba direct pair count
- **330 verified direct pairs** (59 Warang Citi, 271 Latin Ho).

## 2. Newly discovered Tatoeba pairs
- **0**. The previous exhaustive paginated API extraction (185 root sentences generating 331 unique translational cross-links) already perfectly captured the entire public graph of direct hin ? hoc nodes available on Tatoeba.

## 3. OPUS verified pairs
- **0**.

## 4. OPUS unverified pairs
- **419** reported alignments from Translatewiki.
- Exhaustive probing of OPUS file server endpoints (moses, 	mx) returned HTTP 404 (Not Found). The only existing asset was a structural .xml.gz map pointing to hi.zip and hoc.zip payloads which failed on SSL/network timeouts. The strings remain inaccessible and entirely **UNVERIFIED**.

## 5. Hugging Face findings
- Extensive targeted tag filtering (language:hoc) revealed 16 datasets.
- Result: Most were ASR monolingual Ho datasets (project-boli/ho, espnet/mms_ulab_v2), English-Ho sets (google/smol), or word-level dictionaries (panlex). **No direct Hindi-Ho parallel sentences were found**.

## 6. GitHub findings
- Re-scanned repos for hin hoc, Warang Citi Hindi, etc. All were false positives. **0 datasets found**.

## 7. Zenodo/Kaggle findings
- Zenodo API exact matches: **0**.
- Kaggle search matches: **0**.

## 8. ELRC/ELG findings
- No open Hindi-Ho parallel subsets found.

## 9. Indian institutional findings
- Bharatavani/CIIL publish monolingual Ho or dictionaries. No downloadable aligned bitext.
- Bhashik Parallel Corpora is gated behind 232 GB of interleaved Parquet arrays, remaining inaccessible for targeted remote extraction as verified in prior audits.

## 10. Other public-source findings
- AI4Bharat (Samanantar, IndicCorp, IndicTrans2) does not natively support Ho.

## 11. Duplicate count
- N/A (No new data was found to deduplicate against the 330-pair seed).

## 12. Verified Warang Citi count
- **59 pairs** (Original Tatoeba Seed)
- **0 pairs** (Newly discovered)

## 13. Verified Latin Ho count
- **271 pairs** (Original Tatoeba Seed)
- **0 pairs** (Newly discovered)

## 14. Total new verified direct pairs
- **0**

## 15. Total cumulative verified direct Hindi-Ho pairs
- **330 pairs**

## 16. Dataset licenses
- Tatoeba (CC-BY 2.0 FR)
- Bhashik/OPUS (Inaccessible)

## 17. Dataset quality
- The existing 330 Tatoeba pairs are extremely high quality (human-authored, manually validated, genuine script usage).

## 18. Exact files created
- ho_nmt_data_audit/newly_verified_hindi_ho.jsonl (empty)
- ho_nmt_data_audit/newly_verified_warang_hindi_ho.jsonl (empty)
- ho_nmt_data_audit/newly_verified_latin_hindi_ho.jsonl (empty)
- ho_nmt_data_audit/opus_translatewiki_verified_sample.jsonl (empty)
- ho_nmt_data_audit/opus_translatewiki_unverified_sample.jsonl (empty)
- ho_nmt_data_audit/candidate_sources.csv
- ho_nmt_data_audit/rejected_sources.csv
- ho_nmt_data_audit/unverified_sources.csv
- ho_nmt_data_audit/HO-NMT-DATA-8-PUBLIC-DATA-EXPANSION.md

## Cumulative Dataset Size Classification
**100–500**

## FINAL DECISION
**PUBLIC_SEED_DATA_STILL_SMALL**
