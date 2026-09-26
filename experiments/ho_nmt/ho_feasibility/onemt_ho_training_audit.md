# ONEMT / BHASHAVERSE HO TRAINING AUDIT
- **ONEMT_HO_TRAINING_EVIDENCE**: CONFIG_ONLY
- **Explanation**: The official ONEMT/Bhashaverse checkpoints declare hoc_Wara in their model config and README. However, their SentencePiece tokenizer (onemtv3b_spm.model) does not contain a single Warang Citi character. Thus, any Warang Citi training records present in the Bhashik Parallel Corpora were mathematically dropped or replaced by <unk> during tokenization. Consequently, the model could not have meaningfully trained on Warang Citi representations.
