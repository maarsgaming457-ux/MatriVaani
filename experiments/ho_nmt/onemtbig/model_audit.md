# ONEMT-BIG REPOSITORY AUDIT

1. **Exact model checkpoint location**: https://vandanresearch.sgp1.digitaloceanspaces.com/bhashaverse-models/machine-translation/onemtbig/iiith-onemtbig.zip (2.14 GB zip file containing ct2_model and onemtbig_spm.model).
2. **Exact model architecture**: Transformer-based multilingual translation model. Exported to ctranslate2.Translator.
3. **Exact parameter count**: ~1B-2B (claimed).
4. **Exact tokenizer**: SentencePiece (spm.SentencePieceProcessor).
5. **Vocabulary**: Shared SentencePiece vocabulary across 36 languages.
6. **How language codes are passed**: The model is deployed on Triton Inference Server. The user passes sourceLanguage and 	argetLanguage (e.g. hi and hc) which are mapped to internal codes (hin_Deva and hoc_Wara). These are likely prepended to the token stream as __hin_Deva__ / __hoc_Wara__ based on standard Fairseq/CTranslate2 multilingual conventions.
7. **Ho-specific script/vocabulary**: The README claims support for hoc_Wara (Ho in Warang Citi script). The tokenizer model must theoretically contain Warang Citi characters.
8. **Ho Representation**: hoc_Wara
9. **Hindi Representation**: hin_Deva
10. **Is translation direct?**: Yes, the architecture is designed as an all-to-all multilingual translation model. No English intermediate step is defined in the Triton backend.

## BASHIK INTERPRETATION
- **MODEL_TRAINING_SOURCE_CLAIM**: Bhashik Parallel Corpora
- We cannot infer the actual Hindi-Ho pair count since Bhashik access is blocked and the model checkpoint itself cannot be downloaded to run empirical tests.
