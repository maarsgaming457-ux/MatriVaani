# MODEL AUDIT

## RELATION TO ONEMT-BIG
Both Hugging Face models possess identical architectures (MBart 1B+ parameters), shared dictionary schemas (fairseq_dict.json), and the identical SentencePiece tokenizer (onemtv3b_spm.model). They represent the public BhashaVerse base checkpoints underlying the ONEMT-BIG API.

## LANGUAGE SUPPORT VERIFICATION
- Hindi (hin_Deva): YES. The tokenizer has extensive Devanagari coverage.
- Ho (hoc_Wara): NO. An exhaustive code-point scan (U+118A0 - U+118FF) of the SentencePiece vocabulary returned 0 matches for Warang Citi. By contrast, Santali (Ol Chiki) returned 602 matches.
- Direct Hindi-Ho Possible: NO. Because the tokenizer lacks the target script entirely, any Ho Warang Citi input is tokenized exclusively into <unk>s. Thus, semantic translation is structurally impossible.
