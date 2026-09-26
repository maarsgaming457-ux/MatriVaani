# HO-NMT-DATA-7 — SEED CORPUS AUDIT

## 1. Tatoeba Total Pairs
- The initial extraction yielded 331 unique hin_Deva ? hoc translation links directly from the Tatoeba graph.

## 2. Warang Citi Pairs
- Rigorous Unicode block filtering (U+118A0–U+118FF) confirmed exactly **59** pairs written in genuine Warang Citi script.
- Exported to: seed_warang_hindi_ho.jsonl

## 3. Latin Ho Pairs
- **271** pairs were identified as Latin-script Ho.
- Exported to: seed_latin_hindi_ho.jsonl

## 4. Quality Results
- **Semantic alignment**: High. The Tatoeba sentences are manually human-authored translations (e.g., "?????!" -> "??????????!").
- **Exact duplicate pairs**: Removed during initial extraction.
- **Identical source/target or empty**: Found 1 pair that contained transliteration artifacts/mixed scripts, which was moved to seed_unverified.jsonl.
- **Length**: Sentences vary from single words/exclamations to full conversational clauses. No automated rejection based on length was applied.

## 5. OPUS 419 Investigation
- OPUS reported 419 hi ? hoc alignments in the 	ranslatewiki corpus.
- However, OPUS only provides an .xml.gz alignment map (containing numerical sentence IDs), without directly providing the text. Attempts to download the monolithic hi.zip and hoc.zip monolingual corpora to map the text strings failed due to repeated SSL verification errors and server timeouts from the Finnish CSC object store.
- **Status**: UNVERIFIED. The 419 OPUS records cannot be independently verified as natural-language sentences and have been excluded from the seed datasets.

## 6. Additional Direct Tatoeba Links Discovered
- The 331 pairs represent the exhaustive list of *direct* hin ? hoc links currently exposed by the Tatoeba web API graph.

## 7. Direct vs Indirect Links
- We strictly extracted **Direct Translation Chains** (hin directly linked to hoc).
- Indirect translation chains (e.g., hin ? eng ? hoc) were deliberately excluded from this audit to maintain the highest standard of semantic equivalence and avoid English pivoting errors.

## 8. License Information
- **Tatoeba Pairs**: CC BY 2.0 FR / CC0
- **OPUS (Unverified)**: CC0 / Free

## 9. Final Verified Seed Size
- **Verified Warang Citi pairs**: 59
- **Verified Latin Ho pairs**: 271
- **Unverified pairs**: 1 (Mixed script)
- **Verified OPUS pairs**: 0
- **Total unique direct Hindi-Ho pairs**: 330
- **Dataset Size Classification**: **100–500**

## 10. Exact Files Created
- ho_nmt_data_audit/seed_warang_hindi_ho.jsonl
- ho_nmt_data_audit/seed_latin_hindi_ho.jsonl
- ho_nmt_data_audit/seed_unverified.jsonl
- ho_nmt_data_audit/HO-NMT-DATA-7-SEED-CORPUS-AUDIT.md

## 11. Recommended Next Data-Acquisition Step
Because the public verified seed size is between 100 and 500, we now have enough data to perform a "sanity check" fine-tuning test on a byte-level model (like ByT5) to prove the end-to-end NMT training architecture actually supports Warang Citi processing. However, 330 pairs is insufficient for a production-grade NMT system. We should proceed with an architectural ByT5 pilot using this seed data while waiting for a response from the Bhashik/LTRC research team regarding the 232 GB corpus subset.

## FINAL STATUS
**SEED_CORPUS_READY_NEEDS_MORE_DATA**
