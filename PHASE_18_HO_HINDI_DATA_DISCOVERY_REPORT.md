# PHASE 18 HO-HINDI DATA DISCOVERY REPORT

## 1. Executive Summary
An exhaustive discovery phase was conducted to identify any genuine Ho ↔ Hindi sentence-level parallel datasets suitable for machine translation training. Platforms investigated include Hugging Face, GitHub, ULCA/Bhashini, AI4Bharat, IIIT-H, OPUS, Tatoeba, and various government/educational initiatives (CIIL, Bharatavani).

## 2. Resource Discovery Table

| Resource | URL | Ho present? | Hindi present? | Ho-Hindi aligned? | Approximate pairs | License | Access | Usable for training? |
|---|---|---|---|---|---|---|---|---|
| LTRC Bhashik Generic | huggingface.co/datasets/ltrciiith/bhashik-parallel-corpora-generic | Yes (hoc_Wara) | Yes (hin_Deva) | Unverified | Unknown | CC-BY-NC 4.0 | Gated (Auto-approval) | No |
| CIIL / Bharatavani | haratavani.in | Yes | Yes | No (Pedagogical) | N/A | Copyright | Public | No |
| Glosbe Dictionary | glosbe.com | Yes | Yes | No (Lexical) | Unknown | Proprietary | Public | No |
| Digital Ho Dictionary | Google Play | Yes | Yes | No (Lexical) | Unknown | Proprietary | Public | No |
| OPUS | opus.nlpl.eu | No | Yes | No | 0 | Open | Public | No |
| Tatoeba | 	atoeba.org | No | Yes | No | 0 | CC-BY 2.0 FR | Public | No |
| AI4Bharat/Samanantar | i4bharat.iitm.ac.in | No | Yes | No | 0 | CC-BY-NC 4.0 | Public | No |

## 3. Data Quality Classification
* **LTRC Bhashik Generic:** Likely Class E (Machine-generated/synthetic) or F (Unusable). Metadata contains hoc_Wara and hin_Deva, but zero-shot performance (Phase 13) indicates poor/synthetic quality.
* **CIIL / Bharatavani Educational Materials:** Class C/D (Ho + another language / Monolingual). Useful for language preservation but lacks sentence-level alignment for NMT.
* **Glosbe / Digital Ho Dictionary:** Class B (Genuine Ho-Hindi word-level lexical data). Useful for dictionary lookups or evaluation, but not for Seq2Seq translation training.
* **OPUS / AI4Bharat:** Class F (Unusable). Ho language is absent from these major parallel corpora.

## 4. BEST VERIFIED RESOURCE

NO VERIFIED PUBLIC HO-HINDI PARALLEL DATASET FOUND.

## 5. Conclusion
There is currently no large-scale, publicly accessible, and legally usable sentence-level parallel corpus for Ho ↔ Hindi machine translation. Existing resources are primarily lexical (dictionaries) or pedagogical (primers). Machine translation for this pair remains strictly blocked by the fundamental absence of human-verified ground-truth parallel data.
